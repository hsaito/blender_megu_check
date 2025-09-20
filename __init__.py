bl_info = {
    "name": "Megu Shinonome Accessory Checker",
    "description": "Displays scene checks for Megu Shinonome submission in a UI panel.",
    "author": "Hideki Saito",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "category": "Object",
    "location": "View3D > Sidebar > Megu Check",
    "support": "COMMUNITY"
}

import bpy

def check_megu():
    """
    Run the checks and return a dictionary with results.
    """
    result = {
        "flagged": False,
        "num_materials": 0,
        "material_ok": True,
        "num_objects": 0,
        "objects_ok": True,
        "num_polygons": 0,
        "polygons_ok": True,
        "num_ngons": 0,
        "ngons_ok": True
    }

    # Materials: count unique materials that are assigned to objects (material slots)
    mats_assigned = set()
    for obj in bpy.data.objects:
        # Some object types (e.g. empty) don't have data or materials
        if obj.type == 'MESH' and hasattr(obj.data, "materials"):
            for mat in obj.data.materials:
                if mat is None:
                    continue
                # skip grease pencil materials (if attribute exists)
                if getattr(mat, "is_grease_pencil", False):
                    continue
                mats_assigned.add(mat)
    result["num_materials"] = len(mats_assigned)
    if result["num_materials"] > 1:
        result["material_ok"] = False
        result["flagged"] = True

    # Objects, polygons, ngons
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            result["num_objects"] += 1
            mesh = obj.data
            # accumulate polygon count (triangulation count heuristic: n-2 per polygon)
            result["num_polygons"] += sum(max(0, len(p.vertices) - 2) for p in mesh.polygons)
            for poly in mesh.polygons:
                if len(poly.vertices) > 4:
                    result["num_ngons"] += 1

    if result["num_objects"] > 1:
        result["objects_ok"] = False
        result["flagged"] = True

    # Follow original rule: Max 5000 polygons (original flagged when >= 5000)
    if result["num_polygons"] >= 5000:
        result["polygons_ok"] = False
        result["flagged"] = True

    if result["num_ngons"] > 0:
        result["ngons_ok"] = False
        result["flagged"] = True

    return result


class VIEW3D_PT_megu_accessory_check(bpy.types.Panel):
    """Panel that displays Megu accessory check results"""
    bl_label = "Megu Shinonome Check"
    bl_idname = "VIEW3D_PT_megu_accessory_check"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Megu Check"

    def draw(self, context):
        layout = self.layout
        res = check_megu()

        # Summary
        row = layout.row()
        if res["flagged"]:
            row.label(text="Issues found", icon='ERROR')
        else:
            row.label(text="All checks OK", icon='CHECKMARK')

        box = layout.box()
        # Materials
        if res["material_ok"]:
            box.label(text=f"Materials: OK (assigned to objects: {res['num_materials']})", icon='CHECKMARK')
        else:
            box.label(text=f"Materials: NG — Max 1 (assigned to objects: {res['num_materials']})", icon='ERROR')

        # Objects
        if res["objects_ok"]:
            box.label(text=f"Objects: OK (meshes: {res['num_objects']})", icon='CHECKMARK')
        else:
            box.label(text=f"Objects: NG — Max 1 (meshes: {res['num_objects']})", icon='ERROR')

        # Polygons
        if res["polygons_ok"]:
            box.label(text=f"Polygons: OK (approx: {res['num_polygons']})", icon='CHECKMARK')
        else:
            box.label(text=f"Polygons: NG — Max 5000 (approx: {res['num_polygons']})", icon='ERROR')

        # N-gons
        if res["ngons_ok"]:
            box.label(text=f"N-gons: OK (count: {res['num_ngons']})", icon='CHECKMARK')
        else:
            box.label(text=f"N-gons: NG — Max 0 (count: {res['num_ngons']})", icon='ERROR')

        # No popup button is provided — panel only.


classes = (
    VIEW3D_PT_megu_accessory_check,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()