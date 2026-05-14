<div align="center">

# DTX to DDS Converter

### Lightweight texture conversion utility for the LithTech Engine

</div>

---

## Overview

**DTX → DDS Converter** is a small command-line tool designed to convert  
LithTech `.dtx` texture files into standard `.dds` textures.

The tool supports several common compression formats used by older  
LithTech-based games and preserves mipmaps during conversion.

---

## Features

- Convert `.dtx` textures to `.dds`
- Supports:
  - DXT1
  - DXT3
  - DXT5
  - BGRA8888
- Preserves mipmaps
- Fast batch conversion
- Lightweight and dependency-free

---

## Usage

Place your `.dtx` files near the script and run:

```bash
python script.py texture.dtx