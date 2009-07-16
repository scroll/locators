##############################################################
# -----------------------beginHelpText------------------------
# mpLocators  v0.9
# Marin Petrov
# scroll_lock@abv.bg
# http://scroll-lock.eu
# 04.2009
#
#
#
# ------------------------//Usage//---------------------------
# set of custom OpenGL locators. Various shapes and attributes 
# controling the color and alpha. The locators can be seen 
# behind other objects using the backAlpha attribute.
#
#
# ----------------------//Requires//--------------------------
# PyMel module
# Pymel is used to derive the plug values from various Color
# and Point attributes (eg: core.datatypes.getPlugValue())
#
#
# ------------------------//Author//---------------------------
# Marin Petrov;
#
#
# -----------------------endHelpText--------------------------
##############################################################

import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMayaRender as OpenMayaRender
import maya.OpenMayaUI as OpenMayaUI
import math
from pymel import *

glRenderer = OpenMayaRender.MHardwareRenderer.theRenderer()
glFT = glRenderer.glFunctionTable()

curvedArrowVerts = ([0,0,-1.001567],
[-0.336638,0.327886,-0.751175],
[-0.0959835,0.327886,-0.751175],
[-0.0959835,0.500458,-0.500783],
[-0.0959835,0.604001,-0.0987656],
[-0.500783,0.500458,-0.0987656],
[-0.751175,0.327886,-0.0987656],
[-0.751175,0.327886,-0.336638],
[-1.001567,0,0],
[-0.751175,0.327886,0.336638],
[-0.751175,0.327886,0.0987656],
[-0.500783,0.500458,0.0987656],
[-0.0959835,0.604001,0.0987656],
[-0.0959835,0.500458,0.500783],
[-0.0959835,0.327886,0.751175],
[-0.336638,0.327886,0.751175],
[0,0,1.001567],
[0.336638,0.327886,0.751175],
[0.0959835,0.327886,0.751175],
[0.0959835,0.500458,0.500783],
[0.0959835,0.604001,0.0987656],
[0.500783,0.500458,0.0987656],
[0.751175,0.327886,0.0987656],
[0.751175,0.327886,0.336638],
[1.001567,0,0],
[0.751175,0.327886,-0.336638],
[0.751175,0.327886,-0.0987656],
[0.500783,0.500458,-0.0987656],
[0.0959835,0.604001,-0.0987656],
[0.0959835,0.500458,-0.500783],
[0.0959835,0.327886,-0.751175],
[0.336638,0.327886,-0.751175])

qs1 = [2,30,3,29,4,28,4,12,5,11,6,10,12,20,13,19,14,18,4,12,28,20,27,21,26,22]

crvdArrwTriangleIds = [0, 1, 31, 7, 8, 9, 15, 16, 17, 23, 24, 25]

arrowVerts = ( [ 0.17, 0.0, -0.672 ],
[  0.17, 0.0, 0.0 ],
[  0.283, 0.0, 0.0 ],
[  0.0, 0.0, 0.403 ],
[  -0.283, 0.0, 0.0 ],
[  -0.17, 0.0, 0.0 ],
[  -0.17, 0.0, -0.672 ])

arrowIndex = [0, 1, 6, 6, 1, 5, 1, 2, 3, 1, 3, 5, 5, 3, 4]

doubleArrowVerts = ([1,0,0],
[0.6,0,0.4],
[0.6,0,0.2],
[-0.6,0,0.2],
[-0.6,0,0.4],
[-1,0,0],
[-0.6,0,-0.4],
[-0.6,0,-0.2],
[0.6,0,-0.2],
[0.6,0,-0.4])

doubleArrowIds = [0, 1, 9, 4, 5, 6, 2, 3, 7, 7, 8, 2]

def mpLocAddStandardAttributes(node):
	nAttr = OpenMaya.MFnNumericAttribute()

	node.aColor = nAttr.createColor( "color", "col" )
	nAttr.setDefault( 0.1, 0.1, 0.8 )
	nAttr.setKeyable(1)
	nAttr.setReadable(1)
	nAttr.setWritable(1)
	nAttr.setStorable(1)
	nAttr.setMin(0, 0, 0)
	nAttr.setMax(1, 1, 1)

	node.aRotate = nAttr.createPoint( "rotate", "rot" )
	nAttr.setDefault( 0.0, 0.0, 0.0 )
	nAttr.setKeyable(1)
	nAttr.setReadable(1)
	nAttr.setWritable(1)
	nAttr.setStorable(1)

	
	node.aTransparency = nAttr.create( "transparency", "t", OpenMaya.MFnNumericData.kFloat)
	nAttr.setDefault(0.5)
	nAttr.setKeyable(1)
	nAttr.setReadable(1)
	nAttr.setWritable(1)
	nAttr.setStorable(1)
	nAttr.setMin(0)
	nAttr.setMax(1)

	node.aBackAlpha = nAttr.create( "backAlpha", "ba", OpenMaya.MFnNumericData.kFloat)
	nAttr.setDefault(0.2)
	nAttr.setKeyable(1)
	nAttr.setReadable(1)
	nAttr.setWritable(1)
	nAttr.setStorable(1)
	nAttr.setMin(0)
	nAttr.setMax(1)

	node.aLineWidth = nAttr.create( "lineWidth", "lw", OpenMaya.MFnNumericData.kInt)
	nAttr.setDefault(1)
	nAttr.setKeyable(1)
	nAttr.setReadable(1)
	nAttr.setWritable(1)
	nAttr.setStorable(1)
	nAttr.setMin(1)
	nAttr.setMax(10)

 	node.addAttribute(node.aColor)
 	node.addAttribute(node.aRotate)
	node.addAttribute(node.aTransparency)
	node.addAttribute(node.aBackAlpha)
	node.addAttribute(node.aLineWidth)
	
