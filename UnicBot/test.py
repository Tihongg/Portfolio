from PIL import Image

background = Image.open("background.jpg")
foreground = Image.open("foreground.jpg")

new_width = background.width
new_height = int(foreground.height * (new_width / foreground.width))

foreground = foreground.resize((new_width, new_height))

foreground = foreground.convert("RGBA")
for x in range(foreground.width):
    for y in range(foreground.height):
        r, g, b, a = foreground.getpixel((x, y))
        foreground.putpixel((x, y), (r, g, b, int(a * 0.5)))

x = (background.width - foreground.width) // 2
y = (background.height - foreground.height) // 2

background.paste(foreground, (x, y), foreground)

background.save("result.jpg")