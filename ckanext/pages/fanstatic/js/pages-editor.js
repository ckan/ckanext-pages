$(document).ready(function(){
    editor = new MediumEditor('.editable', {
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

    $('form').submit(function(){
        for (var i=0; i<editor.elements.length; i++){
            input = $(editor.elements[i]).next('input')
            input.val(editor.serialize()[editor.elements[i].id]['value'])
        }
    });
});
