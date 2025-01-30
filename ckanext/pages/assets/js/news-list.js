$(document).ready(function(){
    $(".news-visibility-toggler").click(function(e){
        e.preventDefault();
        var newsId = $(this).data('id'); //
        console.log("Toggling visibility for news ID:", newsId);

        $.ajax({
            url: '/news_toggle_visibility/' + newsId,
            method: 'POST',
            success: function (data) {
                console.log("Success:", data);
                if (data.success) {
                    location.reload();
                } else {
                    alert("Error: " + (data.error || "Unknown error"));
                }
            },
            error: function (xhr, status, error) {
                console.error("AJAX Error:", xhr.responseText);
            }
        });
    });
});
