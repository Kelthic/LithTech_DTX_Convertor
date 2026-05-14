<div align="center">

# DTX to DDS Converter

### Lightweight texture conversion utility for the LithTech Engine

</div>

---

## Overview

**DTX to DDS Converter** is a small command-line tool designed to convert  
LithTech `.DTX` texture files into standard `.DDS` textures.

The tool supports several common compression formats used by older  
LithTech-based games and preserves mipmaps during conversion.

---

## Features

- Convert `.DTX` textures to `.DDS`
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

Place your `.DTX` files near the script and run:

```bash
python script.py texture.DTX
```

---
## Credit

[Five Damned Dollarz](https://github.com/Five-Damned-Dollarz/DTXTool/blob/main/research/DTX_Lithtech_texture_template.bt) for research

[jsj2008](https://github.com/jsj2008/lithtech/blob/master/tools/shared/engine/dtxmgr.h) for example of DTX format

[AkvenJan](https://github.com/AkvenJan/DTX-Meta-Transfer) for useful tips about DTX and DDS formats
