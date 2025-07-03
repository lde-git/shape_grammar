class Engine:
    """Manages the generation process by applying rules to shapes."""
    def __init__(self, initial_shapes, rules):
        """
        Initializes the engine.
        
        Args:
            initial_shapes (list): A list of Shape objects to start with.
            rules (list): A list of rule functions to use.
        """
        self.shapes = list(initial_shapes)
        self.rules = rules
        self.generation_step = 0

    def apply_rules_step(self):
        """
        Performs one step of the generation.
        Finds the first shape that can be modified by a rule and applies it.
        """
        print(f"\n--- Generation Step {self.generation_step} ---")
        
        # Find a shape to apply a rule to. For simplicity, we find the first
        # one that matches any rule.
        for i, shape in enumerate(self.shapes):
            shape.is_selected = False # Clear previous selections
            
            for rule in self.rules:
                # Try to apply the rule
                new_shapes = rule(shape)
                
                # If the rule produced new shapes (i.e., it was applicable)
                if new_shapes:
                    print(f"Applying rule '{rule.__name__}' to shape: {shape}")
                    
                    # Remove the original shape
                    original_shape = self.shapes.pop(i)
                    
                    # Add the new shapes
                    self.shapes.extend(new_shapes)
                    
                    print(f"  -> Replaced with {len(new_shapes)} new shapes.")
                    
                    self.generation_step += 1
                    # Exit after applying one rule for this step
                    return True 
        
        print("No applicable rules found in this step.")
        return False # No rules were applied