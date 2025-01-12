### README for **mut8: Current**

---
<img width="512" alt="Screenshot 2025-01-12 at 4 55 21 PM" src="https://github.com/user-attachments/assets/1517a089-dcb1-44c8-bd40-1f0797f01047" />
<img width="512" alt="Screenshot 2025-01-12 at 4 55 36 PM" src="https://github.com/user-attachments/assets/09e47383-c183-45da-9499-f5eac10fe25c" />

---

## Overview

**mut8: Current** is a Python-based application designed to create interpolated presets for audio plugins. This tool enables users to combine factory presets from a selected category and condition, producing new, blended presets with unique characteristics. By preserving compatibility with existing presets and providing customization options, **mut8: Current** empowers users to explore innovative sound design.

---

## Features

- **Category and Condition-Based Preset Blending:**
  - Combines two existing factory presets to generate new, interpolated presets.
  - Dynamically blends parameters for unique soundscapes.

- **User-Friendly Interface:**
  - Built with a clean **Tkinter GUI** for seamless navigation.
  - Drop-down menus for selecting preset categories and conditions.

- **Enhanced Polar Distortion Handling:**
  - Dynamically includes `PositiveDistType` and `NegativeDistType` for accurate blending.
  - Incorporates additional distortion types beyond the default.

- **Exclusion of Incompatible Categories:**
  - Automatically omits unsupported categories (e.g., `Effect Rack`, `Curve Shapes`, `Chord Bank`, `Rift Distortion`, and `Morph EQ`).

- **Automatic File Management:**
  - Saves generated presets in the appropriate `User` directory under each category.

- **Error Notifications:**
  - Alerts users if presets are insufficient or if the default preset is missing.

---

## Prerequisites

### Software Requirements:
- Python 3.10 or higher.
- Required Python libraries:
  - `tkinter`
  - `os`
  - `xml.etree.ElementTree`

### File Structure:
The application requires the following directory structure:
```
/Library/Application Support/Minimal/Current/SubPresets/
└── [Category Name]
    ├── User/
    ├── [Condition Name 1]/
    ├── [Condition Name 2]/
    └── ...
```
**Note:** Each condition folder must contain XML files representing factory presets.

---

## Installation

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/your-username/mut8-current.git
   cd mut8-current
   ```

2. Ensure Python 3.10 or higher is installed on your system.

3. Install the required Python packages:
   ```bash
   pip install tkinter
   ```

4. Set up the required directory structure and include factory presets in the appropriate folders.

---

## Usage

1. Run the application:
   ```bash
   python3 mut8_current.py
   ```

2. Use the dropdown menus to:
   - Select a **category** (e.g., `Polar Distortion`).
   - Select a **condition** (e.g., `Filtering`).

3. Click **Generate Preset** to create a blended preset. The new preset will be saved in the corresponding `User` directory under the selected category.

4. For `Polar Distortion` presets, distortion types (`PositiveDistType` and `NegativeDistType`) are dynamically blended for added flexibility.

---

## Supported Categories

| **Category**       | **Description**                                      |
|---------------------|------------------------------------------------------|
| Polar Distortion    | Includes blending of parameters and distortion types.|
| [Other Categories]  | Supports parameter interpolation.                    |

**Excluded Categories:**  
- Effect Rack  
- Curve Shapes  
- Chord Bank  
- Rift Distortion  
- Morph EQ  

---

## Known Issues

- Certain categories (e.g., `Effect Rack`, `Morph EQ`) are excluded due to incompatibility with the blending logic.
- Ensure each condition folder contains at least two presets for interpolation to function correctly.

---

## Future Improvements

- Add support for currently excluded categories by implementing custom blending logic.
- Extend parameter interpolation logic to additional plugin features.
- Enhance GUI for advanced customization options (e.g., parameter editing).
- Support additional file formats beyond XML for greater compatibility.


---

## License

**mut8: Current** is licensed under the [MIT License](LICENSE).

---

## Author

**mut8: Current** was developed by **Mitchell Cohen**  
[www.mitchellcohen.net](https://www.mitchellcohen.net)  
Location: Newton, MA  
Year: 2025  

Feel free to reach out for inquiries, suggestions, or collaboration opportunities!
