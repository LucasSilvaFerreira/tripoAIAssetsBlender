
# Sprite Sheet 3D Asset Separator

**Version:** 2.2  
**Blender Compatibility:** 4.1  
**Author:** Lucas

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Accessing the Add-on](#accessing-the-add-on)
  - [Operators and Functions](#operators-and-functions)
    - [Import GLB File](#import-glb-file)
    - [Preprocessing](#preprocessing)
    - [Decimation](#decimation)
    - [Set Origin](#set-origin)
    - [Asset Management](#asset-management)
    - [Automation](#automation)
- [Properties](#properties)
  - [Merge Threshold](#merge-threshold)
  - [Angle Limit](#angle-limit)
- [Notes](#notes)
- [Troubleshooting](#troubleshooting)
- [License](#license)
- [Contributing](#contributing)
- [Contact](#contact)

## Introduction

The **Sprite Sheet 3D Asset Separator** is a Blender add-on designed to streamline the process of separating 3D sprite sheet assets and preparing them as individual assets. This tool automates tasks such as merging vertices, separating loose parts, decimating meshes while preserving UV seams, setting object origins, and marking objects as assets with generated previews.

## Features

- **Import GLB/GLTF Files:** Easily import your 3D sprite sheets in GLB or GLTF formats.
- **Merge Vertices by Distance:** Clean up your mesh by merging close vertices based on a customizable threshold.
- **Separate by Loose Parts:** Automatically split your mesh into individual, connected components.
- **Decimation with UV Preservation:** Reduce mesh complexity using the Decimate modifier while preserving UV seams, with a customizable angle limit.
- **Set Origin Options:** Set the origin of objects to their center of mass or the base of the object.
- **Asset Management:** Mark objects as assets and generate previews for use in Blender's Asset Browser.
- **Automation:** Perform all the above steps automatically with a single click.

## Installation

1. **Download the Add-on:**
   - Save the `sprite_sheet_separator.py` script file to your local machine.

2. **Install the Add-on in Blender:**
   - Open Blender.
   - Navigate to **`Edit > Preferences`**.
   - Select the **`Add-ons`** tab on the left.
   - Click on **`Install...`** at the top.
   - Locate and select the `sprite_sheet_separator.py` file you saved earlier.
   - Click **`Install Add-on`**.

3. **Enable the Add-on:**
   - After installation, ensure the add-on is enabled by checking the box next to **"Sprite Sheet 3D Asset Separator"**.

4. **Save User Preferences (Optional):**
   - To have the add-on enabled every time you start Blender, click **`Save Preferences`** at the bottom of the Preferences window.

## Usage

### Accessing the Add-on

- In the **3D Viewport**, press **`N`** to open the Sidebar.
- Navigate to the **`Sprite Sheet`** tab.

### Operators and Functions

#### Import GLB File

- **Purpose:** Import your 3D sprite sheet in GLB or GLTF format.
- **How to Use:**
  - Click **`Import GLB File`**.
  - A file browser window will appear.
  - Navigate to your `.glb` or `.gltf` file and select it.
  - Click **`Import GLB`**.

#### Preprocessing

- **Merge Vertices by Distance:**
  - **Purpose:** Merge vertices that are within a specified distance to clean up the mesh.
  - **Parameters:**
    - **`Merge Threshold`**: Controls how close vertices need to be to be merged.
  - **How to Use:**
    - Adjust the **`Merge Threshold`** value if necessary.
    - Ensure the imported object is selected.
    - Click **`Merge Vertices by Distance`**.

- **Separate by Loose Parts:**
  - **Purpose:** Split the mesh into individual connected components.
  - **How to Use:**
    - Ensure the object is selected.
    - Click **`Separate by Loose Parts`**.

#### Decimation

- **Purpose:** Reduce mesh complexity while preserving UV seams.
- **Parameters:**
  - **`Angle Limit`**: The maximum angle between face normals (in degrees) below which edges are dissolved.
    - **Default:** 33 degrees.
- **How to Use:**
  - Adjust the **`Angle Limit`** slider if necessary.
  - Select the objects you wish to decimate.
  - Click **`Apply Decimate Modifier`**.

#### Set Origin

- **Set Origin to Center of Mass:**
  - **Purpose:** Sets the origin of selected objects to their center of mass.
  - **How to Use:**
    - Select the objects.
    - Click **`Set Origin to Center of Mass`**.

- **Set Origin to Base:**
  - **Purpose:** Sets the origin of selected objects to the lowest point of their bounding box (useful for aligning objects on a surface).
  - **How to Use:**
    - Select the objects.
    - Click **`Set Origin to Base`**.

#### Asset Management

- **Purpose:** Mark selected objects as assets and generate previews for use in Blender's Asset Browser.
- **How to Use:**
  - Select the objects.
  - Click **`Mark as Asset and Generate Preview`**.

#### Automation

- **Purpose:** Perform all the above steps automatically.
- **How to Use:**
  - Adjust the **`Merge Threshold`** and **`Angle Limit`** if necessary.
  - Select the imported object.
  - Click **`Do All Steps Automatically`**.

## Properties

### Merge Threshold

- **Description:** Sets the distance threshold for merging vertices during the merge operation.
- **Default Value:** `0.0001`
- **Adjustment:**
  - Increase the value to merge vertices that are farther apart.
  - Decrease the value to merge only very close vertices.

### Angle Limit

- **Description:** Sets the angle limit for the Decimate modifier (in degrees).
- **Default Value:** `33` degrees
- **Adjustment:**
  - Lower values preserve more detail (less decimation).
  - Higher values result in greater simplification of the mesh.

## Notes

- **Blender Version Compatibility:** This add-on is designed for Blender **4.1**. Ensure you are using a compatible version to avoid any issues.
- **Object Selection:** The operators work on selected objects of type `'MESH'`. Ensure only mesh objects are selected to avoid errors.
- **Asset Browser:** After marking objects as assets, they will appear in Blender's Asset Browser under the **Current File** asset library.

## Troubleshooting

- **UI Elements Not Visible:**
  - If you cannot see the add-on interface, ensure the add-on is enabled in Blender's preferences.
  - Check that you are looking in the **`Sprite Sheet`** tab of the Sidebar.
- **Operators Not Working:**
  - Ensure you have selected the appropriate objects before running an operator.
  - Check for error messages in Blender's console for more details.
- **Version Mismatch Errors:**
  - If you encounter errors, verify that you are using Blender version **4.1** or later.

## License

[Specify the license under which you are distributing your add-on. For example:]

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! If you would like to contribute to this project, please:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes with clear and descriptive messages.
4. Submit a pull request detailing your changes.

## Contact

For any questions or suggestions, please contact [Your Name](mailto:your.email@example.com).

---

Feel free to customize the README as needed. Replace placeholders like `[Your Name]` and contact information with your actual details. If you have specific license requirements, ensure you include the appropriate license text in a `LICENSE` file and reference it in the README.

I hope this helps you set up your GitHub repository!
