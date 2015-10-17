import bpy
import sys
import os
from os.path import join
from os import remove


if __name__ == '__main__':
    material = sys.argv[5] # recupere le nom du materiau
    #thumbnails_directory = sys.argv[6] # recupere le dossier de stockage des miniatures
    
    bpy.data.objects["_Render_Model"].active_material = bpy.data.materials[material]
    
    bpy.data.materials[material].use_fake_user = False
    bpy.data.materials[material].user_clear()
    
    bpy.ops.wm.save_mainfile()
    bpy.ops.wm.quit_blender()