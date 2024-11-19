import io
from datetime import datetime
from random import randint
import requests
from PIL import Image, ImageDraw, ImageFont

import config
from main import bot


async def check_sub_channel(user_id: int):
    sub_channel = []
    verify_sub_channel = [x["id"] for x in config.SUB_CHANNEL]
    for channel in config.SUB_CHANNEL:
        chat_id = channel['id']
        user_channel_status = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
        if user_channel_status["status"] != 'left':
            sub_channel.append(chat_id)

    if sub_channel == verify_sub_channel:
        return True
    else:
        for x in sub_channel:
            verify_sub_channel.remove(x)
        return verify_sub_channel

async def set_rand_background(foreground: Image) -> Image:
    r = requests.get('https://random.responsiveimages.io/v1/docs')

    image_stream = io.BytesIO(r.content)

    background = Image.open(image_stream)

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

    return background

async def unique_image(old_image: Image) -> None:
    image = Image.new(old_image.mode, old_image.size)
    image.putdata(list(old_image.getdata()))
    pixels = image.load()
    width, height = image.size
    filter_color = (randint(0, 255), randint(0, 255), randint(0, 255))
    filter_image = Image.new("RGBA", (width, height))
    for i in range(width):
        for j in range(height): filter_image.putpixel((i,j), filter_color)
    filter_image.putalpha(int(0.075 * 255))
    image.paste(filter_image, (0, 0), filter_image)
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            rand = randint(-20, 20)
            pixels[x, y] = (r + rand, g + rand, b + rand)
    transparent_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(transparent_layer)
    width, height = image.size
    for _ in range(22):
        x1 = randint(0, width)
        y1 = randint(0, height)
        x2 = randint(0, width)
        y2 = randint(0, height)

        # Generate a random color for the line
        color = (randint(0, 255), randint(0, 255), randint(0, 255), 60)

        # Draw the line on the image
        draw.line([(x1, y1), (x2, y2)], fill=color)
    image = Image.alpha_composite(image.convert("RGBA"), transparent_layer)
    exif = image.getexif()
    curdatetime = datetime.now().strftime("%Y:%m:%d %H:%M:%S")
    exif.update([(36868, f'{curdatetime}\0')])
    exif.update([(36867, f'{curdatetime}\0')])
    exif.update([(306, f'{curdatetime}\0')])
    exif.update([(271, f'Xiaomi\0')])
    exif.update([(272, f'Redmi Note 8 Pro\0')])

    return image

async def add_text_to_image(text):
    r = requests.get('https://random.responsiveimages.io/v1/docs')
    image_stream = io.BytesIO(r.content)
    background = Image.open(image_stream)

    font_type = ImageFont.truetype("font.ttf", 40)
    draw = ImageDraw.Draw(background)
    draw.text(xy=(background.width / 2, background.height / 2), text=text, fill=(255, 38, 53), font=font_type, anchor='mm', embedded_color=True)


    return background
