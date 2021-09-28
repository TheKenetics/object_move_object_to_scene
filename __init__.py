bl_info = {
	"name": "Move Object to Scene",
	"author": "Kenetics",
	"version": (0, 1),
	"blender": (2, 93, 0),
	"location": "View3D > Operator Search > Move to Scene",
	"description": "Allows to move objects between scenes like Move to Collection",
	"warning": "",
	"wiki_url": "",
	"category": "Object"
}

import bpy
from bpy.props import EnumProperty, IntProperty, FloatVectorProperty, BoolProperty, FloatProperty, StringProperty, PointerProperty
from bpy.types import PropertyGroup, UIList, Operator, Panel, AddonPreferences


## Operators
def get_enum_items_scenes(self, context):
	enum_list = []
	current_scene = context.scene
	
	for scene in bpy.data.scenes:
		if scene != current_scene:
			enum_list.append( (scene.name, scene.name, "") )
	
	return enum_list

class MOTS_OT_move_object_to_scene(Operator):
	"""Moves selected objects from this scene to another."""
	bl_idname = "mots.move_object_to_scene"
	bl_label = "Move Object to Scene"
	bl_options = {'REGISTER','UNDO'}
	
	scene_name : EnumProperty(items=get_enum_items_scenes, name="Scene")
	
	@classmethod
	def poll(cls, context):
		return context.selected_objects

	# Dialog invoke
	def invoke(self, context, event):
		return context.window_manager.invoke_props_dialog(self)

	def execute(self, context):
		selected_objects = context.selected_objects[:]
		
		# unlink objs from original collections
		for collection in bpy.data.collections:
			collection_objects = collection.objects[:]
			for obj in selected_objects:
				# prevents name collisions with linked libs
				if obj.name in collection.objects and obj in collection_objects:
					collection.objects.unlink(obj)
		
		# unlink from master collections
		for scene in bpy.data.scenes:
			scene_collection = scene.collection
			scene_collection_objects = scene.collection.objects[:]
			
			for obj in selected_objects:
				if obj.name in scene_collection.objects and obj in scene_collection_objects:
					scene_collection.objects.unlink(obj)
		
		# link to scene collection
		scene_collection_objects = bpy.data.scenes[self.scene_name].collection.objects
		for obj in selected_objects:
			scene_collection_objects.link(obj)
		
		return {'FINISHED'}


## Register
classes = (
	MOTS_OT_move_object_to_scene,
)

def register():
	for cls in classes:
		bpy.utils.register_class(cls)

def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)

if __name__ == "__main__":
	register()
