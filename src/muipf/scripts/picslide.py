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


import argparse


USAGE = \
'''
Mutual information based overlapping of images. Slides pictures on top of each
other so that the most suitable overlap arises, in terms of mutual information.
'''


def main(cmdlineargs=None):
    '''Main driver routine for picslide.

    Args:
        cmdlineargs: List of command line arguments. When None, arguments in
            sys.argv are parsed (default: None)

    '''

    args = parse_cmdline_args(cmdlineargs)
    picslide(args)


def parse_cmdline_args(cmdlineargs=None):
    '''Parses command line arguments.

    Args:
        cmdlineargs: List of command line arguments. When None, arguments in
            sys.argv are parsed (default: None)

    '''

    parser = argparse.ArgumentParser(description=USAGE)

    msg = 'input files'
    parser.add_argument('infile', action='store', nargs='+', type=str, help=msg)

    args = parser.parse_args(cmdlineargs)

    return args


def picslide(args):
    '''Slides pictures on top of each other so that the most suitable overlap
       arises, in terms of mutual information.

    Args:
        args: Namespace of command line arguments

    '''

    infiles = args.infiles
    print(infiles)
