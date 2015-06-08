# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8-80 compliant>
import bpy
from bpy.app.handlers import persistent
import random

bl_info = {
    'name': 'Typewriter Text',
    'author': 'Bassam Kurdali, Vilem Novak, Jimmy Berry',
    'version': '0.3',
    'blender': (2, 7, 0),
    'location': 'Properties Editor, Text Context',
    'description': 'Typewriter Text effect',
    'url': 'http://urchn.org',
    'category': 'Text'}

__bpydoc__ = """
Typewriter Text Animation For Font Objects

"""

def randomize(t,width):
    nt=''
    lines=t.splitlines()
    totlen=len(t)
    i=0
    for l in lines:
        for ch in l:
            if i>totlen+1-width:
                nt+=random.choice(l)
            else:
                nt+=ch
            i+=1
        nt+='\n'
        i+=2
    return(nt)


def uptext(text):
    '''
    slice the source text up to the character_count
    '''
    source = text.source_text
    if source in bpy.data.texts:
        if text.separator!='':    strings=bpy.data.texts[source].as_string().split(text.separator)
        else:
            strings=[bpy.data.texts[source].as_string()]
        idx=min(len(strings),text.text_index)
        t=strings[idx]

        #remove line endings after separator
        while t.find('\n')==0:
            t=t[1:]
    else:
        t = source

    #randomize
    if text.use_randomize and len(t)>text.character_count:
        t=randomize(t[:text.character_count],text.randomize_width)

    prefix = ''
    if text.preserve_newline and text.character_start > 0:
        prefix = '\n' * t.count('\n', 0, text.character_start)

    text.body = prefix + t[text.character_start:text.character_count]

@persistent
def typewriter_text_update_frame(scene):
    '''
    sadly we need this for frame change updating
    '''
    for text in scene.objects:
        if text.type == 'FONT' and text.data.use_animated_text:
            uptext(text.data)


def update_func(self, context):
    '''
    updates when changing the value
    '''
    uptext(self)






class TEXT_PT_Typewriter(bpy.types.Panel):
    '''
    Typewriter Effect Panel
    '''
    bl_label = "Typewriter Effect"
    bl_idname = "TEXT_PT_Typewriter"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'

    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'FONT'

    def draw_header(self, context):
        text = context.active_object.data
        layout = self.layout
        layout.prop(text, 'use_animated_text', text="")

    def draw(self, context):
        st = context.space_data
        text = context.active_object.data
        layout = self.layout
        layout.prop(text,'character_start')
        layout.prop(text,'preserve_newline')
        layout.prop(text,'character_count')
        layout.prop(text,'source_text')
        if text.source_text in bpy.data.texts:
            layout.prop(text,'separator')
            layout.prop(text,'text_index')
        layout.prop(text,'use_randomize')
        if text.use_randomize:
            layout.prop(text,'randomize_width')

def register():
    '''
    addon registration function
    '''
    # create properties
    bpy.types.TextCurve.character_start = bpy.props.IntProperty(
      name="character_start",update=update_func, min=0, options={'ANIMATABLE'})
    bpy.types.TextCurve.preserve_newline = bpy.props.BoolProperty(
      name="preserve_newline", default=True)
    bpy.types.TextCurve.character_count = bpy.props.IntProperty(
      name="character_count",update=update_func, min=0, options={'ANIMATABLE'})
    bpy.types.TextCurve.backup_text = bpy.props.StringProperty(
      name="backup_text")
    bpy.types.TextCurve.use_animated_text = bpy.props.BoolProperty(
      name="use_animated_text", default=False)
    bpy.types.TextCurve.source_text = bpy.props.StringProperty(
      name="source_text")


    bpy.types.TextCurve.text_index = bpy.props.IntProperty(
      name="index",update=update_func, min=0, options={'ANIMATABLE'})
    bpy.types.TextCurve.separator = bpy.props.StringProperty(
      name="separator", default='#' )
    bpy.types.TextCurve.use_randomize = bpy.props.BoolProperty(
      name="randomize", default=False)
    bpy.types.TextCurve.randomize_width = bpy.props.IntProperty(
      name="randomize width",update=update_func, default=10, min=0, options={'ANIMATABLE'})
    # register the module:
    bpy.utils.register_module(__name__)
    # add the frame change handler
    bpy.app.handlers.frame_change_post.append(typewriter_text_update_frame)


def unregister():
    '''
    addon unregistration function
    '''
    # remove the frame change handler
    bpy.app.handlers.frame_change_post.remove(typewriter_text_update_frame)
    # remove the properties
    # XXX but how???
    # remove the panel
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
