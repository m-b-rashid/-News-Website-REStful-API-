    //adds message when sumbit button presed
    $('#chat-form').on('submit', function (event) {
        event.preventDefault();

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: {msgbox: $('#chat-msg').val()},

            success: function (json) {
                $('#chat-msg').val('');
                $('#msg-list').prepend('<li class="text-right list-group-item">' + json.msg + '</li>');
                var chatlist = document.getElementById('msg-list-div');
                chatlist.scrollTop = chatlist.scrollHeight;
            },
            error: function () {
                alert('You are not logged in')

            }
        });
    });


    //gets the messages (and takes into consideration if scrolling or not).+ refreshes the messages every so often to update page
    function getMessages() {
        if (!scrolling) {
            var url = $('#chat-form2').val();
            $.get(url, function (messages) {
                $('#msg-list').html(messages);
            });
        }
        scrolling = false;
    }


    var scrolling = false;
    $(function () {
        $('#msg-list-div').on('scroll', function () {
            scrolling = true;
        });
        refreshTimer = setInterval(getMessages, 5000);
    });



    //setup when document is ready
    $(document).ready(function () {
        $('#send').attr('disabled', true);
        $('#chat-msg').keyup(function () {
            if ($(this).val() != '') {
                $('#send').removeAttr('disabled');
            }
            else {
                $('#send').attr('disabled', true);
            }
        });

        //DELETING POST
        $("body").on('click', ".btn.btn-danger.btn-sm", function (event) {
            event.preventDefault();
            var id = $(this).attr('id').substring(10); //because deletePost is 10 letters

            $.ajax({
                url: '/comments/delete/',
                type: 'DELETE',
                data: {comment_id: id},

                success: function () {
                    $('#userPost' + id).remove();
                },
                error: function () {
                    alert('Could not delete')

                }
            });
        });


            // using establish csrf stuff
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        var csrftoken = getCookie('csrftoken');
        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

        //shows delete button for user comments.
        $(document).on('mouseenter', '.userPost', function () {
            var commentID = $(this).attr('id').substring(8); //0-7 because userPost is 8 chars long
            $('#deletePost' + commentID).show();
        }).on('mouseleave', '.userPost', function () {
            var commentID = $(this).attr('id').substring(8); //0-7 because userPost is 8 chars long
            $('#deletePost' + commentID).hide();
        });
    });