#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import os.path
import sys
import pkg_resources


# LD_LIBRARY_PATH = os.environ.get('LD_LIBRARY_PATH', '')
# os.environ['LD_LIBRARY_PATH'] = '{}:{}'.format(
#     pkg_resources.resource_filename('installer_platinum_res', 'libs'),
#     LD_LIBRARY_PATH
# )
# print('LD_LIBRARY_PATH={}'.format(os.environ['LD_LIBRARY_PATH']))

# import subprocess
# cmd = 'for SO in {}/*.so; do ldd $SO | grep -e pyglib; done'.format(
#     os.path.normpath(
#         pkg_resources.resource_filename('installer_platinum_res', '..')
#     )
# )
# print('cmd={}'.format(cmd))
# subprocess.call(cmd, shell=True)

os.environ.setdefault('INSTALLER_RESOURCE_MODULE', 'installer_platinum')

# A little hack to find the `installer` package
try:
    import installer.app
except ImportError:
    argv0 = os.path.realpath(sys.argv[0])
    if os.path.isdir(argv0):
        d = argv0
    else:
        d = os.path.dirname(argv0)
    sys.path.append(os.path.dirname(os.path.dirname(d)))
    import installer.app


installer.app.main()
