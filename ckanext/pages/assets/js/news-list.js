$(document).ready(function(){
    $("#news-visibility-toggler").click(function(e){
        e.preventDefault();
        var newsId = $(this).data('id');
        $.ajax({
            url: '/news_toggle_visibility/' + newsId,
            method: 'POST',
            success: function (data) {
             location.reload();
            }
        })
    });
});

