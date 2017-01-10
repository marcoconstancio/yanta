// getSelectionBoundaryElement on table_insert_common.js

var table_cell = getSelectionBoundaryElement("start");
var table_element = closest(table_cell,'table');
var table_cell_column_number = table_cell.cellIndex;

for (var i = 0, row; row = table_element.rows[i]; i++) {
    row.deleteCell(table_cell_column_number)
}