import toml
from uniseg import wordbreak
from PIL import Image
from PIL import ImageDraw, ImageFont

config = toml.load("config.toml")

DESCRIPTION_FONTS = {
    "en": ImageFont.truetype("HelveticaNeue", 38, 7),
    "es": ImageFont.truetype("HelveticaNeue", 38, 7),
    "ja": ImageFont.truetype("./hiragino.ttc", 38, 0),
    "zh-CN": ImageFont.truetype("PingFang", 38, 9),
}


def wrap_text(
    font: ImageFont.ImageFont, text: str, max_width: int, direction: str = "ltr"
) -> str:
    lines: list[str] = [""]
    curr_line_width = 0

    for word in wordbreak.words(text):
        if curr_line_width == 0:
            word_width = font.getlength(word, direction)

            lines[-1] = word
            curr_line_width = word_width
        else:
            new_line_width = font.getlength(f"{lines[-1]}{word}".lstrip(), direction)

            if new_line_width > max_width:
                # Word is too long to fit on the current line
                word_width = font.getlength(word, direction)

                # Put the word on the next line
                lines.append(word)
                curr_line_width = word_width
            else:
                # Put the word on the current line
                lines[-1] = f"{lines[-1]}{word}".lstrip()
                curr_line_width = new_line_width

    return "\n".join(lines)


for lang, d in config["languages"].items():
    img = Image.new("RGB", (1200, 630), (0x21, 0x25, 0x29))

    emblem = Image.open("static/background.png").resize((500, 500))
    img.paste(
        emblem, (img.width - emblem.width + 40, img.height - emblem.height + 40), emblem
    )

    margin_h = 100
    logo_spacing = 50

    logo = Image.open("static/logo.png").resize((380, 380))
    img.paste(
        logo,
        (margin_h, img.height // 2 - logo.height // 2),
        logo,
    )

    dr = ImageDraw.Draw(img)

    title_font = ImageFont.truetype("HelveticaNeue", 84, 10)
    description_font = DESCRIPTION_FONTS.get(lang, DESCRIPTION_FONTS["en"])

    title = "Tango"
    wrapped_description = wrap_text(
        description_font,
        d["translations"]["home-lead"],
        img.width - logo.width - margin_h - logo_spacing - margin_h,
    )

    _, _, _, description_height = dr.multiline_textbbox(
        (0, 0), wrapped_description, description_font
    )
    _, _, _, title_height = dr.multiline_textbbox((0, 0), title, title_font)
    spacing = 24

    text_height = title_height + spacing + description_height
    offset = img.height // 2 - text_height // 2

    dr.fontmode = "L"
    dr.text(
        (margin_h + logo.width + logo_spacing, offset),
        "Tango",
        fill=(0xF8, 0xF9, 0xFA),
        font=title_font,
    )

    dr.text(
        (margin_h + logo.width + logo_spacing, offset + title_height + spacing),
        wrapped_description,
        fill=(0xF8, 0xF9, 0xFA),
        font=description_font,
    )

    img.save(f"static/card.{lang}.png")
