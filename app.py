from flask import Flask, render_template, request, send_from_directory
import os 
from deeplearning import modify
from flask_cors import CORS
# webserver gateway interface
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


BASE_PATH = os.getcwd()
UPLOAD_PATH = os.path.join(BASE_PATH,'static/upload/')


@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        upload_file = request.files['image']
        filename = upload_file.filename
        path_save = os.path.join(UPLOAD_PATH,filename)
        upload_file.save(path_save)
        text = modify(path_save,filename)
        print(len(text))
        if len(text) <2 :
            text="No text found"
        # return render_template('index.html', upload=True, upload_image=filename ,text=text)
        return filename

    # return render_template('index.html', upload=False)

@app.route('/uploads/<filename>', methods=['GET'])
def get_uploaded_file(filename):
    return send_from_directory('static/modified_uploads', filename)


if __name__ =="__main__":
    app.run(debug=True)