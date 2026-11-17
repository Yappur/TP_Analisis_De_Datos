let graficos = [];
let ejercicioActual = null;
// Cada página indica su API en <body data-api="...">; el TP 1 usa la ruta original
const API = document.body.dataset.api || "/api/ejercicios";

function inicializarTema() {
  const guardado = localStorage.getItem("tp-estadistica-tema");
  const tema = guardado || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
  document.documentElement.dataset.theme = tema;
  const boton = document.querySelector(".theme-toggle");
  if (!boton) return;
  actualizarBotonTema(boton, tema);
  boton.addEventListener("click", () => {
    const nuevoTema = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
    document.documentElement.dataset.theme = nuevoTema;
    localStorage.setItem("tp-estadistica-tema", nuevoTema);
    actualizarBotonTema(boton, nuevoTema);
    if (ejercicioActual !== null) mostrar(ejercicioActual);
  });
}

function actualizarBotonTema(boton, tema) {
  const oscuro = tema === "dark";
  boton.setAttribute("aria-pressed", String(oscuro));
  boton.setAttribute("aria-label", oscuro ? "Activar modo claro" : "Activar modo oscuro");
}

inicializarTema();

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
  const respuesta = await fetch(API);
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
  ejercicioActual = numero;
  document.querySelectorAll(".menu-ejercicios button").forEach((boton) => {
    const activo = boton.dataset.ejercicio === String(numero);
    boton.classList.toggle("activo", activo);
    if (activo) boton.setAttribute("aria-current", "true");
    else boton.removeAttribute("aria-current");
  });

  const respuesta = await fetch(`${API}/${numero}`);
  const ejercicio = await respuesta.json();
  limpiarGraficos();

  let html = `
    <header class="ejercicio-cabecera">
      <span class="ejercicio-numero">Ejercicio ${ejercicio.numero}</span>
      <h2>${ejercicio.titulo}</h2>
    </header>
    <div class="enunciado-wrap">
      <p class="enunciado-label">Enunciado</p>
      <p class="enunciado">${ejercicio.enunciado}</p>
    </div>
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
          backgroundColor: getComputedStyle(document.documentElement).getPropertyValue("--accent").trim(),
          borderColor: getComputedStyle(document.documentElement).getPropertyValue("--accent-strong").trim(),
          borderWidth: 1,
        })),
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            labels: {
              color: getComputedStyle(document.documentElement).getPropertyValue("--ink").trim(),
              font: { weight: "bold" },
            },
          },
        },
        scales: {
          x: {
            ticks: { color: getComputedStyle(document.documentElement).getPropertyValue("--ink-soft").trim() },
            grid: { display: false },
          },
          y: {
            beginAtZero: true,
            ticks: { color: getComputedStyle(document.documentElement).getPropertyValue("--ink-soft").trim() },
            grid: { color: getComputedStyle(document.documentElement).getPropertyValue("--rule").trim() },
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
