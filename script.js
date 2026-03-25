let chart; // para controlar el gráfico

function calcular() {
    let cabeza = parseFloat(document.getElementById("cabeza").value);
    let concentrado = parseFloat(document.getElementById("concentrado").value);
    let tonelaje = parseFloat(document.getElementById("tonelaje").value);
    let resultado = document.getElementById("resultado");

    if (isNaN(cabeza) || isNaN(concentrado) || isNaN(tonelaje)) {
        resultado.innerText = "⚠️ Ingresa todos los datos correctamente";
        return;
    }

    if (cabeza <= 0 || concentrado <= 0 || tonelaje <= 0) {
        resultado.innerText = "⚠️ Los valores deben ser mayores a 0";
        return;
    }

    if (concentrado < cabeza) {
        resultado.innerText = "⚠️ La ley de concentrado no puede ser menor a la de cabeza";
        return;
    }

    let recuperacion = (concentrado / cabeza) * 100;
    let metal = (cabeza * tonelaje) / 100;

    resultado.innerHTML =
        "📊 <strong>Resultados:</strong><br><br>" +
        "✅ Recuperación: " + recuperacion.toFixed(2) + "%<br>" +
        "📦 Tonelaje: " + tonelaje + " ton<br>" +
        "⛏️ Metal contenido: " + metal.toFixed(2);

    crearGrafico(cabeza, concentrado);
}

function limpiar() {
    document.getElementById("cabeza").value = "";
    document.getElementById("concentrado").value = "";
    document.getElementById("tonelaje").value = "";
    document.getElementById("resultado").innerHTML = "";

    if (chart) {
        chart.destroy();
    }
}

function crearGrafico(cabeza, concentrado) {
    const ctx = document.getElementById("grafico").getContext("2d");

    if (chart) {
        chart.destroy();
    }

    chart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: ["Ley de Cabeza", "Ley de Concentrado"],
            datasets: [{
                label: "Comparación de Leyes (%)",
                data: [cabeza, concentrado]
            }]
        }
    });
}