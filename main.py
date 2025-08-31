import sys
import os
from PIL import Image, ImageSequence

def resize_and_crop(img, target_width=140, target_height=68):
    """
    Resize proportionally to match target_width first, then center-crop height.
    Final image before rotation is target_height x target_width.
    """
    # Match target width first
    scale = target_width / img.width
    new_height = int(img.height * scale)

    # Resize proportionally
    img = img.resize((target_width, new_height), Image.Resampling.LANCZOS)

    # If taller than target_height, crop vertically
    if new_height > target_height:
        top = (new_height - target_height) // 2
        img = img.crop((0, top, target_width, top + target_height))
    return img

def process_image(input_path, width=140, height=68):
    """
    Convert an image or GIF to 1-bit pixel art (black/white) with dithering.
    GIFs are split into frames and each frame is processed separately.
    """
    if not os.path.exists(input_path):
        print(f"❌ Error: File '{input_path}' not found.")
        return

    # Name output folder based on input filename
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    output_folder = f"{base_name}_frames"
    os.makedirs(output_folder, exist_ok=True)

    img = Image.open(input_path)
    frame_count = getattr(img, "n_frames", 1)
    MAX_FRAMES = 30  # maximum frames to process
    step = max(1, frame_count // MAX_FRAMES)

    print(f"Processing '{input_path}' - {frame_count} frame(s) detected...")

    count = 0

    for i, frame in enumerate(ImageSequence.Iterator(img)):
        if i % step != 0:  # skip frames proportionally
            continue

        frame_index = i // step  # new index for saved frames


        # Convert to RGB (remove alpha channel & palette)
        frame = frame.convert("RGB")

        # Rotate 90° clockwise
        frame = frame.rotate(-90, expand=True)

        # Resize to target size
        frame = resize_and_crop(frame, width, height)

        # Convert to 1-bit black/white with dithering
        frame = frame.convert("1")  # Dithered 1-bit

        # Convert to grayscale (L mode) for saving safety
        frame = frame.convert("L")

        # 🔥 Strip all transparency and other metadata
        frame.info.pop("transparency", None)

        # Save safely as PNG
        output_path = os.path.join(output_folder, f"frame_{count:03d}.png")
        frame.save(output_path, "PNG")
        print(f"✅ Saved {output_path}")
        count += 1

    print("🎉 Conversion complete!")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    process_image(input_file)

