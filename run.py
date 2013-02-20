# -*- coding: utf-8 -*-
"""
This is chemsafety,
Created on Wed Feb 20 09:26:59 2013


@author: nick
"""
import msds

import sys


debug=False
#name output files
outfile='safety.tex'
outfile2='safety.bib'



argcount = len(sys.argv)
if argcount > 1:
    print 'Number of arguments:', len(sys.argv), 'arguments.'


for item in sys.argv:
    print item
    if 'py' not in item:
        msds.getmsds(item)


def filewrite(outfile, text):
    f = open(outfile,'w')
    f.write(text)
    f.close()


#The chemicals we are looking for
#msds.getmsds('Ammonium Molybdate')
#msds.getmsds('Chloroform')





# Write our tex formatted strings to file.
filewrite(outfile,msds.safetymaster)
filewrite(outfile2,msds.bibmaster)


if debug ==True:
    print ''
    print '--------Begin LaTEX Output---------------'
    print msds.safetymaster
    print msds.bibmaster

#end