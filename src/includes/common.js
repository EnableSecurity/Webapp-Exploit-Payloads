function notify(status)
{
	if (statusurl)
	{
		nstatusurl = statusurl + '?status=' + escape(status);
		$.getScript(nstatusurl);
	}
};