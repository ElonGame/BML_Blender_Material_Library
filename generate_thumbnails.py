# -*- coding: utf-8 -*-

import bpy
import sys
import os
from os.path import join

if __name__ == '__main__':
    material = sys.argv[5] # récupére le nom du matériau
    thumbnails_directory = sys.argv[6] # récupére le dossier de stockage des miniatures
    render_type = sys.argv[7]

    if not material in [line.body for line in bpy.data.texts["BML_material_list"].lines]: #### Peut être mieux de rajouter une option lors de l'import, plus pratique ensutie avec les tags, plus sùr
        bpy.data.texts["BML_material_list"].lines[-1].body = material + ';' + render_type[1:] + '\n'

    if render_type == '_Sphere':
        bpy.context.scene.layers[0] = True
        bpy.context.scene.layers[1] = True
        bpy.context.scene.layers[2] = False
        bpy.context.scene.layers[3] = False
        bpy.context.scene.layers[4] = False
    elif render_type == '_Cloth':
        bpy.context.scene.layers[0] = True
        bpy.context.scene.layers[1] = False
        bpy.context.scene.layers[2] = True
        bpy.context.scene.layers[3] = False
        bpy.context.scene.layers[4] = False
    elif render_type == '_Softbox':
        bpy.context.scene.layers[0] = True
        bpy.context.scene.layers[1] = False
        bpy.context.scene.layers[2] = False
        bpy.context.scene.layers[3] = True
        bpy.context.scene.layers[4] = False
    elif render_type == '_Hair':
        bpy.context.scene.layers[0] = True
        bpy.context.scene.layers[1] = False
        bpy.context.scene.layers[2] = False
        bpy.context.scene.layers[3] = False
        bpy.context.scene.layers[4] = True

    bpy.data.objects[render_type].active_material = bpy.data.materials[material]

    bpy.ops.object.select_all(action='DESELECT')
    # Selection du texte
    bpy.data.objects["Text"].select = True
    # Le mettre en Actif
    bpy.context.scene.objects.active = bpy.data.objects["Text"]

    bpy.ops.object.mode_set(mode='EDIT')

    # suppression des lettres
    for item in bpy.context.object.data.body:
        bpy.ops.font.delete()

    # insert le nom du matériau de l'objet à rendre
    bpy.ops.font.text_insert(text=material)

    bpy.ops.object.mode_set(mode='OBJECT')

    bpy.ops.object.select_all(action='DESELECT')
    # Selection de l'objet à rendre
    bpy.data.objects[render_type].select = True
    # passage de _render_Model en objet actif
    bpy.context.scene.objects.active = bpy.data.objects[render_type]

    bpy.ops.render.render()

    bpy.data.images['Render Result'].save_render(filepath=join(thumbnails_directory, material + '.jpeg'))

    print("[BML] - Preview Created:", join(thumbnails_directory, material + '.jpeg'))

    bpy.ops.wm.quit_blender()
