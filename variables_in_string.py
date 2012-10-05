#!/usr/bin/env python
"""Expand variables to their values inside strings"""

var_one = "one"
var_two = 2

outstring = "first variable is {var_one}, and second variable is {var_two}".format(**locals())
print outstring
