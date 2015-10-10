'''
Copyright (C) 2015 YOUR NAME
YOUR@MAIL.com

Created by YOUR NAME

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {
    "name": "Blender Shader Library",
    "description": "Create your own shader library with thumbnail",
    "author": "Lapineige, Pitiwazou, Pistiwique",
    "version": (0, 0, 1),
    "blender": (2, 74, 0),
    "location": "3D View",
    "warning": "This addon is still in development.",
    "wiki_url": "",
    "category": "Material" }
    
    
import bpy      


# load and reload submodules
##################################    
    
from . import developer_utils
modules = developer_utils.setup_addon_modules(__path__, __name__)



# register
################################## 

import traceback
from . draw import register_pcoll_preview, unregister_pcoll_preview, BSL_AddMaterial                                    
    
def register():
    try: bpy.utils.register_module(__name__)
    except: traceback.print_exc()
    bpy.types.Cycles_PT_context_material.append(BSL_AddMaterial)
    register_pcoll_preview()
    print("Registered {} with {} modules".format(bl_info["name"], len(modules)))

def unregister():
    unregister_pcoll_preview()
    try: bpy.utils.unregister_module(__name__)
    except: traceback.print_exc()
    bpy.types.Cycles_PT_context_material.remove(BSL_AddMaterial)
    
    print("Unregistered {}".format(bl_info["name"]))
