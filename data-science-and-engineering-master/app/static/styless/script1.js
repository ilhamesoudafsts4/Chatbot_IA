// Adds .js class to HTML
document.querySelector("html").classList.add('js');

// init our variables
var fileInput = document.querySelector( ".input-file" ),
	button = document.querySelector( ".input-file-trigger" ),
	the_return = document.querySelector(".file-return");

// Trigger when Space bar or Enter is hit
button.addEventListener( "keydown", function( event ) {
	if ( event.keyCode == 13 || event.keyCode == 32 ) {
		fileInput.focus();
	}
});

// Trigger when the label is clicked
button.addEventListener( "click", function( event ) {
	fileInput.focus();
	return false;
});

// Display a visual feedback
fileInput.addEventListener( "change", function( event ) {
	the_return.innerHTML = this.value;
});