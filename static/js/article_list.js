$(document).ready(function(){
    //page setup
    var pageNo = $('.PageID').attr('id').substring(4);
    var currentGenre = 'ALL';
    $('#article-panel').hide();
    reloadArticles(currentGenre, pageNo);

    //changes pangeNo variable to turn page back
    $('#PrevLink').on('click', function (event) {
        event.preventDefault();
        pageNo = pageNo -1;
        if(pageNo == 0){
            pageNo = 1
        }
        else
        {
            reloadArticles(currentGenre, pageNo);
        }
    });

    //changes pangeNo variable to turn page forward
    $('#NextLink').on('click', function (event) {
        event.preventDefault();
        pageNo = parseInt(pageNo) +1;
        reloadArticles(currentGenre, pageNo); //Need to stop the max.
    });

    //refreshes articles once genre is clicked on navbar.
    $('.nav-link').on('click', function (event){
        event.preventDefault();
       var genre = $(this).attr('id');
       currentGenre = genre;
       $('.PageID').attr('id', 'page1'); //reset page number when change genres
        pageNo = 1;

       $.ajax({
            url: '/filter/',
            type: 'GET',
            data: {page: pageNo, genre: genre},

            success: function (json) {
                var data = JSON.parse(json);
                $('#article-panel').empty();
                loadArticles(data);
                if(data.length == 0)
                {
                    alert('ITS TIME FOR SOME JOURNALISM. GET YOSELF SUM STORIES')
                }
            },
            error: function () {
                alert('You done gone fudged up now');

            }
       });
    });
});

//loads article information after recieving json from server
function loadArticles(data){
    var html_List;
     $.each(data, function(i, article){
         articleEntry = $(document.createElement('div')).attr('class', 'row');
         html_List = '<div class="col-sm-12"><div class="thumbnail">';
         if(article.fields.image != ""){
             html_List += ('<img src="/media/' + article.fields.image + '" class="img-responsive" style="display: block; width: 100%; margin: 0 auto;"/>');
         }
         else{
             html_List += ('<img src="https://orig00.deviantart.net/5dbd/f/2016/285/7/8/pepe_the_frog___minimalist_by_anoanidude-dakrmth.jpg" class="img-responsive" style="display: block; width: 100%; margin: 0 auto;"/>')
         }
         html_List += ('<div class="caption">');
         html_List += ('<h3><a href="/' + article.pk + '/"> ' + article.fields.title + '</a> <small> by <b>' + article.fields.author + '</b> published on ' + article.fields.postTime + '</small></h3>');
         html_List += ('<p>' + article.fields.content + '</p>');
         html_List += ('<p><a href="/' + article.pk + '/" class="btn btn-primary" role="button">View</a></p></div></div></div>');
         articleEntry.after().html(html_List);
         articleEntry.appendTo('#article-panel');
         $('#article-panel').hide();
         $('#article-panel').slideDown(1600);
         $('#paginator').show();
     });
}

//HELPER METHOD, refreshes article based on genre and page number
function reloadArticles(genre, pageNo){
    $('#article-panel').slideUp(1600, function(){
        $('#article-panel').empty();
    });

    $.ajax({
            url: '/filter/',
            type: 'GET',
            data: {genre: genre, page: pageNo},

            success: function (json) {
                var data = JSON.parse(json);
                loadArticles(data);
            },
            error: function () {
                alert('You done gone fudged up now');

            }
    });
}