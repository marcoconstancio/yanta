// getSelectionBoundaryElement on table_insert_common.js
var table_cell = getSelectionBoundaryElement("start");
var table_element = closest(table_cell,'table');

//console.log(table_cell.parentNode.rowIndex);
table_element.deleteRow(table_cell.parentNode.rowIndex);