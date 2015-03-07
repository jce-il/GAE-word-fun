console.log("game.js");

//$(function() happens when the document DOM is built
//so only then we can bind functions to DOM elements
$(function() {
	$('#guess_submit').on('click', guessSubmit);	//bind the guessSubmit function to the guess_submit event
	$('#guess_field').on('keyup', function(e) {		//submitting on enter also
		if(e.keyCode === 13) {
			guessSubmit();
		}
	});
});

function guessSubmit() {
	$.get('/api/guess', {word:$('input[name=guess]').val()}, function(data){
		console.log(data);
		if(data.solved) {
			$('#youwin').show().animate({fontSize:"400px"}, 1000, function(){
				document.location.reload();				
			});
		}
		else {
			$('#wrong').fadeIn('slow', function() {
				$('#wrong').fadeOut('slow');
			});
			$('input[name=guess]').val('');		//empty the content of the guess input field
			if(data.wordLen) {
				//if we got the word length as part of the reply, update the relevant fields
				$('#word_len').text(data.wordLen);
				$('input[name=guess]').attr('maxlength', data.wordLen);
			}			
		}
	}, 'json');	
}