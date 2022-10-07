from flask import Flask
from flask_cors import CORS
from deepface import DeepFace

import os
from flask import Flask, request


def face_verify(img_1: str, img_2: str):
    try:
        result_dict = DeepFace.verify(img1_path=img_1, img2_path=img_2)
        return result_dict
    except Exception as _ex:
        return _ex


def face_analyze(img_1: str, img_2: str):
    try:
        result_dict = DeepFace.analyze(img_path=img_1, actions=['emotion', 'age', 'race']) #enforce_detection=False)
        return {
            "age": result_dict.get("age"),
            "emotion": result_dict.get("dominant_emotion"),
            "race": result_dict.get("dominant_race")
        }

    except Exception as _ex:
        return _ex


def main(img_1, img_2):
    r = face_analyze(img_1, img_2)
    print(type(r))
    if isinstance(r, ValueError):
        return {
            "error": str(r)
        }
    return r


UPLOAD_FOLDER = './upload'

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file1' not in request.files:
            return 'there is no file1 in form!'
        file1 = request.files['file1']
        path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        file1.save(path)
        members(path)
        return members(path)
    return '''
    <h1>Upload new File</h1>
    <form method="post" enctype="multipart/form-data">
      <input type="file" name="file1">
      <input type="submit">
    </form>
    '''


@app.route('/members/<name>')
def members(name):
    return {"members": main(img_1=name,
                            img_2='https://www.syfy.pt/sites/default/files/profiles/776465_2162429_4912x7360_1.jpg')}


if __name__ == '__main__':
    app.run(debug=True)
