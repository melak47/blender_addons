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

def sharpen_crease_from_autosmooth_angle(mode: str):
    prev_mode = bpy.context.object.mode

    objects = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
    if objects:

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')

        for obj in objects:
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj

            bpy.ops.object.mode_set(mode='EDIT')

            bpy.ops.mesh.select_mode(use_extend=False, use_expand=True, type='EDGE')
            bpy.ops.mesh.select_all(action='DESELECT')

            angle = bpy.context.object.data.auto_smooth_angle
            bpy.ops.mesh.edges_select_sharp(sharpness=angle)

            if mode == 'sharpen':
                bpy.ops.mesh.mark_sharp()
            elif mode == 'crease':
                bpy.ops.transform.edge_crease(value=1)

            bpy.ops.object.mode_set(mode='OBJECT')
            obj.select_set(False)
        for obj in objects:
            obj.select_set(True)
        bpy.ops.object.mode_set(mode=prev_mode)

def copy_sharp_crease(mode: str):
    for obj in bpy.context.selected_objects:
        if obj.type == 'MESH':
            for e in obj.data.edges:
                if mode == 'crease':
                    if e.use_edge_sharp:
                        e.crease = 1
                elif mode == 'sharp':
                    if e.crease >= 0.5:
                        e.use_edge_sharp = True


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
    bl_label = 'Sharp Crease'
    bi_description = 'Make all sharp edges also creases'

    def execute(self, context):
        copy_sharp_crease(mode='crease')
        return {'FINISHED'}

class OBJECT_OT_SharpCrease(bpy.types.Operator):
    '''Make crease edges also sharp'''
    bl_idname = 'object.sharp_crease'
    bl_label = 'Crease Sharp'
    bi_description = 'Make all crease edges also sharp'

    def execute(self, context):
        copy_sharp_crease(mode='sharp')
        return {'FINISHED'}


def button_sharpen(self, context):
    self.layout.operator(
        OBJECT_OT_AutoSharpen.bl_idname,
        text='Auto Sharpen'
    )

def button_crease(self, context):
    self.layout.operator(
        OBJECT_OT_AutoCrease.bl_idname,
        text='Auto Crease'
    )

def button_crease_sharp(self, context):
    self.layout.operator(
        OBJECT_OT_CreaseSharp.bl_idname,
        text='Sharp Crease'
    )

def button_sharp_crease(self, context):
    self.layout.operator(
        OBJECT_OT_SharpCrease.bl_idname,
        text='Crease Sharp'
    )

def register():
    bpy.utils.register_class(OBJECT_OT_AutoSharpen)
    bpy.utils.register_class(OBJECT_OT_AutoCrease)
    bpy.utils.register_class(OBJECT_OT_CreaseSharp)
    bpy.utils.register_class(OBJECT_OT_SharpCrease)

    bpy.types.VIEW3D_MT_object_context_menu.append(button_sharpen)
    bpy.types.VIEW3D_MT_object_context_menu.append(button_crease)
    bpy.types.VIEW3D_MT_object_context_menu.append(button_crease_sharp)
    bpy.types.VIEW3D_MT_object_context_menu.append(button_sharp_crease)

    bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(button_sharpen)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(button_crease)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(button_crease_sharp)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(button_sharp_crease)

def unregister():
    bpy.types.VIEW3D_MT_object_context_menu.remove(button_sharpen)
    bpy.types.VIEW3D_MT_object_context_menu.remove(button_crease)
    bpy.types.VIEW3D_MT_object_context_menu.remove(button_crease_sharp)
    bpy.types.VIEW3D_MT_object_context_menu.remove(button_sharp_crease)

    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(button_sharpen)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(button_crease)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(button_crease_sharp)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(button_sharp_crease)

    bpy.utils.unregister_class(OBJECT_OT_AutoSharpen)
    bpy.utils.unregister_class(OBJECT_OT_AutoCrease)
    bpy.utils.unregister_class(OBJECT_OT_CreaseSharp)
    bpy.utils.unregister_class(OBJECT_OT_SharpCrease)

if __name__ == '__main__':
    register()
