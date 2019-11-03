import bpy

class Test_OT_A2_Operator01(bpy.types.Operator):
    bl_idname = "view3d.analysecoord"
    bl_label = "Simple operator"
    bl_description = "desc - test01"


    def execute(self, context):
        selection = bpy.context.selected_objects
        obj = selection[0]
        if obj.type == 'MESH':
            print("-------------------  name :",obj.name)
            loc, rot, scale = obj.matrix_world.decompose()    # https://blender.stackexchange.com/questions/7576/how-can-i-use-a-python-script-to-get-the-transformation-of-an-object
            print("loc :",loc," rot :", rot, " scale : ", scale)
            for vertex in obj.data.vertices:
                print("  vertex : ", vertex.co)

            #scene = bpy.context.scene                        # https://blender.stackexchange.com/questions/34789/how-to-get-vertex-coordinates-after-modifier-in-python
            #use_modifiers=True
            #settings='PREVIEW'
            obj_data = obj.to_mesh()   # to create a mesh data block from the current state of the object
            verts = [v.co for v in obj_data.vertices]
            print("-----vertex : ", verts)
            #bpy.context.scene.cursor_location = verts[0]
            obj.to_mesh_clear()

            # SI on effectu sous Blender un transform apply à un objet CtrlA > Apply..
            # Les coordonnées sont recalculée.. maintenant comment faire ça en script.. 
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)  # apparement s'applique a l'objet actif
                                                                                     # voir https://blender.stackexchange.com/questions/107962/apply-transformations-does-not-work-in-automated-process
            for vertex in obj.data.vertices:
               print("After apply :  vertex : ", vertex.co)

            # voir : https://www.blender.org/forum/viewtopic.php?t=11648  pour faire a la main..

        return {'FINISHED'}