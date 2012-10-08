from pymel.core import *
from maya import OpenMaya
from blackbody.maya import blackbodyMaya
from blackbody import blackbody

VALID_TYPES = ['fluidShape', 'ramp']
MINT = 100.0 # K
MAXT = 20000.0 # K

ws = {}
TOOL_INFO = None

def __maya_version():
	return about(v=True).split(' ')[0]

def __initialize():
	ws = {}
	TOOL_INFO = None

def __open(wName, wInfo):
	__initialize()
	with window(wName, **wInfo) as wnd:
		#with menu(l='Menu'):
		#	menuItem(l='About', c=lambda x: about())
		#	menuItem(l='Exit', c=lambda x, w=wName: close(w))
		with autoLayout(ratios=[8, 2]):
			with frameLayout(bs='etchedIn', lv=False, bv=True, cll=False, cl=False):
				with autoLayout():
					#with optionMenuGrp(l='Preset') as ws['preset']:
					#	for p in PRESETS:
					#		menuItem(l=p)
					ws['mode'] = radioButtonGrp(l='Mode', nrb=2, la2=['Expression', 'Node'], sl=1)
					with horizontalLayout(ratios=[9, 1]):
						ws['mint'] = floatSliderGrp(l='Min Temperature', min=MINT, max=MAXT/2., fmx=MAXT, fs=10.0, v=500.0, field=True,
							cc=lambda c:refreshMinTemperatureColorCB())
						ws['col_mint'] = canvas(en=False)
						refreshMinTemperatureColorCB()
					with horizontalLayout(ratios=[9, 1]):
						ws['maxt'] = floatSliderGrp(l='Max Temperature', min=MINT, max=MAXT/2., fmx=MAXT, fs=10.0, v=2000.0, field=True,
							cc=lambda c:refreshMaxTemperatureColorCB())
						ws['col_maxt'] = canvas(en=False)
						refreshMaxTemperatureColorCB()
					ws['nsamples'] = intSliderGrp(l='Samples', fmn=2, max=50, fs=1, v=20, field=True)
					separator(h=5, st='none')
			with horizontalLayout():
				button(l='Set to Selected', c=lambda x: setToSelectedCB())
				button(l='Close', c=lambda x, w=wName: close(w))

def open(kwargs):
	close(kwargs['name'])
	TOOL_INFO = kwargs
	wInfo = {'width': 260, 'height': 570, 'menuBar': True}
	__open(kwargs['name'], wInfo)

def close(wName):
	if window(wName, q=True, ex=True):
		deleteUI(wName, window=True)

def getBlackbodyColor(t):
	return blackbody.blackbodyToRGB(t)

def clampRGB(color):
	eps = 1e-6
	color[0] = eps if color[0] < eps else color[0]
	color[1] = eps if color[1] < eps else color[1]
	color[2] = eps if color[2] < eps else color[2]
	return color

def refreshMinTemperatureColorCB():
	t = max(1e-6, ws['mint'].getValue())
	rgb = clampRGB(getBlackbodyColor(t))
	if 'col_mint' in ws:
		ws['col_mint'].setRgbValue(rgb)

def refreshMaxTemperatureColorCB():
	t = max(1e-6, ws['maxt'].getValue())
	rgb = clampRGB(getBlackbodyColor(t))
	if 'col_maxt' in ws:
		ws['col_maxt'].setRgbValue(rgb)

def getItemsFromSelected():
	validItem = []
	for sel in selected():
		if sel.type() in VALID_TYPES:
			validItem.append(sel)
			continue
		if sel.type() == 'transform':
			for sh in sel.getShapes():
				if sh.type() in VALID_TYPES:
					validItem.append(sh)
					break
	return validItem

def setToSelectedCB():
	mode = ws['mode'].getSelect()
	mint = ws['mint'].getValue()
	maxt = ws['maxt'].getValue()
	nsamples = ws['nsamples'].getValue()
	items = getItemsFromSelected()
	if maxt <= mint:
		dispError('Invalid temperature.')
		return
	if nsamples < 2:
		dispError('Invalid sample number.')
		return
	if len(items) == 0:
		dispError('No valid object found.')
		return
	else:
		if mode == 1: # expression
			blackbodyMaya.setupWithExpression(items, mint, maxt, nsamples)
		else: # node
			blackbodyMaya.setupWithNode(items, mint, maxt, nsamples)
		print('# Done')

def about():
	pass

def dispError(msg):
	OpenMaya.MGlobal.displayError(msg)

if __name__ == '__main__':
	wInfo = {'name': 'blackbodyWindow', 'title': 'Blackbody', 'w':570, 'h':260, 'menuBar':True}
	open(wInfo)

