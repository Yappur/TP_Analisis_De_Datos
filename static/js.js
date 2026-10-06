let graficos = [];

function limpiarGraficos() {
  graficos.forEach((grafico) => grafico.destroy());
  graficos = [];
}

function tabla(columnas, filas) {
  const cabecera = columnas.map((columna) => `<th scope="col">${columna}</th>`).join("");
  const cuerpo = filas
    .map((fila) => `<tr>${fila.map((valor) => `<td>${valor}</td>`).join("")}</tr>`)
    .join("");

  return `
    <div class="tabla-scroll">
      <table>
        <thead><tr>${cabecera}</tr></thead>
        <tbody>${cuerpo}</tbody>
      </table>
    </div>
  `;
}

async function cargarMenu() {
  const respuesta = await fetch("/api/ejercicios");
  const lista = await respuesta.json();
  const menu = document.getElementById("menu");

  menu.innerHTML = lista
    .map((ejercicio) => (
      `<button type="button" id="b${ejercicio.numero}" data-ejercicio="${ejercicio.numero}" aria-label="${ejercicio.titulo}">
        ${ejercicio.numero}
      </button>`
    ))
    .join("");

  menu.querySelectorAll("button").forEach((boton) => {
    boton.addEventListener("click", () => mostrar(Number(boton.dataset.ejercicio)));
  });

  if (lista.length > 0) {
    await mostrar(lista[0].numero);
  }
}

async function mostrar(numero) {
  document.querySelectorAll(".menu-ejercicios button").forEach((boton) => {
    boton.classList.toggle("activo", boton.dataset.ejercicio === String(numero));
  });

  const respuesta = await fetch(`/api/ejercicios/${numero}`);
  const ejercicio = await respuesta.json();
  limpiarGraficos();

  let html = `
    <h2>${ejercicio.titulo}</h2>
    <p class="enunciado">${ejercicio.enunciado}</p>
    <p class="enlace-excel">
      <a href="${ejercicio.excel_url}" target="_blank" rel="noopener noreferrer">
        Abrir Excel de ${ejercicio.titulo}
      </a>
    </p>
  `;

  ejercicio.bloques.forEach((bloque, indice) => {
    html += `
      <section class="bloque">
        <h3>${bloque.subtitulo}</h3>
        ${tabla(bloque.columnas, bloque.filas)}
        ${bloque.notas.length ? `<ul class="notas">${bloque.notas.map((nota) => `<li>${nota}</li>`).join("")}</ul>` : ""}
        ${bloque.grafico ? `<div class="grafico"><canvas id="g${indice}"></canvas></div>` : ""}
      </section>
    `;
  });

  document.getElementById("contenido").innerHTML = html;

  ejercicio.bloques.forEach((bloque, indice) => {
    if (!bloque.grafico || typeof Chart === "undefined") return;

    const contexto = document.getElementById(`g${indice}`);
    graficos.push(new Chart(contexto, {
      type: "bar",
      data: {
        labels: bloque.grafico.etiquetas,
        datasets: bloque.grafico.series.map((serie) => ({
          label: serie.nombre,
          data: serie.valores,
          backgroundColor: "rgba(22, 106, 122, 0.78)",
          borderColor: "#166a7a",
          borderWidth: 1,
        })),
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            labels: {
              color: "#203038",
              font: { weight: "bold" },
            },
          },
        },
        scales: {
          x: {
            ticks: { color: "#60747d" },
            grid: { display: false },
          },
          y: {
            beginAtZero: true,
            ticks: { color: "#60747d" },
            grid: { color: "rgba(96, 116, 125, 0.18)" },
          },
        },
      },
    }));
  });
}

cargarMenu().catch(() => {
  document.getElementById("contenido").innerHTML = (
    '<p class="estado">No se pudieron cargar los ejercicios.</p>'
  );
});
