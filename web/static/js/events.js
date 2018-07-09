$(document).ready(function() {
    $("#realtick").hide();
    $("#stat tr a:first-child").hover(function() {
        var code = $(this).attr("data-code");
        setTimeout(function() {
        var tick_url = "/tick/" + code;
        $.get(tick_url, function(data, status) {
            $("#realtick").html(data).show();
        })
    }, 5)}, function() {
        $("#realtick").html("").hide();
    })
});