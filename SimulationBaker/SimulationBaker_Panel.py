import bpy

from . PhysicsDynamic_Op import SimulationBaker_OT_DynamicDeactivate
from . DestructionBaker_Op import SimulationBaker_OT_DestructionBaker

class SimulationBaker_PT_Panel(bpy.types.Panel):
    bl_label = "Destruction Baker Panel"
    bl_idname = "OBJECT_PT_DestructionBaker"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Simulation Baker'

    def draw(self, context):
        layout = self.layout
#        obj = context.object
        row = layout.row()
        scene = context.scene
        rbw = scene.rigidbody_world
        
        row.label(text='RigidBody Settings')
        row = layout.row()
        row.operator(operator = "rigidbody.objects_add", text = 'Set Active').type = 'ACTIVE'
        row.operator(operator = "rigidbody.objects_add", text = 'Set Passive').type = 'PASSIVE'
        row = layout.row()
        row.operator(operator = "rigidbody.shape_change")
        row = layout.row()
        row.operator(operator = "rigidbody.mass_calculate")
        row = layout.row()
        row.operator(operator = "rigidbody.object_settings_copy")
        row = layout.row()
        row = layout.row()
        row.operator(operator = "rigidbody.bake_to_keyframes")
        row = layout.row()
        
        row.label(text='Simulation Quality')
        
        if rbw is None:
            layout.operator("rigidbody.world_add")
            row = layout.row()
            rbw = scene.rigidbody_world
        else :
            row = layout.row()
            row.prop(rbw, "steps_per_second", text="Steps Per Second")
            row = layout.row()
            row.prop(rbw, "solver_iterations", text="Solver Iterations")
            row = layout.row()
        
        row.label(text='Dynamics Deactivation')
        row = layout.row()
        row.operator(operator = SimulationBaker_OT_DynamicDeactivate.bl_idname, text = 'Activate').state = 'ACTIVATE'
        row.operator(operator = SimulationBaker_OT_DynamicDeactivate.bl_idname, text = 'Desactivate').state = 'DEACTIVATE'
        row = layout.row()
        
        row.label(text='Baker')
        row = layout.row()
        row.operator(operator = SimulationBaker_OT_DestructionBaker.bl_idname, text='Bake Destruction', icon="BONE_DATA")