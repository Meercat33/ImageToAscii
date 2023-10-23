# Some really awful Image to ASCII converter.
# This was made in an afternoon after a long night for lack of better word
# Please take none of this seriously if you're someone from a future job I apply to
# BTW: this exports the ascii-ified image through a text file
# The resolution has only been halved. It may be a very large text file
# Please zoom out and use a monospaced font for best viewing experience
# Thank you for your time.

from PIL import Image, ImageEnhance
import numpy as np

chars = "$$$$$@@@@@BBBBB%%%%%dddddpppppqqqqqwwwwwmmmmmJJJJJUUUUUYYYYYXXXXXzzzzzcccccvvvvvuuuuuxxxxxrrrrrjjjjjfffffttttt/////\\\\\\\\\\|||||((((()))))11111{{{{{}}}}}[[[[[]]]]]?????-----_____+++++~~~~~<<<<<>>>>>iiiii!!!!!lllllIIIII;;;;;:::::,,,,,\"\"\"\"\"^^^^^`````'''''......"
chars = chars[::-1]


def center_crop(img, new_width=None, new_height=None):
    width = img.shape[1]
    height = img.shape[0]

    if new_width is None:
        new_width = min(width, height)

    if new_height is None:
        new_height = min(width, height)

    left = int(np.ceil((width - new_width) / 2))
    right = width - int(np.floor((width - new_width) / 2))

    top = int(np.ceil((height - new_height) / 2))
    bottom = height - int(np.floor((height - new_height) / 2))

    if len(img.shape) == 2:
        center_cropped_img = img[top:bottom, left:right]
    else:
        center_cropped_img = img[top:bottom, left:right, ...]

    return center_cropped_img

img = Image.open("tester3.jpg")
imgArr = np.asarray(img)
bwArr = np.zeros((len(imgArr), len(imgArr[0]), 3), dtype="uint8")

# Copy Image to new array
for i in range(0, len(imgArr)):
    for j in range(0, len(imgArr[0])):
        for k in range(0, 3):
            bwArr[i][j][k] = imgArr[i, j, k]

# Turn new image into black and white
for i in range(0, len(bwArr)):
    for j in range(0, len(bwArr[0])):
        pixel = bwArr[i][j].tolist()
        # Take the average of the RGB values in the pixel
        mono = sum(pixel) / len(pixel)
        # Make a new monochrome pixel
        newPixel = [mono, mono, mono]
        bwArr[i][j] = np.asarray(newPixel)

# crop
centerBwArr = center_crop(bwArr) # Also ends up being a square
cbwi = Image.fromarray(centerBwArr)  # Centered Black and White Image
cbwi = cbwi.resize((cbwi.width // 2, cbwi.height // 2))
filter = ImageEnhance.Contrast(cbwi) # Enhance contrast
cbwi = filter.enhance(2)
centerBwArr = np.asarray(cbwi)
final = []
for i in range(0, len(centerBwArr)):
    line = ""
    for j in range(0, len(centerBwArr)):
        try:
            pixel = centerBwArr[i, j]
            brightness = pixel[0]
            line += chars[brightness]
        except Exception as e:
            print(e)
            print(brightness)
    final.append(line)

final = "\n".join(final)
with open("out.txt", "w+") as f:
    f.write(final)
