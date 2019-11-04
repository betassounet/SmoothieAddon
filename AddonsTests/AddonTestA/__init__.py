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
    "name" : "AddonTestA",
    "author" : "Fred",
    "description" : "Deuxieme Addon Test A",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "View3D",
    "warning" : "",
    "category" : "Generic"
}

#Tab0
    #Tab1 ( 4 espaces ) Automatique dans VScode !!
        #Tab2 ( 4 espaces )    

import bpy

from . panel import Test_PT_A_Panel
from . op import Test_OT_A_Operator01
from . op import Test_OT_A_Operator02
from . op1 import Test_OT_A_Operator03
from . opTest import Test_OT_A_Operator04
from . op2 import Test_OT_A2_Operator01


classes = (
    Test_PT_A_Panel,
    Test_OT_A_Operator01,
    Test_OT_A_Operator02,
    Test_OT_A_Operator03,
    Test_OT_A_Operator04,
    Test_OT_A2_Operator01
)


def register():
    from bpy.utils import register_class
    # register_class(Test_PT_A_Panel)
    # register_class(Test_OT_A_Operator01)
    for cls in classes:
       register_class(cls)
       

    

def unregister():
    from bpy.utils import unregister_class
    # unregister_class(Test_OT_A_Operator01)
    # unregister_class(Test_PT_A_Panel)

    for cls in reversed(classes):
       unregister_class(cls)

