# Imports
import os
import PythonMagick
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename

# Configuration
UPLOAD_FOLDER = './uploads'
STATIC_FOLDER = './static'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# Create the "app" object
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Functions
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

def append_name(filename):
	name, ext = os.path.splitext(filename)
	return name + '_processed' + ext

def process_image(filename):
	newFilename = append_name(filename)
	image = PythonMagick.Image(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	imagesize = '%sx%s' % (image.columns() * 0.5, image.rows() * 0.5)
	seal = PythonMagick.Image(os.path.join(STATIC_FOLDER, 'seal.svg'))
	seal.type = image.type
	seal.transparent('#FFFFFF')
	seal.resize(imagesize)
	image.composite(seal, image.columns() / 4, image.rows() / 4, PythonMagick.CompositeOperator.SrcOverCompositeOp)
	image.write(os.path.join(app.config['UPLOAD_FOLDER'], newFilename))
	return newFilename

# Routes
@app.route('/', methods=['GET', 'POST'])
def home():
	if request.method == 'GET':
		return render_template('home.html')
	else:
		file = request.files.get('file')
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			newFilename = process_image(filename)
			return redirect(url_for('uploaded_file', filename=newFilename))

		else:
			filename = request.form['filename']
			if filename and allowed_file(filename):
				newFilename = append_name(filename)
				return redirect(url_for('uploaded_file', filename=newFilename))
				
	return "Invalid file. You've been a naughty boy."

@app.route('/uploads/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Run! Run for your life!
if __name__ == '__main__':
	app.debug = True
	app.run()

