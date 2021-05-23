import bpy
import copy

class Move(bpy.types.Operator):

    bl_idname = 'move.hello'
    bl_label = 'Move'

    objects = []

    position_x = 0
    position_y = 0

    def execute(self, context):

        for obj in self.objects:

            obj.location[0] = self.position_x
            obj.location[1] = self.position_y

    def invoke(self, context, event):

        context.window_manager.modal_handler_add(self)
        self.objects = context.selected_objects

        for obj in self.objects:
            #print(obj.location)
            exec('self.{} = obj.location.copy()'.format(obj.name+'_start'))
            #print(self.Cube_start)

        return {'RUNNING_MODAL'}

    def undo(self):

        for obj in self.objects:
            #print(self.Cube_start)
            exec('obj.location[0] = self.{}[0]'.format(obj.name+'_start'))
            exec('obj.location[1] = self.{}[1]'.format(obj.name+'_start'))

    def modal(self, context, event):

        self.position_x = event.mouse_x/100
        self.position_y = event.mouse_y/100

        self.execute(context)

        if event.type == 'LEFTMOUSE':

            return {'FINISHED'}

        if event.type == 'RIGHTMOUSE':
            print(self.Cube_start)
            self.undo()
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}


class CustomPanel(bpy.types.Panel):

    bl_label = 'Random.Panel'
    bl_idname = 'OBJECT_PT_random'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Random Spheres'

    def draw(self, context):

        layout = self.layout
        obj = context.object
        row = layout.row()
        row.operator(Move.bl_idname, text='Generate', icon='SPHERE')


_class = [Move, CustomPanel]


def register():

    for cls in _class:

        bpy.utils.register_class(cls)


def unregister():

    for cls in _class:

        bpy.utils.unregister_class(cls)


register()