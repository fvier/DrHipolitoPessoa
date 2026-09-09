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

font_brand = get_font(FONT_BOLD, 22)
font_crm = get_font(FONT_SEMIBOLD, 13)
font_badge = get_font(FONT_BOLD, 13)
font_title = get_font(FONT_BOLD, 42)
font_subtitle = get_font(FONT_REGULAR, 19)
font_bullet = get_font(FONT_SEMIBOLD, 16)
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

# ==========================================================
# BANNER 1: GERIATRIA & LONGEVIDADE ATIVA
# ==========================================================
def make_banner_1():
    print("Creating Banner 1 (Geriatria)...")
    bg = create_horizontal_gradient((7, 18, 35), (14, 34, 58))
    
    # Glow behind doctor
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse([980, 20, 1880, 720], fill=(14, 116, 144, 75))
    glow = glow.filter(ImageFilter.GaussianBlur(95))
    bg = Image.alpha_composite(bg, glow)

    # Doctor photo (white coat isolated)
    doc = Image.open('larkon/static/images/dr_hipolito_isolated.png').convert("RGBA")
    doc = ImageEnhance.Brightness(doc).enhance(1.15)
    doc = ImageEnhance.Contrast(doc).enhance(1.08)
    doc = ImageEnhance.Color(doc).enhance(1.06)
    doc = doc.filter(ImageFilter.UnsharpMask(radius=2, percent=130, threshold=2))

    target_h = 750
    target_w = int(doc.width * (target_h / doc.height))
    doc_scaled = doc.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    # Balanced horizontal position
    doc_x = 1060
    bg.paste(doc_scaled, (doc_x, 0), doc_scaled)

    draw = ImageDraw.Draw(bg)

    # Left Column at x = 125
    LX = 125
    
    # Brand Top
    logo = Image.open('larkon/static/images/logo/symbol_white.png').convert("RGBA")
    logo = logo.resize((46, 46), Image.Resampling.LANCZOS)
    bg.paste(logo, (LX, 56), logo)

    draw.text((LX + 56, 58), "DR. HIPÓLITO PESSOA", font=font_brand, fill=(255, 255, 255))
    draw.text((LX + 56, 85), "GERIATRIA & PSIQUIATRIA • CRM RN 7742", font=font_crm, fill=(56, 189, 248))

    # Pill Badge
    draw_pill(draw, (LX, 126), fill=(8, 145, 178), text="GERIATRIA CLÍNICA • LONGEVIDADE ATIVA", font=font_badge, text_color=(255, 255, 255), pad_x=14, pad_y=6)

    # Title - cohesive grouping
    draw.text((LX, 175), "ENVELHECIMENTO COM DIGNIDADE,", font=font_title, fill=(255, 255, 255))
    draw.text((LX, 225), "AUTONOMIA E BEM-ESTAR", font=font_title, fill=(245, 158, 11))

    # Subtitle
    draw.text((LX, 285), "Acompanhamento médico integral com tempo de escuta ampliado,", font=font_subtitle, fill=(203, 213, 225))
    draw.text((LX, 313), "foco na prevenção de doenças e preservação da independência.", font=font_subtitle, fill=(203, 213, 225))

    # Glassmorphic Card for Bullets (x=125 to 975, width=850)
    card_box = [LX, 362, LX + 850, 528]
    draw.rounded_rectangle(card_box, radius=14, fill=(15, 23, 42, 190), outline=(56, 189, 248, 85), width=1)

    bullets = [
        "Preservação da autonomia física, funcional e cognitiva",
        "Avaliação Geriátrica Ampla (AGA) e prevenção de quedas",
        "Cuidado compartilhado e acolhimento direto aos familiares",
    ]
    by = 388
    for txt in bullets:
        draw_check_icon(draw, LX + 32, by + 9, radius=10, fill_color=(16, 185, 129))
        draw.text((LX + 56, by), txt, font=font_bullet, fill=(241, 245, 249))
        by += 44

    # Location Pill Tag directly under card
    x1, y1 = draw_pill(draw, (LX, 554), fill=(245, 158, 11), text="      ATENDIMENTO EM CONSULTÓRIO & DOMICILIAR • ALTO OESTE RN", font=font_tag, text_color=(15, 23, 42), pad_x=18, pad_y=8)
    draw_pin_icon(draw, LX + 18, 554 + 15, radius=7, fill_color=(15, 23, 42))

    out_path = "larkon/static/images/hero_banner_1_geriatria.jpg"
    bg.convert("RGB").save(out_path, "JPEG", quality=95)
    print("Saved:", out_path)

