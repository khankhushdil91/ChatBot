from flask import Flask, request, jsonify,send_file
from flask_restful import Resource,Api
from werkzeug.utils import secure_filename
import os, sys
from pracey import audverter
current_directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_directory)
# import speeching_translate
from flask_cors import CORS
# from speeching_translate import *
# module_path = os.path.join(os.getcwd(), 'speech_translation_main/')
# print(module_path)
# # Add the path to the Python path
# sys.path.insert(1,module_path)

# app = Flask(__name__)

# api = Api(app)

app = Flask(__name__)
origins  = ['https://dev.ai.workreel.com','https://ai.workreel.com','https://www.ai.workreel.com' , 'http://localhost:8000','http://localhost:3000' , 'http://localhost:5100' , 'http://localhost:7000' , 'http://localhost:5000']
CORS(app, origins=origins)
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1  # Disable caching
api = Api(app)

errors = {
    'BadRequestError': {
        'messae':"The File is not in the correct format",
        'status':400,
        },
    
    'UserAlreadyExistsError': {
        'message': "A user with that username already exists.",
        'status': 409,
    },
    'ResourceDoesNotExist': {
        'message': "A resource with that ID no longer exists.",
        'status': 410,
        'extra': "Any extra information you want.",
    },
}

### ___________________________------------------------______________---------------------




class UploadAudio(Resource):
    ALLOWED_EXTENSIONS = ["m4a", "flac", "mp3", "mp4", "wav", "wma", "aac"]

    def post(self):
        #The file obj to be feed in model
        file = request.files["file"]
        print ('inside post request 11111111111')
        if file.filename.split(".")[-1] not in self.ALLOWED_EXTENSIONS:
            return jsonify(
                {
                    "Success":False,
                    "message": "File is not in correct format",
                }
            )
        print ('inside post request 2222222222222222')
      

        file_name = secure_filename(file.filename)
        print(f"printing the file name ::::::::::{file_name}")
        
        file_path = os.path.join('./uploads/', file_name)
        
        print(f"printing the file path {file_path}")
        
        file.save(file_path)
        lan = request.form["language"]
        gen = request.form["gender"]
        language=None
        gender=None
        # Check if the lan and gen are in quotes
        if len(lan) != 0 and len(gen) !=0:
            if lan[0] == "'" or lan[0]== '"':
                print (f"The language parameter start with ' ")
                language = lan[1:len(lan)-1]
            if gen[0] == "'" or gen[0] == '"':
                print (f"The gender parameter start with ' ")
                gender=gen[1:len(gen)-1]
        
        
        print ('inside post request 33333333333')
        
        return audverter(gender=gender, language=language, file=file_path)

        # return speeching_translate.main1(filePath= file_path, targetLanguage=lan, targetGender=gen)
        
        
        
api.add_resource(UploadAudio, "/upload_audio_file")


if __name__ == "__main__":
    app.run()

        
        
# api.add_resource(UploadAudio, "/upload_audio_file")
# if __name__ == "__main__":
#     app.run()
       
       
       
       
       
        # audioFile=""
        # textFile=""
        
        # files = [
        #     # os.path.join('uploads', 'audio.mp3'),
        #     # os.path.join('uploads', 'text.txt'),
        #     audioFile,
        #     textFile,
        # ]
        
        #Do uncomment the belsow return statement after implementing the model
        # return send_file(files, as_attachment=True, filename=[audio_fileName, text_fileName]) 
        # return jsonify(
        #     {
        #         "Success": True,
        #         "message": "Working correctly",
        #         "lan": lan,
        #         "gen": gen,
        #     }
        # )

#### ___________________________------------------------______________---------------------




#         """
#         Implement your model here. 
#         The file that the model will be utalizing is stre in {file} variable, {lan, gen} variable stores the language and gender.
#         Store the returened files in the {audio, text} variables.
        
#         """

#         files = [
#             # os.path.join('uploads', 'audio.mp3'),
#             # os.path.join('uploads', 'text.txt'),
#             audio,
#             text,
#         ]
#         # return send_file(files, as_attachment=True)
#         return jsonify(
#                 {
#                     "message": "Working correctly",
#                     "lan": lan,
#                     "gen": gen,
#                 }
#             ),            200,

# # @app.route('/file_format_error')
# # def file_format_error():
# #     return jsonify(
# #         {
# #             "message": "File is not in correct format",
# #         }
# #     ), 302


# api.add_resource(UploadAudio, "/upload_audio")

# if __name__ == "__main__":
#     app.run(debug=True)
