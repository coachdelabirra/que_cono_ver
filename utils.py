"""
Utilidades varias: compartir por WhatsApp y generación de tarjetas gráficas
para el ranking, usando únicamente Pillow (sin APIs externas).
"""

import io
import urllib.parse
from PIL import Image, ImageDraw, ImageFont

from database import RATING_LEVELS

NES_BG = (20, 18, 24)
NES_ORANGE = (222, 141, 63)
NES_WHITE = (245, 245, 245)
NES_BLACK = (10, 10, 10)

# Las fuentes del sistema usadas por Pillow no siempre incluyen glifos de
# emoji a color, así que para las imagenes PNG generadas usamos texto plano.
RATING_LABELS_PLAIN = {
    0: "1 CAFE (peor)",
    1: "1 BIRRA",
    2: "2 BIRRAS",
    3: "3 BIRRAS",
    4: "4 BIRRAS",
    5: "5 BIRRAS",
    6: "6 BIRRAS - LA MAJOE",
}


def whatsapp_link(text, phone=None):
    """Genera un enlace wa.me. Si no hay telefono, abre el selector de contactos."""
    encoded = urllib.parse.quote(text)
    if phone:
        return f"https://wa.me/{phone}?text={encoded}"
    return f"https://wa.me/?text={encoded}"


def build_list_share_text(username, items):
    lines = [f"🍿 *Que coño ver!!!* de {username} #YConCervezaEsMejor", ""]
    for it in items[:15]:
        emoji = "🎬" if it["category"] == "pelicula" else "📺"
        lines.append(f"{emoji} {it['title']} — {RATING_LEVELS[it['rating']]}")
    lines.append("")
    lines.append("👉 www.rockandbirra.com")
    return "\n".join(lines)


def build_profile_share_text(username):
    return (
        f"👤 Mira mi perfil cinéfilo en *Que coño ver!!!*: {username}\n"
        f"🍺 Calificamos pelis y series en birras, de 1 café a LA MAJOE (6 birras)\n"
        f"#YConCervezaEsMejor\n"
        f"👉 www.rockandbirra.com"
    )


def _strip_non_ascii(text):
    """Quita emoji y caracteres que la fuente de Pillow no puede dibujar,
    conservando tildes y eñes españolas."""
    allowed_extra = "áéíóúÁÉÍÓÚñÑüÜ¡!¿?"
    return "".join(c for c in text if c.isascii() or c in allowed_extra).strip()


def _load_font(size, bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()


def generate_ranking_card(username, items, title="🏆 MI RANKING"):
    """Genera una tarjeta PNG estilo retro con el top de items. Devuelve bytes PNG."""
    width = 800
    row_h = 70
    header_h = 160
    top_items = items[:8]
    height = header_h + max(1, len(top_items)) * row_h + 60

    img = Image.new("RGB", (width, height), NES_BG)
    draw = ImageDraw.Draw(img)

    # borde estilo "pixel" grueso
    border = 8
    draw.rectangle([0, 0, width - 1, height - 1], outline=NES_ORANGE, width=border)

    font_title = _load_font(34, bold=True)
    font_sub = _load_font(18, bold=True)
    font_row = _load_font(22, bold=True)
    font_small = _load_font(16)

    plain_title = _strip_non_ascii(title)
    draw.text((width // 2, 40), plain_title, font=font_title, fill=NES_ORANGE, anchor="mm")
    draw.text((width // 2, 85), f"JUGADOR: {_strip_non_ascii(username)}", font=font_sub, fill=NES_WHITE, anchor="mm")
    draw.text((width // 2, 115), "#YConCervezaEsMejor", font=font_small, fill=NES_WHITE, anchor="mm")

    y = header_h
    if not top_items:
        draw.text((width // 2, y + 30), "Aun no hay titulos calificados", font=font_row, fill=NES_WHITE, anchor="mm")
    else:
        for idx, it in enumerate(top_items, start=1):
            tag = "PELI" if it["category"] == "pelicula" else "SERIE"
            label = f"{idx}. [{tag}] {_strip_non_ascii(it['title'])}"
            if len(label) > 34:
                label = label[:31] + "..."
            rating_txt = RATING_LABELS_PLAIN[it["rating"]]
            # fila con separador
            draw.line([(30, y), (width - 30, y)], fill=(60, 55, 65), width=2)
            draw.text((40, y + row_h // 2), label, font=font_row, fill=NES_WHITE, anchor="lm")
            draw.text((width - 40, y + row_h // 2), rating_txt, font=font_small, fill=NES_ORANGE, anchor="rm")
            y += row_h

    draw.text((width // 2, height - 25), "www.rockandbirra.com", font=font_small, fill=NES_ORANGE, anchor="mm")

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf.getvalue()
