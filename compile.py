# -*- coding: utf-8 -*-
"""
Created on 2019-03-07T13:20:31.888Z

@author: mrader1248
"""

########################### python 2/3 compatibility ###########################
from __future__ import absolute_import, division, print_function
from six.moves import range
################################################################################

import os
import subprocess
import sys

# --enable-config=haswell
# --with-blas=~/anaconda3/lib/libmkl_rt.so

CONFIG_ARGS = sys.argv[1:]
GIT_URL = "https://github.com/devinamatthews/tblis.git"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

if os.path.isdir("tblis_git"):
    os.chdir("tblis_git")
    subprocess.run(["git", "pull"])
else:
    subprocess.run(["git", "clone", GIT_URL, "tblis_git"])
    os.chdir("tblis_git")

err = subprocess.run(["./configure",
                      "--prefix={}/tblis_install".format(SCRIPT_DIR),
                      "--with-length-type=long int",
                      "--with-stride-type=long int",
                      "--with-label-type=char"] + CONFIG_ARGS).returncode
if err != 0:
    print("ERROR: failed to configure tblis")
    exit(-1)

err = subprocess.run("make").returncode
if err != 0:
    print("ERROR: building of tblis failed")
    exit(-1)

err = subprocess.run(["make", "install"]).returncode
if err != 0:
    print("ERROR: install of tblis failed")
    exit(-1)
