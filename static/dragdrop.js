function DragDrop_init() {
	var doc = document.body;

	doc.ondragenter = function () {
		console.log('ondragenter');
		this.className = 'fileHover';
		return false;
	}

	doc.ondragover = function () {
		return false;
	}

	doc.ondragleave = function() {
		console.log('ondragleave');
		this.className = '';
		return false;
	}

	doc.ondrop = function(event) {
		console.log('ondrop');
		event.stopPropagation && event.stopPropagation();
		event.preventDefault && event.preventDefault();
		this.className = '';

		document.forms.fileUploading.reset();
		document.forms.fileUploading.filename.value = event.dataTransfer.files[0].name;
		
		var formData = new FormData();
		formData.append('file', event.dataTransfer.files[0]);
		var xhr = new XMLHttpRequest();
		xhr.open('POST', '/');
		xhr.onload = function () {
			if (xhr.status === 200) {
				console.log('OK');
				document.forms.fileUploading.submit();
			} else {
				console.log('Something went wrong...');
			}
		}
		xhr.send(formData);

		return false;
	}



	console.log('Init OK');
}

