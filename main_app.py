import tkinter as tk
from tkinter import ttk, messagebox
from preset_interpolator import PresetInterpolatorApp
from preset_generator import PresetGeneratorApp


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set title and window geometry
        self.title("mut8: Current")
        self.geometry("800x500")  # Expanded interface
        self.center_window()

        # Add main title label
        title_label = tk.Label(
            self,
            text="mut8: Current",
            font=("Helvetica", 16, "bold"),
            pady=10,
        )
        title_label.pack()

        # Add ? button with instructions
        help_button = tk.Button(
            self,
            text="?",
            command=self.show_help,
            font=("Helvetica", 12, "bold"),
            width=2,
        )
        help_button.place(relx=0.97, rely=0.02, anchor="ne")  # Position top-right

        # Create tab control
        tab_control = ttk.Notebook(self)

        # Create tabs
        interpolator_tab = tk.Frame(tab_control)
        generator_tab = tk.Frame(tab_control)

        # Add apps to tabs
        PresetInterpolatorApp(interpolator_tab).pack(expand=1, fill="both", padx=10, pady=10)
        PresetGeneratorApp(generator_tab).pack(expand=1, fill="both", padx=10, pady=10)

        # Add tabs to the tab control with updated labels
        tab_control.add(interpolator_tab, text="mut8 Preset")
        tab_control.add(generator_tab, text="mut8 Effects")

        # Pack tab control into the main window
        tab_control.pack(expand=1, fill="both", padx=10, pady=10)

    def center_window(self):
        """Center the application window on the screen."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (400 // 2)
        y = (screen_height // 2) - (500 // 2)
        self.geometry(f"400x500+{x}+{y}")

    def show_help(self):
        """Show instructions and credits."""
        messagebox.showinfo(
            "About",
            "mut8: Current\n\n"
            "Instructions:\n"
            "- Use 'mut8 Preset' to interpolate presets.\n"
            "- Use 'mut8 Effects' to generate and save effects.\n\n"
            "Developed by: Mitchell Cohen\n"
            "Newton, MA, 2024\n"
            "www.mitchellcohen.net",
        )


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
