import bpy
import bmesh
from math import cos, sin, pi

bl_info = {
    "name": "Arc",
    "author": "OAlpha",
    "version": (1,0,0),
    "blender": (2, 73, 0),
    "location": "View3D > Add > Mesh",
    "description": "Add aa arc",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "",
    "category": "Add Arc",
}

def add_arc(theta, psi, segments, radius):
    """
    This function takes inputs and returns vertex and face arrays.
    no actual mesh data creation is done here.
    """

    tolerance = .00001

    verts = []

    edges = []
    
    ns = segments + 1
    sc = 0
    if theta > 2*pi - tolerance :
        theta = 2*pi
        ns = ns - 1
        sc = 1
    for u in range(ns) :
        verts.append( (radius*cos(psi+theta*u/segments),radius*sin(psi+theta*u/segments),0) )
        if u > 0 :
            edges.append( (u,u-1) )
        if sc == 1 and u == ns - 1 :
            edges.append( (u,0) )

    return verts, edges


from bpy.props import FloatProperty, IntProperty, BoolProperty, FloatVectorProperty


class AddArc(bpy.types.Operator):
    """Add an arc"""
    bl_idname = "mesh.primitive_arc_add"
    bl_label = "Add Arc"
    bl_options = {'REGISTER', 'UNDO'}

    theta = FloatProperty(
            name="Theta",
            description="Arc Angle Size",
            min=0.01, max=360,
            default=0.0,
            )
    psi = FloatProperty(
            name="Psi",
            description="Arc Start Angle",
            min=-180, max=180,
            default=0.0,
            )
    radius = FloatProperty(
            name="Radius",
            description="Arc Radius",
            min=0.01, max=1000.0,
            default=1.0,
            )
    #'''
    segments = IntProperty(
            name="Segments",
            description="Arc Number of Segments",
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

        verts_loc, edges = add_arc(self.theta*pi/180, self.psi*pi/180, self.segments, self.radius)

        mesh = bpy.data.meshes.new("Arc")

        bm = bmesh.new()

        for v_co in verts_loc:
            bm.verts.ensure_lookup_table()
            bm.verts.new(v_co)
        bm.verts.ensure_lookup_table()

        for e_idx in edges:
            bm.edges.new([bm.verts[i] for i in e_idx])

        bm.to_mesh(mesh)
        mesh.update()

        # add the mesh as an object into the scene with this utility module
        from bpy_extras import object_utils
        object_utils.object_data_add(context, mesh, operator=self)

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(AddArc.bl_idname, icon='MESH_GRID')


def register():
    bpy.utils.register_class(AddArc)
    bpy.types.INFO_MT_mesh_add.append(menu_func)


def unregister():
    bpy.utils.unregister_class(AddArc)
    bpy.types.INFO_MT_mesh_add.remove(menu_func)

if __name__ == "__main__":
    register()

    # test call
    #bpy.ops.mesh.primitive_box_add()
