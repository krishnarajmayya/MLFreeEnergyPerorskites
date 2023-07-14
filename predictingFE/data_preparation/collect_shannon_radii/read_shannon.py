#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 01:18:44 2023

@author: krishnarajmayya
"""

import json
with open("shannon-radii.json") as f:
    out = f.read()

d = json.loads(out)

# Enter Element, Charge, Coordination and one of - r_crystal, r_ionic, spin, remark

print(d['Br'])