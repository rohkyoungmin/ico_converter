## ICO Converter

`ico_converter.py` is a Python-based CLI tool that converts PNG or SVG images into multi-resolution `.ico` icon files. It is particularly useful for Electron apps, Windows executables, or any software that requires properly scaled `.ico` assets.

### Features
- Supports both PNG and SVG inputs  
- Automatically includes multiple icon sizes (`256,128,64,48,32,16`)  
- Single-file utility based on Pillow  
- Optional SVG rasterization using `cairosvg`

---

### Installation

```bash
pip install pillow
# Required only for SVG input:
pip install cairosvg
```

---

### Usage

```bash
python ico_converter.py [INPUT] [-o OUTPUT] [-s SIZES] [--svg]
```

#### Basic example

```bash
# Converts icon.png → icon.ico with multiple sizes
python ico_converter.py icon.png
```

#### Specify output path

```bash
python ico_converter.py icon.png -o build/app.ico
```

#### Customize sizes

```bash
python ico_converter.py icon.png -s 512,256,128,64,32,16
```

#### Convert SVG input (requires cairosvg)

```bash
python ico_converter.py icon.svg --svg -o icon.ico
```

---

### Output

- Generates a `.ico` file containing all specified sizes.
- Each resolution is auto-resized and embedded into the `.ico` file by Pillow.

---

### Notes

- Square input images (e.g., 512×512) are recommended.
- Transparency is preserved (RGBA supported).
- Windows taskbar and Explorer require at least 256×256 for crisp rendering.

---

### File structure

```
ico_converter.py        # This script
icon.png                # Input example
icon.ico                # Output result
```

### Before & After

## Before
<img width="1024" height="1024" alt="icon" src="https://github.com/user-attachments/assets/ed9b84ad-c469-40c9-bca2-bb4ccb25ee39" />

## After
<img width="1920" height="1032" alt="{DEEF6CA3-D39C-420E-9A22-566BD66756E8}" src="https://github.com/user-attachments/assets/c902701c-5f2a-46cf-b89d-db210e8ac613" />


---

You can also package this script as an executable using tools like PyInstaller. If needed, a `build.bat` or `.spec` file can be provided.
