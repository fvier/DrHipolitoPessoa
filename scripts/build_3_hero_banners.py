import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

W = 1920
H = 750

FONT_BOLD = "/usr/share/fonts/truetype/NotoSans-Bold.ttf"
FONT_SEMIBOLD = "/usr/share/fonts/truetype/NotoSans-SemiBold.ttf"
FONT_REGULAR = "/usr/share/fonts/truetype/OpenSans-Regular.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

font_brand = get_font(FONT_BOLD, 21)
font_crm = get_font(FONT_SEMIBOLD, 13)
font_badge = get_font(FONT_BOLD, 13)
font_title = get_font(FONT_BOLD, 45)
font_subtitle = get_font(FONT_REGULAR, 20)
font_bullet = get_font(FONT_SEMIBOLD, 17)
font_tag = get_font(FONT_BOLD, 13)

def create_horizontal_gradient(c_start, c_end, width=W, height=H):
    img = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(img)
    for x in range(width):
        t = x / width
        t_smooth = t * t * (3 - 2 * t)
        r = int(c_start[0] * (1 - t_smooth) + c_end[0] * t_smooth)
        g = int(c_start[1] * (1 - t_smooth) + c_end[1] * t_smooth)
        b = int(c_start[2] * (1 - t_smooth) + c_end[2] * t_smooth)
        draw.line([(x, 0), (x, height)], fill=(r, g, b, 255))
    return img

def draw_pill(draw, xy, fill, text, font, text_color=(255, 255, 255), pad_x=16, pad_y=7):
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x, y = xy
    x1 = x + tw + pad_x * 2
    y1 = y + th + pad_y * 2
    r = (y1 - y) // 2
    draw.rounded_rectangle([x, y, x1, y1], radius=r, fill=fill)
    draw.text((x + pad_x, y + pad_y - bbox[1]), text, font=font, fill=text_color)
    return x1, y1

def draw_check_icon(draw, cx, cy, radius=11, fill_color=(16, 185, 129), check_color=(255, 255, 255)):
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=fill_color)
    p1 = (cx - radius * 0.45, cy + radius * 0.05)
    p2 = (cx - radius * 0.1, cy + radius * 0.42)
    p3 = (cx + radius * 0.5, cy - radius * 0.35)
    draw.line([p1, p2], fill=check_color, width=2)
    draw.line([p2, p3], fill=check_color, width=2)

def draw_pin_icon(draw, cx, cy, radius=7, fill_color=(15, 23, 42)):
    draw.ellipse([cx - radius, cy - radius - 3, cx + radius, cy + radius - 3], fill=fill_color)
    draw.ellipse([cx - radius * 0.35, cy - radius * 0.35 - 3, cx + radius * 0.35, cy + radius * 0.35 - 3], fill=(245, 158, 11))
    draw.polygon([(cx - radius * 0.65, cy - 2), (cx + radius * 0.65, cy - 2), (cx, cy + radius + 3)], fill=fill_color)

def feather_left_edge(img_rgba, fade_width=180):
    w, h = img_rgba.size
    r, g, b, a = img_rgba.split()
    a_data = list(a.getdata())
    new_a = []
    for y in range(h):
        for x in range(w):
            idx = y * w + x
            orig_alpha = a_data[idx]
            if x < fade_width:
                factor = (x / fade_width) ** 1.8
                new_a.append(int(orig_alpha * factor))
            else:
                new_a.append(orig_alpha)
    a.putdata(new_a)
    img_rgba.putalpha(a)
    return img_rgba

