//Prints the preview of the article being created
$(document).ready(function(){
   var titleItem = $('#id_title');
   $('#preview-title').text(titleItem.val());

   var contentItem = $('#id_content');
   $('#preview-content').text(contentItem.val());
});