from flask import Flask, request, redirect, url_for, send_from_directory, render_template_string
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXT = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
FLAG_PATH = 'flag.txt'


def allowed_filename(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT


@app.route('/')
def index():
    return '''<h2>Upload avatar</h2>
<form method="POST" action="/upload" enctype="multipart/form-data">
  <input type="file" name="file">
  <input type="submit" value="Upload">
</form>
<p>But pédagogique : le flag est sur le serveur ; l'objectif est d'accéder à son contenu si possible.</p>
'''


@app.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('file')
    if not f:
        return 'No file uploaded', 400

    filename = f.filename
    if allowed_filename(filename):
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        f.save(path)
        # Warning: stored under webroot and may be processed/displayed
        return redirect(url_for('uploaded_file', filename=filename))
    else:
        return 'Extension non autorisée', 400


@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/flag')
def flag():
    # page non liée depuis l'UI, located on server
    try:
        with open(FLAG_PATH) as fh:
            return '<pre>Flag: ' + fh.read() + '</pre>'
    except Exception:
        return 'Flag non disponible.'


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # create flag file
    if not os.path.exists(FLAG_PATH):
        with open(FLAG_PATH, 'w') as fh:
            fh.write('FLAG{upload_demo_2025}')

    app.run(host='0.0.0.0', port=5000)