##########################################################################################
################################## curvedArrowNode class #################################
##########################################################################################
		
curvedArrowNodeName = "mpCurvedArrow"
curvedArrowNodeId = OpenMaya.MTypeId(0x87117)

class mpCurvedArrow(OpenMayaMPx.MPxLocatorNode):

	def __init__(self):
		OpenMayaMPx.MPxLocatorNode.__init__(self)
		
	def compute(self, plug, dataBlock):
		return OpenMaya.kUnknownParameter

	def draw(self, view, path, style, status):
		fnThisNode = OpenMaya.MFnDependencyNode(self.thisMObject())
		lw = OpenMaya.MPlug(self.thisMObject(), fnThisNode.attribute("lineWidth")).asInt()
		rt = OpenMaya.MPlug(self.thisMObject(), fnThisNode.attribute ("rotate"))
		a = OpenMaya.MPlug(self.thisMObject(), fnThisNode.attribute("transparency")).asFloat()
		ba = OpenMaya.MPlug(self.thisMObject(), fnThisNode.attribute("backAlpha")).asFloat()
		dt = OpenMaya.MPlug (self.thisMObject(), fnThisNode.attribute ("drawType")).asInt()
		cl = OpenMaya.MPlug(self.thisMObject(), fnThisNode.attribute ("color"))
		rotation = core.datatypes.getPlugValue(rt)
		color = core.datatypes.getPlugValue(cl)
		(r,g,b) = tuple(color)[:3]
		
		def drawShaded(self):
			glFT.glBegin (OpenMayaRender.MGL_TRIANGLES)
			for idx in crvdArrwTriangleIds:
				x,y,z = curvedArrowVerts[idx][0],curvedArrowVerts[idx][1],curvedArrowVerts[idx][2]
				glFT.glVertex3f(x,y,z)
			glFT.glEnd()
			glFT.glBegin(OpenMayaRender.MGL_QUAD_STRIP)
			for idx in qs1[0:6]:
				x,y,z = curvedArrowVerts[idx][0],curvedArrowVerts[idx][1],curvedArrowVerts[idx][2]
				glFT.glVertex3f(x,y,z)
			glFT.glEnd()
			glFT.glBegin(OpenMayaRender.MGL_QUAD_STRIP)
			for idx in qs1[6:12]:
				x,y,z = curvedArrowVerts[idx][0],curvedArrowVerts[idx][1],curvedArrowVerts[idx][2]
				glFT.glVertex3f(x,y,z)
			glFT.glEnd()
			glFT.glBegin(OpenMayaRender.MGL_QUAD_STRIP)
			for idx in qs1[12:18]:
				x,y,z = curvedArrowVerts[idx][0],curvedArrowVerts[idx][1],curvedArrowVerts[idx][2]
				glFT.glVertex3f(x,y,z)
			glFT.glEnd()
			glFT.glBegin(OpenMayaRender.MGL_QUAD_STRIP)
			for idx in qs1[18:]:
				x,y,z = curvedArrowVerts[idx][0],curvedArrowVerts[idx][1],curvedArrowVerts[idx][2]
				glFT.glVertex3f(x,y,z)
			glFT.glEnd()

		def drawWireframe(self):
			glFT.glLineWidth(lw)
			glFT.glBegin(OpenMayaRender.MGL_LINE_LOOP)
			for i in xrange(len(curvedArrowVerts)):
				x,y,z = curvedArrowVerts[i][0],curvedArrowVerts[i][1],curvedArrowVerts[i][2]
				glFT.glVertex3f(x,y,z)
			glFT.glEnd()

		view.beginGL()
		glFT.glPushMatrix()
		glFT.glRotatef(rotation[0],1.0,0.0,0.0)
		glFT.glRotatef(rotation[1],0.0,1.0,0.0)
		glFT.glRotatef(rotation[2],0.0,0.0,1.0)
		glFT.glPushAttrib(OpenMayaRender.MGL_ALL_ATTRIB_BITS)
		f = drawShaded
		if style not in [OpenMayaUI.M3dView.kFlatShaded, OpenMayaUI.M3dView.kGouraudShaded]:
			f = drawWireframe
		if dt == 1:   f = drawShaded
		elif dt == 0: f = drawWireframe
		glFT.glEnable( OpenMayaRender.MGL_BLEND )
		glFT.glBlendFunc( OpenMayaRender.MGL_SRC_ALPHA, OpenMayaRender.MGL_ONE_MINUS_SRC_ALPHA )
		glFT.glDepthFunc(OpenMayaRender.MGL_LESS)
		glFT.glColor4f( r, g, b, a )
		f(self)
		glFT.glDepthFunc(OpenMayaRender.MGL_GREATER)
		glFT.glColor4f( r, g, b, ba )
		f(self)
		glFT.glPopAttrib()
		glFT.glPopMatrix()
		view.endGL()
		
	def isBounded(self):
		return True

	def drawLast(self):
		return True

	def boundingBox(self):
		corner1 = OpenMaya.MPoint(-1,0.6,1)
		corner2 = OpenMaya.MPoint(1,0,-1)
		bbox = OpenMaya.MBoundingBox( corner1, corner2 )
		return bbox

def curvedArrowNodeCreator():
	return OpenMayaMPx.asMPxPtr( mpCurvedArrow() )

def curvedArrowNodeInitializer():
	mpLocAddStandardAttributes(mpCurvedArrow)
	
	enumAttr = OpenMaya.MFnEnumAttribute()
	mpCurvedArrow.aDrawType = enumAttr.create("drawType", "dt")
	enumAttr.addField("wireframe", 0)
	enumAttr.addField("shaded", 1)
	enumAttr.addField("normal", 2)
	enumAttr.setHidden(False)
	enumAttr.setKeyable(True)
	enumAttr.setDefault(2)
	mpCurvedArrow.addAttribute(mpCurvedArrow.aDrawType)

	
