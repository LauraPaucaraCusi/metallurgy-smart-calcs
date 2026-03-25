function calcular() {
    let cabeza = parseFloat(document.getElementById("cabeza").value);
    let concentrado = parseFloat(document.getElementById("concentrado").value);
    let tonelaje = parseFloat(document.getElementById("tonelaje").value);
    let resultado = document.getElementById("resultado");

    if (isNaN(cabeza) || isNaN(concentrado) || isNaN(tonelaje)) {
        resultado.innerText = "⚠️ Completa todos los campos";
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

    resultado.innerText =
        "✅ Recuperación: " + recuperacion.toFixed(2) + "%\n" +
        "📦 Tonelaje procesado: " + tonelaje + " ton";
}