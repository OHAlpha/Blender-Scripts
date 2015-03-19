import bpy
import bmesh
from math import cos, sin, pi


def add_uvgrid(theta, psi, longitude, latitude, segments, rings, radius):
    """
    This function takes inputs and returns vertex and face arrays.
    no actual mesh data creation is done here.
    """

    verts = []

    faces = []

    for u in range(segments + 1) :
        for v in range(rings + 1) :
            verts.append( (radius*cos(theta+longitude*u/segments)*cos(psi+latitude*v/rings),radius*sin(theta+longitude*u/segments)*cos(psi+latitude*v/rings),radius*sin(psi+latitude*v/rings)) )
            if u * v > 0 :
                faces.append( ((u-1)*(rings+1)+v-1,(u-1)*(rings+1)+v,u*(rings+1)+v,u*(rings+1)+v-1) )

    return verts, faces


from bpy.props import FloatProperty, IntProperty, BoolProperty, FloatVectorProperty


def execute(theta, psi, longitude, latitude, segments, rings, radius, context):

    verts_loc, faces = add_uvgrid(theta*pi/180, psi*pi/180, longitude*pi/180, latitude*pi/180, segments, rings, radius)

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
    object_utils.object_data_add(context, mesh, None)

    return {'FINISHED'}

context = bpy.context
execute( 0, -45, 270, 90, 6, 2, 1, context )