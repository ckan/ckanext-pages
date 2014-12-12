$(document).ready(function(){
    var editor = new MediumEditor('.editable', {
            buttons: ['bold',
                'italic',
                'quote',
                'header1',
                'header2',
                'anchor',
                'unorderedlist',
                'pre'
            ],
    });

    //editor.serialize()['field-content-editor']['value']
    //$(editor.elements[0])

    $('form').submit(function(){
        input = $(editor.elements[0]).next('input')
        input.val(editor.serialize()['field-content-editor']['value'])
    });
});
