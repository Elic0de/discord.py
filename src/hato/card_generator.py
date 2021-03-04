import io
import random
import glob
import textwrap
import urllib.request
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def add_text_to_image(img, text, font_path, font_size, font_color, height, width, max_length=740):
    position = (width, height)
    font = ImageFont.truetype(font_path, font_size)
    draw = ImageDraw.Draw(img)

    if draw.textsize(text, font=font)[0] > max_length:
        s_wrap_list = textwrap.wrap(text, 11)
        text = '\n'.join(s_wrap_list)
        
    draw.text(position, text, font_color, font=font)

    return img

def generate_card(author):
    username = author.name
    file = [
        f'あ！野生の{username}が飛び出してきた！',
        f'{username}がサーバーに滑り込みました。',
        f'{username}がパーティーに加わりました。',
        f'{username}がサーバーに飛び乗りました。',
        f'{username}がただいま着陸しました。',
        f'やぁ、{username} 君。ピザは持ってきたよね',
        f'{username}さん、お会いできて何よりです。',
        f'いらっしゃい{username}ちゃん。ほら、ちゃんとご挨拶して！。',
        f'{username}にご挨拶しな！',
        f'{username}さん、ようこそ。',
        f'いらっしゃい{username}ちゃん。ほら、ちゃんとご挨拶して！',
        f'やったー、{username}が来たー！',
        f'{username}がやってきました。',
        f'{username}が出たぞー！'
    ]
    
    icon = Image.open('hato/icon.png').copy()
    icon = icon.resize(size=(252, 252), resample=Image.ANTIALIAS)
    base_image_path = random.choice(glob.glob('hato/assets/images/*.png'))
    base_img = Image.open(base_image_path).copy()
    base_img = base_img.resize(size=(1100, 500), resample=Image.ANTIALIAS)
    base = base_img.copy().convert('RGBA')
    rect = Image.new('RGBA', base_img.size)
    draw = ImageDraw.Draw(rect)
    draw.rectangle((50, 50, 1050, 450), fill=(0,0,0,127))
    base_img = Image.alpha_composite(base,rect)

    mask = Image.new("L", icon.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, icon.size[0], icon.size[1]), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(1))
    icon.putalpha(mask)
    base_img.paste(icon, (80, 134), icon)

    font_path = "hato/assets/fonts/SourceHanSans-Heavy.otf"

    random_message = random.choice(file)
    font_size = 57
    font_color = (255, 255, 255)
    height = 155
    width = 380 
    img = add_text_to_image(base_img, random_message, font_path, font_size, font_color, height, width)

    welcome_message = "ようこそ hatoいろいろ鯖へ"
    font_size = 50
    font_color = (255, 255, 255)
    height = 60
    width = 80
    img = add_text_to_image(base_img, welcome_message, font_path, font_size, font_color, height, width)

    base_img.save('hato/card.png', quality=95)