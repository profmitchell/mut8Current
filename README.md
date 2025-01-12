# mut8Current
<img width="687" alt="Screenshot 2025-01-11 at 8 41 55 PM" src="https://github.com/user-attachments/assets/6798e0d6-4f79-47df-aee3-51a0dcab9a3f" />

<img width="495" alt="Screenshot 2025-01-11 at 8 06 57 PM" src="https://github.com/user-attachments/assets/cdbc46bb-b659-4e4f-9f7e-0b74b17068fe" />
<img width="405" alt="Screenshot 2025-01-11 at 8 06 09 PM" src="https://github.com/user-attachments/assets/f05a537a-f5c1-47da-ae62-6792c650d7d9" />
<img width="435" alt="Screenshot 2025-01-11 at 8 06 15 PM" src="https://github.com/user-attachments/assets/89639976-09db-4d0b-b92f-fbd3ee0923a9" />



Version: 1.0.1
Author: Mitchell Cohen
Location: Newton, MA
Date: 01/11/25
Overview

mut8Current is a Python-based toolset and framework designed for working with Synth VST presets in XML format. The project aims to simplify the management, mutation, interpolation, and creation of synthesizer presets. This app will support workflows for analyzing, editing, and generating presets in a structured, user-friendly manner.
The project is modular and versioned, with detailed documentation for each milestone. Future versions will expand functionality, introducing advanced interpolation features, batch processing, and a highly customizable user interface.
Current Features (Version 1.0.1)

mut8CurrentInitAnalyzer
Purpose: Analyze and format Synth VST XML patch files.
Functionality:
Load XML files via a GUI.
Parse and prettify the XML structure, ensuring consistent formatting with proper white spaces and indentation.
Save the formatted XML to a specified location.
Display app details, versioning, and author information via a ? button.
GUI Labeling:
Includes app name, author, location, and date stamp in the interface.
Version control is displayed in the help message.
Planned Features

1. Patch Mutation and Interpolation
Description: Develop a mechanism to interpolate between two or more presets to generate new variations.
Features:
Load multiple XML patches as input.
Blend parameter values between patches based on user-defined interpolation factors.
Export mutated presets as properly formatted XML files.
2. Default Patch Template Integration
Description: Hardcode a default patch format into the app, allowing consistent creation of initialized presets.
Features:
Define a base template XML structure.
Provide a one-click option to generate a new default preset.
3. Batch Processing
Description: Allow users to process multiple presets simultaneously.
Features:
Batch format XML files.
Batch interpolate multiple patches to generate unique presets.
4. Advanced GUI with Preset Management
Description: Expand the GUI to include preset browsing, parameter editing, and visualization tools.
Features:
Browse and preview XML presets.
Edit parameters directly via sliders, dropdowns, and text inputs.
Visualize preset parameters and changes graphically.
5. Version Control
Description: Maintain version tracking for presets and the application.
Features:
Embed version metadata in generated XML presets.
Track application versions in a changelog.
6. Documentation and Help
Description: Ensure all tools are thoroughly documented.
Features:
Add a dedicated help section to the app with descriptions of all functionalities.
Include inline tooltips for key features.
Roadmap

Version	Feature Milestones	Estimated Completion
1.0.1	Initial release: Analyze and format XML files.	Complete (01/11/25)
1.1.0	Add hardcoded default patch template.	Q1 2025
1.2.0	Implement basic interpolation between two presets.	Q1 2025
1.3.0	Enable batch processing of multiple presets for formatting and interpolation.	Q2 2025
1.4.0	Expand GUI for preset browsing, editing, and graphical visualization.	Q2 2025
2.0.0	Full-fledged patch management app with advanced mutation and interpolation features, including batch tools.	Q3 2025
How to Contribute

Contributions are welcome! Feel free to submit pull requests or report issues to improve functionality, UI, or documentation.
License

This project is currently private and owned by Mitchell Cohen. Future licensing details will be provided as the project progresses.
Contact

For inquiries, reach out to Mitchell Cohen at Newton, MA.
Notes:
This README can evolve as the project grows. Let me know if you’d like to add anything or adjust the timeline!
