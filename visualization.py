import svgwrite

def draw_shapes_to_svg(shapes, filename, size=("800px", "600px")):
    """Saves a list of shapes to an SVG file."""
    dwg = svgwrite.Drawing(filename, profile='tiny', size=size)
    
    for shape in shapes:
        transformed_verts = shape.get_transformed_vertices()
        
        if len(transformed_verts) >= 3:
            dwg.add(dwg.polygon(
                points=transformed_verts,
                fill=shape.fill_color,
                stroke=shape.stroke_color,
                stroke_width=shape.stroke_width
            ))
            
    dwg.save()
    print(f"Successfully saved {len(shapes)} shapes to {filename}")