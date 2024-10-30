bl_info = {
    "name": "Sprite Sheet 3D Asset Separator",
    "author": "Your Name",
    "version": (2, 2),
    "blender": (4, 1, 0),  # Updated for Blender 4.1
    "location": "View3D > Sidebar > Sprite Sheet",
    "description": "Separate 3D sprite sheet assets and prepare them as individual assets",
    "category": "Object",
}

import bpy
import math
from bpy.props import StringProperty, FloatProperty, PointerProperty
from mathutils import Vector

# Property Group for storing properties
class SpriteSheetProperties(bpy.types.PropertyGroup):
    angle_limit_degrees: FloatProperty(
        name="Angle Limit",
        description="Maximum angle between face normals (in degrees)",
        default=33.0,  # Updated default angle to 33 degrees
        min=0.0,
        max=180.0,
        subtype='ANGLE'
    )

    merge_threshold: FloatProperty(
        name="Merge Threshold",
        description="Distance threshold for merging vertices",
        default=0.0001,
        min=0.0,
        precision=6
    )

# Operator to import GLB file
class ImportGLBOperator(bpy.types.Operator):
    """Import GLB File"""
    bl_idname = "import_scene.glb_custom"
    bl_label = "Import GLB File"

    filepath: StringProperty(subtype="FILE_PATH")

    filter_glob: StringProperty(
        default="*.glb;*.gltf",
        options={'HIDDEN'},
    )

    def execute(self, context):
        bpy.ops.import_scene.gltf(filepath=self.filepath)
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

# Operator to merge vertices by distance
class MergeByDistanceOperator(bpy.types.Operator):
    """Merge Vertices by Distance"""
    bl_idname = "object.merge_by_distance"
    bl_label = "Merge Vertices by Distance"

    def execute(self, context):
        objects = context.selected_objects
        threshold = context.scene.sprite_sheet_props.merge_threshold

        for obj in objects:
            if obj.type == 'MESH':
                context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                # Use remove_doubles operator
                bpy.ops.mesh.remove_doubles(threshold=threshold)
                bpy.ops.object.mode_set(mode='OBJECT')
        return {'FINISHED'}

# Operator to separate by loose parts
class SeparateByLoosePartsOperator(bpy.types.Operator):
    """Separate by Loose Parts"""
    bl_idname = "object.separate_loose_parts"
    bl_label = "Separate by Loose Parts"

    def execute(self, context):
        selected_objects = context.selected_objects

        for obj in selected_objects:
            if obj.type == 'MESH':
                context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.separate(type='LOOSE')
                bpy.ops.object.mode_set(mode='OBJECT')
        return {'FINISHED'}

# Operator to set origin to center of mass
class SetOriginCenterOfMassOperator(bpy.types.Operator):
    """Set Origin to Center of Mass"""
    bl_idname = "object.set_origin_center_of_mass"
    bl_label = "Set Origin to Center of Mass"

    def execute(self, context):
        objects = context.selected_objects

        for obj in objects:
            if obj.type == 'MESH':
                context.view_layer.objects.active = obj
                bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
        return {'FINISHED'}

# Operator to set origin to base of object
class SetOriginToBaseOperator(bpy.types.Operator):
    """Set Origin to Base of Object"""
    bl_idname = "object.set_origin_to_base"
    bl_label = "Set Origin to Base"

    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                # Deselect all
                bpy.ops.object.select_all(action='DESELECT')
                obj.select_set(True)
                # Calculate the lowest Z point of the bounding box
                local_bbox = [Vector(corner) for corner in obj.bound_box]
                min_z = min([v.z for v in local_bbox])

                # Transform to world coordinates
                world_matrix = obj.matrix_world
                min_world = world_matrix @ Vector((0, 0, min_z))

                # Set cursor to lowest point
                bpy.context.scene.cursor.location = min_world

                # Set origin to cursor
                bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

        return {'FINISHED'}

# Operator to apply decimate modifier
class DecimateOperator(bpy.types.Operator):
    """Apply Decimate Modifier to Selected Objects"""
    bl_idname = "object.apply_decimate"
    bl_label = "Apply Decimate Modifier"

    def execute(self, context):
        angle_limit_degrees = context.scene.sprite_sheet_props.angle_limit_degrees
        angle_limit_radians = math.radians(angle_limit_degrees)
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                decimate_modifier = obj.modifiers.new(name='Decimate', type='DECIMATE')
                decimate_modifier.decimate_type = 'DISSOLVE'
                decimate_modifier.delimit = {'UV'}  # Preserve UV seams
                decimate_modifier.angle_limit = angle_limit_radians
                # Apply the modifier
                context.view_layer.objects.active = obj
                bpy.ops.object.modifier_apply(modifier=decimate_modifier.name)
        return {'FINISHED'}

