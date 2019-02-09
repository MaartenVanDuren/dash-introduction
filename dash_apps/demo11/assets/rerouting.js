function clear_url() {
    if (window.location.pathname.startsWith('/annotations')) {
        window.history.pushState('', '', '/');
    }
}

function callback(e) {
    var e = window.e || e;

    if (e.target.tagName !== 'A')
        return;

    clear_url()
}

if (document.addEventListener)
    document.addEventListener('click', callback, false);
else
    document.attachEvent('onclick', callback);

document.body.addEventListener('DOMSubtreeModified', function() {
    clear_url()
}, false);
