function redirectToPage(buttonId, redirectPath) {
    $(buttonId).on('click', function() {
	var url = "https://" + window.location.hostname + redirectPath;
	window.location = url;
    });
}
