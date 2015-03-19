import bpy
import bmesh
from math import cos, sin, acos, pi, sqrt
from mathutils import Vector, Quaternion, Matrix

bl_info = {
    "name": "Dipole Grid",
    "author": "OAlpha",
    "version": (1,0,0),
    "blender": (2, 73, 0),
    "location": "View3D > Add > Mesh",
    "description": "Add a portion of a uv sphere",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "",
    "category": "Add Mesh",
}

class SphereCircle :
    def __init__( self, normal, angle, zero, center, radius ) :
        self.normal = normal.normalized()
        self.angle = angle
        self.zero = zero - zero.project(self.normal)
        self.zero.normalize()
        self.center = center
        self.radius = radius
        self.perpendicular = self.normal.cross(self.zero)
    
    def convertAngle( self, angle ) :
        return self.radius * ( cos( self.angle ) * ( Quaternion( self.normal, angle ) * self.zero ) + sin( self.angle ) * self.normal ) + self.center
    
    def convertAngles( self, angles ) :
        return [ self.radius * ( cos( self.angle ) * ( Quaternion( self.normal, angle ) * self.zero ) + sin( self.angle ) * self.normal ) + self.center for angle in angles ]
    
    def getRotation( self ) :
        mat = Matrix()
        mat[0].xyz = self.zero.to_tuple()
        mat[1].xyz = self.perpendicular.to_tuple()
        mat[2].xyz = self.normal.to_tuple()
        return mat.to_euler('XYZ')

def greatCircle( a, b, sphere ) :
    va = Vector((cos(a[0])*cos(a[1]),sin(a[0])*cos(a[1]),sin(a[1])))
    vb = Vector((cos(b[0])*cos(b[1]),sin(b[0])*cos(b[1]),sin(b[1])))
    vc = (va+vb)/2
    vc.normalize()
    c = SphereCircle(va.cross(vb),0,vc,sphere.to_3d(),sphere[3])
    return c, -acos(va * vc), acos(vb * vc)

def angledCircle( a, b, sphere, angle ) :
    va = Vector((cos(a[0])*cos(a[1]),sin(a[0])*cos(a[1]),sin(a[1])))
    vb = Vector((cos(b[0])*cos(b[1]),sin(b[0])*cos(b[1]),sin(b[1])))
    vc = (va+vb)/2
    vc.normalize()
    c = SphereCircle(va.cross(vb),0,vc,sphere.to_3d(),sphere[3])
    return c, -acos(va * vc), acos(vb * vc)

c, a, b = greatCircle((pi/4,-pi/4),(-pi/4,-pi/4),Vector((-3,-3,1,1)))
op = bpy.ops.mesh.primitive_arc_add(psi=a*180/pi,theta=(b-a)*180/pi,segments=32,radius=2,location=c.center.to_tuple(),rotation=c.getRotation())
