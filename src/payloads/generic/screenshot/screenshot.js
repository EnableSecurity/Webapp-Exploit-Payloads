$(document).ready(function(){
	$('body').html2canvas({
		onrendered: function(canvas){
			screenshot = canvas.toDataURL();
			$.post(scdumpurl, { screenshot: screenshot } );
		}
	})
});