##########################################################################################
##################################### arrowNode class ####################################
##########################################################################################

arrowNodeName = "mpArrow"
arrowNodeId = OpenMaya.MTypeId(0x87118)

class mpArrow(OpenMayaMPx.MPxLocatorNode):
		
	def __init__(self):
		OpenMayaMPx.MPxLocatorNode.__init__(self)
		
	def compute(self, plug, dataBlock):
		return OpenMaya.kUnknownParameter

	def draw(self, view, path, style, status):
		fnThisNode = OpenMaya.MFnDependencyNode(self.thisMObject())
		lw = OpenMaya.MPlug(self.thisMObject(), fnThisNode.attribute("lineWidth")).asInt()
		rt = OpenMaya.MPlug(self.thisMObject(), fnThisNode.attribute ("rotate"))
		a = OpenMaya.MPlug(self.thisMObject(), fnThisNode.attribute("transparency")).asFloat()
		ba = OpenMaya.MPlug(self.thisMObject(), fnThisNode.attribute("backAlpha")).asFloat()
		dt = OpenMaya.MPlug (self.thisMObject(), fnThisNode.attribute ("drawType")).asInt()
		cl = OpenMaya.MPlug(self.thisMObject(), fnThisNode.attribute ("color"))

		rotation = core.datatypes.getPlugValue(rt)
		color = core.datatypes.getPlugValue(cl)
		(r,g,b) = tuple(color)[:3]

		def drawShaded(self):
			glFT.glBegin (OpenMayaRender.MGL_TRIANGLES)
			for idx in arrowIndex:
				glFT.glVertex3f(arrowVerts[idx][0], arrowVerts[idx][1], arrowVerts[idx][2])
			glFT.glEnd()
						
		def drawWireframe(self):
			glFT.glLineWidth(lw)
			glFT.glBegin(OpenMayaRender.MGL_LINE_LOOP)
			for i in xrange(len(arrowVerts)):
				glFT.glVertex3f( arrowVerts[i][0], arrowVerts[i][1], arrowVerts[i][2] )
			glFT.glEnd()

		view.beginGL()
		glFT.glPushMatrix()
		glFT.glRotatef(rotation[0],1.0,0.0,0.0)
		glFT.glRotatef(rotation[1],0.0,1.0,0.0)
		glFT.glRotatef(rotation[2],0.0,0.0,1.0)
		glFT.glPushAttrib(OpenMayaRender.MGL_ALL_ATTRIB_BITS)
		f = drawShaded
		if style not in [OpenMayaUI.M3dView.kFlatShaded, OpenMayaUI.M3dView.kGouraudShaded]:
			f = drawWireframe
		if dt == 1:   f = drawShaded
		elif dt == 0: f = drawWireframe
		glFT.glEnable( OpenMayaRender.MGL_BLEND )
		glFT.glBlendFunc( OpenMayaRender.MGL_SRC_ALPHA, OpenMayaRender.MGL_ONE_MINUS_SRC_ALPHA )
		glFT.glDepthFunc(OpenMayaRender.MGL_LESS)
		glFT.glColor4f( r, g, b, a )
		f(self)
		glFT.glDepthFunc(OpenMayaRender.MGL_GREATER)
		glFT.glColor4f( r, g, b, ba )
		f(self)
		glFT.glPopAttrib()
		glFT.glPopMatrix()
		view.endGL()

	def isBounded(self):
		return True

	def drawLast(self):
		return True

	def boundingBox(self):
		corner1 = OpenMaya.MPoint(-0.273,0.005,0.395)
		corner2 = OpenMaya.MPoint(0.273,-0.005,-0.673)
		bbox = OpenMaya.MBoundingBox( corner1, corner2 )
		return bbox

def arrowNodeCreator():
	return OpenMayaMPx.asMPxPtr( mpArrow() )

def arrowNodeInitializer():
	mpLocAddStandardAttributes(mpArrow)
	
	enumAttr = OpenMaya.MFnEnumAttribute()
	mpCurvedArrow.aDrawType = enumAttr.create("drawType", "dt")
	enumAttr.addField("wireframe", 0)
	enumAttr.addField("shaded", 1)
	enumAttr.addField("normal", 2)
	enumAttr.setHidden(False)
	enumAttr.setKeyable(True)
	enumAttr.setDefault(2)
	mpCurvedArrow.addAttribute(mpCurvedArrow.aDrawType)

##########################################################################################
##################################### boxNode class ######################################
##########################################################################################

boxNodeName = "mpBox"
boxNodeId = OpenMaya.MTypeId(0x87119)