# ==========================================================
# BANNER 2: PSIQUIATRIA CLÍNICA & SAÚDE MENTAL
# ==========================================================
def make_banner_2():
    print("Creating Banner 2 (Psiquiatria)...")
    bg = create_horizontal_gradient((5, 25, 34), (10, 42, 54))

    # High-definition portrait of Dr. Hipolito in navy blue suit
    psyc_img_path = '/home/vier/.gemini/antigravity/brain/4f4fed9d-2804-4611-870f-6190a1cdc263/dr_hipolito_psiquiatria_portrait_1788975883958.jpg'
    doc2 = Image.open(psyc_img_path).convert("RGBA")
    
    target_h = 660
    target_w = int(doc2.width * (target_h / doc2.height))
    doc2_scaled = doc2.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    doc2_scaled = ImageEnhance.Brightness(doc2_scaled).enhance(1.03)
    doc2_scaled = ImageEnhance.Contrast(doc2_scaled).enhance(1.05)
    doc2_scaled = doc2_scaled.filter(ImageFilter.UnsharpMask(radius=2, percent=110, threshold=2))

    # Glassmorphism Card on right
    card_w = target_w + 20
    card_h = target_h + 20
    photo_card = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
    p_draw = ImageDraw.Draw(photo_card)
    p_draw.rounded_rectangle([0, 0, card_w, card_h], radius=22, fill=(8, 30, 38, 240), outline=(45, 212, 191, 140), width=2)
    
    mask = Image.new("L", (target_w, target_h), 0)
    m_draw = ImageDraw.Draw(mask)
    m_draw.rounded_rectangle([0, 0, target_w, target_h], radius=16, fill=255)
    
    photo_card.paste(doc2_scaled, (10, 10), mask)
    
    # Inner Badge
    draw_pill(p_draw, (24, 24), fill=(13, 148, 136), text="SAÚDE MENTAL & ACOLHIMENTO", font=font_badge, text_color=(255, 255, 255), pad_x=14, pad_y=6)

    card_x = W - card_w - 50
    card_y = (H - card_h) // 2
    bg.paste(photo_card, (card_x, card_y), photo_card)

    draw = ImageDraw.Draw(bg)

    LX = 125

    # Brand
    logo = Image.open('larkon/static/images/logo/symbol_white.png').convert("RGBA")
    logo = logo.resize((46, 46), Image.Resampling.LANCZOS)
    bg.paste(logo, (LX, 56), logo)

    draw.text((LX + 56, 58), "DR. HIPÓLITO PESSOA", font=font_brand, fill=(255, 255, 255))
    draw.text((LX + 56, 85), "GERIATRIA & PSIQUIATRIA • CRM RN 7742", font=font_crm, fill=(45, 212, 191))

    # Pill Badge
    draw_pill(draw, (LX, 126), fill=(13, 148, 136), text="PSIQUIATRIA CLÍNICA • SAÚDE MENTAL & MEMÓRIA", font=font_badge, text_color=(255, 255, 255), pad_x=14, pad_y=6)

    # Title
    draw.text((LX, 175), "SAÚDE MENTAL, MEMÓRIA E", font=font_title, fill=(255, 255, 255))
    draw.text((LX, 225), "EQUILÍBRIO EM TODAS AS IDADES", font=font_title, fill=(45, 212, 191))

    # Subtitle
    draw.text((LX, 285), "Diagnóstico atencioso, escuta acolhedora e conduta humanizada", font=font_subtitle, fill=(203, 213, 225))
    draw.text((LX, 313), "para ansiedade, depressão e bem-estar emocional na maturidade.", font=font_subtitle, fill=(203, 213, 225))

    # Card
    card_box = [LX, 362, LX + 850, 528]
    draw.rounded_rectangle(card_box, radius=14, fill=(8, 30, 38, 190), outline=(45, 212, 191, 85), width=1)

    bullets = [
        "Atenção qualificada aos transtornos de memória e do sono",
        "Manejo ético, seguro e humanizado da ansiedade e humor",
        "Apoio próximo, orientação e acolhimento aos familiares",
    ]
    by = 388
    for txt in bullets:
        draw_check_icon(draw, LX + 32, by + 9, radius=10, fill_color=(45, 212, 191), check_color=(8, 30, 38))
        draw.text((LX + 56, by), txt, font=font_bullet, fill=(241, 245, 249))
        by += 44

    # Location Pill Tag
    x1, y1 = draw_pill(draw, (LX, 554), fill=(245, 158, 11), text="      PAU DOS FERROS • SÃO MIGUEL • ALEXANDRIA • MARTINS • UMARIZAL", font=font_tag, text_color=(15, 23, 42), pad_x=18, pad_y=8)
    draw_pin_icon(draw, LX + 18, 554 + 15, radius=7, fill_color=(15, 23, 42))

    out_path = "larkon/static/images/hero_banner_2_psiquiatria.jpg"
    bg.convert("RGB").save(out_path, "JPEG", quality=95)
    print("Saved:", out_path)

