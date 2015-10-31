# -*- coding: utf-8 -*-

import bpy
import os
import subprocess
import bpy.utils.previews
from os import listdir
from os.path import join
from . import_utils import import_materials_from_files
from bpy.types import Panel, Operator
from bpy.types import WindowManager
from bpy.props import EnumProperty

preview_collections = {}


#### !!!!!!! 

# Ne garder QUE la partie affichage dans draw

#### !!!!!!!

        ####################################
        ####    THUMBNAILS FONCTIONS    ####
        ####################################
        

class UpdateThumbnails(Operator): # à mettre dans import_utils ? - en changeant le nom 
    bl_idname = "material.update_thumbnails"
    bl_label = "Update Thumbnails"
    bl_description = "(Re)generate thumbnails images. May take a while"
    bl_options = {"REGISTER", "INTERNAL"}

    def execute(self, context):
        
        register_pcoll_preview()

        self.report({'INFO'}, 'Thumbnails and preview updated') # marche que si appel depuis l'UI

        return {"FINISHED"}

def update_preview_type(self, context):
    register_pcoll_preview()


def get_enum_previews(self, context): # self et context demandés par l'API
    """ """
    return enum_previews_from_directory_items(context.window_manager.is_generating_preview)

def enum_previews_from_directory_items(is_generating_preview):
    """ N'utilise pas self et context, pour un appel externe au preset de Blender """
    enum_items = []

    if bpy.context is None:
        return enum_items

    wm = bpy.context.window_manager

    if wm.preview_type == '1':
        thumbnail_type= "Sphere"
    elif wm.preview_type == '2':
        thumbnail_type= "Cloth"
    elif wm.preview_type == '3':
        thumbnail_type= "Softbox"
        
    directory = join(os.path.dirname(__file__), "Thumbnails",thumbnail_type )

    # Get the preview collection (defined in register func).
    pcoll = preview_collections["main"]

    if is_generating_preview or directory == pcoll.my_previews_dir:
        return pcoll.my_previews

    print("[BML] Scanning thumbnails directory: %s" % directory)

    if directory and os.path.exists(directory):
        # Scan the directory for jpg files
        image_paths = []
        for fn in os.listdir(directory):
            if fn.lower().endswith(".jpg") or fn.lower().endswith(".jpeg") or fn.lower().endswith(".png"):
                image_paths.append(fn)

        for i, name in enumerate(image_paths):
            # generates a thumbnail preview for a file.
            filepath = os.path.join(directory, name)
            thumb = pcoll.load(filepath, filepath, 'IMAGE')
            enum_items.append((name, name, name, thumb.icon_id, i)) # 3 bpy.utils.resource_path('USER') + "scripts/addons/material_lib

    pcoll.my_previews = enum_items ## Pourquoi cette ligne + return ?
    
    # print('[BML] - Thumbnails list:', enum_items)
    print('[BML] - Thumbnails list:', [item[0] for item in enum_items], 'Length:', len(enum_items))
    pcoll.my_previews_dir = directory

    return pcoll.my_previews


        ######################
        ####    PANELS    ####
        ######################


