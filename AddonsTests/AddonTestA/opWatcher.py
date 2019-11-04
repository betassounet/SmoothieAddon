import bpy
from mathutils import Vector

#Ajout maison d'un espion de comportement de la souris a partir de :
# voir : https://blender.stackexchange.com/questions/76303/how-to-use-script-get-event-3d-cursorposition-change-in-blender

# Ca ne marche pas en version 2.8 parceque a modifié son API au niveau de la gestion des Handlers...
# voir.. https://devtalk.blender.org/t/porting-my-addons-to-2-8-missing-scene-update-post-handler/2465
# la communauté n'est pas contente..


#A class that takes into account a context and one of its attributes value
#If the value changes a callback is fired
class EventWatcher:

    #Set of watchers
    eventWatchers = set()

    @staticmethod
    def AddWatcher( watcher ):
        EventWatcher.eventWatchers.add( watcher )    

    @staticmethod
    def RemoveWatcher( watcher ):
        EventWatcher.eventWatchers.remove( watcher )

    @staticmethod
    def RemoveAllWatchers():
        EventWatcher.eventWatchers.clear()
    
    #From 'context', 'path' needs to exist
    #'comparer' is to compare the previous value of context.path to its new value
    #'callback' is the cb called if the value if changed
    #'copyValue' indicates if the value needs to be copied (that can be needed as if not old and new value may point onto the same object)
    def __init__( self, context, path, comparer, callback, copyValue ):
        self.context = context
        self.path = path
        self.comparer = comparer
        self.callback = callback
        self.copyValue = copyValue
        self.currentValue = self.GetValue()

    def GetValue( self ):
        value = getattr( self.context, self.path )
        if self.copyValue:
            value = value.copy()
        return value

    def Fire( self ):
        newValue = self.GetValue()
        if self.comparer( self.currentValue, newValue ) == False:
            self.callback( self, newValue )
            self.currentValue = newValue


#Global loop on the watchers. This callback responds to scene_update_post global handler
def cb_scene_update(context):
    from . opWatcher import EventWatcher
    for ew in EventWatcher.eventWatchers:
        ew.Fire()

def dir_watcher():
    from . opWatcher import EventWatcher
    cpt=0
    for ew in EventWatcher.eventWatchers:
        print("Context : ", ew.context, " path : ", ew.path)   
        cpt = cpt+1
    if(cpt == 0):
        print("Aucun event enregistré ")

#To stop the calls at the scene_update_post event level
class InitGlobal(bpy.types.Operator):
    bl_idname = "scene.init_global"
    bl_label = "Init global"

    def execute(self, context):
        from . globalJob import global_class
        global_class()
        return {'FINISHED'}

#To stop the calls at the scene_update_post event level
class StopCallback(bpy.types.Operator):
    bl_idname = "scene.stop_callback"
    bl_label = "Stop Callback"

    @classmethod
    def poll(cls, context):
        #toto = bpy.app.handlers
        # ajout de fonctionnalité suivant : # voir : https://blender.stackexchange.com/questions/76303/how-to-use-script-get-event-3d-cursorposition-change-in-blender
        #return cb_scene_update in bpy.app.handlers.scene_update_post   # A priori ça a changé en version 2.8 : https://docs.blender.org/api/current/bpy.app.handlers.html
        return cb_scene_update in bpy.app.handlers.depsgraph_update_post

    def execute(self, context):
        bpy.app.handlers.depsgraph_update_post.remove(cb_scene_update)
        print("Stop : ")
        dir_watcher()
        return {'FINISHED'}

#To start the calls at the scene_update_post event level
class StartCallback(bpy.types.Operator):
    bl_idname = "scene.start_callback"
    bl_label = "Start Callback"

    @classmethod
    def poll(cls, context):
        return cb_scene_update not in bpy.app.handlers.depsgraph_update_post

    def execute(self, context):
        bpy.app.handlers.depsgraph_update_post.append(cb_scene_update)
        print("Start : ")
        dir_watcher()
        return {'FINISHED'}