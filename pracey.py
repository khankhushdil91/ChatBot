import speech_recognition as sr
from deep_translator import GoogleTranslator
import os
from azure.cognitiveservices import speech as speechsdk 
from dotenv import load_dotenv
from flask import jsonify, send_file

def audverter(file : any, language: str, gender:str):
  
    global speech_config        
    #global translation_config
            # Get Configuration Settings        
    load_dotenv()        
    cog_key = os.getenv('COG_SERVICE_KEY')        
    cog_region = os.getenv('COG_SERVICE_REGION')
    speech_config = speechsdk.SpeechConfig(cog_key, cog_region)

    # Initialize recognizer class (for recognizing the speech)
    recognizer = sr.Recognizer()

    # Reading Audio file as source
    # Listening to the audio file and storing it in audio_text variable
    with sr.AudioFile(file) as source:
        audio_text = recognizer.listen(source)
        
    

    # Recognize_() method will throw a request error if the API is unreachable, hence using exception handling
    try:
        # Using Google Speech Recognition to transcribe the audio
        orig_text = recognizer.recognize_google(audio_text)
        print('Converting audio transcripts into text ...')
        print(orig_text)
        
    except sr.UnknownValueError:
       return jsonify ({
           "success":False,
           'data': 'Google Speech Recognition could not understand audio'
       })
    except sr.RequestError as e:
        return jsonify ({"success": False,
                         'data':'Could not request results from Google Speech Recognition service; {e}'})
        
    #TODO: set gender and language params here
    # Function to translate text to the target language
    def Translate(targetLanguage, target_gender):
        translated = GoogleTranslator(source="auto", target=targetLanguage).translate(orig_text)
        print(f'Translated to \n {targetLanguage}: {translated}')
        
        voices = {
            "fr": {"male": "fr-FR-DeniseNeural", "female": "fr-FR-HenriNeural"},            
            "es": {"male": "es-ES-PedroNeural", "female": "es-ES-ElviraNeural"},            
            "ko": {"male": "ko-KR-InJoonNeural", "female": "ko-KR-SunHiNeural"},
            "de": {"male": "de-DE-ConradNeural", "female": "de-DE-KatjaNeural"},
            "ms": {"male": "ms-MY-OsmanNeural", "female": "ms-MY-YasminNeural"},
            "wuu": {"male": "wuu-CN-YunzheNeural", "female": "wuu-CN-XiaotongNeural"}
        }
        
        # Prompt the user to choose the voice gender
        # while True:
        #     voice_gender = input(f"Choose voice gender for {targetLanguage} (male/female): ").strip().lower()
        #     if voice_gender in ("male", "female"):
        #         break
        #     else:
        #         print("Invalid input. Please enter 'male' or 'female'.")
                
        # TODO: Input your target language and voice sex here
        selected_voice = voices[targetLanguage][target_gender]
        speech_config.speech_synthesis_voice_name = selected_voice
        
        #speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)    
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)    
        speak = speech_synthesizer.speak_text_async(translated).get()
        if speak.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:        
            print(speak.reason)
        else:
            output_audio_file = os.path.join(f"output_{targetLanguage}_{voice_gender}.wav")
            with open(output_audio_file, "wb") as file:
                file.write(speak.audio_data)
            print(f"Saved synthesized audio to {output_audio_file}")
            
    # TODO: Remove the below code and send the actual files.
    # Loop to continuously prompt for target languages until 'quit' is entered
    # targetLanguage = ''
    # while targetLanguage != 'quit':
    #     # targetLanguage = input('\nEnter a target language ("de", "fr", "es", "ko", or "quit" to stop)\n').lower()
    #     if targetLanguage != 'quit':
    Translate(language, gender)
    
    return jsonify({
        'success': True,
        'data': "successfuly translated the file"
    })    
