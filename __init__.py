bl_info = {
    "name": "Megu Shinonome Accessory Checker",
    "description": "Checks the correctness of the objects in the scene for Megu Shinonome submission.",
    "author": "Hideki Saito",
    "version": (0, 0, 3),
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

        num_materials = 0

        material_result = ""

        for material_item in bpy.data.scenes.data.materials:
            if material_item.is_grease_pencil == False and material_item.users > 0:
                num_materials += 1
        
        if num_materials > 1:
            flagged = True
            material_result = "Materials: NG. Max 1. You have "+str(num_materials)
        else:
            material_result = "Materials: OK"

        num_object = 0
        num_polygons = 0
        num_ngons = 0
        
        object_result = ""
        polygons_result = ""

        for object_item in bpy.data.scenes.data.objects:
            if object_item.type == 'MESH':
                num_object += 1
                num_polygons = sum(len(p.vertices) - 2 for p in object_item.data.polygons)
                mesh = object_item.data
                for poly in mesh.polygons:
                    if len(poly.vertices) > 4:
                        num_ngons += 1
                
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
            
        if num_ngons > 0:
            flagged = True
            ngons_result = "N-gons: NG. Max 0. You have "+str(num_ngons)
        else:
            ngons_result = "N-gons: OK"

        
        if(flagged == False):
            ShowMessageBox(material_result + " / " + object_result + " / " + polygons_result + " / " + ngons_result)
        else:
            ShowMessageBox(material_result + " / " + object_result + " / " + polygons_result + " / " + ngons_result, 'ERROR')
            
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