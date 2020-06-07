bl_info = {
    "name": "Lock View Rotation",
    "author": "melak47",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > View",
    "description": "Locks/unlocks rotation for the active 3d view",
    "warning": "",
    "wiki_url": "",
    "category": "3D View",
}


import bpy

class VIEW3D_OT_LockViewRotation(bpy.types.Operator):
    """Lock 3d view rotation"""
    bl_idname = "view3d.lock_view_rotation"
    bl_label = "Lock View Rotation"
    bi_description = "Lock 3d view rotation"

    def execute(self, context):
        try:
            context.space_data.region_3d.lock_rotation = not context.space_data.region_3d.lock_rotation
        except:
            pass
        return {'FINISHED'}

def lock_rotation_button(self, context):
    self.layout.operator(
        VIEW3D_OT_LockViewRotation.bl_idname,
        text='Lock View Rotation',
        icon='PLUGIN',
    )

def register():
    bpy.utils.register_class(VIEW3D_OT_LockViewRotation)
    bpy.types.VIEW3D_MT_view.append(lock_rotation_button)


def unregister():
    bpy.utils.unregister_class(VIEW3D_OT_LockViewRotation)
    bpy.types.VIEW3D_MT_view.remove(lock_rotation_button)


if __name__ == "__main__":
    register()
