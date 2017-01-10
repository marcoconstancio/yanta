// getSelectionBoundaryElement on table_insert_common.js
var table_cell = getSelectionBoundaryElement("start");
var table_element = closest(table_cell, 'table');

var table_cell_row_number = table_cell.parentNode.rowIndex;
var table_cell_column_number = table_cell.cellIndex;

var element_tag = null;
var new_element = null;

var cell_colspan = table_cell.colSpan;
var cell_rowspan = table_cell.rowSpan;

if (table_cell.nodeName == 'TD'){
    element_tag = "td";
}else if(table_cell.nodeName == 'TH'){
    element_tag = "th";
}

new_element = '<' + element_tag + '></' + element_tag + '>';

if(new_element){
    for (i = table_cell_row_number; i < table_cell_row_number + cell_rowspan; i++) {
        for (j = table_cell_column_number; j < table_cell_column_number + cell_colspan; j++) {
            if(i == table_cell_row_number){
                if(j != (table_cell_column_number + cell_colspan) - 1){
                    if (element_tag == 'td'){
                        table_element.rows[i].cells[table_cell_column_number].insertAdjacentHTML('afterend','<td></td>');
                    }else{
                        table_element.rows[i].cells[table_cell_column_number].insertAdjacentHTML('afterend','<th></th>');
                    }
                }else{

                }
            }else{
                if (element_tag == 'td'){
                    table_element.rows[i].cells[table_cell_column_number].insertAdjacentHTML('afterend','<td></td>');
                }else{
                    table_element.rows[i].cells[table_cell_column_number].insertAdjacentHTML('afterend','<th></th>');
                }
            }
        }
    }
    table_cell.colSpan = 1;
    table_cell.rowSpan = 1;
}