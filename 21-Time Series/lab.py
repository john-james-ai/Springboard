#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ======================================================================================================================== #
# Project  : Business One Customer (B1C)                                                                                   #
# Version  : 0.1.0                                                                                                         #
# File     : \lab.py                                                                                                       #
# Language : Python 3.8                                                                                                    #
# ------------------------------------------------------------------------------------------------------------------------ #
# Author   : John James                                                                                                    #
# Company  : Your Company                                                                                                  #
# Email    : john.james.ai.studio@gmail.com                                                                                #
# URL      : https://github.com/john-james-ai/b1c                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# Created  : Tuesday, December 7th 2021, 8:01:43 pm                                                                        #
# Modified : Tuesday, December 7th 2021, 8:03:48 pm                                                                        #
# Modifier : John James (john.james.ai.studio@gmail.com)                                                                   #
# ------------------------------------------------------------------------------------------------------------------------ #
# License  : BSD 3-clause "New" or "Revised" License                                                                       #
# Copyright: (c) 2021 Your Company                                                                                         #
# ======================================================================================================================== #
#%%
import itertools
a = [1,2,3]
b = [1,3,4]
c = [5,6,7]
d = [a,b,c]
e = list(itertools.product(*d))
print(e, len(e))
# %%
