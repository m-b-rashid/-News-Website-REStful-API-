$(document).ready(function(){
    //preview initial text
    $('#preview-title').text($('#id_title').val());
    $('#preview-content').text($('#id_content').val());

    //preview added text
    $('#id_title').keyup(function(){
       $('#preview-title').text($(this).val());
    });
    $('#id_content').keyup(function(){
       $('#preview-content').text($(this).val());
    });
});