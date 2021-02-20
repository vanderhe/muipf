#------------------------------------------------------------------------------#
#  MUIPF: Mutual Information Image Processing Framework                        #
#  Copyright (C) 2020 - 2021  MUIPF developers group                           #
#                                                                              #
#  See the LICENSE file for terms of usage and distribution.                   #
#------------------------------------------------------------------------------#


'''Common things needed by the command line scripts.'''


class ScriptError(Exception):
    '''Exception thrown by the command line scripts.'''


def print_line(lenght=80):
    '''Prints a simple line of given length to stdout.

    Args:

        lenght (int): line lenght

    '''

    line = '-'

    print('\n' + lenght * line + '\n')
