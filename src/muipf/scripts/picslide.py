#------------------------------------------------------------------------------#
#  MUIPF: Mutual Information Image Processing Framework                        #
#  Copyright (C) 2020 - 2021  MUIPF developers group                           #
#                                                                              #
#  See the LICENSE file for terms of usage and distribution.                   #
#------------------------------------------------------------------------------#


'''
Mutual information based overlapping of images. Slide pictures on top of each
other so that the most suitable overlap arises, in terms of mutual information.
'''


import os
import sys
import argparse
import multiprocessing
import logging
from joblib import Parallel, delayed
from skimage.io import imread
import numpy as np
from matplotlib import pyplot as plt
from scipy import signal

from muipf.scripts.common import ScriptError, print_line


VERSION = (0, 1)
MIOUT = 'hypersurface.dat'
CCOUT = 'hypersurface_cc.dat'


USAGE = \
'''
Mutual information based overlapping of images. Slides pictures on top of each
other so that the most suitable overlap arises, in terms of mutual information.
'''


def main(cmdlineargs=None):
    '''Main driver routine for picslide.

    Args:

        cmdlineargs: list of command line arguments
            When None, arguments in sys.argv are parsed (default: None)

    '''

    args = parse_cmdline_args(cmdlineargs)
    picslide(args)


def parse_cmdline_args(cmdlineargs=None):
    '''Parses command line arguments.

    Args:

        cmdlineargs: list of command line arguments
            When None, arguments in sys.argv are parsed (default: None)

    '''

    parser = argparse.ArgumentParser(description=USAGE)

    msg = 'input files'
    parser.add_argument('infiles', action='store', nargs=2, type=str, help=msg)

    msg = 'output file'
    parser.add_argument('-o', '--outfile', action='store', default=MIOUT,
                        dest='outfile', type=str, help=msg)

    msg = 'targeted number of entries per bin'
    parser.add_argument('-b', '--binning', dest='entriesperbin',
                        default=50, type=int, help=msg)
    
    msg = 'if cross correlation should be calculated'
    parser.add_argument('-c', '--ccorr', dest='tccorr', action='store_true',
                        help=msg)

    msg = 'log level (INFO, DEBUG)'
    parser.add_argument('-l', '--loglvl', dest='loglvl',
                        default='INFO', type=str, help=msg)

    args = parser.parse_args(cmdlineargs)

    return args


def picslide(args):
    '''Slides pictures on top of each other so that the most suitable overlap
       arises, in terms of mutual information.

    Args:

        args: namespace of command line arguments

    '''

    print_header(VERSION)

    loglvl = args.loglvl
    loglvl = getattr(logging, loglvl.upper(), None)
    logging.basicConfig(filename='picslide.log', level=loglvl)

    logging.info('Starting picslide')
    print('Starting main program...')
    print_line()

    logging.info('Starting parsing arguments')
    infiles = args.infiles
    infiles = [os.path.join(os.getcwd(), entry) for entry in infiles]

    outfile = args.outfile

    entriesperbin = args.entriesperbin
    tccorr = args.tccorr
    logging.info('Finished parsing arguments')


    logging.info('Starting reading images')
    try:
        print('Reading images...')
        baseim = np.asarray(imread(infiles[0], as_gray=True))
        print('base image: ', infiles[0])
        subim = np.asarray(imread(infiles[1], as_gray=True))
        print('sub image: ', infiles[1])
    except FileNotFoundError as exc:
        raise ScriptError('Invalid infile path(s) specified.') from exc
    print_line()
    logging.info('Finished reading images')

    # calculate entropies of seperate images
    logging.info('Starting individual entropy calculations')
    print('Calculating individual entropies...')
    entropybase = get_entropy(baseim, entriesperbin)
    print('base image: {0:.6f}'.format(entropybase))
    entropysub = get_entropy(subim, entriesperbin)
    print('sub image: {0:.6f}'.format(entropysub))
    print_line()
    logging.info('Finished individual entropy calculations')

    hsize = np.shape(baseim)[0] - np.shape(subim)[0]
    vsize = np.shape(baseim)[1] - np.shape(subim)[1]
    logging.info('Starting generation of displacement vectors')
    shifts = get_displacement_vectors(hsize, vsize)
    logging.info('Finished generation of displacement vectors')

    # calculate mutual information hypersurface
    logging.info('Starting hypersurface calculation')
    print('Calculating mutual information hypersurface...')
    mi = scan_hypersurface(
        baseim, subim, (entropybase, entropysub), shifts, entriesperbin)
    logging.info('Finished hypersurface calculation')
    print('obtained properties:')
    print('min: {0:.6f}, max: {1:.6f}, mean: {2:.6f}, rms: {3:.6f}'
          .format(np.amin(mi), np.amax(mi), np.mean(mi),
                  np.sqrt(np.mean(mi**2))))
    np.savetxt(outfile, mi)
    print('written to file "{}"'.format(outfile))
    print_line()
    
    if tccorr:
        logging.info('Starting cross correlation hypersurface calculation')
        print('Calculating cross correlation hypersurface...')
        ccorr = get_cross_correlation(baseim, subim)
        logging.info('Finished cross correlation hypersurface calculation')
        print('obtained properties:')
        print('min: {0:.6f}, max: {1:.6f}, mean: {2:.6f}, rms: {3:.6f}'
              .format(np.amin(ccorr), np.amax(ccorr), np.mean(ccorr),
                      np.sqrt(np.mean(ccorr**2))))
        np.savetxt(CCOUT, ccorr)
        print('written to file "{}"'.format(CCOUT))
        print_line()

    msg = 'Finished'
    logging.info(msg)
    print(msg)