class mpBox(OpenMayaMPx.MPxLocatorNode):
		
	def __init__(self):
		OpenMayaMPx.MPxLocatorNode.__init__(self)
		
	def compute(self, plug, dataBlock):
		return OpenMaya.kUnknownParameter

	def draw(self, view, path, style, status):
		fnThisNode = OpenMaya.MFnDependencyNode(self.thisMObject())
		lw = OpenMaya.MPlug(self.thisMObject(), fnThisNode.attribute("lineWidth")).asInt()
		rt = OpenMaya.MPlug(self.thisMObject(), fnThisNode.attribute ("rotate"))
		a = OpenMaya.MPlug(self.thisMObject(), fnThisNode.attribute("transparency")).asFloat()
		ba = OpenMaya.MPlug(self.thisMObject(), fnThisNode.attribute("backAlpha")).asFloat()
		xsize = OpenMaya.MPlug(self.thisMObject(), fnThisNode.attribute("xsize")).asFloat()
		ysize = OpenMaya.MPlug(self.thisMObject(), fnThisNode.attribute("ysize")).asFloat()
		zsize = OpenMaya.MPlug(self.thisMObject(), fnThisNode.attribute("zsize")).asFloat()
		dt = OpenMaya.MPlug (self.thisMObject(), fnThisNode.attribute ("drawType")).asInt()
		cl = OpenMaya.MPlug(self.thisMObject(), fnThisNode.attribute ("color"))
		rotation = core.datatypes.getPlugValue(rt)
		color = core.datatypes.getPlugValue(cl)
		(r,g,b) = tuple(color)[:3]

		def drawCube(self):
			glFT.glBegin (OpenMayaRender.MGL_QUADS)
			glFT.glNormal3f (0.0, 0.0, zsize)
			glFT.glVertex3f (-xsize, -ysize, zsize)
			glFT.glVertex3f (xsize, -ysize, zsize)
			glFT.glVertex3f (xsize, ysize, zsize)
			glFT.glVertex3f (-xsize, ysize, zsize)

			glFT.glNormal3f (0.0, 0.0,-zsize)
			glFT.glVertex3f (-xsize, -ysize, -zsize)
			glFT.glVertex3f (-xsize, ysize, -zsize)
			glFT.glVertex3f (xsize, ysize, -zsize)
			glFT.glVertex3f (xsize, -ysize, -zsize)

			glFT.glNormal3f (0.0, ysize, 0.0)
			glFT.glVertex3f (-xsize, ysize, -zsize)
			glFT.glVertex3f (-xsize, ysize, zsize)
			glFT.glVertex3f (xsize, ysize, zsize)
			glFT.glVertex3f (xsize, ysize, -zsize)

			glFT.glNormal3f (0.0, -ysize, 0.0)
			glFT.glVertex3f (-xsize, -ysize, -zsize)
			glFT.glVertex3f (xsize, -ysize, -zsize)
			glFT.glVertex3f (xsize, -ysize, zsize)
			glFT.glVertex3f (-xsize, -ysize, zsize)

			glFT.glNormal3f (xsize, 0.0, 0.0)
			glFT.glVertex3f (xsize, -ysize, -zsize)
			glFT.glVertex3f (xsize, ysize, -zsize)
			glFT.glVertex3f (xsize, ysize, zsize)
			glFT.glVertex3f (xsize, -ysize, zsize)

			glFT.glNormal3f (-xsize, 0.0, 0.0)
			glFT.glVertex3f (-xsize, -ysize, -zsize)
			glFT.glVertex3f (-xsize, -ysize, zsize)
			glFT.glVertex3f (-xsize, ysize, zsize)
			glFT.glVertex3f (-xsize, ysize, -zsize)
			glFT.glEnd()

		def drawShaded(self):
			glFT.glEnable (OpenMayaRender.MGL_CULL_FACE)
			glFT.glPolygonMode(OpenMayaRender.MGL_FRONT, OpenMayaRender.MGL_FILL)

		def drawWireframe(self):
			glFT.glPolygonMode(OpenMayaRender.MGL_FRONT_AND_BACK, OpenMayaRender.MGL_LINE)
			glFT.glLineWidth(lw)

		view.beginGL()
		glFT.glPushMatrix()
		glFT.glRotatef(rotation[0],1.0,0.0,0.0)
		glFT.glRotatef(rotation[1],0.0,1.0,0.0)
		glFT.glRotatef(rotation[2],0.0,0.0,1.0)
		glFT.glPushAttrib(OpenMayaRender.MGL_ALL_ATTRIB_BITS)
		f = drawShaded
		if style not in [OpenMayaUI.M3dView.kFlatShaded, OpenMayaUI.M3dView.kGouraudShaded]:
			f = drawWireframe
		if dt == 1:   f = drawShaded
		elif dt == 0: f = drawWireframe
		glFT.glEnable( OpenMayaRender.MGL_BLEND )
		glFT.glBlendFunc( OpenMayaRender.MGL_SRC_ALPHA, OpenMayaRender.MGL_ONE_MINUS_SRC_ALPHA )
		glFT.glDepthFunc(OpenMayaRender.MGL_LESS)
		glFT.glColor4f( r, g, b, a )
		f(self)
		drawCube(self)
		glFT.glDepthFunc(OpenMayaRender.MGL_GREATER)
		glFT.glColor4f( r, g, b, ba )
		f(self)
		drawCube(self)
		glFT.glPopAttrib()
		glFT.glPopMatrix()
		view.endGL()

	def isBounded(self):
		return True

	def drawLast(self):
		return True

	def boundingBox(self):
		fnThisNode = OpenMaya.MFnDependencyNode(self.thisMObject())
		xsize = OpenMaya.MPlug(self.thisMObject(), fnThisNode.attribute("xsize")).asFloat()
		ysize = OpenMaya.MPlug(self.thisMObject(), fnThisNode.attribute("ysize")).asFloat()
		zsize = OpenMaya.MPlug(self.thisMObject(), fnThisNode.attribute("zsize")).asFloat()
		corner1 = OpenMaya.MPoint(xsize,ysize,zsize)
		corner2 = OpenMaya.MPoint(-xsize,-ysize,-zsize)
		bbox = OpenMaya.MBoundingBox( corner1, corner2 )
		return bbox

def boxNodeCreator():
	return OpenMayaMPx.asMPxPtr( mpBox())

