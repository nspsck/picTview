# picTview

## Usage
```shell
# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Convert to images
python3 main.py filename.xxx

# Combine output of lvgl files into one art.c
python3 generate.py path

# Generate list of frames
python3 num.py
```
## LVGL site
[https://lvgl.io/tools/imageconverter](https://lvgl.io/tools/imageconverter)
color format: `CF_INDEXED_1BIT`, ouput format: `C array`.
