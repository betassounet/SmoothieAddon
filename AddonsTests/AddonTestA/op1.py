import bpy
import blf
        

# voir : https://blender.stackexchange.com/questions/150267/how-to-move-object-while-tracking-to-mouse-cursor-with-a-modal-operator
def draw_callback_px(self, context):
    font_id = 0
    blf.position(font_id, 15, 100, 0)
    blf.size(font_id, 12, 72)
    blf.draw(font_id, "Mouse position: " )
    blf.position(font_id, 15, 115, 0)
    blf.draw(font_id, "Location on plane " )
    blf.position(font_id, 15, 130, 0)
    blf.draw(font_id, "Object location " )

class Test_OT_A_Operator03(bpy.types.Operator):
    bl_idname = "view3d.analyse1"
    bl_label = "Simple operator"
    bl_description = "desc - test01"

    def execute(self, context):

        class MyLine(object):
            def __init__(self, name, vector):
                self.name = name
                self.vector1 = vector
                self.vector2 = None

        MyList = []
        scene = context.scene
        for obj in scene.objects:
            if obj.type == 'MESH':
                for vertex in obj.data.vertices:
                    print("name :",obj.name," location :", obj.location , "  vertex : ", vertex.co)
                    if("P_Line" in obj.name):

                        obj.select_set(state=True)                   # rendre actif un objet avec l'API 2.8
                        bpy.context.view_layer.objects.active = obj  
                        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)  # apparement s'applique a l'objet actif

                        existIter = next(filter(lambda x:x.name == obj.name, MyList), None)   # next est un iterateur en python, c'est une peut comme une boucle while...
                        if existIter:                                                         # on peut ecrire aussi next( (x for x in MyList if x.name == obj.name)), defautValue)
                            existIter.vector2 =  obj.location + vertex.co
                        else:
                            MyList.append(MyLine(obj.name, obj.location + vertex.co))
        print("--------------------------------------------")
        for obj in MyList:
            print("name :",obj.name," v1 :", obj.vector1 , "  v2 : ", obj.vector2)


        # constitution des faces , mais pas évidents a partir des edges.. et les quad de blender
        # La succesion des points n'est pas 0,1,2,3 .. les mesh se croisent
        # il faut 'tourner' autour des points
        # arbitrairement on va mettre face = 0, 1, 3, 2, mais ça il va falloir le calculer..
        # c'est pas un point positif pour le quad pllutôt que le triangle en suface minimale..

        listObject3D = []
        class MyObject3D(object):
            def __init__(self, name, verts):
                self.name = name
                self.verts=verts
                self.edges=[]
                self.faces = [(0, 1, 3, 2),]    # attention histoire des croisements qui donne une surface en bonnet d'ane..

        lngList = len(MyList)
        for i in range(lngList-1):
            print(i)
            verts = [
                (MyList[i].vector1.x,MyList[i].vector1.y, 0),
                (MyList[i].vector2.x,MyList[i].vector2.y, 0),
                (MyList[i+1].vector1.x,MyList[i+1].vector1.y, 0),
                (MyList[i+1].vector2.x,MyList[i+1].vector2.y, 0),
            ]
            listObject3D.append(MyObject3D("Box_"+ str(i),verts ))

        for obj3D in listObject3D:
            print(obj3D.name)
            mesh = bpy.data.meshes.new(obj3D.name)      
            mesh.from_pydata(obj3D.verts, obj3D.edges, obj3D.faces) 
            mesh.update()
            from bpy_extras import object_utils
            #object_utils.object_data_add(context, mesh, operator=self)
            object_utils.object_data_add(context, mesh, None)  # solution pour les parametres..: https://docs.blender.org/api/current/bpy_extras.object_utils.html


        bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, (None), 'WINDOW', 'POST_PIXEL')

        return {'FINISHED'}

