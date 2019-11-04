import bpy
           
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

        