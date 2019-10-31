import bpy
import bmesh

class Test_OT_Operator(bpy.types.Operator):
    bl_idname = "view3d.cursor_center"
    bl_label = "Simple operator"
    bl_description = "Center 3d cursor"

    def execute(self, context):
        bpy.ops.view3d.snap_cursor_to_center()
        return {'FINISHED'}

        
class Test_OT_Operator01(bpy.types.Operator):
    bl_idname = "view3d.test01"
    bl_label = "Simple operator"
    bl_description = "desc - test01"

    def execute(self, context):
        #bpy.ops.view3d.snap_cursor_to_center()
        active_object = bpy.context.view_layer.objects.active
        selected_object = bpy.context.view_layer.objects.selected
        listSelected = []
        for obj in selected_object:
            listSelected.append(obj) 

        bpy.ops.object.select_all( action = 'SELECT' )
        bpy.ops.object.origin_set( type = 'ORIGIN_GEOMETRY' )
        bpy.ops.object.select_all( action = 'INVERT' )


        for obj in listSelected:
            if obj.type == 'MESH':
                for vertex in obj.data.vertices:
                    print("name :",obj.name," location :", obj.location , "  vertex : ", vertex.co)

        verts = [(+1.0, +2.0, -1.0),
                (+1.0, -1.0, -2.0),
                (-1.0, -1.0, -1.0),
                (-1.0, +2.0, -1.0),
                (+1.0, +1.0, +1.0),
                (+1.0, -1.0, +1.0),
                (-1.0, -1.0, +1.0),
                (-1.0, +1.0, +1.0),
                ]
        edges=[]
        faces = [   
                    (0, 1, 2, 3),
                    (4, 7, 6, 5),
                    (0, 4, 5, 1),
                    (1, 5, 6, 2),
                    (2, 6, 7, 3),
                    (4, 0, 3, 7),
                ]
        mesh = bpy.data.meshes.new("Box")      
        mesh.from_pydata(verts, edges, faces) 
#        bm = bmesh.new()

#https://svn.blender.org/svnroot/bf-blender/trunk/blender/release/scripts/templates_py/operator_mesh_add.py

 #       for v_co in verts:
 #           bm.verts.new(v_co)

        # for t in bm.verts:
        #     u=t
        # print(list(bm.verts))
        # bm.verts.ensure_lookup_table()
        # print(bm.verts[0])
        
        
        # for f_idx in faces:
        #     bm.faces.new([bm.verts[i] for i in f_idx])

        # bm.to_mesh(mesh)
        # mesh.update()
        #  # add the mesh as an object into the scene with this utility module
        from bpy_extras import object_utils
        object_utils.object_data_add(context, mesh, operator=self)

        #bpy.ops.mesh.primitive_plane_add(size=2.0, calc_uvs=True, enter_editmode=False, align='WORLD', location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0))


        mode = active_object.mode
        return {'FINISHED'}

class Test_OT_Operator_TestMove(bpy.types.Operator):
    # """My Object Moving Script"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.move_x"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Move X by One"         # Display name in the interface.
    #bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    x=0

    def execute(self, context):

        self.report({'INFO'},"param x %d" % (self.x))
        toto = self.x
        # The original script
        scene = context.scene
        for obj in scene.objects:
            obj.location.x += 1.0
        return {'FINISHED'}            # Lets Blender know the operator finished successfully.


class WM_OT_HelloWorld(bpy.types.Operator):
    bl_label = "Print Values Operator"
    bl_idname = "wm.hello_world"

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool

        # print the values to the console
        print("Hello World")
        print("bool state:", mytool.my_bool)
        print("int value:", mytool.my_int)
        print("float value:", mytool.my_float)
        print("string value:", mytool.my_string)
        print("enum state:", mytool.my_enum)

        return {'FINISHED'}