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

        
class Test_OT_A_Operator03(bpy.types.Operator):
    bl_idname = "view3d.analyse1"
    bl_label = "Simple operator"
    bl_description = "desc - test01"


    # voir : https://blender.stackexchange.com/questions/34789/how-to-get-vertex-coordinates-after-modifier-in-python
    # Mais marche pas ici..
    def get_verts_edges(obj, use_modifiers=True, settings='PREVIEW'):
        scene = bpy.context.scene
        obj_data = obj.to_mesh(scene, use_modifiers, settings)

        verts = [v.co for v in obj_data.vertices]

        # or..use a copy to avoid dereferencing due to the .remove()
        # verts = [v.co.copy() for v in obj_data.vertices]  

        edges = obj_data.edge_keys
        bpy.data.meshes.remove(obj_data)

        return verts, edges


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

                    # Il faut aussi récupèrer les transformations pour l'objet :
                    # voir :   https://blender.stackexchange.com/questions/7576/how-can-i-use-a-python-script-to-get-the-transformation-of-an-object  
                    # voir : https://blender.stackexchange.com/questions/34789/how-to-get-vertex-coordinates-after-modifier-in-python

                    print("name :",obj.name," location :", obj.location , "  vertex : ", vertex.co)
                    # next est un iterateur en python, c'est une peut comme une boucle while...
                    # on peut ecrire aussi next( (x for x in MyList if x.name == obj.name)), defautValue)
                    if("P_Line" in obj.name):

                        # _verts, _edges = self.get_verts_edges(obj)   # marche pas..
                        # print(_verts, _edges)

                        existIter = next(filter(lambda x:x.name == obj.name, MyList), None)
                        if existIter:
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

        return {'FINISHED'}


            
class Test_OT_A_Operator04(bpy.types.Operator):
    bl_idname = "view3d.analyse2"
    bl_label = "Simple operator"
    bl_description = "desc - test01"

    listVal = []
    cptIteration=0

    def updateList(self, iteration, path, level, index,  value=None):
        if value:
            self.listVal.append(str(iteration)+"["+str(level)+","+str(index)+ "]  " + path + "  :" + str(value))
        else:
            self.listVal.append(str(iteration)+"["+str(level)+","+str(index)+ "]  " + path)

    def Introspection(self, Myobj, path, level, index=0):
        self.cptIteration = self.cptIteration+1
        if(self.cptIteration == 3426):
            print("Stop")

        nameobj = str(Myobj)

        if self.cptIteration == 3427:   # Blender plante ici
            print(Myobj)
            print(nameobj)
            if(nameobj == "MeshLoopTriangle"):  # Blender plante sur cet objet
                print(self.cptIteration)
                return

        if self.cptIteration == 3898:   # Blender plante ici
            print(Myobj)
            print(nameobj)
            return

        if "MeshLoopTriangle" in nameobj:  # Blender plante sur cet objet
            print(self.cptIteration)
            return

        pathFile = "C:/Partage/"
        with open(pathFile + "file.txt", "w") as file:
            file.write("%i " % (self.cptIteration))

        dirObj = dir(Myobj)
        cptAtt=0
        try:
            for att in dirObj:
                newPath = path+"."+att
                if "__len__" in att:
                    #nb = getattr(Myobj,att)
                    nb = len(Myobj)

                    # ici on pourrait poursuivre l'introspection sur un tableau.. mais.. on va noter.. 
                    #self.updateList(self.cptIteration, newPath + "["+ str(nb)+"]", level, index)
                        
                    # for i in range(nb):
                    #     self.Introspection(Myobj[i], newPath,level, i)


                else:
                    if not "__" in att:
                        #typeCallale = callable(att)
                        #typeAtt = type(att)
                        #dirAtt = dir(att)
                        if att == "edges" or att=="vector":
                            typeAtt = type(att)
                        try:
                            valAtt = getattr(Myobj,att)
                        except:
                            typeAtt = type(att)
                            self.updateList(self.cptIteration, newPath + "  : Exception ("+att+")", level, index)
                            continue
                        #typeValAtt = type(valAtt)
                        if valAtt == None:
                            #self.updateList(self.cptIteration, newPath + "  : None", level, index)
                            continue
                        else:
                            if isinstance(valAtt,int) or isinstance(valAtt,str):
                                #self.updateList(self.cptIteration, newPath,level,index, valAtt)
                                continue
                            else:
                                if level < 5:
                                    self.Introspection(valAtt, newPath,level+1 )
                                else:
                                    #self.updateList(self.cptIteration, newPath + "   --- END", level, index)
                                    continue
                    else:
                        cptAtt = cptAtt+1
            #self.updateList(self.cptIteration, path + "  "+ str(cptAtt)+" Att non traité ("+att+")", level, index)
        except:
            print("Exception")

    def execute(self, context):
        selection = bpy.context.selected_objects
        self.Introspection(selection[0], "root",0)
        self.updateList(-1, "END", -1, -1)

        # objType = type(selection)
        # emptyobj = objType()
        # print(selection)


        return {'FINISHED'}

        