#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from pkg_resources import resource_filename
import os.path
import sys

from cx_Freeze import Executable, setup

# Add `installer` and `installer_res` to PYTHONPATH
sys.path.append(os.path.realpath('../..'))
installer_res_path = os.path.relpath(resource_filename('installer_res', ''))


build_exe_options = {
    "packages": ["gtk", "installer", "installer_platinum"],
    "excludes": ["tkinter"],
    "include_files": ["installer_platinum_res",
                      (installer_res_path, "installer_res"),]
}


setup(name='Installer',
      version='0.1',
      description='',
      options={'build_exe': build_exe_options},
      executables=[Executable('platinum.py')])
