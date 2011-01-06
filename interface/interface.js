$(document).ready(function() {
	$("li").click(function(e) { $(this).find("article").toggle(); });
	$("button").click(function(e) {
		$(this).parent().parent().find("code").hide();
		$(this).parent().parent().parent().find("article").show();
	    });
});