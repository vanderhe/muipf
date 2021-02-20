#------------------------------------------------------------------------------#
#  MUIPF: Mutual Information Image Processing Framework                        #
#  Copyright (C) 2020 - 2021  MUIPF developers group                           #
#                                                                              #
#  See the LICENSE file for terms of usage and distribution.                   #
#------------------------------------------------------------------------------#


'''
Regression tests for the picslide command line script.
'''


import sys
import os.path
import unittest
from muipf.scripts.common import ScriptError
import muipf.scripts.picslide as picslide
import common


SCRIPTDIR = os.path.dirname(sys.argv[0])


class PicslideTest(common.TestInWorkDir):
    '''Regression tests for the picslide command line script.'''


    def setUp(self):
        self.inputdir = os.path.join(SCRIPTDIR, 'picslide')
        self.workroot = './'
        common.TestInWorkDir.setUp(self)


    def test_core_easy(self):
        '''Testcase for core functionality (easy).'''

        infile1 = self.get_full_inpath('retina_base.png')
        infile2 = self.get_full_inpath('retina_sub.png')

        reffile = self.get_full_inpath('hypersurface_ref_retina.dat')
        outfile = self.get_full_outpath('hypersurface_cur_retina.dat')

        cmdargs = [infile1, infile2, '-o', outfile]

        with common.OutputCatcher() as _:
            picslide.main(cmdargs)

        equal = common.hypersurface_file_equals(outfile, reffile)

        self.assertTrue(equal)


    def test_core_difficult(self):
        '''Testcase for core functionality (difficult).'''

        infile1 = self.get_full_inpath('grass_base.png')
        infile2 = self.get_full_inpath('grass_sub.png')

        reffile = self.get_full_inpath('hypersurface_ref_grass.dat')
        outfile = self.get_full_outpath('hypersurface_cur_grass.dat')

        cmdargs = [infile1, infile2, '-o', outfile]

        with common.OutputCatcher() as _:
            picslide.main(cmdargs)

        equal = common.hypersurface_file_equals(outfile, reffile)

        self.assertTrue(equal)

        infile1 = self.get_full_inpath('gravel_base.png')
        infile2 = self.get_full_inpath('gravel_sub.png')

        reffile = self.get_full_inpath('hypersurface_ref_gravel.dat')
        outfile = self.get_full_outpath('hypersurface_cur_gravel.dat')

        cmdargs = [infile1, infile2, '-o', outfile]

        with common.OutputCatcher() as _:
            picslide.main(cmdargs)

        equal = common.hypersurface_file_equals(outfile, reffile)

        self.assertTrue(equal)


    def test_fail_invalid_infile(self):
        '''Testcase for invocation with invalid infile(s).'''

        # get unique temporary filename as invalid input file
        tmpname = common.get_temporary_filename(self.workroot)

        infile1 = self.get_full_inpath('base.png')
        infile2 = os.path.join(self.workdir, tmpname)

        outfile = self.get_full_outpath('hypersurface_cur.dat')

        cmdargs = [infile1, infile2, '-o', outfile]

        with common.OutputCatcher() as _:
            with self.assertRaises(ScriptError):
                picslide.main(cmdargs)


if __name__ == '__main__':
    unittest.main()
