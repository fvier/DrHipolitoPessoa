from django.conf import settings

def store_info(request):
    """Disponibiliza os dados de contato, endereço, horários e redes sociais do Dr. Hipólito Pessoa globalmente em todos os templates."""
    info = getattr(settings, "VAKARIA_INFO", {})
    return {
        "STORE_NAME": info.get("NAME", "Dr. Hipólito Pessoa"),
        "STORE_CRM": "CRM RN 7742",
        "STORE_SPECIALTY": "Geriatria e Psiquiatria",
        "STORE_ADDRESS": info.get("ADDRESS", "Pau dos Ferros, São Miguel, Alexandria, Martins e Umarizal - RN"),
        "STORE_CITY": info.get("CITY", "Pau dos Ferros - RN"),
        "STORE_PHONE": info.get("PHONE", "+55 84 9 9617-9445"),
        "STORE_WHATSAPP_NUMBER": info.get("WHATSAPP_NUMBER", "5584996179445"),
        "STORE_WHATSAPP_URL": info.get("WHATSAPP_URL", "https://wa.me/5584996179445"),
        "STORE_WHATSAPP_GROUP_URL": info.get("WHATSAPP_GROUP_URL", "https://wa.me/5584996179445"),
        "STORE_INSTAGRAM_URL": info.get("INSTAGRAM_URL", "https://www.instagram.com/drhipolitopessoa/"),
        "STORE_INSTAGRAM_HANDLE": info.get("INSTAGRAM_HANDLE", "@drhipolitopessoa"),
        "STORE_SCHEDULE_HOURS": info.get("SCHEDULE_HOURS", "08:00 - 17:00 (Segunda a Sexta)"),
    }

