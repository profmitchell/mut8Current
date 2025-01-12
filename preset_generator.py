import os
import xml.etree.ElementTree as ET
import random
import tkinter as tk
from tkinter import ttk, messagebox

BASE_DIR = "/Library/Application Support/Minimal/Current/SubPresets/"
EXCLUDED_CATEGORIES = ["Effect Rack", "Curve Shapes", "Chord Bank", "Rift Distortion", "Morph EQ"]

def load_categories_and_conditions(base_dir):
    categories = {}
    for category_name in os.listdir(base_dir):
        if category_name in EXCLUDED_CATEGORIES:
            continue  # Skip excluded categories
        category_path = os.path.join(base_dir, category_name)
        if os.path.isdir(category_path):
            conditions = [
                folder for folder in os.listdir(category_path)
                if os.path.isdir(os.path.join(category_path, folder)) and folder != "User"
            ]
            categories[category_name] = conditions
    return categories

def generate_output_directories(base_dir, categories):
    output_dirs = {}
    for category in categories:
        output_dirs[category] = os.path.join(base_dir, category, "User/")
    return output_dirs

def load_factory_effects(base_dir, categories_and_conditions):
    factory_effects = {}
    for category, conditions in categories_and_conditions.items():
        factory_effects[category] = {}
        for condition in conditions:
            condition_path = os.path.join(base_dir, category, condition)
            factory_effects[category][condition] = []
            for file in os.listdir(condition_path):
                if file.endswith(".xml"):
                    file_path = os.path.join(condition_path, file)
                    try:
                        tree = ET.parse(file_path)
                        root_element = tree.getroot()
                        preset_name = root_element.get("name", os.path.basename(file).replace(".xml", ""))
                        factory_effects[category][condition].append({"name": preset_name, "path": file_path, "xml": root_element})
                    except Exception as e:
                        print(f"Error loading {file_path}: {e}")
    return factory_effects

def interpolate_parameters(default_params, preset1_params, preset2_params):
    blended_params = []
    for default_param in default_params:
        name = default_param.tag
        unmapped1 = float(preset1_params.find(name).get("unmapped_value", 0))
        unmapped2 = float(preset2_params.find(name).get("unmapped_value", 0))
        mapped1 = float(preset1_params.find(name).get("mapped_value", 0))
        mapped2 = float(preset2_params.find(name).get("mapped_value", 0))

        blended_unmapped = (unmapped1 + unmapped2) / 2
        blended_mapped = (mapped1 + mapped2) / 2

        default_param.set("unmapped_value", str(blended_unmapped))
        default_param.set("mapped_value", str(blended_mapped))
        blended_params.append(default_param)
    return blended_params

def interpolate_distortion_types(node_properties, preset1_node_properties, preset2_node_properties):
    """Interpolates PositiveDistType and NegativeDistType."""
    positive1 = int(preset1_node_properties.get("PositiveDistType", 0))
    positive2 = int(preset2_node_properties.get("PositiveDistType", 0))
    negative1 = int(preset1_node_properties.get("NegativeDistType", 0))
    negative2 = int(preset2_node_properties.get("NegativeDistType", 0))

    interpolated_positive = random.choice([positive1, positive2])
    interpolated_negative = random.choice([negative1, negative2])

    node_properties.set("PositiveDistType", str(interpolated_positive))
    node_properties.set("NegativeDistType", str(interpolated_negative))

def generate_interpolated_preset_with_defaults(factory_effects, category, condition, target_directory):
    if category not in factory_effects or condition not in factory_effects[category] or len(factory_effects[category][condition]) < 2:
        messagebox.showerror("Error", f"Not enough presets in category: {category}, condition: {condition}")
        return

    preset1 = random.choice(factory_effects[category][condition])["xml"]
    preset2 = random.choice(factory_effects[category][condition])["xml"]

    default_path = os.path.join(target_directory, "DEFAULT.xml")
    if not os.path.exists(default_path):
        messagebox.showerror("Error", f"Default preset not found: {default_path}")
        return

    default_tree = ET.parse(default_path)
    default_root = default_tree.getroot()

    # Generate file name and encode it into SubPresetName
    base_name = f"blended_{category}_{condition}"
    counter = 1
    existing_files = os.listdir(target_directory)
    while f"{base_name}_{counter}.xml" in existing_files:
        counter += 1
    output_filename = f"{base_name}_{counter}.xml"
    sub_preset_name = f"{base_name}_{counter}"

    # Update SubPresetName
    default_root.set("name", sub_preset_name)
    node_properties = default_root.find(".//Node_Properties")
    if node_properties is not None:
        node_properties.set("SubPresetName", sub_preset_name)

        # Special handling for Polar Distortion
        if category == "Polar Distortion":
            preset1_node_properties = preset1.find(".//Node_Properties")
            preset2_node_properties = preset2.find(".//Node_Properties")
            if preset1_node_properties is not None and preset2_node_properties is not None:
                interpolate_distortion_types(node_properties, preset1_node_properties, preset2_node_properties)

    # Interpolate parameters
    default_params = default_root.find("Parameters")
    preset1_params = preset1.find("Parameters")
    preset2_params = preset2.find("Parameters")

    blended_params = interpolate_parameters(default_params, preset1_params, preset2_params)
    default_params.clear()
    default_params.extend(blended_params)

    # Write the output file
    os.makedirs(target_directory, exist_ok=True)
    output_path = os.path.join(target_directory, output_filename)
    default_tree.write(output_path, encoding="unicode", xml_declaration=True)
    messagebox.showinfo("Success", f"Preset saved to: {output_path}")

class PresetGeneratorApp(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Load data
        self.categories_and_conditions = load_categories_and_conditions(BASE_DIR)
        self.output_directories = generate_output_directories(BASE_DIR, self.categories_and_conditions)
        self.factory_effects = load_factory_effects(BASE_DIR, self.categories_and_conditions)

        # UI setup
        tk.Label(self, text="Category").grid(row=0, column=0, padx=10, pady=10)
        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(self, textvariable=self.category_var)
        self.category_dropdown["values"] = list(self.categories_and_conditions.keys())
        self.category_dropdown.bind("<<ComboboxSelected>>", self.update_conditions)
        self.category_dropdown.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self, text="Condition").grid(row=1, column=0, padx=10, pady=10)
        self.condition_var = tk.StringVar()
        self.condition_dropdown = ttk.Combobox(self, textvariable=self.condition_var)
        self.condition_dropdown.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(self, text="Generate Preset", command=self.generate_preset).grid(row=3, column=0, columnspan=2, pady=20)

    def update_conditions(self, event):
        category = self.category_var.get()
        if category in self.categories_and_conditions:
            self.condition_dropdown["values"] = self.categories_and_conditions[category]

    def generate_preset(self):
        category = self.category_var.get()
        condition = self.condition_var.get()
        if not category or not condition:
            messagebox.showerror("Error", "Please select a category and condition.")
            return
        target_directory = self.output_directories.get(category, "./output/")
        generate_interpolated_preset_with_defaults(self.factory_effects, category, condition, target_directory)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Preset Generator Tool")  # Set the window title
    root.geometry("400x200")  # Set the window size (can be adjusted based on content)
    app = PresetGeneratorApp(root)  # Initialize the PresetGeneratorApp
    app.pack(expand=1, fill="both")  # Pack the app into the window
    root.mainloop()
