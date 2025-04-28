import os
import tempfile
from pydub import AudioSegment
import speech_recognition as sr
from gtts import gTTS
from deep_translator import GoogleTranslator



def convert_mp3_to_wav(input_path, output_path):
    """Convert MP3 file to WAV format."""
    try:
        audio = AudioSegment.from_mp3(input_path)
        audio.export(output_path, format="wav")
    except Exception as e:
        print(f"❌ Error converting MP3 to WAV: {e}")
        raise


def transcribe_audio(audio_path, language_code):
    """Transcribe audio file to text using speech recognition."""
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)
        return recognizer.recognize_google(audio, language=language_code)
    except Exception as e:
        print(f"❌ Speech recognition failed: {e}")
        raise


def translate_text(text, source_language='auto', target_language='english'):
    """Translate text using Deep Translator with optional source language."""
    try:
        translated = GoogleTranslator(source=source_language, target=target_language).translate(text)
        print(f"🔹 Translated Text ({source_language} → {target_language}): {translated}")
        return translated
    except Exception as e:
        print(f"❌ Translation failed: {e}")
        return text  # Return original text as fallback


def text_to_speech(text, output_path, language='en'):
    """Convert text to speech using gTTS."""
    try:
        tts = gTTS(text=text, lang=language)
        tts.save(output_path)
    except Exception as e:
        print(f"❌ Text-to-speech failed: {e}")
        raise


def get_speech_recognition_language_code(language_code):
    """Map of ISO language codes to Google Speech Recognition-compatible locale formats."""
    language_map = {
        'af': 'af-ZA',
        'sq': 'sq-AL',
        'am': 'am-ET',
        'ar': 'ar-SA',
        'hy': 'hy-AM',
        'az': 'az-AZ',
        'eu': 'eu-ES',
        'be': 'be-BY',
        'bn': 'bn-IN',
        'bs': 'bs-BA',
        'bg': 'bg-BG',
        'ca': 'ca-ES',
        'ceb': 'ceb-PH',
        'ny': 'ny-MW',
        'zh-cn': 'zh-CN',
        'zh-tw': 'zh-TW',
        'co': 'co-FR',
        'hr': 'hr-HR',
        'cs': 'cs-CZ',
        'da': 'da-DK',
        'nl': 'nl-NL',
        'en': 'en-US',
        'eo': 'eo',
        'et': 'et-EE',
        'tl': 'fil-PH',
        'fi': 'fi-FI',
        'fr': 'fr-FR',
        'fy': 'fy-NL',
        'gl': 'gl-ES',
        'ka': 'ka-GE',
        'de': 'de-DE',
        'el': 'el-GR',
        'gu': 'gu-IN',
        'ht': 'ht-HT',
        'ha': 'ha-NG',
        'haw': 'haw-US',
        'he': 'he-IL',
        'hi': 'hi-IN',
        'hmn': 'hmn',
        'hu': 'hu-HU',
        'is': 'is-IS',
        'ig': 'ig-NG',
        'id': 'id-ID',
        'ga': 'ga-IE',
        'it': 'it-IT',
        'ja': 'ja-JP',
        'jw': 'jv-ID',
        'kn': 'kn-IN',
        'kk': 'kk-KZ',
        'km': 'km-KH',
        'ko': 'ko-KR',
        'ku': 'ku-TR',
        'ky': 'ky-KG',
        'lo': 'lo-LA',
        'la': 'la',
        'lv': 'lv-LV',
        'lt': 'lt-LT',
        'lb': 'lb-LU',
        'mk': 'mk-MK',
        'mg': 'mg-MG',
        'ms': 'ms-MY',
        'ml': 'ml-IN',
        'mt': 'mt-MT',
        'mi': 'mi-NZ',
        'mr': 'mr-IN',
        'mn': 'mn-MN',
        'my': 'my-MM',
        'ne': 'ne-NP',
        'no': 'nb-NO',
        'or': 'or-IN',
        'ps': 'ps-AF',
        'fa': 'fa-IR',
        'pl': 'pl-PL',
        'pt': 'pt-PT',
        'pa': 'pa-Guru-IN',
        'ro': 'ro-RO',
        'ru': 'ru-RU',
        'sm': 'sm-WS',
        'gd': 'gd-GB',
        'sr': 'sr-RS',
        'st': 'st-LS',
        'sn': 'sn-ZW',
        'sd': 'sd-IN',
        'si': 'si-LK',
        'sk': 'sk-SK',
        'sl': 'sl-SI',
        'so': 'so-SO',
        'es': 'es-ES',
        'su': 'su-ID',
        'sw': 'sw-KE',
        'sv': 'sv-SE',
        'tg': 'tg-TJ',
        'ta': 'ta-IN',
        'te': 'te-IN',
        'th': 'th-TH',
        'tr': 'tr-TR',
        'uk': 'uk-UA',
        'ur': 'ur-PK',
        'ug': 'ug-CN',
        'uz': 'uz-UZ',
        'vi': 'vi-VN',
        'cy': 'cy-GB',
        'xh': 'xh-ZA',
        'yi': 'yi',
        'yo': 'yo-NG',
        'zu': 'zu-ZA'
    }
    return language_map.get(language_code.lower(), 'en-US')  # Default to English if unsupported



