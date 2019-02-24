 $(document).ready(function () {
     //login post request
     $('#login-form').on('submit', function (event) {
        event.preventDefault();
        $.ajax({
            url: '/login/',
            type: 'POST',
            data: {email: $('#email-login-entry').val(), password: $('#password-login-entry').val()},

            success: function (json_result) {
                $('#login-form').remove();
                $('#register-form').remove();
                var data = JSON.parse(json_result);
                var name = data[0].fields.name;

                helloMessage = $(document.createElement('li'));
                helloMessage.html('<span class="nav-text"> Hi there, ' + name
                    + '! <form class="form-inline my-2 my-lg-0" method="GET" action="/profile/"><button type="submit" class="btn btn-outline-warning my-2 my-sm-0" id="btn-logout">Profile</button></form> <form class="form-inline my-2 my-lg-0" method="GET" action="/logout/"><button class="btn btn-outline-warning my-2 my-sm-0" id="btn-logout">'
                    + 'Logout</button></form></span>');
                helloMessage.appendTo('#nav-right')
                },
            error: function () {
                alert('Incorrect login details')

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