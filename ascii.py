from PIL import Image
import os
import sys

ASCII_CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

def resize_image(image, new_width=250):
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio * 0.45)
    return image.resize((new_width, new_height))

def grayify(image):
    return image.convert("L")

def pixels_to_ascii(image):
    pixels = image.getdata()
    ascii_str = ""
    for pixel in pixels:
        char = ASCII_CHARS[pixel * len(ASCII_CHARS) // 256]
        ascii_str += char
    return ascii_str

def image_to_ascii(path, new_width=250):
    image = Image.open(path)
    image = resize_image(image, new_width)
    image = grayify(image)
    ascii_str = pixels_to_ascii(image)
    ascii_str_len = len(ascii_str)
    ascii_img = "\n".join(
        ascii_str[i:(i+new_width)] for i in range(0, ascii_str_len, new_width)
    )
    return ascii_img

if __name__ == "__main__":
    path = input("Enter image path (or type 'exit' to quit): ").strip().strip('"').strip("'")
    if path.lower() == "exit":
        sys.exit()

    if len(path) > 2 and path[1] == ":":
        drive_letter = path[0].lower()
        path = path.replace("\\", "/")
        path = f"/mnt/{drive_letter}{path[2:]}"

    width = input("Enter ASCII width (default 250, or 'exit' to quit): ").strip()
    if width.lower() == "exit":
        sys.exit()
    width = int(width) if width.isdigit() else 250

    ascii_art = image_to_ascii(path, new_width=width)

    save_path = os.path.join(os.getcwd(), "save.txt")
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(ascii_art)

    print(f"ASCII art saved to: {save_path}")
