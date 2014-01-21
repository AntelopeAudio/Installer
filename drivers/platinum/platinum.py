#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import os.path
import sys

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
