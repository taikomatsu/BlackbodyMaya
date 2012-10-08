#! /usr/bin/python

from CIE_X import CIE_X
from CIE_Y import CIE_Y
from CIE_Z import CIE_Z
import os.path
import os
import sys

reformatFile = '%s/stdObserver.py' % os.path.dirname(os.getcwd())
f = file(reformatFile, 'w')
elems_per_line = 5

f.write('# CIE starndard observer 1931\n')
f.write('# http://www.cis.rit.edu/mcsl/online/cie.php\n')

def reformat(f, name, ls):
	f.write('%s = (' % name)
	s = ''
	i = 0
	size = len(ls)
	for l in ls:
		s += '%e' % l
		i += 1
		s += ', ' if i != size else ')'
		if i % elems_per_line == 0:
			s += '\n'
			f.write(s)
			s = ''
	f.write('\n')

reformat(f, 'CIE_X', CIE_X)
reformat(f, 'CIE_Y', CIE_Y)
reformat(f, 'CIE_Z', CIE_Z)
f.close()
print('// written to %s' % reformatFile)

