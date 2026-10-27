"""Export the selected responsive wordmark. Authoring only: Pillow + FontTools."""
from math import ceil
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'design/assets/brand/center'
FONT = ROOT / 'design/assets/fonts/seravek/Seravek-Medium.otf'
WINE, INK = '#7A1A37', '#242126'


def outlines(text, size, x, baseline, color):
    font = TTFont(FONT)
    glyphs = font.getGlyphSet()
    cmap = font.getBestCmap()
    scale = size / font['head'].unitsPerEm
    face = ImageFont.truetype(str(FONT), size)
    tracking = -.025 * size if text != 'UP' else 0
    paths = []
    for i, char in enumerate(text):
        advance = face.getlength(text[:i + 1]) - face.getlength(char)
        pen = SVGPathPen(glyphs)
        glyphs[cmap[ord(char)]].draw(TransformPen(pen, (scale, 0, 0, -scale, x + advance + i * tracking, baseline)))
        paths.append(f'<path fill="{color}" d="{pen.getCommands()}"/>')
    return ''.join(paths)


def export(name, width, height, rows, rules=()):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
           'role="img" aria-labelledby="title"><title id="title">UP Economics Research Center</title>'
           + ''.join(outlines(*row) for row in rows)
           + ''.join(f'<path d="M{x} {y1}V{y2}" stroke="#B9975B" stroke-width="1"/>' for x,y1,y2 in rules) + '</svg>\n')
    (OUT / f'{name}.svg').write_text(svg)
    ratio = 4
    image = Image.new('RGBA', (width * ratio, height * ratio), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    for text, size, x, baseline, color in rows:
        face = ImageFont.truetype(str(FONT), size * ratio)
        tracking = -.025 * size * ratio if text != 'UP' else 0
        for i,char in enumerate(text):
            advance = face.getlength(text[:i+1]) - face.getlength(char)
            draw.text((x*ratio + advance + i*tracking, baseline*ratio), char,
                      font=face, fill=color, anchor='ls')
    for x,y1,y2 in rules:
        draw.line((round(x*ratio),round(y1*ratio),round(x*ratio),round(y2*ratio)),fill='#B9975B',width=ratio)
    image.save(OUT / f'{name}.png')


OUT.mkdir(parents=True, exist_ok=True)
primary = 'UP Economics'
rows = [(primary, 30, 0, 25, INK), ('Research Center', 26, 0, 53.6, INK)]
width = ceil(max(ImageFont.truetype(str(FONT), size).getlength(text) - .025*size*(len(text)-1)
                 for text,size,*_ in rows)) + 2
for name in ('up-economics-research-center', 'up-economics-research-center-editorial'):
    export(name, width, 61, rows)
# A typographic icon shares the selected wordmark, without a box or oak.
(OUT / 'favicon.svg').write_text(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-label="UP">'
    '<style>@media(prefers-color-scheme:dark){path{fill:#eee7dc}}</style>'
    + outlines('UP', 36, 8, 45, WINE) + '</svg>\n')
icon = Image.new('RGBA', (180, 180), '#ffffff')
ImageDraw.Draw(icon).text((22, 126), 'UP', font=ImageFont.truetype(str(FONT), 100), fill=WINE, anchor='ls')
icon.save(OUT / 'apple-touch-icon.png')
print('Exported horizontal and editorial SVG/PNG wordmarks and typographic icons.')
