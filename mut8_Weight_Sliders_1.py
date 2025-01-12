import tkinter as tk
from tkinter import filedialog, messagebox
import xml.etree.ElementTree as ET
from uuid import uuid4

# Metadata
APP_NAME = "Preset Interpolator"
VERSION = "1.0.4"
AUTHOR = "Mitchell Cohen"
LOCATION = "Newton, MA"
DATE = "01/11/25"


def interpolate_presets(xml_list, weights):
    """Interpolates multiple presets based on weights."""
    roots = [ET.fromstring(xml) for xml in xml_list]

    # Use the first preset as the template
    new_root = ET.fromstring(xml_list[0])

    # Update UUID
    meta = new_root.find('.//Meta')
    if meta is not None:
        meta.set('UUID', str(uuid4()))

    # Interpolate Parameters
    params_list = [root.findall('.//Parameters/*') for root in roots]
    new_params = new_root.findall('.//Parameters/*')

    for param_set in zip(*params_list, new_params):
        try:
            values = {"unmapped_value": [], "mapped_value": []}
            for i, param in enumerate(param_set[:-1]):
                for key in values.keys():
                    value = float(param.get(key, '0')) * weights[i]
                    values[key].append(value)

            for key in values.keys():
                interpolated_value = sum(values[key])
                param_set[-1].set(key, f"{interpolated_value}")
        except Exception as e:
            print(f"Warning: Couldn't interpolate parameter {param_set[0].tag}: {e}")
            continue

    return ET.tostring(new_root, encoding='unicode', xml_declaration=True)


def load_file():
    return filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])


def save_file(content: str):
    file_path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML files", "*.xml")])
    if file_path:
        with open(file_path, 'w') as f:
            f.write(content)
        messagebox.showinfo("Success", f"Preset saved to {file_path}")


def show_help():
    """Display help and credits."""
    messagebox.showinfo(
        "About",
        f"{APP_NAME}\nVersion: {VERSION}\nAuthor: {AUTHOR}\nLocation: {LOCATION}\nDate: {DATE}\n\nThis application interpolates between 2-4 XML presets. Select presets and use the appropriate interface to generate interpolated outputs."
    )

# GUI setup
class PresetInterpolatorApp:
    def __init__(self, master):
        self.master = master
        self.master.title(f"{APP_NAME} - {VERSION}")

        # Variables
        self.presets = []
        self.weights = []

        # File input buttons
        self.file_buttons = []
        for i in range(4):
            button = tk.Button(master, text=f"Load Preset {i + 1}", command=lambda i=i: self.load_preset(i))
            button.grid(row=i, column=0, padx=5, pady=5)
            self.file_buttons.append(button)

        # Weight input sliders
        self.weight_sliders = []
        for i in range(4):
            slider = tk.Scale(master, from_=0.0, to=1.0, resolution=0.01, orient=tk.HORIZONTAL, label=f"Weight {i + 1}")
            slider.grid(row=i, column=1, padx=5, pady=5)
            self.weight_sliders.append(slider)

        # Normalize button
        self.normalize_button = tk.Button(master, text="Normalize Weights", command=self.normalize_weights)
        self.normalize_button.grid(row=4, column=1, padx=10, pady=10)

        # Generate button
        self.generate_button = tk.Button(master, text="Generate Interpolated Preset", command=self.generate_preset)
        self.generate_button.grid(row=5, column=0, pady=10)

        # Help button
        self.help_button = tk.Button(master, text="?", command=show_help)
        self.help_button.grid(row=5, column=1, pady=10)

    def load_preset(self, index):
        file_path = load_file()
        if file_path:
            with open(file_path, 'r') as f:
                xml = f.read()
                if index < len(self.presets):
                    self.presets[index] = xml
                else:
                    self.presets.append(xml)
            messagebox.showinfo("Loaded", f"Loaded Preset {index + 1}.")

    def normalize_weights(self):
        """Normalize weights to ensure they sum to 1."""
        total = sum(slider.get() for slider in self.weight_sliders if slider.get() > 0)
        if total > 0:
            for slider in self.weight_sliders:
                slider.set(slider.get() / total)

    def generate_preset(self):
        if len(self.presets) < 2:
            messagebox.showerror("Error", "Please load at least two presets.")
            return

        try:
            weights = [slider.get() for slider in self.weight_sliders[:len(self.presets)]]
            self.normalize_weights()
            new_preset = interpolate_presets(self.presets, weights)
            save_file(new_preset)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate preset: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = PresetInterpolatorApp(root)
    root.mainloop()
