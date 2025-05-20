from flask import Flask, render_template, request, redirect, url_for
import cv2
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'input.png')
        file.save(filepath)

        # معالجة الصورة باستخدام OpenCV
        img = cv2.imread(filepath)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        processed_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.png')
        cv2.imwrite(processed_path, gray)

        return redirect(url_for('result'))

@app.route('/result')
def result():
    return render_template('result.html', image_path='static/output.png')

if __name__ == '__main__':
    app.run(debug=True)