bl_info = {
    'name': 'Tetrahelix',
    'author': 'melak47',
    'version': (1, 0),
    'blender': (2, 80, 0),
    'location': 'View3D > Add > Mesh > Tetrahelix',
    'description': 'Adds a Tetrahelix',
    'warning': '',
    'doc_url': '',
    'category': 'Add Mesh',
}

import bpy
from bpy.types import Operator
from bpy.props import FloatProperty, IntProperty, BoolProperty, EnumProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector
from math import sqrt, acos, cos, sin

def add_object(self, context):
    if self.mode_select == 'EDGE_LENGTH':
        a = self.edge_length
        r = a * 3 * sqrt(3) / 10
    elif self.mode_select == 'EXTERIOR_RADIUS':
        r = self.exterior_radius
        a = r * 10 / (sqrt(3) * 3)
    elif self.mode_select == 'INTERIOR_RADIUS':
        r = 2 * self.interior_radius
        a = r * 10 / (sqrt(3) * 3)

    chirality = -1 if self.chirality else 1
    n = self.number
    interior = self.interior
    exterior = self.exterior

    theta = acos(-2/3)
    h = a / sqrt(10)

    verts = [
        Vector((r * cos(n * theta), chirality * r * sin(n * theta), n * h)) for n in range(n)
    ]

    edges = [
        (i, i+1) for i in range(n-1)
    ] + [
        (i, i+2) for i in range(n-2)
    ] + [
        (i, i+3) for i in range(n-3)
    ]

    faces = []
    if interior:
        faces += [
            (i, i+1, i+2) for i in range(n-2)
        ]
    if exterior:
        faces += [
            (i, i+1, i+3) for i in range(n-3)
        ] + [
            (i, i+3, i+2) for i in range(n-3)
        ]

    mesh = bpy.data.meshes.new(name='tetrahelix')
    mesh.from_pydata(verts, edges, faces)
    object_data_add(context, mesh, operator=self)

class OBJECT_OT_add_tetrahelix(Operator, AddObjectHelper):
    '''Create a new Tetrahelix'''
    bl_idname = 'mesh.add_tetrahelix'
    bl_label = 'Tetrahelix'
    bl_options = {'REGISTER', 'UNDO'}

    mode_select: EnumProperty(
        name='Mode',
        description='Creation mode',
        items = [
            ('EDGE_LENGTH', 'Edge Length', '', 1),
            ('EXTERIOR_RADIUS', 'Exterior Radius', '', 2),
            ('INTERIOR_RADIUS', 'Interior Radius', '', 3),
        ],
        default='EXTERIOR_RADIUS',
    )
    chirality: BoolProperty(
        name='Chirality',
        description='Flip chirality',
        default=False,
    )
    number: IntProperty(
        name='Number of verts',
        default=9,
        min=4,
    )
    edge_length: FloatProperty(
        name='Edge Length',
        default=1.0,
    )
    exterior_radius: FloatProperty(
        name='Exterior Radius',
        default=1.0,
    )
    interior_radius: FloatProperty(
        name='Interior Radius',
        default=0.5,
    )
    interior: BoolProperty(
        name='Interior Faces',
        default=False,
    )
    exterior: BoolProperty(
        name='Exterior Faces',
        default=True,
    )

    def draw(self, context):
        layout = self.layout
        which_mode = self.mode_select
        col = layout.column()
        col.prop(self, 'mode_select')
        col.prop(self, 'number')
        if which_mode == 'EDGE_LENGTH':
            col.prop(self, 'edge_length')
        elif which_mode == 'EXTERIOR_RADIUS':
            col.prop(self, 'exterior_radius')
        elif which_mode == 'INTERIOR_RADIUS':
            col.prop(self, 'interior_radius')
        col.prop(self, 'interior')
        col.prop(self, 'exterior')
        col.prop(self, 'chirality')
        col.prop(self, 'align')

    def execute(self, context):
        add_object(self, context)
        return {'FINISHED'}

# Registration

def add_object_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_object.bl_idname,
        text='Tetrahelix',
        icon='MESH_ICOSPHERE'
    )

def register():
    bpy.utils.register_class(OBJECT_OT_add_object)
    bpy.types.VIEW3D_MT_mesh_add.append(add_object_button)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_object)
    bpy.types.VIEW3D_MT_mesh_add.remove(add_object_button)

if __name__ == '__main__':
    register()
