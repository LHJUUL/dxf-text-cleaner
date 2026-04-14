# DXF Text Cleaner 🧹

> Remove text, dimensions, and annotations from DXF files for clean Revit/AutoCAD import

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## The Problem

When importing DXF files into Revit or other BIM software, text annotations clutter the model:
- Room labels overlap with geometry
- Dimensions interfere with modeling
- Block attributes display unwanted information
- Anonymous blocks contain hidden text

**This tool removes ALL text while preserving geometry.**

## Features

✅ **TEXT and MTEXT** removal (loose text entities)  
✅ **ATTDEF** removal from block definitions  
✅ **ATTRIB** removal from INSERT entities (the tricky ones!)  
✅ **DIMENSION** entities removal  
✅ **Anonymous blocks** (*U, *D) cleaning  
✅ **Layer-based** removal  
✅ **Xref** handling  
✅ **Batch processing** support  
✅ **Analysis mode** (preview before cleaning)  

## Quick Start

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/dxf-text-cleaner.git
cd dxf-text-cleaner

# 2. Install dependencies
pip install -r requirements.txt
```

### Usage

**Interactive mode (easiest):**
```bash
python dxf_cleaner.py
```

**Command line:**
```bash
python dxf_cleaner.py input.dxf
# Creates: input_CLEAN.dxf
```

**Windows drag & drop:**
```
Drag your DXF file onto clean_dxf.bat
```

## Advanced Usage

### Analyze before cleaning
```bash
python dxf_cleaner.py input.dxf --analyze
```

### Keep dimensions, remove text
```bash
python dxf_cleaner.py input.dxf --keep-dimensions
```

### Remove specific layers
```bash
python dxf_cleaner.py input.dxf --remove-layers "Skissestreker,TextLayer,Notes"
```

### Add date to output
```bash
python dxf_cleaner.py input.dxf --add-date
# Creates: input_CLEAN_20250414.dxf
```

### Custom output name
```bash
python dxf_cleaner.py input.dxf -o output.dxf
```

## Command Line Options

| Option | Description |
|--------|-------------|
| `--analyze` | Analyze file without cleaning |
| `--keep-text` | Keep TEXT/MTEXT entities |
| `--keep-dimensions` | Keep DIMENSION entities |
| `--keep-attribs` | Keep ATTRIB entities |
| `--skip-blocks` | Skip cleaning block definitions |
| `--skip-anonymous` | Skip anonymous (*U/*D) blocks |
| `--keep-xrefs` | Keep Xref layers |
| `--add-date` | Add date to output filename |
| `--remove-layers LAYERS` | Comma-separated list of layers to remove |
| `-o, --output FILE` | Specify output file |

## What Gets Removed

### 1. Modelspace Entities
- TEXT, MTEXT (loose text)
- DIMENSION, ALIGNED_DIMENSION, ROTATED_DIMENSION, etc.
- ATTRIB (rare in modelspace)
- Entities on specified layers

### 2. Block Definitions
- TEXT, MTEXT inside blocks
- ATTDEF (attribute templates)
- **Includes anonymous blocks (*U, *D)** - often missed by other tools!

### 3. Attached Attributes
- ATTRIB values attached to INSERT blocks
- These are the "1/2", "Room 101", etc. texts that appear with blocks
- **The most commonly missed text type!**

## Technical Details

This tool was created after hours of debugging Norwegian architectural DXF files for Revit import. It handles edge cases that most cleaners miss:

### Why This Tool Exists

**Problem 1: Anonymous Blocks**
Standard cleaners skip blocks starting with `*`, assuming they're system blocks. But `*U` and `*D` blocks are USER-DEFINED and contain text!

**Problem 2: Attached ATTRIB**
Text like "1/2" on blocks is often ATTRIB attached to INSERT entities, not separate TEXT entities. Most tools don't handle this.

**Problem 3: Layer "0"**
Text on layer "0" inside blocks inherits the INSERT entity's layer when displayed. Needs special handling.

**Solution:** This tool removes ALL text types, including these edge cases.

## Examples

### Before
```
DXF with:
- 310 TEXT/MTEXT entities
- 214 text entities in blocks
- 117 ATTRIB attached to inserts
- 23 DIMENSION entities
= 664 annotations cluttering the model
```

### After
```
Clean DXF with:
- All geometry preserved
- All blocks preserved (without text)
- All layers preserved
- 0 text entities
= Ready for Revit import!
```

## Import in Revit

After cleaning:
1. **Insert > Import CAD**
2. **Import units:** Check if Meters or Millimeters
3. **Positioning:** Auto - Origin to Origin
4. ❌ **Uncheck:** "Correct lines that are slightly off axis"
5. ❌ **Uncheck:** "Orient to View"

## Requirements

- Python 3.8 or higher
- ezdxf library (installed automatically via requirements.txt)

## Troubleshooting

### "No module named 'ezdxf'"
```bash
pip install -r requirements.txt
```

### Text still visible after cleaning
Some text might be drawn as LWPOLYLINE (lines shaped like letters). This is geometry, not text, and can't be automatically removed.

### Blocks look incomplete
If blocks lose important content, try:
```bash
python dxf_cleaner.py input.dxf --skip-anonymous
```

## Contributing

Contributions are welcome! This tool was built from real-world experience. If you find bugs or have suggestions:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Roadmap

### Planned Features
- [ ] GUI version with drag-and-drop
- [ ] Preview mode (show what will be removed)
- [ ] Batch processing (clean multiple files)
- [ ] Executable (.exe) version (no Python required)
- [ ] Undo functionality
- [ ] Export cleaning report
- [ ] Support for more entity types (LEADER, MULTILEADER)

### Community Requests
Open an issue to suggest features!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built from real-world experience cleaning Norwegian architectural DXF files
- Based on the excellent [ezdxf](https://github.com/mozman/ezdxf) library
- Created after a 3+ hour debugging session with stubborn ATTRIB entities!

## Support

If this tool saved you hours of manual cleanup, consider:
- ⭐ Starring the repository
- 🐛 Reporting bugs
- 💡 Suggesting features
- 📖 Improving documentation

---

**Made with ☕ and frustration during a very long debugging session**

**May your DXF files be forever text-free! 🎯**
