const inputsDiv = document.getElementById("inputs");

// PROCESOS
function cargarProcesos() {
    let el = document.getElementById("elemento").value;
    let proceso = document.getElementById("proceso");

    proceso.innerHTML = "<option value=''>Selecciona proceso</option>";

    if (el === "Cu") {
        proceso.innerHTML += `<option value="hidro">Hidrometalurgia</option>`;
        proceso.innerHTML += `<option value="piro">Pirometalurgia</option>`;
    }

    if (el === "Ca") {
        proceso.innerHTML += `<option value="cal">Calcinación</option>`;
    }

    if (el === "Na") {
        proceso.innerHTML += `<option value="eva">Evaporación</option>`;
    }
}

// INPUTS DINÁMICOS
function mostrarInputs() {
    let el = document.getElementById("elemento").value;
    let proceso = document.getElementById("proceso").value;

    inputsDiv.innerHTML = "";

    if (el === "Cu" && proceso === "hidro") {
        inputsDiv.innerHTML = `
            <input type="number" id="ley" placeholder="Ley cabeza (%)">
            <input type="number" id="ton" placeholder="Toneladas (t)">
            <input type="number" id="rec" placeholder="Recuperación (%)">
            <input type="number" id="acido" placeholder="Ácido (kg)">
        `;
    }

    if (el === "Cu" && proceso === "piro") {
        inputsDiv.innerHTML = `
            <input type="number" id="ley" placeholder="Ley cabeza (%)">
            <input type="number" id="leyC" placeholder="Ley concentrado (%)">
            <input type="number" id="ton" placeholder="Toneladas (t)">
            <input type="number" id="rec" placeholder="Recuperación (%)">
        `;
    }

    if (el === "Ca") {
        inputsDiv.innerHTML = `
            <input type="number" id="ton" placeholder="Toneladas">
        `;
    }

    if (el === "Na") {
        inputsDiv.innerHTML = `
            <input type="number" id="ton" placeholder="Producción sal">
        `;
    }
}

// CALCULAR
function calcular() {
    let el = document.getElementById("elemento").value;
    let proceso = document.getElementById("proceso").value;
    let res = document.getElementById("resultado");

    res.innerHTML = "";

    // HIDROMETALURGIA
    if (el === "Cu" && proceso === "hidro") {
        let ley = parseFloat(document.getElementById("ley").value);
        let ton = parseFloat(document.getElementById("ton").value);
        let rec = parseFloat(document.getElementById("rec").value);
        let acido = parseFloat(document.getElementById("acido").value);

        let contenido = ton * (ley / 100);
        let recuperado = contenido * (rec / 100);
        let consumo = acido / ton;

        res.innerHTML = `
            🔵 Hidrometalurgia<br><br>
            Cobre contenido: ${contenido.toFixed(2)} t<br>
            Cobre recuperado: ${recuperado.toFixed(2)} t<br>
            Consumo ácido: ${consumo.toFixed(2)} kg/t
        `;
    }

    // PIROMETALURGIA
    if (el === "Cu" && proceso === "piro") {
        let ley = parseFloat(document.getElementById("ley").value);
        let leyC = parseFloat(document.getElementById("leyC").value);
        let ton = parseFloat(document.getElementById("ton").value);
        let rec = parseFloat(document.getElementById("rec").value);

        let contenido = ton * (ley / 100);
        let recuperado = contenido * (rec / 100);

        res.innerHTML = `
            🔴 Pirometalurgia<br><br>
            Cobre contenido: ${contenido.toFixed(2)} t<br>
            Cobre recuperado: ${recuperado.toFixed(2)} t<br>
            Ley concentrado: ${leyC} %
        `;
    }

    if (el === "Ca") {
        let ton = parseFloat(document.getElementById("ton").value);
        res.innerHTML = `Producción caliza: ${ton} t`;
    }

    if (el === "Na") {
        let ton = parseFloat(document.getElementById("ton").value);
        res.innerHTML = `Producción sal: ${ton} t`;
    }
}

// LIMPIAR
function limpiar() {
    document.getElementById("resultado").innerHTML = "";
    inputsDiv.innerHTML = "";
}

// CONVERSOR
function convertir() {
    let v = parseFloat(document.getElementById("valor").value);
    let u = document.getElementById("unidad").value;

    if (u === "porcentaje") {
        document.getElementById("conversion").innerHTML =
            v + "% = " + (v * 10000) + " ppm";
    } else {
        document.getElementById("conversion").innerHTML =
            v + " ppm = " + (v / 10000) + "%";
    }
}