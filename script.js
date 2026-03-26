let chart;
const inputsDiv = document.getElementById("inputs");

document.getElementById("calculo").addEventListener("change", mostrarInputs);
document.getElementById("tipo").addEventListener("change", mostrarInputs);

window.onload = mostrarInputs;

// INPUTS
function mostrarInputs() {
    let tipo = document.getElementById("tipo").value;
    let calc = document.getElementById("calculo").value;

    inputsDiv.innerHTML = "";

    if (calc === "recuperacion") {
        if (tipo === "metalica") {
            inputsDiv.innerHTML = `
                <input type="number" id="cabeza" placeholder="Ley cabeza">
                <input type="number" id="concentrado" placeholder="Ley concentrado">
            `;
        } else {
            inputsDiv.innerHTML = `
                <input type="number" id="produccion" placeholder="Producción">
                <input type="number" id="humedad" placeholder="Humedad %">
            `;
        }
    }

    if (calc === "balance") {
        inputsDiv.innerHTML = `
            <input type="number" id="F" placeholder="Alimentación">
            <input type="number" id="C" placeholder="Concentrado">
        `;
    }
}

// CALCULO
function calcular() {
    let tipo = document.getElementById("tipo").value;
    let calc = document.getElementById("calculo").value;
    let res = document.getElementById("resultado");

    res.innerHTML = "";

    if (calc === "recuperacion") {
        if (tipo === "metalica") {
            let cabeza = parseFloat(cabeza.value);
            let conc = parseFloat(concentrado.value);

            let rec = (conc / cabeza) * 100;

            let msg = rec < 60 ? "⚠️ Baja" : rec < 85 ? "✅ Media" : "🚀 Alta";

            res.innerHTML = `Recuperación: ${rec.toFixed(2)}%<br>${msg}`;
            grafico(["Cabeza","Conc"],[cabeza,conc]);
        } else {
            let prod = parseFloat(produccion.value);
            let hum = parseFloat(humedad.value);

            let seco = prod * (1 - hum/100);

            res.innerHTML = `Producto seco: ${seco.toFixed(2)}`;
            grafico(["Producción","Seco"],[prod,seco]);
        }
    }

    if (calc === "balance") {
        let F = parseFloat(document.getElementById("F").value);
        let C = parseFloat(document.getElementById("C").value);

        let T = F - C;

        res.innerHTML = `Relave: ${T}`;
        grafico(["F","C","T"],[F,C,T]);
    }
}

// LIMPIAR
function limpiar() {
    document.getElementById("resultado").innerHTML = "";
    if (chart) chart.destroy();
    mostrarInputs();
}

// GRAFICO
function grafico(labels,data) {
    const ctx = document.getElementById("grafico").getContext("2d");
    if(chart) chart.destroy();

    chart = new Chart(ctx,{
        type:"bar",
        data:{labels:labels,datasets:[{data:data}]}
    });
}

// CONVERSOR
function convertir(){
    let v = parseFloat(valor.value);
    let u = unidad.value;

    if(u==="porcentaje"){
        conversion.innerHTML = v + "% = " + (v*10000) + " ppm";
    } else {
        conversion.innerHTML = v + " ppm = " + (v/10000) + "%";
    }
}

// PROCESOS
function cargarProcesos(){
    let el = elemento.value;
    proceso.innerHTML = "<option>Selecciona proceso</option>";

    if(el==="Cu"){
        proceso.innerHTML += `<option value="lix">Lixiviación</option>`;
        proceso.innerHTML += `<option value="fun">Fundición</option>`;
    }

    if(el==="Ca"){
        proceso.innerHTML += `<option value="cal">Calcinación</option>`;
    }

    if(el==="Na"){
        proceso.innerHTML += `<option value="eva">Evaporación</option>`;
    }
}

function mostrarProceso(){
    let p = proceso.value;

    let info = {
        lix:"Lixiviación con ácido sulfúrico",
        fun:"Fundición a alta temperatura",
        cal:"Transformación CaCO3 → CaO",
        eva:"Evaporación solar de sal"
    };

    infoProceso.innerHTML = info[p] || "";
}