# ==========================================================
# BANNER 1: GERIATRIA & LONGEVIDADE SAUDÁVEL
# ==========================================================
def make_banner_1():
    print("Creating Banner 1 (Geriatria)...")
    bg = create_horizontal_gradient((7, 18, 35), (12, 32, 54))
    
    # Warm radial glow behind doctor to illuminate him
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse([1150, 40, 1880, 720], fill=(14, 116, 144, 60))
    glow = glow.filter(ImageFilter.GaussianBlur(90))
    bg = Image.alpha_composite(bg, glow)

    # Doctor photo (white coat)
    doc = Image.open('larkon/static/images/dr_hipolito_isolated.png').convert("RGBA")
    # Enhance doctor: bright, sharp, lively colors
    doc = ImageEnhance.Brightness(doc).enhance(1.15)
    doc = ImageEnhance.Contrast(doc).enhance(1.08)
    doc = ImageEnhance.Color(doc).enhance(1.06)
    doc = doc.filter(ImageFilter.UnsharpMask(radius=2, percent=130, threshold=2))

    target_h = 750
    target_w = int(doc.width * (target_h / doc.height))
    doc_scaled = doc.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    doc_x = W - target_w - 20
    bg.paste(doc_scaled, (doc_x, 0), doc_scaled)

    # Left side typography
    draw = ImageDraw.Draw(bg)

    # Logo Tree of Life
    logo = Image.open('larkon/static/images/logo/symbol_white.png').convert("RGBA")
    logo = logo.resize((48, 48), Image.Resampling.LANCZOS)
    bg.paste(logo, (90, 65), logo)

    # Brand Title & CRM
    draw.text((150, 66), "DR. HIPÓLITO PESSOA", font=font_brand, fill=(255, 255, 255))
    draw.text((150, 93), "GERIATRIA & PSIQUIATRIA • CRM RN 7742", font=font_crm, fill=(56, 189, 248))

    # Pill Badge
    draw_pill(draw, (90, 142), fill=(8, 145, 178), text="GERIATRIA CLÍNICA • LONGEVIDADE ATIVA", font=font_badge, text_color=(255, 255, 255), pad_x=14, pad_y=6)

    # Title
    t1 = "ENVELHECIMENTO COM DIGNIDADE,"
    t2 = "AUTONOMIA E BEM-ESTAR"
    draw.text((90, 198), t1, font=font_title, fill=(255, 255, 255))
    draw.text((90, 254), t2, font=font_title, fill=(245, 158, 11))

    # Subtitle
    sub1 = "Acompanhamento médico integral com tempo de escuta ampliado,"
    sub2 = "foco na prevenção de doenças e preservação da independência."
    draw.text((90, 328), sub1, font=font_subtitle, fill=(203, 213, 225))
    draw.text((90, 358), sub2, font=font_subtitle, fill=(203, 213, 225))

    # Card background for bullets
    card_box = [90, 415, 870, 595]
    draw.rounded_rectangle(card_box, radius=16, fill=(15, 23, 42, 175), outline=(56, 189, 248, 75), width=1)

    bullets = [
        "Preservação da autonomia física, funcional e cognitiva",
        "Avaliação Geriátrica Ampla (AGA) e prevenção de quedas",
        "Cuidado compartilhado e acolhimento direto aos familiares",
    ]
    by = 445
    for txt in bullets:
        draw_check_icon(draw, 125, by + 9, radius=11, fill_color=(16, 185, 129))
        draw.text((150, by), txt, font=font_bullet, fill=(241, 245, 249))
        by += 48

    # Location Pill Tag with pin icon
    x1, y1 = draw_pill(draw, (90, 626), fill=(245, 158, 11), text="      ATENDIMENTO EM CONSULTÓRIO & DOMICILIAR • ALTO OESTE RN", font=font_tag, text_color=(15, 23, 42), pad_x=18, pad_y=8)
    draw_pin_icon(draw, 108, 626 + 15, radius=7, fill_color=(15, 23, 42))

    out_path = "larkon/static/images/hero_banner_1_geriatria.jpg"
    bg.convert("RGB").save(out_path, "JPEG", quality=95)
    print("Saved:", out_path)

