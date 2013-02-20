# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 09:26:59 2013


@author: nick
"""

import msds

msds.getmsds('ammonium molybdate')
msds.getmsds('chloroform')
msds.getmsds('Hydrochloric Acid')
msds.getmsds('Potassium Chromate')
msds.getmsds('Sodium Sulfate Anh')
print ''
print '--------Begin LaTEX Output---------------'

print msds.safetymaster
print msds.bibmaster