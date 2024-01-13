import unreal

# Loading Libs
# load the weight modifier
weight_modifier = unreal.SkinWeightModifier()
# load the skeleton modifier
skeleton_modifier = unreal.SkeletonModifier()

unreal.log("Hello from AddBones!")
EUL = unreal.EditorUtilityLibrary
# Get the selected Assets in the unreal engine content browser
selected_assets = EUL.get_selected_assets()
# Filter for skeletal meshes
skeletal_mesh_assets = [asset for asset in selected_assets if (asset and type(asset) == unreal.SkeletalMesh)]
# Get the paths for each selected skeletal mesh and return them
skeletal_mesh_paths = [unreal.EditorAssetLibrary.get_path_name_for_loaded_asset(skeletal_mesh_asset) for skeletal_mesh_asset in skeletal_mesh_assets]
# Hard reference to MC Pauls synty mannequin
source_skeletal_mesh_path = "/Game/Assets/Characters/Humanoids/SyntyBaseRTG/MCSynPoly/Meshes/SK_MCSynPoly.SK_MCSynPoly"
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




for skeletal_mesh_path in skeletal_mesh_paths:
    missing_bones = []
    # Load the skeletal mesh asset
    skeletal_mesh = unreal.EditorAssetLibrary.load_asset(skeletal_mesh_path)
    # Get the skeleton associated with the skeletal mesh
    #skeleton = skeletal_mesh.get_editor_property("skeleton")
    #print(skeleton)
    # Get the array of Bone structures
    skeleton_modifier.set_skeletal_mesh(skeletal_mesh)
    bones_array = skeleton_modifier.get_all_bone_names()
    for bone in source_bones_array:
        if bone not in bones_array:
            #print(bone) # For debug purposes
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

unreal.log("Actions in AddBones completed!")