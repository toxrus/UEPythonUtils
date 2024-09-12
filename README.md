#Unreal Engine Python Scripts

UESkeletonRenamer
Currently only adds missing IK Bones as well as Jaw Bone for Synty Skeletal Meshes. Renames Bones with _ik to ik. To be used in conjungtion with SkeletonFix Asset Action Util (https://blueprintue.com/blueprint/gvwkv37g/ , See also comment for info on how to setup the Asset Action Util BP) 

CorrectBoneOffSet
Corrects root bone position to to able to socket to correct bone for synty meshes - cyberpunk tail, modular fantasy heroes cape

UESkeletonRenamer_Legacy
Python script for Unreal Engine 5. Renames the skeleton of skeletal meshes to match a unified Synty Skeleton.
Currently only adds missing IK Bones as well as Jaw Bone. Renames _ik to ik and removes all bones not matching source in the end, if bRemoveBones = true.
USAGE AT OWN RISK. MAKE A BACKUP!
