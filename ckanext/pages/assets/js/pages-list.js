$(document).ready(function(){
    $(".page-visibility-toggler").click(function(e){
        e.preventDefault();
        var page_id = $(this).data('id');
        console.log("Toggling visibility for page ID:", page_id);
        $.ajax({
            url: '/pages_toggle_visibility/' + page_id,
            method: 'POST',
            success: function (data) {
                console.log("Success:", data);
                location.reload();
            },
            error: function (error) {
                console.error("Error toggling visibility:", error);
            }
        });
    });
});