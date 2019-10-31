import bpy

# voir  https://blender.stackexchange.com/questions/57306/how-to-create-a-custom-ui

# ------------------------------------------------------------------------
#    Scene Properties
# ------------------------------------------------------------------------

class MyProperties(bpy.types.PropertyGroup):

    my_bool: bpy.props.BoolProperty(
        name="Enable or Disable",
        description="A bool property",
        default = False
        )

    my_int: bpy.props.IntProperty(
        name = "Int Value",
        description="A integer property",
        default = 23,
        min = 10,
        max = 100
        )

    my_float: bpy.props.FloatProperty(
        name = "Float Value",
        description = "A float property",
        default = 23.7,
        min = 0.01,
        max = 30.0
        )

    my_float_vector: bpy.props.FloatVectorProperty(
        name = "Float Vector Value",
        description="Something",
        default=(0.0, 0.0, 0.0), 
        min= 0.0, # float
        max = 0.1
    ) 

    my_string: bpy.props.StringProperty(
        name="User Input",
        description=":",
        default="",
        maxlen=1024,
        )

    my_path: bpy.props.StringProperty(
        name = "Directory",
        description="Choose a directory:",
        default="",
        maxlen=1024,
        subtype='DIR_PATH'
        )

    my_enum: bpy.props.EnumProperty(
        name="Dropdown:",
        description="Apply Data to attribute.",
        items=[ ('OP1', "Option 1", ""),
                ('OP2', "Option 2", ""),
                ('OP3', "Option 3", ""),
               ]
        )