# ==========================================================
# BANNER 2: PSIQUIATRIA CLÍNICA & SAÚDE MENTAL
# ==========================================================
def make_banner_2():
    print("Creating Banner 2 (Psiquiatria)...")
    bg = create_horizontal_gradient((5, 25, 34), (10, 42, 54))

    # Doctor photo in blue blazer (crop from image 5, start x=248 to avoid any text letters)
    src = Image.open('/home/vier/.gemini/antigravity/brain/4f4fed9d-2804-4611-870f-6190a1cdc263/.user_uploaded/media_1788971654958.png').convert("RGBA")
    w, h = src.size
    doc_crop = src.crop((248, 0, w, h))
    
    target_h = 750
    target_w = int(doc_crop.width * (target_h / doc_crop.height))
    doc_scaled = doc_crop.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    # Enhance lighting so doctor is bright & vivid
    doc_scaled = ImageEnhance.Brightness(doc_scaled).enhance(1.12)
    doc_scaled = ImageEnhance.Contrast(doc_scaled).enhance(1.08)
    doc_scaled = ImageEnhance.Color(doc_scaled).enhance(1.05)
    doc_scaled = doc_scaled.filter(ImageFilter.UnsharpMask(radius=2, percent=125, threshold=2))
    
    # Feather left edge
    doc_scaled = feather_left_edge(doc_scaled, fade_width=160)

    doc_x = W - target_w
    bg.paste(doc_scaled, (doc_x, 0), doc_scaled)

    draw = ImageDraw.Draw(bg)

    # Logo Tree of Life
    logo = Image.open('larkon/static/images/logo/symbol_white.png').convert("RGBA")
    logo = logo.resize((48, 48), Image.Resampling.LANCZOS)
    bg.paste(logo, (90, 65), logo)

    draw.text((150, 66), "DR. HIPÓLITO PESSOA", font=font_brand, fill=(255, 255, 255))
    draw.text((150, 93), "GERIATRIA & PSIQUIATRIA • CRM RN 7742", font=font_crm, fill=(45, 212, 191))

    # Pill Badge
    draw_pill(draw, (90, 142), fill=(13, 148, 136), text="PSIQUIATRIA CLÍNICA • SAÚDE MENTAL & MEMÓRIA", font=font_badge, text_color=(255, 255, 255), pad_x=14, pad_y=6)

    # Title
    t1 = "SAÚDE MENTAL, MEMÓRIA E"
    t2 = "EQUILÍBRIO EM TODAS AS IDADES"
    draw.text((90, 198), t1, font=font_title, fill=(255, 255, 255))
    draw.text((90, 254), t2, font=font_title, fill=(45, 212, 191))

    # Subtitle
    sub1 = "Diagnóstico atencioso, escuta acolhedora e conduta humanizada"
    sub2 = "para ansiedade, depressão e bem-estar emocional na maturidade."
    draw.text((90, 328), sub1, font=font_subtitle, fill=(203, 213, 225))
    draw.text((90, 358), sub2, font=font_subtitle, fill=(203, 213, 225))

    # Card background for bullets
    card_box = [90, 415, 870, 595]
    draw.rounded_rectangle(card_box, radius=16, fill=(8, 30, 38, 180), outline=(45, 212, 191, 75), width=1)

    bullets = [
        "Atenção qualificada aos transtornos de memória e do sono",
        "Manejo ético, seguro e humanizado da ansiedade e humor",
        "Apoio próximo, orientação e acolhimento aos familiares",
    ]
    by = 445
    for txt in bullets:
        draw_check_icon(draw, 125, by + 9, radius=11, fill_color=(45, 212, 191), check_color=(8, 30, 38))
        draw.text((150, by), txt, font=font_bullet, fill=(241, 245, 249))
        by += 48

    # Location Pill Tag
    x1, y1 = draw_pill(draw, (90, 626), fill=(245, 158, 11), text="      PAU DOS FERROS • SÃO MIGUEL • ALEXANDRIA • MARTINS • UMARIZAL", font=font_tag, text_color=(15, 23, 42), pad_x=18, pad_y=8)
    draw_pin_icon(draw, 108, 626 + 15, radius=7, fill_color=(15, 23, 42))

    out_path = "larkon/static/images/hero_banner_2_psiquiatria.jpg"
    bg.convert("RGB").save(out_path, "JPEG", quality=95)
    print("Saved:", out_path)

