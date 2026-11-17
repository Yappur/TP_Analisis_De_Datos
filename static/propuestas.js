const direcciones = {
  paper: {
    numero: "01", nombre: "Academic Paper",
    tesis: "Una hoja universitaria bien diseñada convierte el ejercicio en el centro de la experiencia.",
    porQue: "La cuadrícula tenue evoca el trabajo matemático y la columna de lectura sostiene enunciados largos sin competir con ellos.",
    mejor: "Lectura diaria, resolución paso a paso y consulta prolongada de enunciados.",
    coste: "Bajo: comparte tokens y componentes con el sitio existente; CSS y temas nativos.",
  },
  math: {
    numero: "02", nombre: "Modern Mathematics",
    tesis: "Una retícula geométrica y una ficha dividida ordenan el ejercicio como un objeto matemático preciso.",
    porQue: "Una columna separa metadatos y enunciado; el ritmo amplio aporta claridad sin adornos editoriales.",
    mejor: "Una experiencia más minimalista y estructurada para alternar rápidamente entre ejercicios.",
    coste: "Medio: los metadatos necesitan reglas para ocultarse o reorganizarse en pantallas estrechas.",
  },
  notebook: {
    numero: "03", nombre: "Scientific Notebook",
    tesis: "El margen de anotación y la ficha de observación evocan un cuaderno de investigación en uso.",
    porQue: "El margen marcado, las líneas y las etiquetas técnicas organizan el contenido con una personalidad de laboratorio.",
    mejor: "Un tono de apuntes experimentales y seguimiento de datos durante la resolución.",
    coste: "Medio: sus motivos de cuaderno requieren control de contraste y densidad en móvil.",
  },
  editorial: {
    numero: "04", nombre: "Editorial Academic",
    tesis: "Una jerarquía tipográfica de revista lleva la mirada del título al texto del problema.",
    porQue: "El enunciado se trata como una cita principal; una composición abierta favorece la lectura de texto extenso.",
    mejor: "Enunciados narrativos largos y una interfaz con énfasis en la lectura pausada.",
    coste: "Medio: la gran escala tipográfica necesita buen ancho de pantalla y ajuste responsive fino.",
  },
  lab: {
    numero: "05", nombre: "Digital Laboratory",
    tesis: "Un panel técnico oscuro presenta los ejercicios como registros listos para inspeccionar.",
    porQue: "Las etiquetas monoespaciadas y la cuadrícula de contraste bajo sugieren una herramienta de análisis precisa.",
    mejor: "Sesiones nocturnas de consulta y una identidad más instrumental y contemporánea.",
    coste: "Medio-alto: exige afinar el contraste oscuro de tablas, contenido académico y gráficos.",
  },
};

const selector = document.querySelector(".selector-direcciones");
const shell = document.querySelector(".preview-shell");
const tabs = [...selector.querySelectorAll("[role='tab']")];

function seleccionarDireccion(clave) {
  const direccion = direcciones[clave];
  shell.dataset.variant = clave;
  tabs.forEach((tab) => {
    const seleccionada = tab.dataset.variant === clave;
    tab.setAttribute("aria-selected", String(seleccionada));
    tab.tabIndex = seleccionada ? 0 : -1;
  });
  document.getElementById("direction-index").textContent = `DIRECCIÓN ${direccion.numero}`;
  document.getElementById("direction-name").textContent = direccion.nombre;
  document.getElementById("direction-thesis").textContent = direccion.tesis;
  document.getElementById("direction-why").textContent = direccion.porQue;
  document.getElementById("direction-fit").textContent = direccion.mejor;
  document.getElementById("direction-cost").textContent = direccion.coste;
}

selector.addEventListener("click", (event) => {
  const tab = event.target.closest("[role='tab']");
  if (tab) seleccionarDireccion(tab.dataset.variant);
});

selector.addEventListener("keydown", (event) => {
  const indice = tabs.indexOf(document.activeElement);
  if (indice < 0 || !["ArrowRight", "ArrowLeft", "Home", "End"].includes(event.key)) return;
  event.preventDefault();
  const siguiente = event.key === "Home" ? 0 : event.key === "End" ? tabs.length - 1
    : (indice + (event.key === "ArrowRight" ? 1 : tabs.length - 1)) % tabs.length;
  tabs[siguiente].focus();
  seleccionarDireccion(tabs[siguiente].dataset.variant);
});

const toggle = document.querySelector(".theme-toggle");
const temaGuardado = localStorage.getItem("tp-estadistica-tema");
const temaInicial = temaGuardado || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
document.documentElement.dataset.theme = temaInicial;

function actualizarToggle() {
  const oscuro = document.documentElement.dataset.theme === "dark";
  toggle.setAttribute("aria-pressed", String(oscuro));
  toggle.setAttribute("aria-label", oscuro ? "Activar modo claro" : "Activar modo oscuro");
}
actualizarToggle();
toggle.addEventListener("click", () => {
  document.documentElement.dataset.theme = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
  localStorage.setItem("tp-estadistica-tema", document.documentElement.dataset.theme);
  actualizarToggle();
});

seleccionarDireccion("paper");

fetch("/api/ejercicios/1")
  .then((respuesta) => {
    if (!respuesta.ok) throw new Error("API no disponible");
    return respuesta.json();
  })
  .then((ejercicio) => {
    document.getElementById("exercise-number").textContent = String(ejercicio.numero).padStart(2, "0");
    document.getElementById("exercise-index").textContent = `Ejercicio ${String(ejercicio.numero).padStart(2, "0")}`;
    document.getElementById("exercise-title").textContent = ejercicio.titulo;
    document.getElementById("exercise-statement").innerHTML = ejercicio.enunciado;
    document.getElementById("excel-link").href = ejercicio.excel_url;
  })
  .catch(() => {
    document.getElementById("exercise-title").textContent = "Vista previa del ejercicio";
    document.getElementById("exercise-statement").textContent = "Iniciá la aplicación para ver aquí un enunciado real y completo.";
  });
