$(document).ready(function(){
    $("#page-visibility-toggler").click(function(e){
        alert()
        e.preventDefault();
        var page_id = $(this).data('id');
        $.ajax({
            url: '/pages_toggle_visibility/' + page_id,
            method: 'POST',
            success: function (data) {
             location.reload();
            }
        })
    });
});
