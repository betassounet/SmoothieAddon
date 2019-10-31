##############################################################################
# ICI la partie interface IHM est codée
# Inspiré de :
# https://blender.stackexchange.com/questions/57306/how-to-create-a-custom-ui
##############################################################################

import bpy

# ------------------------------------------------------------------------
#    Menus
# ------------------------------------------------------------------------

class OBJECT_MT_CustomMenu(bpy.types.Menu):
    bl_label = "Select"
    bl_idname = "OBJECT_MT_custom_menu"

    def draw(self, context):
        layout = self.layout

        # Built-in operators
        layout.operator("object.select_all", text="Select/Deselect All").action = 'TOGGLE'  # appel direct d'opérateur existant dans Blender
        layout.operator("object.select_all", text="Inverse").action = 'INVERT'  # en passant l'action a effectuer
        layout.operator("object.select_random", text="Random")
# ------------------------------------------------------------------------


class Test_PT_Panel(bpy.types.Panel):
    bl_idname = "Test_PT_Panel"
    bl_label = "Test Panel"
    bl_category = "Test Addon"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    #bl_context = "objectmode"                  #Si l'on veut le panel que dans context object..


    @classmethod
    def poll(self,context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        mytool = scene.my_tool   # l'objet my_tool a été instancié dans le register..

        row = layout.row()   # aligne les boutons sur la row
        row.operator('view3d.cursor_center', text="Center 3D cursor")
        row.operator('view3d.test01', text="Test01")

        layout.operator('object.move_x', text="Test Move x") # ici un bouton a la ligne suivante

        layout.separator()
        layout.menu(OBJECT_MT_CustomMenu.bl_idname, text="Presets", icon="SCENE")  # ici le menu défini plus haut

        layout.separator()

        layout.prop(mytool, "my_bool")              # ici les propriétées définies dans test_prop.py  qui vont trouver automatiquement leur représentation layout dans Blender
        layout.prop(mytool, "my_enum", text="") 
        layout.prop(mytool, "my_int")
        layout.prop(mytool, "my_float")
        layout.prop(mytool, "my_float_vector", text="")
        layout.prop(mytool, "my_string")
        layout.prop(mytool, "my_path")
        layout.operator('wm.hello_world')

        
