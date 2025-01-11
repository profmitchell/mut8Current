import tkinter as tk
from tkinter import filedialog, messagebox
import xml.etree.ElementTree as ET
from uuid import uuid4


def interpolate_presets(xml1: str, xml2: str, amount: float) -> str:
    """Simple preset interpolator that works directly with XML strings."""

    # Parse the XMLs
    root1 = ET.fromstring(xml1)
    root2 = ET.fromstring(xml2)

    # Create new preset from the first one (as template)
    new_root = ET.fromstring(xml1)

    # Update UUID
    meta = new_root.find('.//Meta')
    if meta is not None:
        meta.set('UUID', str(uuid4()))

    # Get all parameters with values
    params1 = root1.findall('.//Parameters/*')
    params2 = root2.findall('.//Parameters/*')
    new_params = new_root.findall('.//Parameters/*')

    # Interpolate each parameter
    for p1, p2, new_p in zip(params1, params2, new_params):
        try:
            # Get unmapped values
            u1 = float(p1.get('unmapped_value', '0'))
            u2 = float(p2.get('unmapped_value', '0'))

            # Get mapped values
            m1 = float(p1.get('mapped_value', '0'))
            m2 = float(p2.get('mapped_value', '0'))

            # Calculate interpolated values
            new_unmapped = u1 + (u2 - u1) * amount
            new_mapped = m1 + (m2 - m1) * amount

            # Set new values
            new_p.set('unmapped_value', f"{new_unmapped}")
            new_p.set('mapped_value', f"{new_mapped}")
        except Exception as e:
            print(f"Warning: Couldn't interpolate parameter {p1.tag}: {e}")
            continue

    # Convert back to string
    return ET.tostring(new_root, encoding='unicode', xml_declaration=True)


def load_file():
    return filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])


def save_file(content: str):
    file_path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML files", "*.xml")])
    if file_path:
        with open(file_path, 'w') as f:
            f.write(content)
        messagebox.showinfo("Success", f"Preset saved to {file_path}")


# GUI setup
class PresetInterpolatorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Preset Interpolator")

        # Variables to store file paths and interpolation amount
        self.preset1_path = None
        self.preset2_path = None
        self.interpolation_amount = tk.DoubleVar(value=0.5)

        # File selection buttons
        self.file1_button = tk.Button(master, text="Load Preset 1", command=self.load_preset1)
        self.file1_button.pack(pady=5)

        self.file2_button = tk.Button(master, text="Load Preset 2", command=self.load_preset2)
        self.file2_button.pack(pady=5)

        # Interpolation slider
        self.slider_label = tk.Label(master, text="Interpolation Amount (0.0 to 1.0):")
        self.slider_label.pack(pady=5)

        self.slider = tk.Scale(master, from_=0.0, to=1.0, resolution=0.01, orient=tk.HORIZONTAL,
                               variable=self.interpolation_amount)
        self.slider.pack(pady=5)

        # Generate button
        self.generate_button = tk.Button(master, text="Generate Interpolated Preset", command=self.generate_preset)
        self.generate_button.pack(pady=10)

        # Exit button
        self.exit_button = tk.Button(master, text="Exit", command=master.quit)
        self.exit_button.pack(pady=5)

    def load_preset1(self):
        self.preset1_path = load_file()
        if self.preset1_path:
            messagebox.showinfo("Loaded", f"Loaded Preset 1: {self.preset1_path}")

    def load_preset2(self):
        self.preset2_path = load_file()
        if self.preset2_path:
            messagebox.showinfo("Loaded", f"Loaded Preset 2: {self.preset2_path}")

    def generate_preset(self):
        if not self.preset1_path or not self.preset2_path:
            messagebox.showerror("Error", "Please load both Preset 1 and Preset 2.")
            return

        try:
            with open(self.preset1_path, 'r') as f:
                xml1 = f.read()
            with open(self.preset2_path, 'r') as f:
                xml2 = f.read()

            # Perform interpolation
            amount = self.interpolation_amount.get()
            new_preset = interpolate_presets(xml1, xml2, amount)

            # Save interpolated preset
            save_file(new_preset)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate preset: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = PresetInterpolatorApp(root)
    root.mainloop()
