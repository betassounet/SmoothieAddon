import bpy

# voir : https://blender.stackexchange.com/questions/76303/how-to-use-script-get-event-3d-cursorposition-change-in-blender

class global_class:

    #from . opWatcher import EventWatcher

    def __init__(self):
        print( '--------  INIT GLOBAL ------------------' )

        #Example:

        #The comparaison (for cursor location, it is a vector comparison)
        def CompareLocation( l1, l2 ):
            return l1 == l2

        #The callback to execute when the cursor's location changes    
        def CompareLocationCallback( watcher, newValue ):
            print( 'New value', newValue )

        #Install the watcher which will run the callback
        from . opWatcher import EventWatcher
        #watch = EventWatcher( bpy.data.scenes[0], "cursor_location", CompareLocation, CompareLocationCallback, True )   # ca aussi.. ça change...https://devtalk.blender.org/t/cursor-location-as-scene-attribute/6110
        watch = EventWatcher( bpy.data.scenes[0].cursor, "location", CompareLocation, CompareLocationCallback, True )
        EventWatcher.AddWatcher(watch)

    