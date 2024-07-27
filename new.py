import azure.cognitiveservices.speech as speech_sdk
from dotenv import load_dotenv
import os as os
import io as io

def main(targetLanguage='ko'):
    try:
        global speech_config
        global translation_config
        # Get Configuration Settings
        load_dotenv()
        cog_key = os.getenv('COG_SERVICE_KEY')
        cog_region = os.getenv('COG_SERVICE_REGION')

        # Configure translation
        translation_config = speech_sdk.translation.SpeechTranslationConfig(cog_key, cog_region)
        translation_config.speech_recognition_language = 'en-US'
        translation_config.add_target_language(targetLanguage)
        print('Ready to translate from', translation_config.speech_recognition_language)
        # Configure speech
        speech_config = speech_sdk.SpeechConfig(cog_key, cog_region)

        # Get user input
        targetLanguage = ''

        # Comming from the end user through API
        while targetLanguage != 'quit':
            targetLanguage = input('\nEnter a target language\n wuu = Chinese\n de = German\n ms = Malay\n fr = French\n es = Spanish\n ko = Korean\n Enter anything else to stop\n').lower()
            if targetLanguage in translation_config.target_languages:
                translate(targetLanguage)
            else:
                targetLanguage = 'quit'

    except Exception as ex:
        print(ex)

def translate(targetLanguage):

    # Translate speech
    audioFile = '0902 (enhanced).wav'
    audio_config = speech_sdk.AudioConfig(filename=audioFile)
    translator = speech_sdk.translation.TranslationRecognizer(translation_config, audio_config=audio_config)
    print("Getting speech from file...")
    result = translator.recognize_once_async().get()
    print(f'Translating "{result.text}"')

    translation = result.translations[targetLanguage]
    print(translation)

    # Synthesize translation

    voices = {
        "fr": "fr-FR-HenriNeural",
        "es": "es-ES-ElviraNeural",
        "hi": "hi-IN-MadhurNeural",
        "de": "de-DE-KatjaNeural"
    }

    speech_config.speech_synthesis_voice_name = voices[targetLanguage]
    speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config)
    speak = speech_synthesizer.speak_text_async(translation).get()

    if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(speak.reason)

    else:
        output_audio_file = f"output_{targetLanguage}.wav"
        with open(output_audio_file, "rb") as audfile:
            speak.audio_data

