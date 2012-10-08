#! /usr/bin/python
from stdObserver import CIE_X, CIE_Y, CIE_Z
import math

XYZtosRGB = (
  3.2404542, -1.5371385, -0.4985314,
 -0.9692660,  1.8760108,  0.0415560,
  0.0556434, -0.2040259,  1.0572252
  )

def stdObserverX(w):
	return CIE_X[w]

def stdObserverY(w):
	return CIE_Y[w]

def stdObserverZ(w):
	return CIE_Z[w]

def planck(w, t):
	wm = w * 1e-9	# wavelength from nanometers to meters
	c1 = 3.7402e-16
	c2 = 1.43848e-2
	return (c1*wm**-5.0) / (math.e**(c2/(wm*t))-1)

def planck1(w, t):
	c2 = 1.4388e7
	norm = (555.0**5.0) * (math.e**(c2/(555.0*t)) - 1.0)
	r = norm / ((w**5.0) * (math.e**(c2/(w*t)) - 1))
	return r

def XYZtoRGB(xyz):
	rgb = [0.0, 0.0, 0.0]
	rgb[0] = xyz[0]*XYZtosRGB[0] + xyz[1]*XYZtosRGB[1] + xyz[2]*XYZtosRGB[2]
 	rgb[1] = xyz[0]*XYZtosRGB[3] + xyz[1]*XYZtosRGB[4] + xyz[2]*XYZtosRGB[5]
 	rgb[2] = xyz[0]*XYZtosRGB[6] + xyz[1]*XYZtosRGB[7] + xyz[2]*XYZtosRGB[8]
	biggest = max(rgb)
	# normalize
	if biggest > 0.0:
		rgb[0] /= biggest
		rgb[1] /= biggest
		rgb[2] /= biggest
	return rgb

def blackbodyToXYZ(t):
	xyz = [0.0, 0.0, 0.0]
	step = 5 # unit: nanometer
	startWavelength = 360
	endWavelength = 830
	i = 0
	for w in range(startWavelength, endWavelength + step, step):
		I = planck(w, t)
		#I = planck1(w, t)
		xyz[0] += I * stdObserverX(i)
		xyz[1] += I * stdObserverY(i)
		xyz[2] += I * stdObserverZ(i)
		i += 1
	#mxyz = max(xyz)
	mxyz = xyz[0] + xyz[1] + xyz[2]
	xyz[0] /= mxyz
	xyz[1] /= mxyz
	xyz[2] /= mxyz
	#print '[XYZ]:', xyz, '-',
	return xyz

def stefan_boltzman(t, exp=4):
	sigma = 5.67*10-8
	return sigma*(T**exp)

def blackbodyToRGB(t):
	xyz = blackbodyToXYZ(t)
	return XYZtoRGB(xyz)


if __name__ == '__main__':
	import sys
	for t in range(1000, 10200, 200):
		print t, ':', '[RGB]:', blackbodyToRGB(t)

