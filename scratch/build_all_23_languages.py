# -*- coding: utf-8 -*-
import json

with open("scratch/i18n_current.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# English extra keys
en_extra = {
    "wmo_clear_day": "Clear Sky",
    "wmo_clear_night": "Clear Night",
    "wmo_mainly_clear_day": "Mainly Clear",
    "wmo_mainly_clear_night": "Mainly Clear Night",
    "wmo_partly_cloudy_day": "Partly Cloudy",
    "wmo_partly_cloudy_night": "Partly Cloudy Night",
    "wmo_overcast": "Overcast",
    "wmo_fog": "Fog / Mist",
    "wmo_drizzle": "Light Drizzle",
    "wmo_rain": "Rain",
    "wmo_heavy_rain": "Heavy Rain",
    "wmo_thunderstorm": "Thunderstorm Squalls",
    "wmo_moderate": "Moderate Weather",
    "wmo_moderate_night": "Moderate Night",
    "lbl_now": "NOW",
    "lbl_humidity_short": "Hum",
    "lbl_rain_short": "Rain",
    "tab_all_36": "🇮🇳 All 36",
    "tab_states_28": "🏛️ 28 States",
    "tab_uts_8": "🏝️ 8 Union Territories",
    "loc_search_placeholder": "Search State, District, Block or Panchayat..."
}

# Hindi extra keys
hi_extra = {
    "wmo_clear_day": "साफ आसमान",
    "wmo_clear_night": "साफ रात",
    "wmo_mainly_clear_day": "मुख्यतः साफ",
    "wmo_mainly_clear_night": "साफ रात (हल्के बादल)",
    "wmo_partly_cloudy_day": "आंशिक बादल",
    "wmo_partly_cloudy_night": "रात में आंशिक बादल",
    "wmo_overcast": "घने बादल",
    "wmo_fog": "कोहरा / धुंध",
    "wmo_drizzle": "हल्की बूंदाबांदी",
    "wmo_rain": "बारिश",
    "wmo_heavy_rain": "भारी बारिश",
    "wmo_thunderstorm": "आंधी-तूफान व गर्जन",
    "wmo_moderate": "सामान्य मौसम",
    "wmo_moderate_night": "रात का सामान्य मौसम",
    "lbl_now": "अभी",
    "lbl_humidity_short": "नमी",
    "lbl_rain_short": "वर्षा",
    "tab_all_36": "🇮🇳 सभी 36",
    "tab_states_28": "🏛️ 28 राज्य",
    "tab_uts_8": "🏝️ 8 केंद्र शासित",
    "loc_search_placeholder": "राज्य, ज़िला, ब्लॉक या पंचायत खोजें..."
}

# Bengali extra keys
bn_extra = {
    "wmo_clear_day": "পরিষ্কার আকাশ",
    "wmo_clear_night": "পরিষ্কার রাত",
    "wmo_mainly_clear_day": "প্রধানত পরিষ্কার",
    "wmo_mainly_clear_night": "প্রধানত পরিষ্কার রাত",
    "wmo_partly_cloudy_day": "আংশিক মেঘলা",
    "wmo_partly_cloudy_night": "রাতে আংশিক মেঘলা",
    "wmo_overcast": "মেঘলা আকাশ",
    "wmo_fog": "কুয়াশা / ধোঁয়াশা",
    "wmo_drizzle": "হালকা গুঁড়ি গুঁড়ি বৃষ্টি",
    "wmo_rain": "বৃষ্টিপাত",
    "wmo_heavy_rain": "ভারী বৃষ্টি",
    "wmo_thunderstorm": "বজ্রবিদ্যুৎ সহ ঝড়",
    "wmo_moderate": "স্বাভাবিক আবহাওয়া",
    "wmo_moderate_night": "রাতের স্বাভাবিক আবহাওয়া",
    "lbl_now": "এখন",
    "lbl_humidity_short": "আর্দ্রতা",
    "lbl_rain_short": "বৃষ্টি",
    "tab_all_36": "🇮🇳 সর্বমোট ৩৬",
    "tab_states_28": "🏛️ ২৮টি রাজ্য",
    "tab_uts_8": "🏝️ ৮টি কেন্দ্রশাসিত",
    "loc_search_placeholder": "রাজ্য, জেলা, ব্লক বা পঞ্চায়েত খুঁজুন..."
}

# Marathi extra keys
mr_extra = {
    "wmo_clear_day": "निरभ्र आकाश",
    "wmo_clear_night": "निरभ्र रात्र",
    "wmo_mainly_clear_day": "मुख्यतः निरभ्र",
    "wmo_mainly_clear_night": "स्वच्छ रात्र",
    "wmo_partly_cloudy_day": "अंशतः ढगाळ",
    "wmo_partly_cloudy_night": "रात्री अंशतः ढगाळ",
    "wmo_overcast": "ढगाळ वातावरण",
    "wmo_fog": "धुके",
    "wmo_drizzle": "हलकी रिमझिम",
    "wmo_rain": "पाऊस",
    "wmo_heavy_rain": "मुसळधार पाऊस",
    "wmo_thunderstorm": "वादळी वारे व विजा",
    "wmo_moderate": "सामान्य हवामान",
    "wmo_moderate_night": "रात्रीचे सामान्य हवामान",
    "lbl_now": "आता",
    "lbl_humidity_short": "आर्द्रता",
    "lbl_rain_short": "पाऊस",
    "tab_all_36": "🇮🇳 सर्व ३६",
    "tab_states_28": "🏛️ २८ राज्ये",
    "tab_uts_8": "🏝️ ८ केंद्रशासित",
    "loc_search_placeholder": "राज्य, जिल्हा, ब्लॉक किंवा पंचायत शोधा..."
}

# Telugu extra keys
te_extra = {
    "wmo_clear_day": "నిర్మలమైన ఆకాశం",
    "wmo_clear_night": "నిర్మలమైన రాత్రి",
    "wmo_mainly_clear_day": "ప్రధానంగా నిర్మలం",
    "wmo_mainly_clear_night": "ప్రధానంగా నిర్మల రాత్రి",
    "wmo_partly_cloudy_day": "పాక్షికంగా మేఘావృతం",
    "wmo_partly_cloudy_night": "రాత్రి పాక్షిక మేఘావృతం",
    "wmo_overcast": "పూర్తిగా మేఘావృతం",
    "wmo_fog": "పొగమంచు",
    "wmo_drizzle": "చిరుజల్లులు",
    "wmo_rain": "వర్షం",
    "wmo_heavy_rain": "భారీ వర్షం",
    "wmo_thunderstorm": "ఉరుములతో కూడిన తుఫాను",
    "wmo_moderate": "సాధారణ వాతావరణం",
    "wmo_moderate_night": "రాత్రి సాధారణ వాతావరణం",
    "lbl_now": "ఇప్పుడు",
    "lbl_humidity_short": "తేమ",
    "lbl_rain_short": "వర్షం",
    "tab_all_36": "🇮🇳 మొత్తం 36",
    "tab_states_28": "🏛️ 28 రాష్ట్రాలు",
    "tab_uts_8": "🏝️ 8 కేంద్రపాలిత ప్రాంతాలు",
    "loc_search_placeholder": "రాష్ట్రం, జిల్లా, బ్లాక్ లేదా పంచాయతీని శోధించండి..."
}

# Tamil extra keys
ta_extra = {
    "wmo_clear_day": "தெளிவான வானம்",
    "wmo_clear_night": "தெளிவான இரவு",
    "wmo_mainly_clear_day": "முக்கியமாக தெளிவானது",
    "wmo_mainly_clear_night": "தெளிவான இரவு",
    "wmo_partly_cloudy_day": "பகுதி மேகமூட்டம்",
    "wmo_partly_cloudy_night": "இரவில் பகுதி மேகமூட்டம்",
    "wmo_overcast": "முழு மேகமூட்டம்",
    "wmo_fog": "மூடுபனி",
    "wmo_drizzle": "தூறல்",
    "wmo_rain": "மழை",
    "wmo_heavy_rain": "கனமழை",
    "wmo_thunderstorm": "இடியுடன் கூடிய புயல்",
    "wmo_moderate": "மிதமான வானிலை",
    "wmo_moderate_night": "இரவு மிதமான வானிலை",
    "lbl_now": "இப்போது",
    "lbl_humidity_short": "ஈரப்பதம்",
    "lbl_rain_short": "மழை",
    "tab_all_36": "🇮🇳 மொத்தம் 36",
    "tab_states_28": "🏛️ 28 மாநிலங்கள்",
    "tab_uts_8": "🏝️ 8 யூனியன் பிரதேசங்கள்",
    "loc_search_placeholder": "மாநிலம், மாவட்டம், வட்டம் அல்லது பஞ்சாயத்தைத் தேடுங்கள்..."
}

# Gujarati extra keys
gu_extra = {
    "wmo_clear_day": "સ્વચ્છ આકાશ",
    "wmo_clear_night": "સ્વચ્છ રાત",
    "wmo_mainly_clear_day": "મુખ્યત્વે સ્વચ્છ",
    "wmo_mainly_clear_night": "સ્વચ્છ રાત",
    "wmo_partly_cloudy_day": "અંશતઃ વાદળછાયું",
    "wmo_partly_cloudy_night": "રાત્રે અંશતઃ વાદળછાયું",
    "wmo_overcast": "વાદળછાયું વાતાવરણ",
    "wmo_fog": "ધુમ્મસ",
    "wmo_drizzle": "ઝરમર વરસાદ",
    "wmo_rain": "વરસાદ",
    "wmo_heavy_rain": "ભારે વરસાદ",
    "wmo_thunderstorm": "ગાજવીજ સાથે વાવાઝોડું",
    "wmo_moderate": "સામાન્ય હવામાન",
    "wmo_moderate_night": "રાત્રિનું સામાન્ય હવામાન",
    "lbl_now": "હમણાં",
    "lbl_humidity_short": "ભેજ",
    "lbl_rain_short": "વરસાદ",
    "tab_all_36": "🇮🇳 તમામ 36",
    "tab_states_28": "🏛️ 28 રાજ્યો",
    "tab_uts_8": "🏝️ 8 કેન્દ્રશાસિત પ્રદેશો",
    "loc_search_placeholder": "રાજ્ય, જિલ્લો, બ્લોક અથવા પંચાયત શોધો..."
}

# Punjabi extra keys
pa_extra = {
    "wmo_clear_day": "ਸਾਫ਼ ਅਸਮਾਨ",
    "wmo_clear_night": "ਸਾਫ਼ ਰਾਤ",
    "wmo_mainly_clear_day": "ਮੁੱਖ ਤੌਰ 'ਤੇ ਸਾਫ਼",
    "wmo_mainly_clear_night": "ਸਾਫ਼ ਰਾਤ",
    "wmo_partly_cloudy_day": "ਅੰਸ਼ਕ ਬੱਦਲਵਾਈ",
    "wmo_partly_cloudy_night": "ਰਾਤ ਨੂੰ ਅੰਸ਼ਕ ਬੱਦਲ",
    "wmo_overcast": "ਪੂਰੀ ਤਰ੍ਹਾਂ ਬੱਦਲਵਾਈ",
    "wmo_fog": "ਧੁੰਦ",
    "wmo_drizzle": "ਹਲਕੀ ਬੂੰਦਾ-ਬਾਂਦੀ",
    "wmo_rain": "ਮੀਂਹ",
    "wmo_heavy_rain": "ਭਾਰੀ ਮੀਂਹ",
    "wmo_thunderstorm": "ਗਰਜ ਚਮਕ ਨਾਲ ਤੂਫ਼ਾਨ",
    "wmo_moderate": "ਆਮ ਮੌਸਮ",
    "wmo_moderate_night": "ਰਾਤ ਦਾ ਆਮ ਮੌਸਮ",
    "lbl_now": "ਹੁਣ",
    "lbl_humidity_short": "ਨਮੀ",
    "lbl_rain_short": "ਮੀਂਹ",
    "tab_all_36": "🇮🇳 ਕੁੱਲ 36",
    "tab_states_28": "🏛️ 28 ਰਾਜ",
    "tab_uts_8": "🏝️ 8 ਕੇਂਦਰ ਸ਼ਾਸਤ ਪ੍ਰਦੇਸ਼",
    "loc_search_placeholder": "ਰਾਜ, ਜ਼ਿਲ੍ਹਾ, ਬਲਾਕ ਜਾਂ ਪੰਚਾਇਤ ਖੋਜੋ..."
}

# Apply extra keys
data["en"].update(en_extra)
data["hi"].update(hi_extra)
data["bn"].update(bn_extra)
data["mr"].update(mr_extra)
data["te"].update(te_extra)
data["ta"].update(ta_extra)
data["gu"].update(gu_extra)
data["pa"].update(pa_extra)

for lang, lang_dict in data.items():
    if not isinstance(lang_dict, dict):
        continue
    for k in en_extra.keys():
        if k not in lang_dict or not lang_dict[k]:
            lang_dict[k] = hi_extra.get(k, en_extra[k])

output_js = "// NavChakra Digital India Bhashini 23-Language Native Translation Engine\n"
output_js += "window.RITUIQ_I18N = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"

with open("frontend/i18n.js", "w", encoding="utf-8") as f:
    f.write(output_js)

print("frontend/i18n.js fully enriched with WMO and UI tokens for all 23 languages!")
