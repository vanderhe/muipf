#------------------------------------------------------------------------------#
#  MUIPF: Mutual Information Image Processing Framework                        #
#  Copyright (C) 2020 - 2021  MUIPF developers group                           #
#                                                                              #
#  See the LICENSE file for terms of usage and distribution.                   #
#------------------------------------------------------------------------------#


'''Common functions building the muipf test framework.'''


import sys
import unittest
import tempfile
import shutil
import os.path
from io import StringIO
import numpy as np


RTOL = 1e-05
ATOL = 1e-08


def hypersurface_file_equals(current, reference, rtol=RTOL, atol=ATOL):
    '''Checks contents of mutual information hypersurface files for equality.

    Args:

        current (str): path to current mutual information hypersurface file
        reference (str): path to reference mutual information hypersurface file
        rtol (float): relative tolerance parameter
        atol (float): absolute tolerance parameter

    Returns:

        equal (bool): true, if arrays are equal within given tolerances

    '''

    curmi = np.loadtxt(current)
    refmi = np.loadtxt(reference)

    equal = np.allclose(curmi, refmi, rtol=rtol, atol=atol, equal_nan=False)

    return equal


def get_temporary_filename(path):
    '''Creates a unique temporary file and returns its name.

    Args:

        path: path where temporary file should be created

    Returns:

        tmpname (str): name of generated temporary file

    '''

    tmpfile = tempfile.NamedTemporaryFile(dir=path)
    tmpname = tmpfile.name
    tmpfile.close()

    return tmpname


class TestInWorkDir(unittest.TestCase):
    '''Base class for tests with a working directory for file output.'''


    def setUp(self):
        '''Sets up the current instance based on an already existing inputdir
           and workroot. The default behavior is to delete the working
           directory afterwards. This can be influenced via the keepworkdir
           boolean.
        '''

        prefix = '.'.join(self.id().split('.')[1:]) + '_'

        self.workdir = tempfile.mkdtemp(prefix=prefix, dir=self.workroot)

        # by default, delete working directory
        self.keepworkdir = False


    def tearDown(self):
        '''If desired, cleans up the working directory after running tests.'''

        if not self.keepworkdir:
            shutil.rmtree(self.workdir)


    def get_full_inpath(self, fname):
        '''Returns the full input path for a given file name.

        Args:

            fname (str): file name to prefix with the input directory

        Returns:

            inpath (str): full input path for the given file name

        '''

        inpath = os.path.join(self.inputdir, fname)

        return inpath


    def get_full_outpath(self, fname):
        '''Returns the full output path for a given file name.

        Args:

            fname (str): file name to prefix with the output directory

        Returns:

            outpath (str): full output path for the given file name

        '''

        outpath = os.path.join(self.workdir, fname)

        return outpath


class OutputCatcher:
    '''Catches the standard output of a function. Can be used to intercept the
       output of command line scripts and analyze or redirect it (e.g. devnull)
    '''


    def __enter__(self):

        self._output = None
        self._stdout = sys.stdout
        self._stringio = StringIO()
        sys.stdout = self._stringio

        return self


    def __exit__(self, *args):

        sys.stdout = self._stdout
        self._output = self._stringio.getvalue()
        self._stringio.close()


    def get_as_string(self):
        '''Returns the catched output as string.'''

        return self._output


    def get_as_stringio(self):
        '''Returns the catched output as StringIO file object.'''

        return StringIO(self._output)