# Operator to mark objects as assets and generate previews
class MarkAsAssetOperator(bpy.types.Operator):
    """Mark Objects as Assets and Generate Previews"""
    bl_idname = "object.mark_as_asset"
    bl_label = "Mark as Asset and Generate Preview"

    def execute(self, context):
        for obj in context.selected_objects:
            obj.asset_mark()
            obj.asset_generate_preview()
        return {'FINISHED'}

# Operator to perform all steps automatically
class DoAllOperator(bpy.types.Operator):
    """Do All Steps Automatically"""
    bl_idname = "object.do_all_steps"
    bl_label = "Do All Steps"

    def execute(self, context):
        # Assuming the imported object is selected
        selected_objects = context.selected_objects
        threshold = context.scene.sprite_sheet_props.merge_threshold

        # Merge by distance
        for obj in selected_objects:
            if obj.type == 'MESH':
                context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.remove_doubles(threshold=threshold)
                bpy.ops.object.mode_set(mode='OBJECT')

        # Separate by loose parts
        for obj in selected_objects:
            if obj.type == 'MESH':
                context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.separate(type='LOOSE')
                bpy.ops.object.mode_set(mode='OBJECT')

        # Deselect all and select new objects
        bpy.ops.object.select_all(action='DESELECT')
        for obj in context.scene.objects:
            if obj.type == 'MESH':
                obj.select_set(True)

        # Decimate
        angle_limit_degrees = context.scene.sprite_sheet_props.angle_limit_degrees
        angle_limit_radians = math.radians(angle_limit_degrees)
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                decimate_modifier = obj.modifiers.new(name='Decimate', type='DECIMATE')
                decimate_modifier.decimate_type = 'DISSOLVE'
                decimate_modifier.delimit = {'UV'}  # Preserve UV seams
                decimate_modifier.angle_limit = angle_limit_radians
                # Apply the modifier
                context.view_layer.objects.active = obj
                bpy.ops.object.modifier_apply(modifier=decimate_modifier.name)

        # Set origin
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                context.view_layer.objects.active = obj
                bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')

        # Mark as assets and generate previews
        for obj in context.selected_objects:
            obj.asset_mark()
            obj.asset_generate_preview()

        return {'FINISHED'}

# UI Panel
class OBJECT_PT_SpriteSheetSeparatorPanel(bpy.types.Panel):
    """Creates a Panel in the 3D Viewport Sidebar"""
    bl_label = "Sprite Sheet 3D Asset Separator"
    bl_idname = "OBJECT_PT_sprite_sheet_separator"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Sprite Sheet'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.sprite_sheet_props

        # Import Section
        layout.label(text="Import")
        layout.operator("import_scene.glb_custom", text="Import GLB File")

        layout.separator()

        # Preprocessing Section
        layout.label(text="Preprocessing")
        layout.prop(props, "merge_threshold")
        layout.operator("object.merge_by_distance", text="Merge Vertices by Distance")
        layout.operator("object.separate_loose_parts", text="Separate by Loose Parts")

        layout.separator()

        # Decimation Section
        layout.label(text="Decimation")
        layout.prop(props, "angle_limit_degrees")
        layout.operator("object.apply_decimate", text="Apply Decimate Modifier")

        layout.separator()

        # Set Origin Section
        layout.label(text="Set Origin")
        layout.operator("object.set_origin_center_of_mass", text="Set Origin to Center of Mass")
        layout.operator("object.set_origin_to_base", text="Set Origin to Base")

        layout.separator()

        # Asset Management Section
        layout.label(text="Asset Management")
        layout.operator("object.mark_as_asset", text="Mark as Asset and Generate Preview")

        layout.separator()

        # Automation Section
        layout.label(text="Automation")
        layout.operator("object.do_all_steps", text="Do All Steps Automatically")

# Registration
classes = (
    SpriteSheetProperties,
    ImportGLBOperator,
    MergeByDistanceOperator,
    SeparateByLoosePartsOperator,
    SetOriginCenterOfMassOperator,
    SetOriginToBaseOperator,
    DecimateOperator,
    MarkAsAssetOperator,
    DoAllOperator,
    OBJECT_PT_SpriteSheetSeparatorPanel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.sprite_sheet_props = PointerProperty(type=SpriteSheetProperties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.sprite_sheet_props

if __name__ == "__main__":
    register()
