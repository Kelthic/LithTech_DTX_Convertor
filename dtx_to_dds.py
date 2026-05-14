import struct
import os
import sys

def convert_dtx_to_dds(input_path):
    if not os.path.exists(input_path):
        print(f"ERR: File {input_path} not found.")
        return

    base_name = os.path.splitext(input_path)[0]
    output_path = f"{base_name}.dds"

    with open(input_path, 'rb') as f:
        header = f.read(164)
        if len(header) < 164:
            print(f"ERR: {input_path} has incorrect header size.")
            return

        # Offset 8: Width, 10: Height, 12: Mipmaps, 26: BPPIdent
        width, height, mipmaps = struct.unpack('<HHH', header[8:14])
        bpp_ident = header[26]

        four_cc = b'\x00\x00\x00\x00'
        block_size = 0
        is_compressed = True

        if bpp_ident == 4:
            four_cc = b'DXT1'
            block_size = 8
        elif bpp_ident == 5:
            four_cc = b'DXT3'
            block_size = 16
        elif bpp_ident == 6:
            four_cc = b'DXT5'
            block_size = 16
        elif bpp_ident in (0, 3):
            is_compressed = False
            block_size = 4 # BGRA8888
        else:
            print(f"ERR: Unknown BPPIdent format ({bpp_ident}) in {input_path}")
            return

        total_data_size = 0
        w, h = width, height
        for _ in range(mipmaps):
            if is_compressed:
                total_data_size += max(1, (w + 3) // 4) * max(1, (h + 3) // 4) * block_size
            else:
                total_data_size += w * h * 4
            w = max(1, w // 2)
            h = max(1, h // 2)

        f.seek(164)
        pixel_data = f.read(total_data_size)

    dwFlags = 0x1 | 0x2 | 0x4 | 0x1000 # CAPS, HEIGHT, WIDTH, PIXELFORMAT
    if mipmaps > 1:
        dwFlags |= 0x20000 # MIPMAPCOUNT

    pfFlags = 0
    pfRGBBitCount = 0
    pitch_linear = 0
    masks = (0, 0, 0, 0)

    if is_compressed:
        dwFlags |= 0x80000 # LINEARSIZE
        pfFlags = 0x4 # FOURCC
        pitch_linear = max(1, (width + 3) // 4) * max(1, (height + 3) // 4) * block_size
    else:
        dwFlags |= 0x8 # PITCH
        pfFlags = 0x41 # RGB | ALPHA
        pfRGBBitCount = 32
        pitch_linear = width * 4
        masks = (0x00FF0000, 0x0000FF00, 0x000000FF, 0xFF000000) # BGRA

    dwCaps = 0x1000 # TEXTURE
    if mipmaps > 1:
        dwCaps |= 0x400008 # COMPLEX | MIPMAP

    dds_header = bytearray(128)
    dds_header[0:4] = b'DDS '
    struct.pack_into('<IIIIIII 44x', dds_header, 4, 124, dwFlags, height, width, pitch_linear, 0, mipmaps)
    # Сборка PixelFormat
    struct.pack_into('<II4sIIIII', dds_header, 76, 32, pfFlags, four_cc, pfRGBBitCount, *masks)
    # Сборка Caps
    struct.pack_into('<I', dds_header, 108, dwCaps)

    with open(output_path, 'wb') as f_out:
        f_out.write(dds_header)
        f_out.write(pixel_data)

    print(f"SUCC: {os.path.basename(input_path)} to {os.path.basename(output_path)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            convert_dtx_to_dds(arg)
    else:
        print("Usage: python script.py <file1.dtx> <file2.dtx> ... or just Drag & Drop DTX onto the script")