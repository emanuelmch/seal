# Imports
import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename

# Configuration
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# Create the "app" object
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Functions
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

# Routes
@app.route('/', methods=['GET', 'POST'])
def home():
	if request.method == 'GET':
		return render_template('home.html')
	else:
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			print "********************************************"
			print os.path.join(app.config['UPLOAD_FOLDER'], filename)
			print "********************************************"
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return redirect(url_for('uploaded_file', filename=filename))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
		
# Run! Run for your life!
if __name__ == '__main__':
	app.debug = True
	app.run()

