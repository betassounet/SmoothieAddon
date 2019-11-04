import bpy
import os

# Attention nommage classes et bl_idName : https://wiki.blender.org/wiki/Reference/Release_Notes/2.80/Python_API/Addons

class Test_OT_A_Operator01(bpy.types.Operator):
    bl_idname = "view3d.add_plan1"
    bl_label = "Simple operator"
    bl_description = "desc - test01"


    def execute(self, context):
        verts = [
            (+1.0, +2.0, +0.1),
            (+1.0, -1.0, +0.1),
            (-1.0, -1.0, +0.1),
            (-1.0, +2.0, +0.1),
            # (+1.0, +1.0, +1.0),
            # (+1.0, -1.0, +1.0),
            # (-1.0, -1.0, +1.0),
            # (-1.0, +1.0, +1.0),
        ]
        edges=[]
        faces = [   
            (0, 1, 2, 3),
            # (4, 7, 6, 5),
            # (0, 4, 5, 1),
            # (1, 5, 6, 2),
            # (2, 6, 7, 3),
            # (4, 0, 3, 7),
        ]
        mesh = bpy.data.meshes.new("Box")      
        mesh.from_pydata(verts, edges, faces) 
        from bpy_extras import object_utils
        object_utils.object_data_add(context, mesh, None)
        return {'FINISHED'}


class Test_OT_A_Operator02(bpy.types.Operator):
    bl_idname = "view3d.add_line1"
    bl_label = "Simple operator"
    bl_description = "desc - test01"


    def execute(self, context):
        verts = [
            (+1.0, +2.0, +0.1),
            (+1.0, -1.0, +0.1),
        ]
        edges=[
            (0, 1),
            ]
        faces = []
        mesh = bpy.data.meshes.new("P_Line")      
        mesh.from_pydata(verts, edges, faces) 
        from bpy_extras import object_utils
        object_utils.object_data_add(context, mesh, None)
        return {'FINISHED'}


 