// Stephen Silverstein
// https://github.com/sjsilverstein

$(document).ready(function(){
// BODY
	$('h1').hover(function(){
		$(this).css('color', 'blue');
		},function(){
		$(this).css('color', 'green');
	});
})