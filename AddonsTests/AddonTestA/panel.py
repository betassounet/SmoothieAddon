import bpy

# Attention nommage classes et bl_idName : https://wiki.blender.org/wiki/Reference/Release_Notes/2.80/Python_API/Addons

class Test_PT_A_Panel(bpy.types.Panel):
    bl_idname = "TEST_PT_A1 "
    bl_label = "Test Panel A1"
    bl_category = "Test Addon A1"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    #bl_context = "objectmode"                  #Si l'on veut le panel que dans context object..

    def draw(self, context):
        layout = self.layout
        layout.operator('view3d.add_plan1', text="Ajout Plan") # ici un bouton a la ligne suivante
        layout.operator('view3d.add_line1', text="Ajout Line") # ici un bouton a la ligne suivante
        layout.operator('view3d.add_meshes1', text="Analyse 01") # ici un bouton a la ligne suivante

        