def boxNodeInitializer():
	mpLocAddStandardAttributes(mpBox)
	
	enumAttr = OpenMaya.MFnEnumAttribute()
	nAttr = OpenMaya.MFnNumericAttribute()
	mpBox.aDrawType = enumAttr.create("drawType", "dt")
	enumAttr.addField("wireframe", 0)
	enumAttr.addField("shaded", 1)
	enumAttr.addField("normal", 2)
	enumAttr.setHidden(False)
	enumAttr.setKeyable(True)
	enumAttr.setDefault(2)

	mpBox.aXsize = nAttr.create( "xsize", "xsz", OpenMaya.MFnNumericData.kFloat)
	nAttr.setDefault(0.5)
	nAttr.setKeyable(1)
	nAttr.setReadable(1)
	nAttr.setWritable(1)
	nAttr.setStorable(1)

	mpBox.aYsize = nAttr.create( "ysize", "ysz", OpenMaya.MFnNumericData.kFloat)
	nAttr.setDefault(0.5)
	nAttr.setKeyable(1)
	nAttr.setReadable(1)
	nAttr.setWritable(1)
	nAttr.setStorable(1)

	mpBox.aZsize = nAttr.create( "zsize", "zsz", OpenMaya.MFnNumericData.kFloat)
	nAttr.setDefault(0.5)
	nAttr.setKeyable(1)
	nAttr.setReadable(1)
	nAttr.setWritable(1)
	nAttr.setStorable(1)


	mpBox.addAttribute(mpBox.aXsize)
	mpBox.addAttribute(mpBox.aYsize)
	mpBox.addAttribute(mpBox.aZsize)
	mpBox.addAttribute(mpBox.aDrawType)


##########################################################################################
##################################### doubleArrow class ######################################
##########################################################################################

doubleArrowNodeName = "mpDoubleArrow"
doubleArrowNodeId = OpenMaya.MTypeId(0x87120)

class mpDoubleArrow(OpenMayaMPx.MPxLocatorNode):
		
	def __init__(self):
		OpenMayaMPx.MPxLocatorNode.__init__(self)
		
	def compute(self, plug, dataBlock):
		return OpenMaya.kUnknownParameter

	def draw(self, view, path, style, status):
		fnThisNode = OpenMaya.MFnDependencyNode(self.thisMObject())
		lw = OpenMaya.MPlug(self.thisMObject(), fnThisNode.attribute("lineWidth")).asInt()
		rt = OpenMaya.MPlug(self.thisMObject(), fnThisNode.attribute ("rotate"))
		a = OpenMaya.MPlug(self.thisMObject(), fnThisNode.attribute("transparency")).asFloat()
		ba = OpenMaya.MPlug(self.thisMObject(), fnThisNode.attribute("backAlpha")).asFloat()
		dt = OpenMaya.MPlug (self.thisMObject(), fnThisNode.attribute ("drawType")).asInt()
		cl = OpenMaya.MPlug(self.thisMObject(), fnThisNode.attribute ("color"))

		rotation = core.datatypes.getPlugValue(rt)
		color = core.datatypes.getPlugValue(cl)
		(r,g,b) = tuple(color)[:3]
		
		def drawShaded(self):
			glFT.glBegin(OpenMayaRender.MGL_TRIANGLES)
			for i in doubleArrowIds:
				glFT.glVertex3f(doubleArrowVerts[i][0],doubleArrowVerts[i][1],doubleArrowVerts[i][2])
			glFT.glEnd()
		
		def drawWireframe(self):
			glFT.glLineWidth(lw)
			glFT.glBegin(OpenMayaRender.MGL_LINE_LOOP)
			for i in doubleArrowVerts:
				glFT.glVertex3f(i[0], i[1], i[2])
			glFT.glEnd()

		view.beginGL()
		glFT.glPushMatrix()
		glFT.glRotatef(rotation[0],1.0,0.0,0.0)
		glFT.glRotatef(rotation[1],0.0,1.0,0.0)
		glFT.glRotatef(rotation[2],0.0,0.0,1.0)
		glFT.glPushAttrib(OpenMayaRender.MGL_ALL_ATTRIB_BITS)
		f = drawShaded
		if style not in [OpenMayaUI.M3dView.kFlatShaded, OpenMayaUI.M3dView.kGouraudShaded]:
			f = drawWireframe
		if dt == 1:   f = drawShaded
		elif dt == 0: f = drawWireframe
		glFT.glEnable( OpenMayaRender.MGL_BLEND )
		glFT.glBlendFunc( OpenMayaRender.MGL_SRC_ALPHA, OpenMayaRender.MGL_ONE_MINUS_SRC_ALPHA )
		glFT.glDepthFunc(OpenMayaRender.MGL_LESS)
		glFT.glColor4f( r, g, b, a )
		f(self)
		glFT.glDepthFunc(OpenMayaRender.MGL_GREATER)
		glFT.glColor4f( r, g, b, ba )
		f(self)
		glFT.glPopAttrib()
		glFT.glPopMatrix()
		view.endGL()

	def isBounded(self):
		return True

	def drawLast(self):
		return True

	def boundingBox(self):
		corner1 = OpenMaya.MPoint(doubleArrowVerts[1][0],doubleArrowVerts[1][1],doubleArrowVerts[1][2])
		corner2 = OpenMaya.MPoint(doubleArrowVerts[6][0],doubleArrowVerts[6][1],doubleArrowVerts[6][2])
		bbox = OpenMaya.MBoundingBox( corner1, corner2 )
		bbox.expand(OpenMaya.MPoint(doubleArrowVerts[0][0],doubleArrowVerts[0][1],doubleArrowVerts[0][2]))
		bbox.expand(OpenMaya.MPoint(doubleArrowVerts[5][0],doubleArrowVerts[5][1],doubleArrowVerts[5][2]))
		return bbox

def doubleArrowNodeCreator():
	return OpenMayaMPx.asMPxPtr( mpDoubleArrow() )

