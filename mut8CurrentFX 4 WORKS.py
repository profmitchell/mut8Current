import os
import xml.etree.ElementTree as ET
import random
import tkinter as tk
from tkinter import ttk, messagebox

BASE_DIR = "/Library/Application Support/Minimal/Current/SubPresets/"

def load_categories_and_conditions(base_dir):
    categories = {}
    for category_name in os.listdir(base_dir):
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

CATEGORIES_AND_CONDITIONS = load_categories_and_conditions(BASE_DIR)
OUTPUT_DIRECTORIES = generate_output_directories(BASE_DIR, CATEGORIES_AND_CONDITIONS)

def load_factory_effects(base_dir):
    factory_effects = {}
    for category, conditions in CATEGORIES_AND_CONDITIONS.items():
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

    default_root.set("name", f"Blended_{condition}_Preset")  # Ensure the name is set in the root element

    default_params = default_root.find("Parameters")
    preset1_params = preset1.find("Parameters")
    preset2_params = preset2.find("Parameters")

    blended_params = interpolate_parameters(default_params, preset1_params, preset2_params)

    default_params.clear()
    default_params.extend(blended_params)

    existing_files = os.listdir(target_directory)
    base_name = f"blended_{condition}"
    counter = 1
    while f"{base_name}_{counter}.xml" in existing_files:
        counter += 1
    output_filename = f"{base_name}_{counter}.xml"

    os.makedirs(target_directory, exist_ok=True)
    output_path = os.path.join(target_directory, output_filename)
    default_tree.write(output_path, encoding="unicode", xml_declaration=True)
    messagebox.showinfo("Success", f"Preset saved to: {output_path}")

class PresetGeneratorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Preset Generator")

        self.factory_effects = load_factory_effects(BASE_DIR)

        tk.Label(master, text="Category").grid(row=0, column=0, padx=10, pady=10)
        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(master, textvariable=self.category_var)
        self.category_dropdown["values"] = list(CATEGORIES_AND_CONDITIONS.keys())
        self.category_dropdown.bind("<<ComboboxSelected>>", self.update_conditions)
        self.category_dropdown.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(master, text="Condition").grid(row=1, column=0, padx=10, pady=10)
        self.condition_var = tk.StringVar()
        self.condition_dropdown = ttk.Combobox(master, textvariable=self.condition_var)
        self.condition_dropdown.grid(row=1, column=1, padx=10, pady=10)

        self.generate_button = tk.Button(master, text="Generate Preset", command=self.generate_preset)
        self.generate_button.grid(row=3, column=0, columnspan=2, pady=20)

    def update_conditions(self, event):
        category = self.category_var.get()
        if category in CATEGORIES_AND_CONDITIONS:
            self.condition_dropdown["values"] = CATEGORIES_AND_CONDITIONS[category]
        else:
            self.condition_dropdown["values"] = []

    def generate_preset(self):
        category = self.category_var.get()
        condition = self.condition_var.get()
        if not category or not condition:
            messagebox.showerror("Error", "Please select a category and condition.")
            return
        target_directory = OUTPUT_DIRECTORIES.get(category, "./output/")
        generate_interpolated_preset_with_defaults(self.factory_effects, category, condition, target_directory)

if __name__ == "__main__":
    root = tk.Tk()
    app = PresetGeneratorApp(root)
    root.mainloop()
