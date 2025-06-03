from flask import Flask, render_template, request, send_file
import cv2
import numpy as np
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['image']
        if not file:
            return render_template('index.html', error="الرجاء رفع صورة.")
        
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'original.png')
        file.save(image_path)

        # 1. قراءة الصورة
        image = cv2.imread(image_path)
        if image is None:
            return render_template('index.html', error="تعذر قراءة الصورة.")

        # 2. التحويل إلى رمادي
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], '1_gray.png'), gray)

        # 3. تحسين التباين
        equalized = cv2.equalizeHist(gray)
        cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], '2_equalized.png'), equalized)

        # 4. التنعيم
        blurred = cv2.GaussianBlur(equalized, (5, 5), 0)
        cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], '3_blurred.png'), blurred)

        # 5. الحدة
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])
        sharpened = cv2.filter2D(blurred, -1, kernel)
        cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], '4_sharpened.png'), sharpened)

        return render_template('index.html', images=[
            '1_gray.png', '2_equalized.png', '3_blurred.png', '4_sharpened.png'
        ])

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
