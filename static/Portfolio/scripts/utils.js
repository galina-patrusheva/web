// Cookie function from http://www.w3schools.com/js/js_cookies.asp
function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires="+d.toUTCString();
    document.cookie = cname + "=" + cvalue + "; " + expires;
}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)===' ') c = c.substring(1);
        if (c.indexOf(name) === 0) return c.substring(name.length,c.length);
    }
    return "";
}

function xhrPost(url, params, handler) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', url, true);
    xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
    // POST
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    var params_arr = [];
    for(var k in params)
        params_arr.push(k + '=' + encodeURIComponent(params[k]));
    var params_str = params_arr.join('&');
    xhr.send(params_str);  // Data
    if(handler)
        xhr.onreadystatechange = function(){ handler(xhr) };
}

function xhrGet(url, params, handler) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    var params_arr = [];
    for(var k in params)
        params_arr.push(k + '=' + params[k]);
    var params_str = encodeURIComponent(params_arr.join('&'));
    xhr.send(params_str);  // Data
    if(handler)
        xhr.onreadystatechange = function(){ handler(xhr) };
}

function ajaxFormSubmit(handler) {
    return function(e) {
        e = e || window.event;
        var target = e.target || e.srcElement;
        var data = {};
        for(var i = 0; i < target.length; i++)
            if(target[i].name)
                data[target[i].name] = target[i].value;
        xhrPost(target.action, data, handler);
        return false;
    }
}

function detachDefaultHandler(handler) {
    return function(e) {
        e = e || window.event;
        if(e.stopPropagation)
            e.stopPropagation();
        else
            e.cancelBubble = true;
        handler(e);
        return false;
    };
}

function funcCache(func) {
    var cache = {};
    return function(arg) {
        if(!(arg in cache))
            cache[arg] = func(arg);
        return cache[arg];
    };
}

function crossBrowserStyleSetProperty(obj, property, value) {
    // for FireFox, Chrome, IE9+
    if(obj.style.setProperty)
        obj.style.setProperty(property, value);
    else if(obj.style.setAttribute) { // for IE8
        var parts = property.split('-');
        var propertyCamelCase = parts[0];
        for(var i = 1; i < parts.length; i++) {
            propertyCamelCase += parts[i].charAt(0).toUpperCase() +
                parts[i].substr(1);
        }
        obj.style.setAttribute(propertyCamelCase, value);
    } else
        console.log('setProperty not supported');
}

function preloadImage(src) {
    var img = new Image();
    img.src = src;
}