import unreal


def CorrectMesh(asset, enum):
    ### ###
    #match asset_type:
    #    case "cape":
    #        new_root_translation = unreal.Vector(0.0,0.0,0.0)
    #        unreal.log("cape input accepted")
    #    case "tail":
    #        new_root_translation = unreal.Vector(0.0,0.0,0.0)
    #        unreal.log("tail input accepted")
    #    case "backpack":
    #        new_root_translation = unreal.Vector(0.0,0.0,0.0)
    #        unreal.log("backpack input accepted")
    #    case _:
    #        new_root_translation = unreal.Vector(0.0,0.0,0.0)
    #        unreal.log("Input not accepted -- Defaulting to zeros")
    
    # Loading Libs
    # load the weight modifier
    weight_modifier = unreal.SkinWeightModifier()
    # load the skeleton modifier
    skeleton_modifier = unreal.SkeletonModifier()
    EUL = unreal.EditorUtilityLibrary
    skeleton_modifier.set_skeletal_mesh(asset)
    bone_names = skeleton_modifier.get_all_bone_names()
    # get bone and its transform
    if enum == "tail":
        new_root_translation = unreal.Vector(0.0,0.0,0.0)
        index = 0
        unreal.log("tail input accepted")
    elif enum == "cape":
        new_root_translation = unreal.Vector(0.000000,-2.764120,-13.511305)
        # World space (X=0.000000,Y=-13.511304,Z=2.764117)
        index = 1
        unreal.log("cape input accepted")
    elif enum == "backpack":
        new_root_translation = unreal.Vector(0.0,0.0,0.0)
        index = 0
        unreal.log("backpack input accepted")
    else:
        unreal.log("Input not accepted -- ERROR")
    
    unreal.log(new_root_translation)
    # create a zero vector
    root_translation = unreal.Vector(0.0,0.0,0.0)
    
    # For root (index == 0) -> bone space = world space
    # for index != 0 -> bone space = local space
    # get bone transform in local space
    root_transform = skeleton_modifier.get_bone_transform(bone_names[index], False)
    # add the global translation of the target bone to the zero vec -> sets root translation to the pre offset global translation
    root_translation += skeleton_modifier.get_bone_transform(bone_names[index], True).translation #Global space
    
    # save 
    #root_transform.translation = new_root_translation
    
    # Debug logs: Meshname, RootBone, RootTransform before move, RootTransform after move
    unreal.log(asset.get_name())
    unreal.log(bone_names[index])
    unreal.log(root_transform)
    # affect bone transform by changing to new translation
    unreal.log(root_transform)
    root_transform.translation = new_root_translation
    # Move bone and children
    skeleton_modifier.set_bone_transform(bone_names[index] , root_transform , True)
    # get the new bone translation in global space
    new_root_translation = skeleton_modifier.get_bone_transform(bone_names[index], True).translation
    skeleton_modifier.commit_skeleton_to_skeletal_mesh()
    
    return new_root_translation , root_translation