def doubleArrowNodeInitializer():
	mpLocAddStandardAttributes(mpDoubleArrow)
	
	enumAttr = OpenMaya.MFnEnumAttribute()
	mpDoubleArrow.aDrawType = enumAttr.create("drawType", "dt")
	enumAttr.addField("wireframe", 0)
	enumAttr.addField("shaded", 1)
	enumAttr.addField("normal", 2)
	enumAttr.setHidden(False)
	enumAttr.setKeyable(True)
	enumAttr.setDefault(2)
	mpDoubleArrow.addAttribute(mpDoubleArrow.aDrawType)
	

##########################################################################################
##################################### spiral class ######################################
##########################################################################################

spiralNodeName = "mpSpiral"
spiralNodeId = OpenMaya.MTypeId(0x87121)

class mpSpiral(OpenMayaMPx.MPxLocatorNode):
		
	def __init__(self):
		OpenMayaMPx.MPxLocatorNode.__init__(self)
		
	def compute(self, plug, dataBlock):
		return OpenMaya.kUnknownParameter

	def draw(self, view, path, style, status):
		fnThisNode = OpenMaya.MFnDependencyNode(self.thisMObject())
		lw = OpenMaya.MPlug(self.thisMObject(), fnThisNode.attribute("lineWidth")).asInt()
		rt = OpenMaya.MPlug(self.thisMObject(), fnThisNode.attribute ("rotate"))
		a = OpenMaya.MPlug(self.thisMObject(), fnThisNode.attribute("transparency")).asFloat()
		ba = OpenMaya.MPlug(self.thisMObject(), fnThisNode.attribute("backAlpha")).asFloat()
		cl = OpenMaya.MPlug(self.thisMObject(), fnThisNode.attribute ("color"))
		sa = OpenMaya.MPlug (self.thisMObject(),fnThisNode.attribute("startAngle")).asFloat()
		ea = OpenMaya.MPlug (self.thisMObject(),fnThisNode.attribute("endAngle")).asFloat()
# 		spr = OpenMaya.MPlug (self.thisMObject(),fnThisNode.attribute("spread")).asFloat()
		sa,ea = math.radians(sa), math.radians(ea)
		h = OpenMaya.MPlug (self.thisMObject(),fnThisNode.attribute("height")).asFloat()
		divs = OpenMaya.MPlug (self.thisMObject(),fnThisNode.attribute("divisions")).asInt()
		rotation = core.datatypes.getPlugValue(rt)
		color = core.datatypes.getPlugValue(cl)
		(r,g,b) = tuple(color)[:3]

		def drawSpiral(self):
			glFT.glLineWidth(lw)
			glFT.glBegin(OpenMayaRender.MGL_LINE_STRIP)
			for i in xrange(divs+1):
				phi = sa + (ea-sa) * i / divs
				r = phi/(2*math.pi)
				x = r*math.sin(phi) 
				z = r*math.cos(phi)
				y = h * i / divs
				glFT.glVertex3f(x, y, z)
			glFT.glEnd()

		view.beginGL()
		glFT.glPushMatrix()
		glFT.glRotatef(rotation[0],1.0,0.0,0.0)
		glFT.glRotatef(rotation[1],0.0,1.0,0.0)
		glFT.glRotatef(rotation[2],0.0,0.0,1.0)
		glFT.glPushAttrib(OpenMayaRender.MGL_ALL_ATTRIB_BITS)
		glFT.glEnable( OpenMayaRender.MGL_BLEND )
		glFT.glBlendFunc( OpenMayaRender.MGL_SRC_ALPHA, OpenMayaRender.MGL_ONE_MINUS_SRC_ALPHA )
		glFT.glDepthFunc(OpenMayaRender.MGL_LESS)
		glFT.glColor4f( r, g, b, a )
		drawSpiral(self)
		glFT.glDepthFunc(OpenMayaRender.MGL_GREATER)
		glFT.glColor4f( r, g, b, ba )
		drawSpiral(self)
		glFT.glPopAttrib()
		glFT.glPopMatrix()
		view.endGL()

	def isBounded(self):
		return True

	def drawLast(self):
		return True

	def boundingBox(self):
		fnThisNode = OpenMaya.MFnDependencyNode(self.thisMObject())
		sa = OpenMaya.MPlug (self.thisMObject(),fnThisNode.attribute("startAngle")).asFloat()
		ea = OpenMaya.MPlug (self.thisMObject(),fnThisNode.attribute("endAngle")).asFloat()
		divs = OpenMaya.MPlug (self.thisMObject(),fnThisNode.attribute("divisions")).asInt()
		h = OpenMaya.MPlug (self.thisMObject(),fnThisNode.attribute("height")).asFloat()
		sa,ea = math.radians(sa), math.radians(ea)
		phi = sa + (ea-sa)
		r = phi/(2*math.pi)
		x = r*math.sin(phi)
		z = r*math.cos(phi)
		y = h 
		corner1 = OpenMaya.MPoint(x,y,z)
		corner2 = OpenMaya.MPoint(-x,0,-z)
		corner3 = OpenMaya.MPoint(z,y,x)
		corner4 = OpenMaya.MPoint(-z,0,-x)
		bbox = OpenMaya.MBoundingBox( corner1, corner2 )
		bbox.expand(corner3)
		bbox.expand(corner4)
		return bbox

def spiralNodeCreator():
	return OpenMayaMPx.asMPxPtr( mpSpiral() )

def spiralNodeInitializer():
	mpLocAddStandardAttributes(mpSpiral)

	nAttr = OpenMaya.MFnNumericAttribute()
	mpSpiral.aStartAngle = nAttr.create( "startAngle", "sa", OpenMaya.MFnNumericData.kFloat)
	nAttr.setDefault(360.0)
	nAttr.setKeyable(1)
	nAttr.setReadable(1)
	nAttr.setWritable(1)
	nAttr.setStorable(1)

	mpSpiral.aEndAngle = nAttr.create( "endAngle", "ea", OpenMaya.MFnNumericData.kFloat)
	nAttr.setDefault(1440.0)
	nAttr.setKeyable(1)
	nAttr.setReadable(1)
	nAttr.setWritable(1)
	nAttr.setStorable(1)

	mpSpiral.aHeight = nAttr.create( "height", "h", OpenMaya.MFnNumericData.kFloat)
	nAttr.setDefault(0.0)
	nAttr.setKeyable(1)
	nAttr.setReadable(1)
	nAttr.setWritable(1)
	nAttr.setStorable(1)


