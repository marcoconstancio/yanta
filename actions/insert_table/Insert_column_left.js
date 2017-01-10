// getSelectionBoundaryElement on table_insert_common.js

var table_cell = getSelectionBoundaryElement("start");
var table_element = closest(table_cell,'table');
var table_cell_column_number = table_cell.cellIndex;

var merged_td = '';
var merged_th = '';


for (var i = 0, row; row = table_element.rows[i]; i++) {

    if(row.cells[table_cell_column_number]){
        var this_rowspan = row.cells[table_cell_column_number].rowSpan;
        var th_el = document.createElement('th');

        if (row.cells[table_cell_column_number].tagName.toLowerCase() === 'th') {
            if(this_rowspan === undefined || this_rowspan == 1){
                if(merged_td > 0){
                    merged_td-=1;
                }else{
                    row.cells[table_cell_column_number].insertAdjacentHTML('beforebegin','<th></th>');
                }
            }else{
                merged_td = this_rowspan - 1;
                row.cells[table_cell_column_number].insertAdjacentHTML('beforebegin','<th rowspan="' + this_rowspan + '"></th>');
            }
        }else if (row.cells[table_cell_column_number].tagName.toLowerCase()  === 'td') {
           if(this_rowspan === undefined || this_rowspan == 1){
                if(merged_td > 0){
                    merged_td-=1;
                }else{
                    row.cells[table_cell_column_number].insertAdjacentHTML('beforebegin','<td></td>');
                }
           }else{
                merged_td = this_rowspan - 1;
                row.cells[table_cell_column_number].insertAdjacentHTML('beforebegin','<th rowspan="' + this_rowspan + '"></th>');
           }
        }
    }
}