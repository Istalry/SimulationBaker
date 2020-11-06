import bpy

class SimulationBaker_OT_DestructionBaker(bpy.types.Operator):
    bl_idname = 'destuctionbaker.bakedestruction'
    bl_label = 'Destruction Baker'
    bl_description = 'Baker of destruction in an armature'
    bl_options = {'REGISTER', 'UNDO'}
    
    
    def execute(self, context):
        #Duplicate selected object
        bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)
        src_obj = bpy.context.selected_objects
        if len(src_obj) <= 0:
            return {'FINISHED'} 
        bpy.ops.object.duplicate_move()

        #Reset Position and rotation of the duplicate object
        copy_obj = bpy.context.selected_objects
        bpy.ops.object.location_clear()
        bpy.ops.object.rotation_clear()
        bpy.ops.transform.rotate(value=1.5708, orient_axis='X', orient_type='LOCAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='LOCAL', constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

        #Delete animation data of the selected Object
        for obj in copy_obj:    
            bpy.ops.object.select_all(action='DESELECT')
            bpy.data.objects[obj.name].select_set(True)
            ad = obj.animation_data
            if ad != None:
                obj.animation_data_clear()
                
        #Create Armature
        bpy.ops.object.armature_add()
        armature = bpy.context.selected_objects
        armature[0].name = 'BakeDestruction'
        bpy.ops.object.editmode_toggle()

        #For each duplicate object create a disconnected bone, and copy position and rotation from a src obj
        for i in range(0,len(src_obj)):
            bpy.ops.armature.extrude_move(TRANSFORM_OT_translate={"value":(0,0,1)})
            bpy.ops.armature.select_more()
            bpy.ops.armature.parent_clear(type='DISCONNECT')
            bone = bpy.context.active_bone
            bone.name = src_obj[i].name
            bpy.ops.transform.translate(value=(0,0,-1))
            bpy.ops.armature.select_hierarchy()

        #Create Selection of new bones
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.posemode_toggle()

        bpy.ops.pose.select_all(action='INVERT')
        bones = bpy.context.selected_pose_bones

        #Add bone constrain and link them to the soures object
        for i in range(0,len(bones)):
            location = bones[i].constraints.new('COPY_LOCATION')
            location.target = src_obj[i]
            rotation = bones[i].constraints.new('COPY_ROTATION')
            rotation.target = src_obj[i]
            
        #Link object to armature and his bone
        bpy.ops.object.posemode_toggle()
        for i in range(0,len(copy_obj)):
            bpy.ops.object.select_all(action='DESELECT')
            bpy.data.objects[copy_obj[i].name].select_set(True)
            bpy.data.objects[armature[0].name].select_set(True)
            bpy.ops.object.parent_set(type='ARMATURE_NAME', keep_transform=True)
            
            bpy.ops.object.select_all(action='DESELECT')
            bpy.data.objects[copy_obj[i].name].select_set(True)
            group = copy_obj[i].vertex_groups[bones[i].name]
            vertices = []
            for vert in copy_obj[i].data.vertices:
                vertices.append(vert.index)
            group.add(vertices, 1, 'ADD')
            
        #Bake Action
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects[armature[0].name].select_set(True)    
        bpy.ops.nla.bake(frame_start=bpy.context.scene.frame_start, frame_end=bpy.context.scene.frame_end, visual_keying=True, bake_types={'POSE'})

#        #Move to an new collection
#        collection = bpy.data.collections.new("Bake Destruction")
#        bpy.context.scene.collection.children.link(collection)
#        collection.objects.link(armature[0])
#        armature[0].users_collection[1].objects.unlink(armature[0])
#        for i in range(0,len(copy_obj)):
#            collection.objects.link(copy_obj[i])
#            copy_obj[i].users_collection[1].objects.unlink(copy_obj[i])
#            
        #Delete Unused action animation
        actions = bpy.data.actions
        while len(actions) > 1:
            if actions[0] != armature[0].animation_data.action:        
                bpy.data.actions.remove(actions[0])
            elif actions[1] != armature[0].animation_data.action:
                bpy.data.actions.remove(actions[1])

        #Delete src objects 
#        bpy.data.collections.remove(src_obj[0].users_collection[0])
        for src in src_obj:
            if src != None:
                bpy.ops.object.select_all(action='DESELECT')
                bpy.data.objects[src.name].select_set(True)
                bpy.ops.object.delete()
                
        #Join copied object and rename the final mesh
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects[armature[0].name].select_set(False)
        for obj in copy_obj:
            bpy.data.objects[obj.name].select_set(True)
        bpy.context.view_layer.objects.active = copy_obj[0]
        bpy.ops.object.join()
        finalmesh = bpy.context.selected_objects
        finalmesh[0].name = 'bakedDestruction'
        return {'FINISHED'} 