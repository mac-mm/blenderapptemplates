bl_info = {
    "name": "Create App Template",
    "blender": (2, 80, 0),
    "category": "Import/Export",
}

import os
import platform
import pwd
from pathlib import Path
import bpy

class WM_saveAppTemplate(bpy.types.Operator):
    """Saves the current layout as a new app template."""
    bl_label = "Save App Template"
    bl_idname = "wm.saveapptemplate"
    template_name = bpy.props.StringProperty(name='Template Name', default='New Template')

    def execute(self, context):
        # Get path to save app template to.
        base_path = self.getPath();
        new_template_name = self.template_name
        app_template_dir = base_path + '/%s' % new_template_name
        # Check if directory exists, if not create it.
        Path(app_template_dir).mkdir(parents=True, exist_ok=True)
        bpy.ops.wm.save_as_mainfile(filepath=app_template_dir+'/startup.blend')
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def getPath(self):
        operating_system = platform.uname().system
        logged_in_user = pwd.getpwuid(os.getuid()).pw_name
        blender_version = bpy.app.version
        # Check if user app templates directory exists, if not create it.
        if operating_system == 'Darwin':
            user_templates_dir = '/Users/%s/Library/ApplicationSupport/Blender/%s.%s/scripts/startup/bl_app_templates_user' % (logged_in_user, blender_version[0], blender_version[1])
        elif operating_system == 'Linux':
            home = str(Path.home())
            user_templates_dir = home + '/.config/blender/%s.%s/scripts/startup/bl_app_templates_user' % (blender_version[0], blender_version[1])
        else:
            user_templates_dir = '\\Users\\%s\\AppData\\Roaming\\Blender Foundation\\Blender\\%s.%s\\scripts\\startup\\bl_app_templates_user' % (logged_in_user, blender_version[0], blender_version[1])
        Path(user_templates_dir).mkdir(parents=True, exist_ok=True)
        return user_templates_dir

def draw_menu(self, context):
    self.layout.separator()
    self.layout.operator(WM_saveAppTemplate.bl_idname, text="+ New App Template")

def register():
    bpy.utils.register_class(WM_saveAppTemplate)
    bpy.types.TOPBAR_MT_file_new.append(draw_menu)

def unregister():
    bpy.utils.unregister_class(WM_saveAppTemplate)
    bpy.types.TOPBAR_MT_file_new.remove(draw_menu)

if __name__ == "__main__":
    register()
    bpy.ops.wm.saveapptemplate('INVOKE_DEFAULT')