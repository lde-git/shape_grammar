import math
import numpy as np
import pygame

class Shape:
    """Represents a single geometric entity with visual properties and a label."""
    def __init__(self, vertices, label="default", position=(0, 0), rotation=0.0, scale=1.0,
                 fill_color="gray", stroke_color="black", stroke_width=1):
        """
        Initializes a Shape object.

        Args:
            vertices (list of tuples): Local coordinates, e.g., [(0,0), (10,0), (10,10), (0,10)].
            label (str): Label for rule matching.
            position (tuple): Global (x, y) position.
            rotation (float): Global rotation angle in degrees.
            scale (float or tuple): Uniform or non-uniform scale factor.
            fill_color (str): Fill color (e.g., "red", "#FF0000").
            stroke_color (str): Stroke color.
            stroke_width (float): Stroke width.
        """
        self.local_vertices = np.array(vertices, dtype=float)
        self.label = label
        self.position = np.array(position, dtype=float)
        self.rotation_deg = rotation
        if isinstance(scale, (int, float)):
            self.scale = np.array([scale, scale], dtype=float)
        else:
            self.scale = np.array(scale, dtype=float)

        self.fill_color = fill_color
        self.stroke_color = stroke_color
        self.stroke_width = stroke_width
        self.is_selected = False # Flag for drawing engine to highlight it

    def get_transformed_vertices(self):
        """Calculates global vertex coordinates after scale, rotation, and translation."""
        # 1. Scale
        scaled_vertices = self.local_vertices * self.scale

        # 2. Rotate
        rotation_rad = math.radians(self.rotation_deg)
        cos_r = math.cos(rotation_rad)
        sin_r = math.sin(rotation_rad)
        
        rotated_vertices = np.zeros_like(scaled_vertices)
        for i, vertex in enumerate(scaled_vertices):
            x, y = vertex
            rotated_vertices[i, 0] = x * cos_r - y * sin_r
            rotated_vertices[i, 1] = x * sin_r + y * cos_r

        # 3. Translate
        global_vertices = rotated_vertices + self.position
        return global_vertices.tolist()

    def __repr__(self):
        return (f"Shape(label='{self.label}', position={self.position.tolist()}, "
                f"rotation={self.rotation_deg}, scale={self.scale.tolist()})")

    def draw_pygame(self, surface, camera_offset):
        """
        Draws the shape onto a pygame surface, adjusted by a camera offset.
        
        Args:
            surface (pygame.Surface): The surface to draw on.
            camera_offset (np.array): The [x, y] offset of the camera.
        """
        transformed_verts = self.get_transformed_vertices()
        
        # Adjust vertices by camera offset to get view coordinates
        view_verts = [(v[0] - camera_offset[0], v[1] - camera_offset[1]) for v in transformed_verts]
        
        # Pygame can't draw polygons with less than 3 vertices
        if len(view_verts) < 3:
            return

        # Draw the filled polygon
        pygame.draw.polygon(surface, self.fill_color, view_verts)
        
        # Draw the stroke/outline
        if self.stroke_width > 0:
            draw_width = int(math.ceil(self.stroke_width))
            pygame.draw.polygon(surface, self.stroke_color, view_verts, draw_width)
            
        # Optional: Highlight if selected
        if self.is_selected:
            pygame.draw.polygon(surface, "yellow", view_verts, 3)