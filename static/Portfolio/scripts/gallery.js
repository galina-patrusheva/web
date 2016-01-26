(function(){

/*
 * Variable
 */

var imageViewerLayer,
    viewerDiv,
    currentImage,
    helpLayer,
    helpVisible = false,
    savedState = {albumIndex: null, photoIndex: null},
    saveButton,
    loaderImage;

var State = {
    hidden: true,
    albumIndex: null,
    photoIndex: null,

    dump: function() {
        if(!this.hidden)
            return 'albumIdx=' + this.albumIndex +
                '&photoIdx=' + this.photoIndex;
        else
            return 'hidden';
    },

    storeToHash: function() {
        //var scroll = document.body.scrollTop;
        window.location.hash = this.dump();
        //document.body.scrollTop = scroll;
    },

    storeToCookie: function() {
        setCookie('gallery_state', encodeURIComponent(this.dump()), 7);
    },

    load: function(str, returnOnly) {
        var albumIndex = str.match(/albumIdx=(\d+)/) || undefined;
        var photoIndex = str.match(/photoIdx=(\d+)/) || undefined;
        if(albumIndex && photoIndex) {
            photoIndex = parseInt(photoIndex[1]);
            albumIndex = parseInt(albumIndex[1]);
            var links = getAlbumLinks(albumIndex);
            if(links && 0 <= photoIndex && photoIndex < links.length) {
                if(returnOnly)
                    return { albumIndex: albumIndex, photoIndex: photoIndex};
                this.hidden = false;
                this.photoIndex = photoIndex;
                this.albumIndex = albumIndex;
            } else {
                if(returnOnly)
                    return {albumIndex: null, photoIndex: null};
                this.hidden = true;
            }
        } else {
            if(returnOnly)
                return {albumIndex: null, photoIndex: null};
            this.hidden = true;
        }
    },

    loadFromHash: function() {
        this.load(window.location.hash);
    },

    loadFromCookie: function() {
        this.load(decodeURIComponent(getCookie('gallery_state')));
    },

    readFromCookie: function() {
        return this.load(decodeURIComponent(getCookie('gallery_state')), true);
    },

    clearCookie: function() {
        setCookie('gallery_state', '');
    },
};
GalleryState = State;

/*
 * Event handlers
 */

function previewClickHandler(e) {
    e = e || window.event;
    var target = e.target || e.srcElement; // for IE8
    if(target.tagName != 'A')
        target = target.parentNode;
    var targetInformation = target.id.split('_');
    State.albumIndex = parseInt(targetInformation[1]); // album index
    State.photoIndex = parseInt(targetInformation[2]); // photo index
    State.hidden = false;
    State.storeToHash();
}

/*
 * Gallery functional
 */

function galleryInit() {
    // Get main elements
    imageViewerLayer = document.getElementById('imageViewerLayer');
    viewerDiv = document.getElementById('viewerDiv');
    currentImage = document.getElementById('currentImage');
    helpLayer = document.getElementById('helpLayer');

    // Attach handlers to buttons
    document.getElementById('closeButton').onclick =
        detachDefaultHandler(closeGallery);
    saveButton = document.getElementById('saveButton');
    saveButton.onclick = detachDefaultHandler(saveStateClick);
    document.getElementById('leftButton').onclick =
        detachDefaultHandler(prevImage);
    document.getElementById('rightButton').onclick =
        detachDefaultHandler(nextImage);
    document.getElementById('helpCloseButton').onclick =
        detachDefaultHandler(hideHelp);

    // `loading` gif
    loaderImage = new Image();
    loaderImage.src = '/static/Portfolio/images/loading.gif';
    loaderImage.setAttribute('style',
        'position: absolute;' +
        'left: 50%;' +
        'top: 50%;' +
        'z-index: 0;' +
        'margin-left: -100px;' +
        'margin-top: -100px;');

    // Keyboard handlers
    document.onkeydown = function(e) {
        e = e || window.event;
        var target = e.target || e.srcElement; // for IE8
        switch (e.keyCode) {
            // ESC handler
            case 27:
                if(helpVisible)
                    return detachDefaultHandler(hideHelp)(e);
                else if(!State.hidden)
                    return detachDefaultHandler(closeGallery)(e);
                break;
            // Left arrow
            case 37:
                if(target.tagName != 'TEXTAREA' && target.tagName != 'INPUT')
                    prevImage();
                break;
            // Right arrow
            case 39:
                if(target.tagName != 'TEXTAREA' && target.tagName != 'INPUT')
                    nextImage();
                break;
            // F1
            case 112:
                return detachDefaultHandler(showHelp)(e);
        }
    };

    if (window.addEventListener) {
        window.addEventListener('hashchange', hashChangeHandler);
    } else {
        window.attachEvent('onhashchange', hashChangeHandler);
    }

    // disable onhelp in IE
    if('onhelp' in window)
        window.onhelp = detachDefaultHandler(function(){});

    // attach `onclick` handler to previews
    var innerImagesHrefs =  document.getElementById('imageContainer')
                                    .getElementsByTagName('a');
    for(var i = 0; i < innerImagesHrefs.length; i++)
        innerImagesHrefs[i].onclick = detachDefaultHandler(previewClickHandler);

    // read saved state
    savedState = State.readFromCookie();

    if(window.location.hash) {
        // try to load state from hash
        State.loadFromHash();
        refreshImage();
    } else {
        // try to load saved state from cookie (work only if hash is empty)
        State.loadFromCookie();
        State.storeToHash();
    }

    // init comments and likes
    initComments(State);
}

function hashChangeHandler() {
    State.loadFromHash();
    refreshImage();
}

// read current state and refresh gallery view
function refreshImage() {
    if(State.hidden) {
        // hide layer
        crossBrowserStyleSetProperty(imageViewerLayer, 'display', 'none');
        crossBrowserStyleSetProperty(document.body, 'overflow-y', 'auto');
    } else {
        // show layer
        crossBrowserStyleSetProperty(imageViewerLayer, 'display', 'block');
        crossBrowserStyleSetProperty(document.body, 'overflow-y', 'hidden');
        var links  = getAlbumLinks(State.albumIndex),
            m = links.length,
            nextIndex = (State.photoIndex + 1) % m,
            prevIndex = ((State.photoIndex - 1) % m + m) % m;
        // remove old image
        var container = currentImage.parentNode;
        currentImage.onload = function() {};
        container.removeChild(currentImage);
        container.appendChild(loaderImage);
        // create new image
        currentImage = new Image();
        // load prev and next image after current
        currentImage.onload = function() {
            try {
                container.removeChild(loaderImage);
            } catch (error) { }
            preloadImage(links[prevIndex]);
            preloadImage(links[nextIndex]);
        };
        // show image
        currentImage.src = links[State.photoIndex];
        // change `save button` view
        if(State.albumIndex === savedState.albumIndex &&
           State.photoIndex === savedState.photoIndex)
        {
            saveButton.setAttribute('class', 'button on-saved-image');
        } else {
            saveButton.setAttribute('class', 'button');
        }
        // put image to container
        viewerDiv.appendChild(currentImage);
    }
}

// shift image on `step` (e.g.: changeImage(-1) - prev image)
function changeImage(step) {
    var links = getAlbumLinks(State.albumIndex);
    if(!links)
        return;
    var m = links.length;
    State.photoIndex = ((State.photoIndex + step) % m + m) % m;
    State.storeToHash();
}
function prevImage() { changeImage(-1); }
function nextImage() { changeImage(1); }

// get array of normal-size image hrefs for album n
var getAlbumLinks = funcCache(function(n) {
    var links;
    try {
        links = document.getElementById('album_' + n)
                        .getElementsByTagName('a');
    } catch(error) {
        return;
    }
    return links;
});

function closeGallery() {
    State.hidden = true;
    State.storeToHash();
}

function showHelp() {
    crossBrowserStyleSetProperty(helpLayer, 'display', 'block');
    helpVisible = true;
}

function hideHelp() {
    crossBrowserStyleSetProperty(helpLayer, 'display', 'none');
    helpVisible = false;
}

function saveStateClick() {
    if(State.albumIndex === savedState.albumIndex &&
       State.photoIndex === savedState.photoIndex)
    {
        State.clearCookie();
        savedState = {albumIndex: null, photoIndex: null};
        saveButton.setAttribute('class', 'button');
    } else {
        State.storeToCookie();
        savedState = State.readFromCookie();
        saveButton.setAttribute('class', 'button on-saved-image');
    }
}

/*
 * Crossbrowser `onready` (from jQuery)
 */

(function(handler) {
    if ( document.addEventListener ) {
        document.addEventListener( 'DOMContentLoaded', handler, false);
    // IE
    } else if ( document.attachEvent ) {
        document.attachEvent('onreadystatechange', handler);
        // If IE and not an iframe
        // continually check to see if the document is ready
        if ( document.documentElement.doScroll && window === window.top )
            (function(){
                try {
                    // If IE is used, use the trick by Diego Perini
                    // http://javascript.nwbox.com/IEContentLoaded/
                    document.documentElement.doScroll('left');
                } catch( error ) {
                    setTimeout( arguments.callee, 0 );
                    return;
                }
            })();
    }
})(galleryInit);

})();
