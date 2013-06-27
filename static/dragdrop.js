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
		
		var files = event.dataTransfer.files;
		document.forms.fileUploading.file.files = files;
		document.forms.fileUploading.submit();
		
		return false;
	}
	
	

	console.log('Init OK');
}
