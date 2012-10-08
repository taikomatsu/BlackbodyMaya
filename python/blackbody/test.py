#!/usr/bin/python
import matplotlib.pyplot as plt
import blackbody
from stdObserver import CIE_X, CIE_Y, CIE_Z
import Image, ImageDraw

def testRGB():
	v = [blackbody.blackbodyToRGB(t) for t in range(100, 12100, 100)]
	x = [v[i][0] for i in range(len(v))]
	y = [v[i][1] for i in range(len(v))]
	z = [v[i][2] for i in range(len(v))]
	plt.plot(x, 'r-')
	plt.plot(y, 'g-')
	plt.plot(z, 'b-')
	#plt.plot(v)
	plt.axis([0, len(v), -0.2, 1.0])
	plt.show()

def testXYZ():
	v = [blackbody.blackbodyToXYZ(t) for t in range(100, 12100, 100)]
	x = [v[i][0] for i in range(len(v))]
	y = [v[i][1] for i in range(len(v))]
	z = [v[i][2] for i in range(len(v))]
	#print [i for i in range(0, len(v), 3)] 
	#print [i for i in range(1, len(v), 3)] 
	#print [i for i in range(2, len(v), 3)] 
	plt.plot(x, 'r-')
	plt.plot(y, 'g-')
	plt.plot(z, 'b-')
	plt.axis([0, len(v), -0.2, 0.8])
	plt.show()

def testCIE():
	#v = zip(CIE_X, CIE_Y, CIE_Z)
	#plt.plot(v)
	plt.plot(CIE_X, 'r-')
	plt.plot(CIE_Y, 'g-')
	plt.plot(CIE_Z, 'b-')
	plt.axis([0, 70, 0, 1.8])
	plt.show()

def convertIntRGB(rgb):
	r = int(min(1.0, max(0.0, rgb[0]))*255.0)
	g = int(min(1.0, max(0.0, rgb[1]))*255.0)
	b = int(min(1.0, max(0.0, rgb[2]))*255.0)
	return 'rgb(%s, %s, %s)' % (r, g, b)

def testRGB2():
	st = 100
	ed = 12100
	#v = [blackbody.blackbodyToRGB(t) for t in range(1000, 10000, 10)]
	v = [blackbody.blackbodyToRGB(t) for t in range(st, ed, 10)]
	#x = [v[i][0] for i in range(len(v))]
	#y = [v[i][1] for i in range(len(v))]
	#z = [v[i][2] for i in range(len(v))]
	w = 1
	im = Image.new("RGB", [len(v)*w, 300])
	draw = ImageDraw.Draw(im)
	for i in range(len(v)):
		rgb = convertIntRGB(v[i])
		draw.line((i*w, 0, i*w, 300), width=w, fill=rgb)
	del draw
	im.save('images/blackbodyToRGB_%sk_%sk.png' % (st, ed), "PNG")
	#im.save('images/blackbodyToRGB_%sk_%sk_planck1.png' % (st, ed), "PNG")
	print('>>OK')
	#im.show()


if __name__ == '__main__':
	#testRGB2()
	testXYZ()
	#testCIE()

