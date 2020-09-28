bl_info = {
    "name": "Megu Shinonome Accessory Checker",
    "description": "Checks the scene for the correctness for submitting for Megu Shinonome.",
    "author": "Hideki Saito",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "category": "Object",
    "location": "View3D > Object > Check for Megu Shinonome",
    "support": "COMMUNITY"
}


import bpy

class MeguAccessoryCheck(bpy.types.Operator):
    """Check the scene for Megu accessory compatibility"""
    bl_idname = "object.megu_check"
    bl_label = "Check for Megu Shinonome"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        def ShowMessageBox(message = "",icon = 'INFO', title = "Check for Megu Shinonome"):

            def draw(self, context):
                self.layout.label(text=message)

            bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)


        flagged = False

        num_materials = len(bpy.data.scenes.data.materials)

        material_result = ""

        if num_materials > 2:
            flagged = True
            material_result = "Materials: NG. Max 1. You have"+str(num_materials - 1)
        else:
            material_result = "Materials: OK"

        num_object = 0
        num_polygons = 0

        object_result = ""
        polygons_result = ""

        for object_item in bpy.data.scenes.data.objects:
            if object_item.type == 'MESH':
                num_object += 1
                num_polygons = sum(len(p.vertices) - 2 for p in object_item.data.polygons)
                
                
        if num_object > 1:
            flagged = True
            object_result = "Objects: NG. Max 1. You have "+str(num_object)
        else:
            object_result = "Objects: OK"
            
        if num_polygons >= 5000:
            flagged = True
            polygons_result = "Polygons: NG. Max 5000. You have "+str(num_polygons)
        else:
            polygons_result = "Polygons: OK"
            
        if(flagged == False):
            ShowMessageBox(material_result + " / " + object_result + " / " + polygons_result)
        else:
            ShowMessageBox(material_result + " / " + object_result + " / " + polygons_result, 'ERROR')
            
        return {'FINISHED'}
        
def menu_func(self, context):
    self.layout.operator(MeguAccessoryCheck.bl_idname)
        
def register():
    bpy.utils.register_class(MeguAccessoryCheck)
    bpy.types.VIEW3D_MT_object.append(menu_func)
    
def unregister():
    bpy.utils.unregister_class(MeguAccessoryCheck)
    bpy.types.VIEW3D_MT_object.remove(menu_func)

    
# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()