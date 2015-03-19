import bpy
import bmesh
from math import cos, sin, pi

bl_info = {
    "name": "UV Grid",
    "author": "OAlpha",
    "version": (1,0,0),
    "blender": (2, 73, 0),
    "location": "View3D > Add > Mesh",
    "description": "Add a portion of a uv sphere",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "",
    "category": "Add Mesh",
}

def add_uvgrid(theta, psi, longitude, latitude, segments, rings, radius):
    """
    This function takes inputs and returns vertex and face arrays.
    no actual mesh data creation is done here.
    """

    tolerance = .00001

    verts = []

    faces = []
    
    ns = segments + 1
    nr = rings + 1
    f = 0
    bp = 0
    tp = 0
    sc = 0
    if psi < -pi/2 + tolerance :
        psi = -pi/2
        verts.append( (0,0,-radius) )
        nr = nr - 1
        b = f
        f = f + 1
        bp = 1
    if psi + latitude > pi/2 - tolerance :
        latitude = pi/2 - psi
        verts.append( (0,0,radius) )
        nr = nr - 1
        t = f
        f = f + 1
        tp = 1
    if longitude > 2*pi - tolerance :
        longitude = 2*pi
        ns = ns - 1
        sc = 1
    for u in range(ns) :
        for v in range(nr) :
            verts.append( (radius*cos(theta+longitude*u/segments)*cos(psi+latitude*v/rings),radius*sin(theta+longitude*u/segments)*cos(psi+latitude*v/rings),radius*sin(psi+latitude*v/rings)) )
            if u > 0 :
                if bp == 1 and v == 0 :
                    faces.append( (b,f+(u-1)*nr,f+u*nr) )
                if v > 0 :
                    faces.append( (f+(u-1)*nr+v-1,f+(u-1)*nr+v,f+u*nr+v,f+u*nr+v-1) )
                if tp == 1 and v == nr - 1 :
                    faces.append( (f+(u-1)*nr+v,t,f+u*nr+v) )
            if sc == 1 and u == ns - 1 :
                if bp == 1 and v == 0 :
                    faces.append( (b,f+u*nr,f) )
                if v > 0 :
                    faces.append( (f+u*nr+v-1,f+u*nr+v,f+v,f+v-1) )
                if tp == 1 and v == nr - 1 :
                    faces.append( (f+u*nr+v,t,f+v) )

    return verts, faces


from bpy.props import FloatProperty, IntProperty, BoolProperty, FloatVectorProperty


class AddUVGrid(bpy.types.Operator):
    """Add a uv grid"""
    bl_idname = "mesh.primitive_uvgrid_add"
    bl_label = "Add UV Grid"
    bl_options = {'REGISTER', 'UNDO'}

    theta = FloatProperty(
            name="Theta",
            description="Grid Horizontal Start Angle",
            min=-360, max=360,
            default=0.0,
            )
    psi = FloatProperty(
            name="Psi",
            description="Grid Vertical Start Angle",
            min=-90, max=90,
            default=0.0,
            )
    longitude = FloatProperty(
            name="Longitude",
            description="Grid Horizontal Angle Size",
            min=0.01, max=360,
            default=45.0,
            )
    latitude = FloatProperty(
            name="Latitude",
            description="Grid Vertical Angle Size",
            min=0.01, max=180,
            default=45.0,
            )
    radius = FloatProperty(
            name="Radius",
            description="Grid Radius",
            min=0.01, max=1000.0,
            default=1.0,
            )
    #'''
    segments = IntProperty(
            name="Segments",
            description="Grid Number of Horizontal Segments",
            min=1, max=1024,
            default=4,
            )
    rings = IntProperty(
            name="Rings",
            description="Grid Number of Vertical Segments",
            min=1, max=1024,
            default=4,
            )
    #'''

    # generic transform props
    view_align = BoolProperty(
            name="Align to View",
            default=False,
            )
    location = FloatVectorProperty(
            name="Location",
            subtype='TRANSLATION',
            )
    rotation = FloatVectorProperty(
            name="Rotation",
            subtype='EULER',
            )

    def execute(self, context):

        verts_loc, faces = add_uvgrid(self.theta*pi/180, self.psi*pi/180, self.longitude*pi/180, self.latitude*pi/180, self.segments, self.rings, self.radius)

        mesh = bpy.data.meshes.new("UVGrid")

        bm = bmesh.new()

        for v_co in verts_loc:
            bm.verts.ensure_lookup_table()
            bm.verts.new(v_co)
        bm.verts.ensure_lookup_table()

        for f_idx in faces:
            bm.faces.new([bm.verts[i] for i in f_idx])

        bm.to_mesh(mesh)
        mesh.update()

        # add the mesh as an object into the scene with this utility module
        from bpy_extras import object_utils
        object_utils.object_data_add(context, mesh, operator=self)

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(AddUVGrid.bl_idname, icon='MESH_GRID')


def register():
    bpy.utils.register_class(AddUVGrid)
    bpy.types.INFO_MT_mesh_add.append(menu_func)


def unregister():
    bpy.utils.unregister_class(AddUVGrid)
    bpy.types.INFO_MT_mesh_add.remove(menu_func)

if __name__ == "__main__":
    register()

    # test call
    #bpy.ops.mesh.primitive_box_add()
