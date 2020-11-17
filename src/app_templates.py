bl_info = {
    "name": "Create App Template",
    "blender": (2, 80, 0),
    "category": "Import-Export",
    "description": "Creates a new app template from the current blend file."
}

import os
import platform
import pwd
from pathlib import Path
import bpy

class WM_saveAppTemplate(bpy.types.Operator):
    """Saves the current blend file as a new app template."""
    bl_label = "Create an app template using the current blend file."
    bl_idname = "wm.saveapptemplate"
    template_name = bpy.props.StringProperty(name='Template Name',
                                             default='My Template')

    def execute(self, context):
        # Get path to save app template to.
        base_path =  os.path.join(bpy.utils.resource_path('USER'), 'scripts', 'startup', 'bl_app_templates_user')
        new_template_name = self.template_name
        app_template_dir = os.path.join(base_path, new_template_name)
        # Check if directory exists, if not create it.
        Path(app_template_dir).mkdir(parents=True, exist_ok=True)
        bpy.ops.wm.save_as_mainfile(filepath=app_template_dir+'/startup.blend')
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

def draw_menu(self, context):
    self.layout.separator()
    self.layout.operator(WM_saveAppTemplate.bl_idname, text="+ Create New App Template")


def register():
    bpy.utils.register_class(WM_saveAppTemplate)
    bpy.types.TOPBAR_MT_file_new.append(draw_menu)

def unregister():
    bpy.utils.unregister_class(WM_saveAppTemplate)
    bpy.types.TOPBAR_MT_file_new.remove(draw_menu)

if __name__ == "__main__":
    register()
    bpy.ops.wm.saveapptemplate('INVOKE_DEFAULT')