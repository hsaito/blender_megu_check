Megu Shinonome Accessory Checker

Overview

This repository contains a small Blender add-on that performs scene checks for "Megu Shinonome" accessory submissions. The main add-on code is in `__init__.py` and registers a UI panel in the 3D View sidebar where the checker reports results.

What it checks

- Materials: Counts unique materials assigned to mesh objects (ignores grease pencil materials). Flags if more than 1 material is assigned across the scene.
- Objects: Counts mesh objects in the scene. Flags if more than 1 mesh is present.
- Polygons: Estimates polygon count using a triangulation heuristic (sum of (n-2) for each polygon). Flags if the total is >= 5000.
- N-gons: Counts polygons with more than 4 vertices. Flags if any n-gons are present.

Installation

1. Copy the `blender_megu_check` folder into a location you can access from Blender, or install as an add-on zip.
2. In Blender, go to `Edit > Preferences > Add-ons`.
3. Click `Install...` and select this folder (or a zip containing it) or click `Install` and choose the `__init__.py` file.
4. Enable the add-on from the list.
5. Open the 3D Viewport and look for the `Megu Check` tab in the Sidebar (N-panel).

Usage

- The add-on does not modify the scene; it only inspects it and displays the results in the `Megu Check` panel.
- The panel shows a summary (OK / Issues found) and detailed results for materials, objects, polygons, and n-gons.

Compatibility

- The add-on declares Blender compatibility for 2.80 and above in `bl_info`.
- Tested on Blender 2.80+ (basic API usage). If you encounter issues on newer Blender versions, please report them.

Development notes

- The checker function is `check_megu()` in `__init__.py`.
- The UI panel class is `VIEW3D_PT_megu_accessory_check` and registers itself via `register()`.
- The polygon count uses a heuristic and may differ from Blender's real triangle count after modifiers or custom triangulation; for exact counts consider applying modifiers or using mesh evaluated data.

License

See the `COPYING` file included in the repository.

Author

Hideki Saito
