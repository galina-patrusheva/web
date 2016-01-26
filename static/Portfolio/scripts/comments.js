function signupFormValidator(e) {
    e = e || window.event;
    var password = document.getElementById('signup_password');
    var confirm_password = document.getElementById('signup_password_confirm');
    if(password.value != confirm_password.value) {
        alert('Пароли не совпадают!');
        return false;
    }
}

var refresh, deleteComment, likeCurrent;

function initComments(state) {
    var commentsContainer = document.getElementById('commentsContainer');
    var errorsContainer = document.getElementById('errorsContainer');
    var postCommentForm = document.getElementById('postCommentForm');
    var likesNode = document.getElementById('likes');
    var photoIdElement = document.getElementById('photoIdElement');
    if(errorsContainer)
        crossBrowserStyleSetProperty(errorsContainer, 'display', 'none');

    function loadComments(photoId) {
        xhrGet('/gallery/list_comment/' + photoId, {}, function(xhr) {
            if(xhr.readyState == 4 && xhr.status == 200) {
                commentsContainer.innerHTML = xhr.responseText;
            }
        });
    }

    function postCommentHandler(xhr) {
        // request finished and response is ready
        if(xhr.readyState == 4 && xhr.status == 200) {
            if(xhr.responseText == 'success') {
                postCommentForm.reset();
                crossBrowserStyleSetProperty(errorsContainer, 'display', 'none');
                refresh();
            } else {
                crossBrowserStyleSetProperty(errorsContainer, 'display', 'block');
                errorsContainer.innerHTML = xhr.responseText;
            }
        }
    }

    function getCurrentId() {
        // get photo id
        var preview_id = 'photo_' + state.albumIndex +
            '_' + state.photoIndex;
        var image_id = document.getElementById(preview_id)
                               .getElementsByTagName('img')[0]
                               .id;
        var photo_id = image_id.split('_')[1];
        return photo_id;
    }

    refresh = function() {
        if(!state.hidden) {
            var photo_id = getCurrentId();
            loadComments(photo_id);
            // refresh form
            if(photoIdElement)
                photoIdElement.value = photo_id;
            xhrGet('/gallery/like/' + photo_id, {}, function(xhr) {
                if(xhr.readyState == 4 && xhr.status == 200) {
                    var values = xhr.responseText.split(';'),
                        likes = parseInt(values[0]),
                        liked = values[1] == 'True';
                    likesNode.childNodes[1].innerHTML = likes;
                    if(liked)
                        likesNode.className = 'liked';
                    else
                        likesNode.className = '';
                }
            });
        }
    }

    deleteComment = function(photoId) {
        xhrPost('/gallery/edit_comment/' + photoId + '/delete', {}, function(xhr) {
            if(xhr.readyState == 4 && xhr.status == 200) {
                refresh();
            }
        });
    }

    likeCurrent = function() {
        var photo_id = getCurrentId();
        xhrPost('/gallery/like/' + photo_id, {}, function(xhr) {
            if(xhr.readyState == 4 && xhr.status == 200) {
                if(xhr.responseText == 'success')
                    refresh();
                else
                    alert(xhr.responseText);
            }
        });
    }

    if(postCommentForm)
        postCommentForm.onsubmit = ajaxFormSubmit(postCommentHandler);

    if (window.addEventListener) {
        window.addEventListener('hashchange', refresh);
    } else {
        window.attachEvent('onhashchange', refresh);
    }
    setInterval(refresh, 3000);
    refresh();
}