import sys
from maya import OpenMaya 
from maya import OpenMayaMPx
from blackbody import blackbody

def getBlackbodyColorAndCoord(index, nSamples, minTemp, maxTemp, energyExp, energyOffset, energyMult):
	coordStep = 1.0 / (nSamples - 1)
	sampleStep = (maxTemp-minTemp) / (nSamples-1.0)
	iMaxEnergy = 1.0 / pow(maxTemp, energyExp)
	iEnergyOffset = 1.0 - energyOffset
	t = int(minTemp+sampleStep * index)
	e = (pow(t, energyExp) * iMaxEnergy * iEnergyOffset + energyOffset) * energyMult
	c = blackbody.blackbodyToRGB(t) 
	return OpenMaya.MFloatVector(c[0]*e, c[1]*e, c[2]*e), coordStep

########## BlackbodyNode class ##############################
class BlackbodyNode(OpenMayaMPx.MPxNode):
	kPluginNodeName = 'blackbody'
	kPluginNodeId = OpenMaya.MTypeId(0x999f1) # tmp value. you should change this number.

	aMinTemperature = OpenMaya.MObject()
	aMaxTemperature = OpenMaya.MObject()
	aNumSamples = OpenMaya.MObject()
	aEnergyExp = OpenMaya.MObject()
	aEnergyMult = OpenMaya.MObject()
	aEnergyOffset = OpenMaya.MObject()
	aOutColor = OpenMaya.MObject()
	aOutCoord = OpenMaya.MObject()

	def __init__(self):
		OpenMayaMPx.MPxNode.__init__(self)

	def compute(self, plug, dataBlock):
		if  plug != BlackbodyNode.aOutColor and plug != BlackbodyNode.aOutCoord:
			return OpenMaya.kUnknownParameter

		logicalIndex = plug.logicalIndex()
		minTemp = dataBlock.inputValue(self.aMinTemperature).asDouble()
		maxTemp = dataBlock.inputValue(self.aMaxTemperature).asDouble()
		nSamples = dataBlock.inputValue(self.aNumSamples).asInt()
		energyExp = dataBlock.inputValue(self.aEnergyExp).asDouble()
		energyMult = dataBlock.inputValue(self.aEnergyMult).asDouble()
		energyOffset = dataBlock.inputValue(self.aEnergyOffset).asDouble()
		outColor_hdl = dataBlock.outputArrayValue(self.aOutColor)
		outCoord_hdl = dataBlock.outputArrayValue(self.aOutCoord)

		# set blackbody radiation color
		color, coordStep = getBlackbodyColorAndCoord(logicalIndex, nSamples,
			minTemp, maxTemp, energyExp, energyOffset, energyMult)
		outColor_hdl.jumpToElement(logicalIndex)
		outCoord_hdl.jumpToElement(logicalIndex)
		outColor_hdl.outputValue().setMFloatVector(color)
		outCoord_hdl.outputValue().setFloat(logicalIndex * coordStep)

		dataBlock.setClean(plug)

	# creator
	@staticmethod
	def creator():
		return OpenMayaMPx.asMPxPtr(BlackbodyNode())
	
	# initilize
	@staticmethod
	def initializer():
		nAttr = OpenMaya.MFnNumericAttribute()
		BlackbodyNode.aMinTemperature = nAttr.create('minTemperature', 'mint',
			OpenMaya.MFnNumericData.kDouble, 500.0)
		nAttr.setMin(0.0)
		nAttr.setSoftMax(10000.0)
		nAttr.setKeyable(True)
		nAttr.setReadable(True)
		nAttr.setWritable(True)
		nAttr.setStorable(True)

		BlackbodyNode.aMaxTemperature = nAttr.create('maxTemperature', 'maxt',
			OpenMaya.MFnNumericData.kDouble, 2000.0)
		nAttr.setMin(0.0)
		nAttr.setSoftMax(10000.0)
		nAttr.setKeyable(True)
		nAttr.setReadable(True)
		nAttr.setWritable(True)
		nAttr.setStorable(True)

		BlackbodyNode.aNumSamples = nAttr.create('numberOfSamples', 'ns',
			OpenMaya.MFnNumericData.kInt, 20)
		nAttr.setMin(2)
		nAttr.setSoftMax(100)
		nAttr.setKeyable(True)
		nAttr.setReadable(True)
		nAttr.setWritable(True)
		nAttr.setStorable(True)

		BlackbodyNode.aEnergyExp = nAttr.create('energyExp', 'ee',
			OpenMaya.MFnNumericData.kDouble, 4.0)
		nAttr.setMin(0.0)
		nAttr.setSoftMin(1.0)
		nAttr.setSoftMax(4.0)
		nAttr.setKeyable(True)
		nAttr.setReadable(True)
		nAttr.setWritable(True)
		nAttr.setStorable(True)

		BlackbodyNode.aEnergyMult = nAttr.create('energyMult', 'em',
			OpenMaya.MFnNumericData.kDouble, 5.0)
		nAttr.setMin(0.0)
		nAttr.setSoftMax(20.0)
		nAttr.setKeyable(True)
		nAttr.setReadable(True)
		nAttr.setWritable(True)
		nAttr.setStorable(True)

		BlackbodyNode.aEnergyOffset = nAttr.create('energyOffset', 'eo',
			OpenMaya.MFnNumericData.kDouble, 0.0)
		nAttr.setMin(0.0)
		nAttr.setMax(1.0)
		nAttr.setKeyable(True)
		nAttr.setReadable(True)
		nAttr.setWritable(True)
		nAttr.setStorable(True)

		BlackbodyNode.aOutColor = nAttr.createColor('outColor', 'ocl')
		nAttr.setArray(True)
		nAttr.setKeyable(False)
		nAttr.setReadable(True)
		nAttr.setWritable(False)
		nAttr.setStorable(False)

		BlackbodyNode.aOutCoord = nAttr.create('outCoord', 'ocd',
			OpenMaya.MFnNumericData.kFloat, 0.0)
		nAttr.setArray(True)
		nAttr.setKeyable(False)
		nAttr.setReadable(True)
		nAttr.setWritable(False)
		nAttr.setStorable(False)

		BlackbodyNode.addAttribute(BlackbodyNode.aMinTemperature)
		BlackbodyNode.addAttribute(BlackbodyNode.aMaxTemperature)
		BlackbodyNode.addAttribute(BlackbodyNode.aNumSamples)
		BlackbodyNode.addAttribute(BlackbodyNode.aEnergyExp)
		BlackbodyNode.addAttribute(BlackbodyNode.aEnergyMult)
		BlackbodyNode.addAttribute(BlackbodyNode.aEnergyOffset)
		BlackbodyNode.addAttribute(BlackbodyNode.aOutColor)
		BlackbodyNode.addAttribute(BlackbodyNode.aOutCoord)

		BlackbodyNode.attributeAffects(BlackbodyNode.aMinTemperature, BlackbodyNode.aOutColor)
		BlackbodyNode.attributeAffects(BlackbodyNode.aMaxTemperature, BlackbodyNode.aOutColor)
		BlackbodyNode.attributeAffects(BlackbodyNode.aNumSamples, BlackbodyNode.aOutColor)
		BlackbodyNode.attributeAffects(BlackbodyNode.aEnergyExp, BlackbodyNode.aOutColor)
		BlackbodyNode.attributeAffects(BlackbodyNode.aEnergyMult, BlackbodyNode.aOutColor)
		BlackbodyNode.attributeAffects(BlackbodyNode.aEnergyOffset, BlackbodyNode.aOutColor)
		BlackbodyNode.attributeAffects(BlackbodyNode.aMinTemperature, BlackbodyNode.aOutCoord)
		BlackbodyNode.attributeAffects(BlackbodyNode.aMaxTemperature, BlackbodyNode.aOutCoord)
		BlackbodyNode.attributeAffects(BlackbodyNode.aNumSamples, BlackbodyNode.aOutCoord)
		BlackbodyNode.attributeAffects(BlackbodyNode.aEnergyExp, BlackbodyNode.aOutCoord)
		BlackbodyNode.attributeAffects(BlackbodyNode.aEnergyMult, BlackbodyNode.aOutCoord)
		BlackbodyNode.attributeAffects(BlackbodyNode.aEnergyOffset, BlackbodyNode.aOutCoord)


# Register plag-in
def initializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject)
	try:
		mplugin.registerNode(BlackbodyNode.kPluginNodeName, BlackbodyNode.kPluginNodeId,
			BlackbodyNode.creator, BlackbodyNode.initializer)
	except:
		sys.stderr.write('Failed to register node: %s' % BlackbodyNode.kPluginNodeName)
		raise

# uninitialize the script plug-in
def uninitializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject)
	try:
		mplugin.deregisterNode(BlackbodyNode.kPluginNodeId)
	except:
		sys.stderr.write('Failed to deregister node: %s' % BlackbodyNode.kPluginNodeName)
		raise


