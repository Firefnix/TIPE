//Certains des divs n'ont pas de texte intérieur 
//
// 
// 
// 
// 
// 
// 
// 
// 
// 
// 
// 


function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
}

function allowDrop(ev) {
    ev.preventDefault();
}

function drop(ev) {
    ev.preventDefault();
    let data = ev.dataTransfer.getData("text", ev.innerText);
    ev.target.innerText = data;

}

function clearGrid() {
    let grid = document.getElementById("container_circuit");
    var child = grid.lastElementChild; 

    while (child) {
        grid.removeChild(child);
        child = grid.lastElementChild;
    }
}

function fill(grid, columns, rows) {

    for (let i = 1; i <= columns; i++) {
        for (let j = 1; j <= rows; j++) {

            let rectangle = document.createElement("div");

            rectangle.setAttribute("class", "sub_container_portes");
            rectangle.setAttribute("id", i.toString() + "/" + j.toString());
            rectangle.setAttribute("ondrop", "drop(event)");
            rectangle.setAttribute("ondragover", "allowDrop(event)");
            rectangle.style.zIndex = "10";

            rectangle.style.gridColumn = i.toString() + "/" + (i+1).toString();
            rectangle.style.gridRow = j.toString() + "/" + (j+1).toString();

            grid.appendChild(rectangle);

        }
    }

    setStates(Math.max(columns, rows));
}

function setStates(columns) {
    for (let j = 1; j <= columns; j++) {
        let rect = document.getElementById("1/" + j.toString());
        rect.innerText = "1";
        rect.setAttribute("onclick", "switchStates(event.target)");
        rect.setAttribute("ondrop", "")
        rect.setAttribute("ondragover", "")
    }
}

function switchStates(rect) {
    let txt = rect.innerText;

    if (txt == "1") {
        rect.innerText = "0";
    } else {
        rect.innerText = "1";
    }

}

function submit() {
    console.log("submited")

    //clearGrid();

    let columnsField = document.getElementById("columns_btn");
    let rowsField = document.getElementById("rows_btn");
    let grid = document.getElementById("container_circuit");    

    let columns = columnsField.value;
    let rows = rowsField.value;

    let height = grid.offsetHeight;
    let width = grid.offsetWidth;


    grid.style.gridTemplateColumns = ((width/columns).toString() + "px " ).repeat(columns);
    grid.style.gridTemplateRows = ((height/rows).toString() + "px " ).repeat(rows);

    fill(grid, columns, rows);
    links(grid, columns, rows);
}

function links(grid, columns, rows) {

    // let rect = document.createElement("div");
    // rectangle.setAttribute("class", "sub_container_portes");
    // rect.style.zIndex = "1";

    // grid.appendChild(rect);

    // rect.style.gridColumn = "1/3";
    // rect.style.gridRow = "1/3";

}