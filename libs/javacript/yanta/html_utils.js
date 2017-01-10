// Helper function for getNodesInSelection action
function getNextNode(node){

    if (node.firstChild)
        return node.firstChild;

    while (node){
        if (node.nextSibling)
            return node.nextSibling;
        node = node.parentNode;
    }
}

// Gets selected nodes (html elements)
function getNodesInSelection(element_type)
{
    var range = document.getSelection().getRangeAt(0);
    var start = range.startContainer;
    var end = range.endContainer;
    var commonAncestor = range.commonAncestorContainer;
    var nodes_in_rage = [];
    var node;

    if(element_type === undefined){
        element_type = 'div';
    }

    // walk parent nodes from start to common ancestor
    for (node = start.parentNode; node; node = node.parentNode)
    {
        if(node.localName == element_type){
           nodes_in_rage.push(node);
        }

        if (node == commonAncestor)
            break;
    }
    nodes_in_rage.reverse();

    // walk children and siblings from start until end is found
    for (node = start; node; node = getNextNode(node))
    {
        if(node.localName == element_type){
           nodes_in_rage.push(node);
        }

        if (node == end)
            break;
    }

    return nodes_in_rage;
}

// document.addEventListener("DOMContentLoaded", function() ... DOES NOT WORK

// http://dustindiaz.com/smallest-domready-ever
function ready(cb) {
	/in/.test(document.readyState) // in = loadINg
		? setTimeout('ready('+cb+')', 9)
		: cb();
}

function hasClass(el, className){
    if (el.classList)
      return el.classList.contains(className);
    else
      return new RegExp('(^| )' + className + '( |$)', 'gi').test(el.className);
}
function addClass(el, className){
    if (el.classList)
      el.classList.add(className);
    else
      el.className += ' ' + className;
}
function removeClass(el, className){
    if (el.classList)
      el.classList.remove(className);
    else
      el.className = el.className.replace(new RegExp('(^|\\b)' + className.split(' ').join('|') + '(\\b|$)', 'gi'), ' ');
}
function closest(el, selector) {
    var matchesFn;

    // find vendor prefix
    ['matches','webkitMatchesSelector','mozMatchesSelector','msMatchesSelector','oMatchesSelector'].some(function(fn) {
        if (typeof document.body[fn] == 'function') {
            matchesFn = fn;
            return true;
        }
        return false;
    })

    var parent;

    // traverse parents
    while (el) {
        parent = el.parentElement;
        if (parent && parent[matchesFn](selector)) {
            return parent;
        }
        el = parent;
    }

    return null;
}