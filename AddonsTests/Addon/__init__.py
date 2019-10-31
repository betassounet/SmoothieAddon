##############################################################################
# FICHIER D'init pour l'addon, a chaque nouveau addon via le plugin Blender Development de Jacques Lucke, y a creation du fichier __init__.py
# d'ou obligatoirement un répertoire différent par pluggin..
##############################################################################


# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Test",
    "author" : "Fred",
    "description" : "Simple test addon",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "View3D",
    "warning" : "",
    "category" : "Generic"
}

import bpy


from . test_op import Test_OT_Operator
from . test_op import Test_OT_Operator01
from . test_op import Test_OT_Operator_TestMove
from . test_op import WM_OT_HelloWorld


from . test_panel import Test_PT_Panel
from . test_panel import OBJECT_MT_CustomMenu

from . test_prop import MyProperties



classes = (
    Test_OT_Operator, 
    Test_PT_Panel,
    Test_OT_Operator01, 
    Test_OT_Operator_TestMove,
    MyProperties,
    OBJECT_MT_CustomMenu,
    WM_OT_HelloWorld
    )


# remplacé par register / unregister explicite : 

#register, unregister = bpy.utils.register_classes_factory(classes)

# voir  https://blender.stackexchange.com/questions/57306/how-to-create-a-custom-ui

#register / unregister explicite pour faire le travail a la main et rajouter aussi ce qu'on veut en plus
# comme ici l'instance de my_tool..
def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=MyProperties)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.my_tool