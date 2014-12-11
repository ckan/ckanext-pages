$(document).ready(function(){
    var editor = new MediumEditor('.editable');

    //editor.serialize()['field-content-editor']['value']
    //$(editor.elements[0])

    $('form').submit(function(){
        input = $(editor.elements[0]).next('input')
        input.val(editor.serialize()['field-content-editor']['value'])
    });
});
