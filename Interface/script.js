let circuit = [];

let gatesQubits = {
    '': 1,
    '|0⟩': 1,
    '|1⟩': 1,
    'H': 1,
    'U': NaN,
    'cX': 2,
    'I': 1,
    'S': 2,
    'X': 1
};

function drag(ev) {
    ev.dataTransfer.setData('text', ev.target.id);
}

function allowDrop(ev) {
    ev.preventDefault();
}

function drop(ev) {
    ev.preventDefault();
    let dest = ev.target;
    let name = ev.dataTransfer.getData('text', ev.innerText);
    // dest.innerText = name;
    let x = cellRow(dest);
    let y = cellColumn(dest);
    console.log('Dropping', name, 'at', x, y);
    circuit[y][x] = name;
    if (gatesQubits[name] == 2) {
        circuit[y+1][x] = null;
    }
    console.table(circuit);
    updateGrid();
}

function clearGrid() {
    let grid = document.getElementById('container_circuit');
    var child = grid.lastElementChild;

    while (child) {
        grid.removeChild(child);
        child = grid.lastElementChild;
    }
}

function ketToString(n) {
    if (n == 0) {
        return '|0⟩';
    }
    return '|1⟩';
}

function setStates(qubits) {
    for (let i = 0; i < qubits; i++) {
        let cell = document.getElementById(idRowColumn(0, i));
        cell.innerText = ketToString(0);
        circuit[i][0] = ketToString(0);
        cell.setAttribute('onclick', 'switchState(event.target)');
        cell.setAttribute('ondrop', '');
        cell.setAttribute('ondragover', '');
        // cell.setAttribute('')
    }
}

function switchState(cell) {
    let x = cellRow(cell);
    let y = cellColumn(cell);
    let s = (cell.innerText == ketToString(1)) ? ketToString(0) : ketToString(1);
    cell.innerText = s;
    circuit[y][x] = s;
}


function idRowColumn(i, j) {
    return `r${i}_${j}`
}

function cellRow(element) {
    return parseInt(element.id.slice(1).split('_')[0], 10);
}

function cellColumn(element) {
    return parseInt(element.id.slice(1).split('_')[1], 10);
}

function updateGridSize() {
    let qubits = parseInt(document.getElementById('qubits_input').value);
    let steps = parseInt(document.getElementById('steps_input').value);
    if (isNaN(qubits) || isNaN(steps)) {
        return;
    }
    console.log(`Side updated: ${steps} steps, ${qubits} qubits`);

    circuit = Array(qubits);
    for (let i = 0; i < qubits; i++) {
        circuit[i] = Array(steps).fill('');
    }
    updateGrid();
}

function createCell(i, j, name = '') {
    let qubits = gatesQubits[name];
    let el = document.createElement('div');
    el.style.gridColumn = `${i+1} / ${i+2}`;
    el.style.gridRow = `${j+1} / span ${qubits}`;
    el.style.aspectRatio = (qubits == 2) ? '0.5' : '1';
    el.style.height = (qubits == 2) ? '75%' : '50%';
    el.setAttribute('class', 'sub_container_portes');
    el.setAttribute('id', idRowColumn(i, j));
    el.setAttribute('ondrop', 'drop(event)');
    el.setAttribute('ondragover', 'allowDrop(event)');
    el.style.zIndex = '10';

    return el;
}

function updateGrid() {
    let rows = circuit[0].length;
    let columns = circuit.length;
    let grid = document.getElementById('container_circuit');
    grid.style.gridTemplateColumns = 'auto '.repeat(rows);
    grid.style.gridTemplateRows = 'auto '.repeat(columns);
    clearGrid();

    for (let i = 0; i < rows; i++) {
        for (let j = 0; j < columns; j++) {
            let name = circuit[j][i];
            if (name != null) {
                let cell = createCell(i, j, name);
                cell.innerText = name;
                grid.appendChild(cell);
            }
        }
    }
    setStates(columns);
}

function runCircuit() {
    console.log('Running ...')
}