# 	mpSpiral.aSpread = nAttr.create( "spread", "spr", OpenMaya.MFnNumericData.kFloat)
# 	nAttr.setDefault(1.0)
# 	nAttr.setKeyable(1)
# 	nAttr.setReadable(1)
# 	nAttr.setWritable(1)
# 	nAttr.setStorable(1)

	mpSpiral.aDivisions = nAttr.create( "divisions", "div", OpenMaya.MFnNumericData.kInt)
	nAttr.setDefault(22)
	nAttr.setKeyable(1)
	nAttr.setReadable(1)
	nAttr.setWritable(1)
	nAttr.setStorable(1)
	nAttr.setMin(1)

	mpSpiral.addAttribute(mpSpiral.aStartAngle)
	mpSpiral.addAttribute(mpSpiral.aEndAngle)
	mpSpiral.addAttribute(mpSpiral.aHeight)
# 	mpSpiral.addAttribute(mpSpiral.aSpread)
	mpSpiral.addAttribute(mpSpiral.aDivisions)



##########################################################################################
##################################### sphere class #######################################
##########################################################################################

sphereNodeName = "mpSphere"
sphereNodeId = OpenMaya.MTypeId(0x87122)

class mpSphere(OpenMayaMPx.MPxLocatorNode):
		
	def __init__(self):
		OpenMayaMPx.MPxLocatorNode.__init__(self)
		
	def compute(self, plug, dataBlock):
		return OpenMaya.kUnknownParameter

	def draw(self, view, path, style, status):
		fnThisNode = OpenMaya.MFnDependencyNode(self.thisMObject())
		lw = OpenMaya.MPlug(self.thisMObject(), fnThisNode.attribute("lineWidth")).asInt()
		rt = OpenMaya.MPlug(self.thisMObject(), fnThisNode.attribute ("rotate"))
		a = OpenMaya.MPlug(self.thisMObject(), fnThisNode.attribute("transparency")).asFloat()
		ba = OpenMaya.MPlug(self.thisMObject(), fnThisNode.attribute("backAlpha")).asFloat()
		cl = OpenMaya.MPlug(self.thisMObject(), fnThisNode.attribute ("color"))
		dt = OpenMaya.MPlug (self.thisMObject(), fnThisNode.attribute ("drawType")).asInt()
		lat = OpenMaya.MPlug (self.thisMObject(),fnThisNode.attribute("latitude")).asInt()
		long = OpenMaya.MPlug (self.thisMObject(),fnThisNode.attribute("longitude")).asInt()
		rad = OpenMaya.MPlug (self.thisMObject(),fnThisNode.attribute("radius")).asFloat()

		rotation = core.datatypes.getPlugValue(rt)
		color = core.datatypes.getPlugValue(cl)
		(r,g,b) = tuple(color)[:3]

		def drawSphere(self):
			PI = math.pi
			for i in xrange(lat):
				lat0 = PI * (-0.5 + float(i) / lat)
				z0  = math.sin(lat0)
				zr0 = math.cos(lat0)
				lat1 = PI * (-0.5 + float(i+1) / lat)
				z1 = math.sin(lat1)
				zr1 = math.cos(lat1)
				glFT.glBegin(OpenMayaRender.MGL_QUAD_STRIP)
				for j in xrange(long+1):
					lng = 2 * PI * float(j) / long
					x = math.cos(lng)
					y = math.sin(lng)
					glFT.glVertex3f(x * zr0 * rad, y * zr0 * rad, z0 * rad)
					glFT.glVertex3f(x * zr1 * rad, y * zr1 * rad, z1 * rad)
				glFT.glEnd()

		def drawShaded(self):
			glFT.glEnable (OpenMayaRender.MGL_CULL_FACE)
			drawSphere(self)
			glFT.glDisable (OpenMayaRender.MGL_CULL_FACE)
			glFT.glPolygonMode(OpenMayaRender.MGL_FRONT_AND_BACK, OpenMayaRender.MGL_LINE)
			drawSphere(self)
			glFT.glCullFace(OpenMayaRender.MGL_BACK)
			
		def drawWireframe(self):
			glFT.glPolygonMode(OpenMayaRender.MGL_FRONT_AND_BACK, OpenMayaRender.MGL_LINE)
			drawSphere(self)
				
		view.beginGL()
		glFT.glPushMatrix()
		glFT.glRotatef(rotation[0],1.0,0.0,0.0)
		glFT.glRotatef(rotation[1],0.0,1.0,0.0)
		glFT.glRotatef(rotation[2],0.0,0.0,1.0)
		glFT.glPushAttrib(OpenMayaRender.MGL_ALL_ATTRIB_BITS)
		f = drawShaded
		if style not in [OpenMayaUI.M3dView.kFlatShaded, OpenMayaUI.M3dView.kGouraudShaded]:
			f = drawWireframe
		if dt == 1:   f = drawShaded
		elif dt == 0: f = drawWireframe
		glFT.glEnable( OpenMayaRender.MGL_BLEND )
		glFT.glBlendFunc( OpenMayaRender.MGL_SRC_ALPHA, OpenMayaRender.MGL_ONE_MINUS_SRC_ALPHA )
		glFT.glDepthFunc(OpenMayaRender.MGL_LESS)
		glFT.glColor4f( r, g, b, a )
		glFT.glLineWidth(lw)
		f(self)
		glFT.glDepthFunc(OpenMayaRender.MGL_GREATER)
		glFT.glColor4f( r, g, b, ba )
		f(self)
		glFT.glPopAttrib()
		glFT.glPopMatrix()
		view.endGL()

	def isBounded(self):
		return True

	def drawLast(self):
		return True

	def boundingBox(self):
		fnThisNode = OpenMaya.MFnDependencyNode(self.thisMObject())
		rad = OpenMaya.MPlug (self.thisMObject(),fnThisNode.attribute("radius")).asFloat()
		corner1 = OpenMaya.MPoint(rad,rad,rad)
		corner2 = OpenMaya.MPoint(-rad,-rad,-rad)
		bbox = OpenMaya.MBoundingBox( corner1, corner2 )
		return bbox

