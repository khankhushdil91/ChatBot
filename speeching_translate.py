

from dotenv import load_dotenv
from flask import send_file, jsonify
import os as os
import io as io
import azure.cognitiveservices.speech as speech_sdk
from playsound import playsound
import zipfile as zipfile
import pathlib
import chardet as chrd

def main1(filePath, targetGender='male', targetLanguage='ko'):    
    try:        
        print ('inside tru catct 111111111111')

        global speech_config        
        global translation_config
        # Get Configuration Settings        
        load_dotenv()        
        cog_key = os.getenv('COG_SERVICE_KEY')        
        cog_region = os.getenv('COG_SERVICE_REGION')
        
        # Configure translation        
        translation_config = speech_sdk.translation.SpeechTranslationConfig(cog_key, cog_region)        
        translation_config.speech_recognition_language = 'en-US'        
        translation_config.add_target_language('fr')        
        translation_config.add_target_language('es')        
        translation_config.add_target_language('ko')
        translation_config.add_target_language('de')        
        print('Ready to translate from',translation_config.speech_recognition_language)
        # Configure speech        
        speech_config = speech_sdk.SpeechConfig(cog_key, cog_region)     
           
        # Get user input
           
        print ('inside tru catct 2222222222')
        # availabelLanguages = ['fr','es','ko','de']
        # Comming from the end user through API    
        # while targetLanguage != 'quit':            
        #     targetLanguage = input('\nEnter a target language\n wuu = Chinese\n de = German\n ms = Malay\n fr = French\n es = Spanish\n ko = Korean\n Enter anything else to stop\n').lower()            
        #     if targetLanguage in translation_config.target_languages:                
        #         translate(targetLanguage)            
        #     else:                
        #         targetLanguage = 'quit'   
        
        availabelLanguages= translation_config.target_languages
        
        print('____________________________--------------___________---------__________---------___')
       
        print( len(targetLanguage))
        # print(availabelLanguages[2])
        # targetLanguage =str(targetLanguage)
        print(targetLanguage == availabelLanguages[2])
       
        
        print(availabelLanguages)
        if  targetLanguage.strip().lower() in  availabelLanguages:   
            return translate(filePath=filePath, targetGender=targetGender, targetLanguage=targetLanguage) 
        else:
            return jsonify({
                "seccess":False,
                'error': "The languge is not in correct format"}  )
    except Exception as ex:        
        print(ex)
        
def translate(filePath,targetLanguage, targetGender ):    
    
    # Translate speech
    
    # audioFile = f'./uploads/{file.filename}'
    # with open(audioFile, 'w') as inputAudio:
    #     inputAudio.write(file.read())
    #playsound(audioFile)
    audio_config = speech_sdk.AudioConfig(filename=filePath)
    translator = speech_sdk.translation.TranslationRecognizer(translation_config, audio_config = audio_config)
    print("Getting speech from file...")
    
    result = translator.recognize_once_async().get()
    if not result.text == None or result.text != '':
        print ('result text streng in not emepty')
        print(type(result.text))
    print('Translating "{}"'.format(result.text))
     
    striped_text = result.text.strip()
    
    if len(striped_text) == 0:
        os.remove(filePath)
        return jsonify ({
            "success": False,
            'message': 'Could not translate the requested file'
        })
    
    
    print("outside the +++++++++++++++++++++++++++++++++++++++++++++++++")
    
    temp_file_path_1=f'output_translation_{targetLanguage}.txt'
    
    output_original_textfile_name=  os.path.join('./uploads/', temp_file_path_1)
    with open (output_original_textfile_name, 'w') as orgTextFile:
        orgTextFile.write(result.text)
    # textFileName=file.filename.split(".")[0]
   
    temp_file_path_2 = f"output__{targetLanguage}.txt" 
    output_text_FileName= os.path.join('./uploads/', temp_file_path_2 )
    with open(output_text_FileName, 'w') as textFile:
        textFile.write(result.translations[translation])
        
    translation = result.translations[targetLanguage]
    print(translation)
    print ('inside tru catct 333333333333333333')

    # Synthesize translation    
    """voices = {
        "fr": "fr-FR-HenriNeural",            
        "es": "es-ES-ElviraNeural",            
        "hi": "hi-IN-MadhurNeural",
        "de": "de-DE-KatjaNeural"
        }    ko-KR-SunHiNeural (Female)
            ko-KR-InJoonNeural (Male)
            ms-MY-YasminNeural (Female)
            ms-MY-OsmanNeural (Male)
            zh-CN-XiaoxiaoNeural (Female)
            zh-CN-YunxiNeural (Male)
            zh-CN-XiaozhenNeural (Female)
            zh-CN-YunfengNeural
            
            wuu-CN-XiaotongNeural2 (Female)
            wuu-CN-YunzheNeural2
    speech_config.speech_synthesis_voice_name = voices.get(targetLanguage)    
    speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config)    
    speak = speech_synthesizer.speak_text_async(translation).get()    
    """
    voices = {
        "fr": {"male": "fr-FR-DeniseNeural", "female": "fr-FR-HenriNeural"},            
        "es": {"male": "es-ES-PedroNeural", "female": "es-ES-ElviraNeural"},            
        "ko": {"male": "ko-KR-InJoonNeural", "female": "ko-KR-SunHiNeural"},
        "de": {"male": "de-DE-ConradNeural", "female": "de-DE-KatjaNeural"},
        "ms": {"male": "ms-MY-OsmanNeural", "female": "ms-MY-YasminNeural"},
        "wuu": {"male": "wuu-CN-YunzheNeural", "female": "wuu-CN-XiaotongNeural"}
    }
    
    # Prompt the user to choose the voice gender
    # pyManualInput=False
    # while pyManualInput:
    #     voice_gender = input(f"Choose voice gender for {targetLanguage} (male/female): ").strip().lower()
    #     if voice_gender in ("male", "female"):
    #         break
    #     else:
    #         print("Invalid input. Please enter 'male' or 'female'.")

     
    selected_voice = voices[targetLanguage][targetGender]
    speech_config.speech_synthesis_voice_name = selected_voice    
    speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config)    
    speak = speech_synthesizer.speak_text_async(translation).get()
    if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:        
        print(speak.reason)
    else:
        temp_file_path= f"output_{targetLanguage}_{targetGender}.wav"

        output_audio_file_name = os.path.join('./uploads/', temp_file_path)
        
        with open(output_audio_file_name, "rb") as audfile:
            audfile.write(speak.audio_data)
        # print(f"Saved synthesized audio to {output_audio_file}")
        
    os.remove(filePath)
    
    memoryFile= io.BytesIO()
    directory = pathlib.Path("./uploads/")
    for file_path in directory.iterdir():
            print(f"{file_path.name} +++++++++++++++{ file_path}")
    file_names=[temp_file_path_2, temp_file_path_1, temp_file_path]
    with zipfile.ZipFile(memoryFile, 'w') as zipObj:
            # Add multiple files to the zip
        for file_path in directory.iterdir():
            if file_path in file_names:
                zipObj.write(file_path, arcname=file_path.name)
        print ('inside tru catct 444444444444444444444444')
    os.remove(output_audio_file_name)
    os.remove(output_original_textfile_name)
    os.remove(output_text_FileName)
    return  send_file(memoryFile, as_attachment=True, mimetype='application/zip', download_name=f'{output_audio_file_name}_{output_text_FileName}.zip',) 
        
