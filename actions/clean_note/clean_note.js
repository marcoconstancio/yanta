function removeStyles(el) {
    el.removeAttribute('style');
    el.removeAttribute('data-mce-style');
    if(el.childNodes.length > 0) {
        for(var child in el.childNodes) {
            /* filter element nodes only */
            if(el.childNodes[child].nodeType == 1)
                removeStyles(el.childNodes[child]);
        }
    }
}


if (typeof(style_tag_selected_elements) !== 'undefined') {
    var style_tag_elements_names = {
        'Bold element':['bold'],
        'Code element':['code'],
        'Div element':['div'],
        'Headings':['h1','h2','h3','h4','h5','h6'],
        'Images':['img'],
        'Italic element':['code'],
        'Lists':['ul','ol','li'],
        'Paragraph':['p'],
        'Preformated element':['pre'],
        'Span element':['div'],
        'Tables':['table','tr','td','th','thead','tfooter']
    }

  if (typeof(style_tag_selected_elements) !== 'undefined') {

    if (style_tag_selected_elements['All elements'] === true){
        removeStyles(document.body);
    }else{
        delete style_tag_selected_elements['All elements'];

        Object.keys(style_tag_selected_elements).forEach(function(element_name) {
            if (style_tag_selected_elements[element_name] === true){
                Object.keys(style_tag_elements_names[element_name]).forEach(function(el) {
                    // Array with element names
                    // console.log(style_tag_elements_names[element_name]);
                    // Element name
                    // console.log(style_tag_elements_names[element_name][el]);
                    // Existing founded elements
                    // console.log(document.getElementsByTagName(style_tag_elements_names[element_name][el]));

                    found_elements = document.getElementsByTagName(style_tag_elements_names[element_name][el]);

                    if (found_elements.length > 0){
                        Object.keys(found_elements).forEach(function(fe_idx) {
                            try {
                                // Normal style
                                found_elements[fe_idx].removeAttribute('style');
                                // Special attribute used by mce editor
                                found_elements[fe_idx].removeAttribute('data-mce-style');
                            }catch(err) {
                                //console.log(err);
                            }
                        });
                    }
                });
            }
        });
    }
  }
}