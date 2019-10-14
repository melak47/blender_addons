bl_info = {
    'name': 'Auto Sharpen/Crease',
    'author': 'melak47',
    'version': (1, 0),
    'blender': (2, 80, 0),
    'location': 'View3D > Object/Mesh Context Menu',
    'description': 'Auto sharpen/crease edges based on auto-smooth angle',
    'category': 'Mesh',
}

import bpy

from contextlib import contextmanager

@contextmanager
def selected_meshes():
    selection_mode = bpy.context.object.mode
    selected_objects = [obj for obj in bpy.context.selected_objects]

    meshes = [obj for obj in selected_objects if obj.type == 'MESH']

    # deselect all objects
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')

    try:
        yield meshes
    finally:
        bpy.ops.object.mode_set(mode='OBJECT')
        for obj in selected_objects:
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode=selection_mode)

# put mesh in edit mode with edge selection
@contextmanager
def edit_mesh(mesh):
    # select mesh
    mesh.select_set(True)
    bpy.context.view_layer.objects.active = mesh

    # deselect all edges
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(use_extend=False, use_expand=True, type='EDGE')
    bpy.ops.mesh.select_all(action='DESELECT')

    try:
        yield mesh
    finally:
        bpy.ops.object.mode_set(mode='OBJECT')
        mesh.select_set(False)

def edit_mesh_edges():
    with selected_meshes() as meshes:
        for mesh in meshes:
            with edit_mesh(mesh) as mesh:
                yield mesh

def sharpen_crease_from_autosmooth_angle(mode: str):
    for _mesh in edit_mesh_edges():
        angle = bpy.context.object.data.auto_smooth_angle
        bpy.ops.mesh.edges_select_sharp(sharpness=angle)

        if mode == 'sharpen':
            bpy.ops.mesh.mark_sharp()
        elif mode == 'crease':
            bpy.ops.transform.edge_crease(value=1)

def copy_sharp_crease(mode: str):
    for mesh in edit_mesh_edges():

        # edge selection needs to happen in object mode for some reason
        bpy.ops.object.mode_set(mode='OBJECT')

        for e in mesh.data.edges:
            if mode == 'crease' and e.use_edge_sharp:
                e.select = True
            elif mode == 'sharpen' and e.crease > 0.0:
                e.select = True

        bpy.ops.object.mode_set(mode='EDIT')

        if mode == 'crease':
            bpy.ops.transform.edge_crease(value=1)
        elif mode == 'sharpen':
            bpy.ops.mesh.mark_sharp()


class OBJECT_OT_AutoSharpen(bpy.types.Operator):
    '''Auto sharpen edges'''
    bl_idname = 'object.auto_sharpen'
    bl_label = 'Auto Sharpen'
    bi_description = 'Auto sharpen edges based on auto-smooth angle'

    def execute(self, context):
        sharpen_crease_from_autosmooth_angle(mode='sharpen')
        return {'FINISHED'}

class OBJECT_OT_AutoCrease(bpy.types.Operator):
    '''Auto crease edges'''
    bl_idname = 'object.auto_crease'
    bl_label = 'Auto Crease'
    bi_description = 'Auto crease edges based on auto-smooth angle'

    def execute(self, context):
        sharpen_crease_from_autosmooth_angle(mode='crease')
        return {'FINISHED'}

class OBJECT_OT_CreaseSharp(bpy.types.Operator):
    '''Make sharp edges also creases'''
    bl_idname = 'object.crease_sharp'
    bl_label = 'Crease Sharp'
    bi_description = 'Make all sharp edges also creases'

    def execute(self, context):
        copy_sharp_crease(mode='crease')
        return {'FINISHED'}

class OBJECT_OT_SharpCrease(bpy.types.Operator):
    '''Make crease edges also sharp'''
    bl_idname = 'object.sharp_crease'
    bl_label = 'Sharpen Crease'
    bi_description = 'Make all crease edges also sharp'

    def execute(self, context):
        copy_sharp_crease(mode='sharpen')
        return {'FINISHED'}


def buttons(self, context):
    for op in [OBJECT_OT_AutoSharpen, OBJECT_OT_AutoCrease, OBJECT_OT_CreaseSharp, OBJECT_OT_SharpCrease]:
        self.layout.operator(
            op.bl_idname,
            text=op.bl_label
        )

def register():
    bpy.utils.register_class(OBJECT_OT_AutoSharpen)
    bpy.utils.register_class(OBJECT_OT_AutoCrease)
    bpy.utils.register_class(OBJECT_OT_CreaseSharp)
    bpy.utils.register_class(OBJECT_OT_SharpCrease)

    bpy.types.VIEW3D_MT_object_context_menu.append(buttons)

    bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(buttons)

def unregister():
    bpy.types.VIEW3D_MT_object_context_menu.remove(buttons)

    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(buttons)

    bpy.utils.unregister_class(OBJECT_OT_AutoSharpen)
    bpy.utils.unregister_class(OBJECT_OT_AutoCrease)
    bpy.utils.unregister_class(OBJECT_OT_CreaseSharp)
    bpy.utils.unregister_class(OBJECT_OT_SharpCrease)

if __name__ == '__main__':
    register()
