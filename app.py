from flask import Flask, render_template, request, url_for, redirect, jsonify
import os
import cv2
from werkzeug.utils import secure_filename
from face_detector import FaceDetector  

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['PROCESSED_FOLDER'] = 'static/processed/'
app.config['WEIGHTS_FOLDER'] = 'weights/'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        method = request.form.get('method', 'haarcascade')
        classifier_name = request.form.get('classifier_name', 'Faces')
        scale_factor = float(request.form.get('scale_factor', 1.1))
        min_neighbors = int(request.form.get('min_neighbors', 5))
        rect_thickness = int(request.form.get('rect_thickness', 2))
        upsample_times = int(request.form.get('upsample_times', 1))

        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                filename = secure_filename(file.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(image_path)

                detector = FaceDetector(
                    method=method,
                    classifier_name=classifier_name,
                    upload_folder=app.config['UPLOAD_FOLDER'],
                    processed_folder=app.config['PROCESSED_FOLDER'],
                    rect_thickness=rect_thickness
                )

                processed_image_path = detector.detect(
                    image_path, filename, scale_factor, min_neighbors, upsample_times
                )
                processed_image_filename = os.path.basename(processed_image_path)

                return redirect(url_for('result', filename=processed_image_filename,
                                        method=method, classifier_name=classifier_name,
                                        scale_factor=scale_factor, min_neighbors=min_neighbors,
                                        rect_thickness=rect_thickness, upsample_times=upsample_times))
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    method = request.form.get('method')
    classifier_name = request.form.get('classifier_name')
    scale_factor = float(request.form.get('scale_factor', 1.1))
    min_neighbors = int(request.form.get('min_neighbors', 5))
    rect_thickness = int(request.form.get('rect_thickness', 2))
    upsample_times = int(request.form.get('upsample_times', 1))
    filename = request.form.get('filename')

    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    detector = FaceDetector(
        method=method,
        classifier_name=classifier_name,
        upload_folder=app.config['UPLOAD_FOLDER'],
        processed_folder=app.config['PROCESSED_FOLDER'],
        rect_thickness=rect_thickness
    )

    processed_image_path = detector.detect(
        image_path, filename, scale_factor, min_neighbors, upsample_times
    )
    return jsonify({'processed_image_url': url_for('static', filename='processed/' + filename)})

@app.route('/result')
def result():
    filename = request.args.get('filename')
    method = request.args.get('method', 'haarcascade')
    classifier_name = request.args.get('classifier_name', 'Faces')
    scale_factor = request.args.get('scale_factor', 1.1)
    min_neighbors = request.args.get('min_neighbors', 5)
    rect_thickness = request.args.get('rect_thickness', 2)
    upsample_times = request.args.get('upsample_times', 1)
    return render_template(
        'result.html',
        processed_image=filename,
        method=method,
        classifier_name=classifier_name,
        scale_factor=scale_factor,
        min_neighbors=min_neighbors,
        rect_thickness=rect_thickness,
        upsample_times=upsample_times
    )

if __name__ == '__main__':
    app.run(debug=True)