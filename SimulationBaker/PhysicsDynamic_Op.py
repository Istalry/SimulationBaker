import bpy

class SimulationBaker_OT_DynamicDeactivate(bpy.types.Operator):
    bl_idname = 'destuctionbaker.physicsdeactivation'
    bl_label = 'Destruction Baker Physics Deactivation'
    bl_description = 'Let activate/desactivate dynamic deactivation on all selected object'
    bl_options = {'REGISTER', 'UNDO'}
    

    state: bpy.props.StringProperty(name="ACTIVATE")
    
    def execute(self, context):
        selected = bpy.context.selected_objects
        for obj in selected:
            if obj.rigid_body != None:
                if self.state == 'ACTIVATE':                    
                    obj.rigid_body.use_deactivation = True
                    obj.rigid_body.use_start_deactivated = True
                elif self.state == 'DEACTIVATE':
                    obj.rigid_body.use_deactivation = False
                    obj.rigid_body.use_start_deactivated = False
        return {'FINISHED'}