###### 3DVIEW ######     
class VIEW3D_PT_view_3d_bml(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Blender Material Library"


    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        # layout.operator("material.delete_unused_materials",text="Remove", icon='CANCEL')
        # layout.prop(wm, "preview_type", text="")
        if bpy.context.selected_objects:
            layout.prop(wm, "preview_type")
            layout.template_icon_view(wm, "my_previews")
            layout.operator("object.select_linked", icon='RESTRICT_SELECT_OFF').type='MATERIAL'
        else:
            layout.label("No mesh selected", icon='ERROR')

        


class VIEW3D_PT_tools_bml(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "BML"
    bl_label = "Blender Material Library"


    def draw(self, context):
        layout = self.layout
        wm = context.window_manager


        if bpy.context.selected_objects:
            layout.prop(wm, "preview_type")        
            layout.template_icon_view(wm, "my_previews")
            layout.operator("object.select_linked", icon='RESTRICT_SELECT_OFF').type='MATERIAL' 
        else:
            layout.label("No mesh selected", icon='ERROR')





class view3d_header_preview_bml(bpy.types.Menu):
    bl_idname = "material.view3d_header_preview"
    bl_label = "BML preview"
    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        if bpy.context.selected_objects:
            layout.template_icon_view(wm, "my_previews")
        else:
            layout.label("No mesh selected", icon='ERROR')

def VIEW3D_HT_header_bml_preview(self, context):
    layout = self.layout
    layout.menu("material.view3d_header_preview", text=" BML", icon='MATERIAL')



###### NODE EDITOR ######  
class NODE_PT_tools_bml(Panel):
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'TOOLS'
    bl_category = "BML"
    bl_label = "Blender Material Library"

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        object = bpy.context.active_object.name
        row = layout.row(align=True)
        if bpy.data.objects[object].active_material:
            row.menu("material.import_into_bml_container")# , icon='APPEND_BLEND') # icone à changer
            row.operator("material.import_into_bml_container", text="Add", icon='APPEND_BLEND')
            row.operator("object.material_slot_remove",text="Remove", icon='X')
            row.operator("material.update_thumbnails", text="", icon='FILE_REFRESH')
        if bpy.context.selected_objects:
            layout.prop(wm, "preview_type")         
            layout.template_icon_view(wm, "my_previews")
        else:
            layout.label("No mesh selected", icon='ERROR')
        # row.operator("material.import_into_bml", text="Add", icon='APPEND_BLEND')
        layout.operator("material.delete_unused_materials", icon='X')



class NODE_PT_ui_bml(Panel):
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_label = "Blender Material Library"

    def draw(self, context):

        layout = self.layout

        wm = context.window_manager
        object = bpy.context.active_object.name
        row = layout.row(align=True)
        if bpy.data.objects[object].active_material:
            row.prop(wm, "preview_type", text="")# , icon='APPEND_BLEND') # icone à changer
            row.operator("material.import_into_bml_container", text="Add", icon='APPEND_BLEND')
            row.operator("object.material_slot_remove",text="Remove", icon='X')
            row.operator("material.update_thumbnails", text="", icon='FILE_REFRESH')
        if bpy.context.selected_objects:

            layout.template_icon_view(wm, "my_previews")
        else:
            layout.label("No mesh selected", icon='ERROR')
        # row.operator("material.import_into_bml", text="Add", icon='APPEND_BLEND')
        layout.operator("material.delete_unused_materials",text="Delete unused materials", icon='X')


class node_header_preview_bml(bpy.types.Menu):
    bl_idname = "material.node_header_preview"
    bl_label = "BML preview"

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        if bpy.context.selected_objects:
            layout.template_icon_view(wm, "my_previews")
        else:
            layout.label("No mesh selected", icon='ERROR')

def NODE_HT_header_bml_preview(self, context):
    
    layout = self.layout
    wm = context.window_manager
    
    if bpy.context.selected_objects:            
        layout.menu("material.node_header_preview", text=" BML", icon='MATERIAL')
        layout.prop(wm, "preview_type", text="Preview type ")  
    else:
        layout.label("No mesh selected", icon='ERROR')


###### CLASS ######

class Cycles_PT_bml_panel(Panel):
    '''Blender Material Library preview'''
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'

    bl_label = "Blender Material Library"

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        row = layout.row(align=True)
        object = bpy.context.active_object.name
        if bpy.data.objects[object].active_material:
            #row.prop(wm, "preview_type", text="")# , icon='APPEND_BLEND') # icone à changer
            row.operator("material.import_into_bml_container", text="Add", icon='APPEND_BLEND')
            row.operator("material.remove_material_from_bml", text="Remove", icon='X')
            row.operator("material.update_thumbnails", text="", icon='FILE_REFRESH')
            
        if bpy.context.selected_objects:
            layout.prop(wm, "preview_type", text="Preview type")         
            layout.template_icon_view(wm, "my_previews")
            layout.operator("material.delete_unused_materials",text="Delete unused materials")
            layout.operator("object.select_linked", icon='RESTRICT_SELECT_OFF').type='MATERIAL' 
        else:
            layout.label("No mesh selected", icon='ERROR')
               


def register_pcoll_preview():
    wm = bpy.context.window_manager

    global preview_collections
    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
        
    WindowManager.my_previews = EnumProperty( # Nom à changer - pas clair, trop de preview dans les noms
            items=get_enum_previews,
            update=import_materials_from_files)
    
    pcoll = bpy.utils.previews.new() # pcoll pour preview collection
    pcoll.my_previews_dir = ""
    pcoll.my_previews = ()
    
    preview_collections = {}
    preview_collections["main"] = pcoll

def unregister_pcoll_preview():

    del WindowManager.my_previews

    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()