# ==========================================================
# BANNER 3: ATENDIMENTO CLÍNICO & DOMICILIAR NO RN
# ==========================================================
def make_banner_3():
    print("Creating Banner 3 (Atendimento Clínico & Domiciliar)...")
    bg = create_horizontal_gradient((8, 22, 38), (14, 38, 62))

    # Right side: Consultation card featuring Dr. Hipolito attending a patient
    med3 = Image.open('/home/vier/.gemini/antigravity/brain/4f4fed9d-2804-4611-870f-6190a1cdc263/.user_uploaded/media_1788971593985.png').convert("RGBA")
    w, h = med3.size
    med3_crop = med3.crop((0, 0, w, int(h * 0.76))) # crop out caption text
    
    # Scale to height 650 to fit inside an elegant modern photo card
    target_h = 650
    target_w = int(med3_crop.width * (target_h / med3_crop.height))
    med3_scaled = med3_crop.resize((target_w, target_h), Image.Resampling.LANCZOS)
    med3_scaled = ImageEnhance.Brightness(med3_scaled).enhance(1.10)
    med3_scaled = ImageEnhance.Contrast(med3_scaled).enhance(1.08)
    med3_scaled = med3_scaled.filter(ImageFilter.UnsharpMask(radius=2, percent=120, threshold=2))

    # Create a rounded card with border and shadow for the consultation photo
    card_w = target_w + 24
    card_h = target_h + 24
    photo_card = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
    p_draw = ImageDraw.Draw(photo_card)
    p_draw.rounded_rectangle([0, 0, card_w, card_h], radius=24, fill=(15, 30, 50, 240), outline=(56, 189, 248, 120), width=2)
    
    # Rounded mask for the image itself
    mask = Image.new("L", (target_w, target_h), 0)
    m_draw = ImageDraw.Draw(mask)
    m_draw.rounded_rectangle([0, 0, target_w, target_h], radius=18, fill=255)
    
    photo_card.paste(med3_scaled, (12, 12), mask)
    
    # Badge inside the photo card
    draw_pill(p_draw, (24, 24), fill=(16, 185, 129), text="CONSULTA MÉDICA HUMANIZADA", font=font_badge, text_color=(255, 255, 255), pad_x=12, pad_y=5)

    # Paste photo card on the right
    card_x = W - card_w - 70
    card_y = (H - card_h) // 2
    bg.paste(photo_card, (card_x, card_y), photo_card)

    draw = ImageDraw.Draw(bg)

    # Logo Tree of Life
    logo = Image.open('larkon/static/images/logo/symbol_white.png').convert("RGBA")
    logo = logo.resize((48, 48), Image.Resampling.LANCZOS)
    bg.paste(logo, (90, 65), logo)

    draw.text((150, 66), "DR. HIPÓLITO PESSOA", font=font_brand, fill=(255, 255, 255))
    draw.text((150, 93), "GERIATRIA & PSIQUIATRIA • CRM RN 7742", font=font_crm, fill=(56, 189, 248))

    # Pill Badge
    draw_pill(draw, (90, 142), fill=(217, 119, 6), text="SEGURANÇA DO PACIENTE • DESPRESCRIÇÃO & HOME CARE", font=font_badge, text_color=(255, 255, 255), pad_x=14, pad_y=6)

    # Title
    t1 = "GERENCIAMENTO DE MEDICAÇÕES"
    t2 = "E CUIDADO NO CONFORTO DO LAR"
    draw.text((90, 198), t1, font=font_title, fill=(255, 255, 255))
    draw.text((90, 254), t2, font=font_title, fill=(56, 189, 248))

    # Subtitle
    sub1 = "Saiba como organizar e tomar seus medicamentos da maneira correta,"
    sub2 = "evitando interações perigosas e reduzindo remédios desnecessários."
    draw.text((90, 328), sub1, font=font_subtitle, fill=(203, 213, 225))
    draw.text((90, 358), sub2, font=font_subtitle, fill=(203, 213, 225))

    # Card background for bullets
    card_box = [90, 415, 870, 595]
    draw.rounded_rectangle(card_box, radius=16, fill=(15, 28, 48, 180), outline=(56, 189, 248, 75), width=1)

    bullets = [
        "Prevenção de erros, horários incorretos e esquecimentos",
        "Prevenção de interações perigosas e reações adversas",
        "Desprescrição consciente e alívio da polifarmácia no idoso",
        "Visitas domiciliares para pacientes acamados ou com mobilidade reduzida",
    ]
    by = 432
    for txt in bullets:
        draw_check_icon(draw, 125, by + 8, radius=10, fill_color=(56, 189, 248), check_color=(15, 28, 48))
        draw.text((150, by), txt, font=get_font(FONT_SEMIBOLD, 16), fill=(241, 245, 249))
        by += 38

    # Location Pill Tag
    x1, y1 = draw_pill(draw, (90, 626), fill=(245, 158, 11), text="      ATENDIMENTO PRESENCIAL & VISITAS DOMICILIARES NO ALTO OESTE RN", font=font_tag, text_color=(15, 23, 42), pad_x=18, pad_y=8)
    draw_pin_icon(draw, 108, 626 + 15, radius=7, fill_color=(15, 23, 42))

    out_path = "larkon/static/images/hero_banner_3_medicacoes.jpg"
    bg.convert("RGB").save(out_path, "JPEG", quality=95)
    print("Saved:", out_path)

if __name__ == "__main__":
    make_banner_1()
    make_banner_2()
    make_banner_3()
    print("🎉 All 3 hero banners re-built with vector icons and perfect aesthetics!")
