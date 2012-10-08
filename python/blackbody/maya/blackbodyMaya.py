from pymel.core import *

RAMP_COLOR_TEMPLATE = r'%s.colorEntryList[%d].color'
RAMP_POSITION_TEMPLATE = r'%s.colorEntryList[%d].position'
FLUID_COLOR_TEMPLATE = r'%s.incandescence[%d].incandescence_Color'
FLUID_POSITION_TEMPLATE = r'%s.incandescence[%d].incandescence_Position'
FLUID_INTERP_TEMPLATE = r'%s.incandescence[%d].incandescence_Interp'

def setupWithNode(items, mint, maxt, nsamples):
	loadPlugin('blackbodyNode.py', quiet=True)
	for item in items:
		node = createNode('blackbody')
		node.numberOfSamples.set(nsamples)
		addEnergyCtrlAttr(item)
		setupConnections(item, node, nsamples, mint, maxt)
		print('[INFO] Blackbody node setup: %s' % item.name())

def setupWithExpression(items, mint, maxt, nsamples):
	for item in items:
		addEnergyCtrlAttr(item)
		setupBlackbodyExpression(item, nsamples, mint, maxt)
		print('[INFO] Blackbody expression setup: %s' % item.name())

def addEnergyCtrlAttr(item):
	if not objExists('%s.energyExp' % item.name()):
		item.addAttr('energyExp', sn='eexp', at='double', min=0.0, smx=4.0, dv=4.0)
	if not objExists('%s.energyMult' % item.name()):
		item.addAttr('energyMult', sn='emult', at='double', min=0.0, smx=10.0, dv=5.0)
	if not objExists('%s.energyOffset' % item.name()):
		item.addAttr('energyOffset', sn='eoff', at='double', min=0.0, max=1.0, dv=0.0)
	if not objExists('%s.minTemperature' % item.name()):
		item.addAttr('minTemperature', sn='mint', at='double', min=0.0, smx=10000.0, dv=500.0)
	if not objExists('%s.maxTemperature' % item.name()):
		item.addAttr('maxTemperature', sn='maxt', at='double', min=0.0, smx=10000.0, dv=2000.0)
	item.energyExp.setKeyable(True)
	item.energyMult.setKeyable(True)
	item.energyOffset.setKeyable(True)

def initializeExpression(nodeName, nsamples):
	expl = ''
	expl += 'float $mint = %s.minTemperature;\n' % nodeName
	expl += 'float $maxt = %s.maxTemperature;\n' % nodeName
	expl += 'int $nsamples = %d;\n' % nsamples
	expl += 'float $exp = %s.energyExp;\n' % nodeName 
	expl += 'float $invertedMaxEnergy = 1.0 / pow($maxt, $exp);\n'
	expl += 'float $eMult = %s.energyMult;\n' % nodeName
	expl += 'float $eOffset = clamp(0, 1.0, %s.energyOffset);\n' % nodeName
	expl += 'float $invert_eOffset = 1.0 - $eOffset;\n'
	expl += 'float $energy = 1.0;\n'
	expl += 'float $tstep = ($maxt - $mint) / (float)($nsamples - 1);\n'
	expl += 'float $t = $mint;\n'
	expl += 'float $pstep = 1.0 / ($nsamples - 1);\n'
	expl += 'float $p = 0;\n'
	expl += 'float $rgb[];\n'
	return expl

def setupConnections(item, node, nsamples, mint, maxt):
	colAttrTmpl = RAMP_COLOR_TEMPLATE if item.type() == 'ramp' else FLUID_COLOR_TEMPLATE
	posAttrTmpl = RAMP_POSITION_TEMPLATE if item.type() == 'ramp' else FLUID_POSITION_TEMPLATE
	for i in range(nsamples):
		node.outColor[i] >> Attribute(colAttrTmpl % (item.name(), i))
		node.outCoord[i] >> Attribute(posAttrTmpl % (item.name(), i))
		item.minTemperature.set(mint)
		item.maxTemperature.set(maxt)
		item.minTemperature >> node.minTemperature
		item.maxTemperature >> node.maxTemperature
		item.energyExp >> node.energyExp
		item.energyMult >> node.energyMult
		item.energyOffset >> node.energyOffset
		if item.type() == 'fluidShape':
			Attribute(FLUID_INTERP_TEMPLATE % (item.name(), i)).set(1) # Linear


def setupBlackbodyExpression(item, nsamples, mint, maxt):
	colAttrTmpl = RAMP_COLOR_TEMPLATE if item.type() == 'ramp' else FLUID_COLOR_TEMPLATE
	posAttrTmpl = RAMP_POSITION_TEMPLATE if item.type() == 'ramp' else FLUID_POSITION_TEMPLATE
	item.minTemperature.set(mint)
	item.maxTemperature.set(maxt)
	step = 1.0 / (nsamples - 1)
	expl = initializeExpression(item.name(), nsamples)
	initrgb = [0, 0, 0]
	for i in range(nsamples):
		colAttr = Attribute(colAttrTmpl % (item.name(), i))
		posAttr = Attribute(posAttrTmpl % (item.name(), i))
		# initialize
		colAttr.set(initrgb)
		if item.type() == 'fluidShape':
			Attribute(FLUID_INTERP_TEMPLATE % (item.name(), i)).set(1) # Linear
		# add to expression
 		expl += '$energy = (pow($t, $exp) * $invertedMaxEnergy * $invert_eOffset + $eOffset) * $eMult;\n'
		expl += '$rgb = blackbodyToRGB($t);\n'
		expl += '%sR = $rgb[0] * $energy;\n' % colAttr.name()
		expl += '%sG = $rgb[1] * $energy;\n' % colAttr.name()
		expl += '%sB = $rgb[2] * $energy;\n' % colAttr.name()
		expl += '%s = $p;\n' % posAttr.name()
		expl += '$t += $tstep;\n'
		expl += '$p += $pstep;\n'
		expl += '\n'
	expression(s=expl, alwaysEvaluate=True, unitConversion='all', n='exp_blackbody_%s' % item.name())

