import unreal

def RenameAndFixSkeleton(source_mesh, asset):

    ####
    #   source_mesh - Source skeletal mesh to which the asset is aligned to 
    #   asset - Skeletal Mesh whose skeleton is changed
    ####
    
    # Loading Libs
    # load the weight modifier
    weight_modifier = unreal.SkinWeightModifier()
    # load the skeleton modifier
    skeleton_modifier = unreal.SkeletonModifier()
    # Set the source mesh path
    source_skeletal_mesh_path = unreal.EditorAssetLibrary.get_path_name_for_loaded_asset(source_mesh)

    # Get the path for target skeletal mesh
    skeletal_mesh_path = unreal.EditorAssetLibrary.get_path_name_for_loaded_asset(asset)
    source_skeletal_mesh = unreal.EditorAssetLibrary.load_asset(source_skeletal_mesh_path)
    skeleton_modifier.set_skeletal_mesh(source_skeletal_mesh)
    source_bones_array = skeleton_modifier.get_all_bone_names()

    # Hard coded saves for ik bones and jaw bone
    jaw_transform = skeleton_modifier.get_bone_transform("jaw")
    # IK bones
    ik_foot_root_transform = skeleton_modifier.get_bone_transform("ik_foot_root")
    ik_foot_l_transform = skeleton_modifier.get_bone_transform("ik_foot_l")
    ik_foot_r_transform = skeleton_modifier.get_bone_transform("ik_foot_r")
    ik_hand_root_transform = skeleton_modifier.get_bone_transform("ik_hand_root")
    ik_hand_gun_transform = skeleton_modifier.get_bone_transform("ik_hand_gun")
    ik_hand_l_transform = skeleton_modifier.get_bone_transform("ik_hand_l")
    ik_hand_r_transform = skeleton_modifier.get_bone_transform("ik_hand_r")

    skeleton_modifier.commit_skeleton_to_skeletal_mesh()
    missing_bones = []
    # Load the skeletal mesh asset
    skeletal_mesh = unreal.EditorAssetLibrary.load_asset(skeletal_mesh_path)
    # Get the array of Bone structures of the skeletal mesh to be changed
    skeleton_modifier.set_skeletal_mesh(skeletal_mesh)
    bones_array = skeleton_modifier.get_all_bone_names()
    # Iterate over the bones and rename to default pattern
    for bone in bones_array:
        #Fixing various missspellings of bones
        if bone == "Thight_L":
            skeleton_modifier.rename_bone("Thight_L", "Thigh_L")
        if bone == "Thight_R":
            skeleton_modifier.rename_bone("Thight_R", "Thigh_R")
        if bone == "_ik_foot_root":
            # If the root is wrongly named, so are its children
            skeleton_modifier.rename_bone("_ik_foot_root", "ik_foot_root")
            skeleton_modifier.rename_bone("_ik_foot_l", "ik_foot_l")
            skeleton_modifier.rename_bone("_ik_foot_r", "ik_foot_r")
        if bone == "_ik_hand_root":
            # If the root is wrongly named, so are its children
            skeleton_modifier.rename_bone("_ik_hand_root", "ik_hand_root")
            skeleton_modifier.rename_bone("_ik_hand_gun", "ik_hand_gun")
            skeleton_modifier.rename_bone("_ik_hand_l", "ik_hand_l")
            skeleton_modifier.rename_bone("_ik_hand_r", "ik_hand_r")
    for bone in source_bones_array:
        if bone not in bones_array:
            print(bone) # For debug purposes
            missing_bones.append(bone)
            
    # Iterate over the bones and add them at the correct locations (hard coded for now)
    for bone in missing_bones:
        if bone == "ik_foot_root":
            # If the foot root is missing all ik_foot bones are missing -> add them all in order
            skeleton_modifier.add_bone("ik_foot_root", "root", ik_foot_root_transform)
            skeleton_modifier.add_bone("ik_foot_l", "ik_foot_root", ik_foot_l_transform)
            skeleton_modifier.add_bone("ik_foot_r", "ik_foot_root", ik_foot_r_transform)
        elif bone == "ik_hand_root":
            # If the hand root is missing all ik_hand bones are missing -> add them all in order
            skeleton_modifier.add_bone("ik_hand_root", "root", ik_hand_root_transform)
            skeleton_modifier.add_bone("ik_hand_gun", "ik_hand_root", ik_hand_gun_transform)
            skeleton_modifier.add_bone("ik_hand_l", "ik_hand_gun", ik_hand_l_transform)
            skeleton_modifier.add_bone("ik_hand_r", "ik_hand_gun", ik_hand_r_transform)
        elif bone == "jaw":
            # If the jaw is missing, just add it
            skeleton_modifier.add_bone("jaw", "head", jaw_transform)
        else:
            print(bone)
        
    # Complete the bone operations, commit changes to skeletal mesh
    mesh_name = skeletal_mesh.get_name()
    skeleton_modifier.commit_skeleton_to_skeletal_mesh()
    msg_string = "Missing Bones added to Skeletal Mesh " + mesh_name
    unreal.log(msg_string)

    unreal.log("Skeleton renamer completed for " + asset)
    return
