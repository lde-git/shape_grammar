import pygame
import numpy as np
from shapes import Shape
from rules import ALL_RULES
from engine import Engine
from visualization import draw_shapes_to_svg

# --- Pygame Setup ---
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
BACKGROUND_COLOR = (20, 20, 30) # Dark blue-gray
FONT_COLOR = (230, 230, 230)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Shape Grammar Interpreter [Click and Drag to Pan]")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 16)

    # --- Camera and Panning Setup ---
    camera_offset = np.array([0.0, 0.0])
    is_panning = False
    pan_start_pos = (0, 0)

    # --- Initial Shape Grammar Setup ---
    square_vertices = [(0, 0), (100, 0), (100, 100), (0, 100)]
    initial_shape = Shape(
        vertices=square_vertices,
        label="fractal_square",
        position=(WINDOW_WIDTH/2 - 50, WINDOW_HEIGHT - 150),
        scale=1.5,
        fill_color="#6B4423"
    )
    grammar_engine = Engine(initial_shapes=[initial_shape], rules=ALL_RULES)

    # --- Main Loop ---
    running = True
    auto_generate = False
    
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # --- Panning Controls ---
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    is_panning = True
                    pan_start_pos = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    is_panning = False
            elif event.type == pygame.MOUSEMOTION:
                if is_panning:
                    dx = event.pos[0] - pan_start_pos[0]
                    dy = event.pos[1] - pan_start_pos[1]
                    camera_offset[0] -= dx
                    camera_offset[1] -= dy
                    pan_start_pos = event.pos

            # --- Generation Controls ---
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    grammar_engine.apply_rules_step()
                elif event.key == pygame.K_a:
                    auto_generate = not auto_generate
                elif event.key == pygame.K_ESCAPE:
                    running = False
        
        if auto_generate:
            if not grammar_engine.apply_rules_step():
                auto_generate = False

        # Drawing
        screen.fill(BACKGROUND_COLOR)
        
        # Draw all shapes with camera offset
        for shape in grammar_engine.shapes:
            shape.draw_pygame(screen, camera_offset)
            
        # Draw UI Text
        auto_mode_text = "ON" if auto_generate else "OFF"
        info_text = (
            f"Step: {grammar_engine.generation_step} | "
            f"Shapes: {len(grammar_engine.shapes)} | "
            f"SPACE: Step | A: Auto ({auto_mode_text}) | Drag to Pan"
        )
        text_surface = font.render(info_text, True, FONT_COLOR)
        screen.blit(text_surface, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    # Teardown
    print("\nExiting and saving final state to SVG...")
    # Note: SVG output is not affected by the camera, it saves the raw coordinates.
    draw_shapes_to_svg(grammar_engine.shapes, "fractal_tree.svg", size=(f"{WINDOW_WIDTH}px", f"{WINDOW_HEIGHT}px"))
    pygame.quit()


if __name__ == "__main__":
    main()