# ==========================================================
# BANNER 3: ATENDIMENTO CLÍNICO & DOMICILIAR NO RN (UPRIGHT DOCTOR)
# ==========================================================
def make_banner_3():
    print("Creating Banner 3 (Upright Doctor)...")
    bg = create_horizontal_gradient((8, 22, 38), (14, 38, 62))

    # Use the upright, dignified, smiling consultation photo
    upright_img_path = '/home/vier/.gemini/antigravity/brain/4f4fed9d-2804-4611-870f-6190a1cdc263/dr_hipolito_consulta_upright2_1788975237023.jpg'
    doc3 = Image.open(upright_img_path).convert("RGBA")
    
    target_h = 660
    target_w = int(doc3.width * (target_h / doc3.height))
    doc3_scaled = doc3.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    doc3_scaled = ImageEnhance.Brightness(doc3_scaled).enhance(1.04)
    doc3_scaled = ImageEnhance.Contrast(doc3_scaled).enhance(1.05)
    doc3_scaled = doc3_scaled.filter(ImageFilter.UnsharpMask(radius=2, percent=110, threshold=2))

    # Glassmorphism Card on right
    card_w = target_w + 20
    card_h = target_h + 20
    photo_card = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
    p_draw = ImageDraw.Draw(photo_card)
    p_draw.rounded_rectangle([0, 0, card_w, card_h], radius=22, fill=(15, 30, 50, 240), outline=(56, 189, 248, 140), width=2)
    
    mask = Image.new("L", (target_w, target_h), 0)
    m_draw = ImageDraw.Draw(mask)
    m_draw.rounded_rectangle([0, 0, target_w, target_h], radius=16, fill=255)
    
    photo_card.paste(doc3_scaled, (10, 10), mask)
    
    # Inner Badge inside photo card
    draw_pill(p_draw, (24, 24), fill=(16, 185, 129), text="CONSULTA MÉDICA HUMANIZADA", font=font_badge, text_color=(255, 255, 255), pad_x=14, pad_y=6)

    card_x = W - card_w - 50
    card_y = (H - card_h) // 2
    bg.paste(photo_card, (card_x, card_y), photo_card)

    draw = ImageDraw.Draw(bg)

    LX = 125

    # Brand
    logo = Image.open('larkon/static/images/logo/symbol_white.png').convert("RGBA")
    logo = logo.resize((46, 46), Image.Resampling.LANCZOS)
    bg.paste(logo, (LX, 56), logo)

    draw.text((LX + 56, 58), "DR. HIPÓLITO PESSOA", font=font_brand, fill=(255, 255, 255))
    draw.text((LX + 56, 85), "GERIATRIA & PSIQUIATRIA • CRM RN 7742", font=font_crm, fill=(56, 189, 248))

    # Pill Badge
    draw_pill(draw, (LX, 126), fill=(217, 119, 6), text="SEGURANÇA DO PACIENTE • DESPRESCRIÇÃO & HOME CARE", font=font_badge, text_color=(255, 255, 255), pad_x=14, pad_y=6)

    # Title
    draw.text((LX, 175), "GERENCIAMENTO DE MEDICAÇÕES", font=font_title, fill=(255, 255, 255))
    draw.text((LX, 225), "E CUIDADO NO CONFORTO DO LAR", font=font_title, fill=(56, 189, 248))

    # Subtitle
    draw.text((LX, 285), "Saiba como organizar e tomar seus medicamentos da maneira correta,", font=font_subtitle, fill=(203, 213, 225))
    draw.text((LX, 313), "evitando interações perigosas e reduzindo remédios desnecessários.", font=font_subtitle, fill=(203, 213, 225))

    # Card
    card_box = [LX, 362, LX + 850, 528]
    draw.rounded_rectangle(card_box, radius=14, fill=(15, 28, 48, 190), outline=(56, 189, 248, 85), width=1)

    bullets = [
        "Prevenção de erros, horários incorretos e esquecimentos",
        "Prevenção de interações perigosas e reações adversas",
        "Desprescrição consciente e alívio da polifarmácia no idoso",
        "Visitas domiciliares para pacientes com mobilidade reduzida",
    ]
    by = 378
    for txt in bullets:
        draw_check_icon(draw, LX + 32, by + 8, radius=9, fill_color=(56, 189, 248), check_color=(15, 28, 48))
        draw.text((LX + 56, by), txt, font=get_font(FONT_SEMIBOLD, 15), fill=(241, 245, 249))
        by += 36

    # Location Pill Tag
    x1, y1 = draw_pill(draw, (LX, 554), fill=(245, 158, 11), text="      ATENDIMENTO PRESENCIAL & VISITAS DOMICILIARES NO ALTO OESTE RN", font=font_tag, text_color=(15, 23, 42), pad_x=18, pad_y=8)
    draw_pin_icon(draw, LX + 18, 554 + 15, radius=7, fill_color=(15, 23, 42))

    out_path = "larkon/static/images/hero_banner_3_medicacoes.jpg"
    bg.convert("RGB").save(out_path, "JPEG", quality=95)
    print("Saved:", out_path)

if __name__ == "__main__":
    make_banner_1()
    make_banner_2()
    make_banner_3()
    print("🚀 All 3 hero banners recreated with perfect UX/UI and upright doctor posture!")
