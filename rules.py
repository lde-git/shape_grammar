from shapes import Shape
import numpy as np
import math

def rule_fractal_tree_branch(shape):
    """
    A recursive rule that replaces a square with two smaller, rotated squares
    to create a fractal tree pattern.
    """
    # Rule Condition: Only apply to shapes with the label 'fractal_square'
    if shape.label != 'fractal_square':
        return []

    # --- 1. Get parent's properties ---
    parent_pos = shape.position
    parent_scale = shape.scale
    parent_rotation = shape.rotation_deg

    # --- 2. Define properties for the new child squares ---
    # The new squares are smaller. A factor of 0.7 works well.
    child_scale_factor = 0.7
    new_scale = parent_scale * child_scale_factor

    # The new squares will be rotated relative to the parent
    rotation_angle = 35 # degrees

    # --- 3. Calculate the attachment point for the new branches ---
    # We'll attach the new squares to the middle of the parent's "top" edge.
    # Assuming the local vertices are a 100x100 square: [(0,0), (100,0), (100,100), (0,100)]
    # The local top-middle point is (50, 100).
    local_anchor_point = np.array([50.0, 100.0])

    # Now, transform this local anchor point into the global coordinate space
    # by applying the parent's scale and rotation.
    
    # a. Scale the anchor point
    scaled_anchor = local_anchor_point * parent_scale
    
    # b. Rotate the scaled anchor point
    rad = math.radians(parent_rotation)
    cos_r, sin_r = math.cos(rad), math.sin(rad)
    
    rotated_anchor = np.array([
        scaled_anchor[0] * cos_r - scaled_anchor[1] * sin_r,
        scaled_anchor[0] * sin_r + scaled_anchor[1] * cos_r,
    ])

    # c. The global position for the new shapes is the parent's position + the transformed anchor
    # This is where the base of the two new squares will be.
    global_attachment_pos = parent_pos + rotated_anchor

    # --- 4. Create the two new shapes (branches) ---
    
    # Left Branch
    left_branch = Shape(
        vertices=shape.local_vertices,
        label="fractal_square", # Recursive: This shape can also be branched
        position=global_attachment_pos,
        rotation=parent_rotation + rotation_angle, # Rotate left
        scale=new_scale,
        fill_color="#FFB6C1", # LightPink
        stroke_width=0.5
    )

    # Right Branch
    right_branch = Shape(
        vertices=shape.local_vertices,
        label="fractal_square", # Recursive
        position=global_attachment_pos,
        rotation=parent_rotation - rotation_angle, # Rotate right
        scale=new_scale,
        fill_color="#ADD8E6", # LightBlue
        stroke_width=0.5
    )
    
    # This rule replaces the parent shape with the two new branches.
    return [left_branch, right_branch]

# A list of all rules the engine can use.
# We replace the old rule with our new fractal one.
ALL_RULES = [
    rule_fractal_tree_branch,
]
