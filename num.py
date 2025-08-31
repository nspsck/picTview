# Function to generate LVGL image declarations and array
def generate_lvgl_frames(num):
    # Generate LV_IMG_DECLARE lines
    for i in range(num + 1):
        print(f"LV_IMG_DECLARE(frame_{i:03d});")

    print("\nconst lv_img_dsc_t *anim_imgs[] = {")

    # Generate array entries
    for i in range(num + 1):
        comma = "," if i < num else ","
        print(f"    &frame_{i:03d}{comma}")

    print("};")

# Example usage
if __name__ == "__main__":
    number = int(input("Enter the number of frames: "))
    generate_lvgl_frames(number)

