window.onload = function() { 
	var _markup = document.getElementById('id_markup');
	if (_markup) {
		addEvent(_markup, 'change', function() {
			if (_markup.value=='html') InitTinyMCE();
		});
		if (_markup.value=='html') InitTinyMCE();
		var _author = document.getElementById('id_author');
		if (_author.value=='') {
			_author.options[1].selected='selected';
		}
	}
}