def sphereNodeCreator():
	return OpenMayaMPx.asMPxPtr( mpSphere() )

def sphereNodeInitializer():
	mpLocAddStandardAttributes(mpSphere)

	nAttr = OpenMaya.MFnNumericAttribute()
	mpSphere.aLat = nAttr.create( "latitude", "lat", OpenMaya.MFnNumericData.kInt)
	nAttr.setDefault(6)
	nAttr.setMin(2)
	nAttr.setKeyable(1)
	nAttr.setReadable(1)
	nAttr.setWritable(1)
	nAttr.setStorable(1)

	mpSphere.aLong = nAttr.create( "longitude", "long", OpenMaya.MFnNumericData.kInt)
	nAttr.setDefault(12)
	nAttr.setMin(2)
	nAttr.setKeyable(1)
	nAttr.setReadable(1)
	nAttr.setWritable(1)
	nAttr.setStorable(1)

	mpSphere.aRad = nAttr.create( "radius", "rad", OpenMaya.MFnNumericData.kFloat)
	nAttr.setDefault(0.5)
	nAttr.setKeyable(1)
	nAttr.setReadable(1)
	nAttr.setWritable(1)
	nAttr.setStorable(1)

	enumAttr = OpenMaya.MFnEnumAttribute()
	mpSphere.aDrawType = enumAttr.create("drawType", "dt")
	enumAttr.addField("wireframe", 0)
	enumAttr.addField("shaded", 1)
	enumAttr.addField("normal", 2)
	enumAttr.setHidden(False)
	enumAttr.setKeyable(True)
	enumAttr.setDefault(2)
	
	mpSphere.addAttribute(mpSphere.aLat)
	mpSphere.addAttribute(mpSphere.aLong)
	mpSphere.addAttribute(mpSphere.aRad)
	mpSphere.addAttribute(mpSphere.aDrawType)
	
# initialize the  plug-in and locators nodes
def initializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject,"Marin Petrov", "0.9", "Any")
	try:
		mplugin.registerNode( arrowNodeName, arrowNodeId, arrowNodeCreator, arrowNodeInitializer, OpenMayaMPx.MPxNode.kLocatorNode )
	except:
		sys.stderr.write( "Failed to register node: %s" % arrowNodeName )
		raise
	try:
		mplugin.registerNode( curvedArrowNodeName, curvedArrowNodeId, curvedArrowNodeCreator, curvedArrowNodeInitializer, OpenMayaMPx.MPxNode.kLocatorNode )
	except:
		sys.stderr.write( "Failed to register node: %s" % curvedArrowNodeName )
		raise
	try:
		mplugin.registerNode( boxNodeName, boxNodeId, boxNodeCreator, boxNodeInitializer, OpenMayaMPx.MPxNode.kLocatorNode )
	except:
		sys.stderr.write( "Failed to register node: %s" % boxNodeName )
		raise
	try:
		mplugin.registerNode( doubleArrowNodeName, doubleArrowNodeId, doubleArrowNodeCreator, doubleArrowNodeInitializer, OpenMayaMPx.MPxNode.kLocatorNode )
	except:
		sys.stderr.write( "Failed to register node: %s" % doubleArrowNodeName )
		raise
	try:
		mplugin.registerNode( spiralNodeName, spiralNodeId, spiralNodeCreator, spiralNodeInitializer, OpenMayaMPx.MPxNode.kLocatorNode )
	except:
		sys.stderr.write( "Failed to register node: %s" % spiralNodeName )
		raise
	try:
		mplugin.registerNode( sphereNodeName, sphereNodeId, sphereNodeCreator, sphereNodeInitializer, OpenMayaMPx.MPxNode.kLocatorNode )
	except:
		sys.stderr.write( "Failed to register node: %s" % sphereNodeName )
		raise

# uninitialize the  plug-in and locators nodes
def uninitializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject)
	try:
		mplugin.deregisterNode( arrowNodeId )
	except:
		sys.stderr.write( "Failed to deregister node: %s" % arrowNodeName )
		raise
	try:
		mplugin.deregisterNode( curvedArrowNodeId )
	except:
		sys.stderr.write( "Failed to deregister node: %s" % curvedArrowNodeName )
		raise
	try:
		mplugin.deregisterNode( boxNodeId )
	except:
		sys.stderr.write( "Failed to deregister node: %s" % boxNodeName )
		raise
	try:
		mplugin.deregisterNode( doubleArrowNodeId )
	except:
		sys.stderr.write( "Failed to deregister node: %s" % doubleArrowNodeName )
		raise
	try:
		mplugin.deregisterNode( spiralNodeId )
	except:
		sys.stderr.write( "Failed to deregister node: %s" % spiralNodeName )
		raise
	try:
		mplugin.deregisterNode( sphereNodeId )
	except:
		sys.stderr.write( "Failed to deregister node: %s" % sphereNodeName )
		raise


	