def get_displacement_vectors(hsize, vsize):
    '''Established list of displacement vectors that cover the entire space.

    Args:

        hsize (int): range of horizontal pixel index
        vsize (list): range of vertical pixel index

    Returns:

        shifts (list): list of displacement vectors

    '''

    logging.debug('Enter function: get_displacement_vectors')

    shifts = []

    for hpixel in range(hsize):
        for vpixel in range(vsize):
            shift = np.array([hpixel, vpixel])
            shifts.append(shift)

    return shifts


def scan_hypersurface(baseim, subim, entropies, shifts, entriesperbin):
    '''Calculates the full mutual information hypersurface.

    Args:

        baseim (2darray): array representing the base image
        subim (2darray): array representing the sub image
        entropies (tupel): individual entropies of both images
        shifts (list): list of displacement vectors
        entriesperbin (int): targeted number of entries per bin

    Returns:

        mi (2darray): mutual information hypersurface

    '''

    logging.debug('Enter function: scan_hypersurface')

    calc = lambda shift: scan_hypersurface_point(
        baseim, subim, entropies, shift, entriesperbin)

    num_cores = multiprocessing.cpu_count()
    mi = Parallel(n_jobs=num_cores)(delayed(calc)(shift) for shift in shifts)

    mi = np.reshape(mi, (np.shape(baseim)[0] - np.shape(subim)[0],
                         np.shape(baseim)[1] - np.shape(subim)[1]))

    return mi


def scan_hypersurface_point(baseim, subim, entropies, shift, entriesperbin):
    '''Calculates the mutual information of a single hypersurface point.

    Args:

        baseim (2darray): array representing the base image
        subim (2darray): array representing the sub image
        entropies (tupel): individual entropies of both images
        shift (1darray): displacement vector
        entriesperbin (int): targeted number of entries per bin

    Returns:

        mi (float): corresponding mutual information

    '''

    logging.debug('Enter function: scan_hypersurface_point')

    jentropy = get_joint_entropy(baseim, subim, shift, entriesperbin)

    mi = get_mutual_information(entropies[0], entropies[1], jentropy)

    return mi


def get_entropy(image, entriesperbin):
    '''Calculates the entropy of an individual image.

    Args:

        image (2darray): array representing an image
        entriesperbin (int): targeted number of entries per bin

    Returns:

        entropy (float): corresponding entropy

    '''

    logging.debug('Enter function: get_entropy')

    nbins = int(image.size / entriesperbin)

    hist, _ = np.histogram(image, bins=nbins, density=False)
    hist = hist / image.size

    histlog = np.log(hist, out=np.zeros_like(hist), where=(hist != 0.0))

    # calculate entropy of the image
    entropy = - np.dot(hist, histlog)

    return entropy


def get_joint_entropy(baseim, subim, shift, entriesperbin):
    '''Calculates the joint entropy of two images, for a displacement vector
       defining their relative positions to each other. The displacement vector
       points from the upper left corner of the base image to the upper left
       corner of the sub image.

    Args:

        baseim (2darray): array representing the base image
        subim (2darray): array representing the sub image
        shift (1darray): displacement vector
        entriesperbin (int): targeted number of entries per bin

    Returns:

        jentropy (float): corresponding joint entropy

    '''

    logging.debug('Enter function: get_joint_entropy')

    # ignore parts of base image that have no overlap with the sub image
    # therefore the total amount of bins is determined by the sub image
    nbins = int(np.sqrt(subim.size / entriesperbin))

    subview = baseim[shift[0]:np.shape(subim)[0] + shift[0],
                     shift[1]:np.shape(subim)[1] + shift[1]]

    jhist, _, _ = np.histogram2d(subview.flatten(), subim.flatten(),
                                           bins=nbins, density=False)
    jhist = jhist.flatten()
    jhist = jhist / subim.size

    jhistlog = np.log(jhist, out=np.zeros_like(jhist), where=(jhist != 0.0))

    # calculate joint entropies as negative summed product of all entries
    jentropy = - np.dot(jhist, jhistlog)

    return jentropy


def get_mutual_information(entr1, entr2, entr12):
    '''Based on the individual entropies of two images and their joint entropy,
       the corresponding mutual information gets calculated and returned.

    Args:

        entr1 (float): entropy of the first individual image
        entr2 (float): entropy of the second individual image
        entr12 (float): joint entropy of the images

    Returns:

        mi (float): corresponding mutual information

    '''

    logging.debug('Enter function: get_mutual_information')

    return entr1 + entr2 - entr12


def print_header(version):
    '''Print stdout header of the picslide script.

    Args:

        version (tupel): integer tupel containing the version numbers

    '''

    hbar = '='
    vbar = '|'
    space = ' '

    version = [str(entry) for entry in version]
    vstr = '.'.join(version)

    print(80 * hbar)
    print(vbar, 33 * space, 'Picslide', 33 * space, vbar)
    print(vbar, 30 * space, 'Version: ', vstr, 31 * space, vbar)
    print(80 * hbar)
    print('')
    
    
def get_cross_correlation(baseim, subim):
    '''Calculates the cross correlation of two images

    Args:

        baseim (2darray): array representing the base image
        subim (2darray): array representing the sub image

    Returns:

        ccorr (2darray): cross correlation of images

    '''

    logging.debug('Enter function: get_cross_correlation')
    
    padded_si = (np.pad(subim, ((0, np.shape(baseim)[0] - np.shape(subim)[0]), 
                                (0, np.shape(baseim)[1] - np.shape(subim)[1]))))
                        
    basefft = np.fft.fft2(baseim)
    subfft = np.fft.fft2(padded_si)
    
    ccorr = np.abs(np.fft.ifft2(basefft * np.conj(subfft)))
    
    return ccorr