import os
import sys

def combine_c_files(input_dir, output_file):
    """
    Combine all .c files in input_dir into one single output_file.
    The output file will be structured like your example.
    """
    # Header template for art.c
    header = """/*
 *
 * Copyright (c) 2023 Collin Hodge
 * Copyright (c) 2023 The ZMK Contributors
 * SPDX-License-Identifier: MIT
 *
 */

#include <lvgl.h>

#ifndef LV_ATTRIBUTE_MEM_ALIGN
#define LV_ATTRIBUTE_MEM_ALIGN
#endif
"""
    # Replacement block (7 lines)
    replacement_block = [
        "#if CONFIG_NICE_VIEW_WIDGET_INVERTED\n",
        "        0xff, 0xff, 0xff, 0xff, /*Color of index 0*/\n",
        "        0x00, 0x00, 0x00, 0xff, /*Color of index 1*/\n",
        "#else\n",
        "        0x00, 0x00, 0x00, 0xff, /*Color of index 0*/\n",
        "        0xff, 0xff, 0xff, 0xff, /*Color of index 1*/\n",
        "#endif\n"
    ]

    with open(output_file, 'w') as out_f:
        # Write the header first
        out_f.write(header + "\n\n")

        # Get all .c files sorted alphabetically
        c_files = sorted(f for f in os.listdir(input_dir) if f.endswith('.c'))

        for file in c_files:
            file_path = os.path.join(input_dir, file)
            with open(file_path, 'r') as in_f:
                lines = in_f.readlines()
                trimmed_lines = lines[18:]
                # Replace lines 8 and 9 (index 7 and 8) with the 7-line block
                # Make sure there are enough lines
                if len(trimmed_lines) >= 9:
                    trimmed_lines = (
                        trimmed_lines[:6] +  # lines 0-5 remain
                        replacement_block +  # insert replacement block
                        trimmed_lines[8:]    # keep rest starting from line 10
                    )
                else:
                    print(f"Warning: {c_file} has fewer than 9 lines after trimming. Skipping replacement.")
                out_f.write(f"/* Contents of {file} */\n")
                out_f.writelines(trimmed_lines)
                out_f.write("\n\n")

    print(f"Combined {len(c_files)} files into {output_file}")

if __name__ == "__main__":
    output_file = "art.c"
    if len(sys.argv) < 2:
        print("Usage: python main.py <input_file>")
        sys.exit(1)

    input_dir = sys.argv[1]
    combine_c_files(input_dir, output_file)

