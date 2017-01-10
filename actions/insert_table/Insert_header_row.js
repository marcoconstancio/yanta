// getSelectionBoundaryElement - table_insert_common.js
var table_element = closest(table_cell,'table');
var table_cell = getSelectionBoundaryElement("start");
var table_cell_row_element = table_cell.parentNode;

var td_children = table_cell_row_element.children;
var num_td = 0;

for (i = 0; i < td_children.length; i++) {
    if (td_children[i].tagName.toLowerCase()  === 'td') {
        num_td++;
    }
}

if(num_td > 0){
    var new_table_cell_row_element = '<tr>';

    for (i = 0; i < num_td; i++) {
        new_table_cell_row_element += '<th></th>';
    }
    new_table_cell_row_element += '</tr>';

    table_element.rows[0].insertAdjacentHTML('beforebegin',new_table_cell_row_element);
}