/* ==========================================================================
   Chatbot flotante del proyecto (JavaScript vanilla, sin frameworks).

   Para usarlo en cualquier página alcanza con UNA línea antes de </body>:
       <script src="/chatbot/chatbot.js" defer></script>

   Este archivo se encarga de todo lo demás:
     1. Cargar su propio CSS (chatbot.css, en la misma carpeta).
     2. Cargar desde CDN: marked (Markdown), highlight.js (código) y KaTeX (fórmulas).
     3. Crear el botón, el panel y manejar la conversación con /api/chat.

   Importante: el bot nunca inventa texto. Lo que se muestra como respuesta es
   el fragmento literal del .md que devolvió el servidor.
   ========================================================================== */
(() => {
  'use strict';

  // ---------------------------------------------------------------------
  // Configuración
  // ---------------------------------------------------------------------
  const API = '/api/chat';
  const MAX_CARACTERES = 300;          // igual que el límite de Pydantic en router.py
  const DEMORA_MINIMA_MS = 350;        // para que el "escribiendo..." no sea un parpadeo
  // Subí este número cada vez que cambies chatbot.css: obliga al navegador a descargarlo de nuevo.
  const VERSION = '2';

  const CDN = {
    marked: 'https://cdn.jsdelivr.net/npm/marked@12.0.2/marked.min.js',
    hljs: 'https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/highlight.min.js',
    hljsCss: 'https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/styles/github-dark.min.css',
    katex: 'https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js',
    katexCss: 'https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css',
  };

  // Botones rápidos del mensaje de bienvenida.
  // tipo "temas": muestra la lista de títulos de esos grupos (sale de GET /api/chat/temas).
  // tipo "pregunta": envía el texto como si el usuario lo hubiera escrito.
  const BOTONES_RAPIDOS = [
    { texto: 'TP1', tipo: 'temas', grupos: ['TP1'] },
    { texto: 'TP2', tipo: 'temas', grupos: ['TP2'] },
    { texto: 'TP3', tipo: 'temas', grupos: ['TP3'] },
    { texto: 'Glosario', tipo: 'pregunta', pregunta: 'Glosario' },
    { texto: '¿Cómo se programó?', tipo: 'temas', grupos: ['Programación', 'Arquitectura'] },
  ];

  // La URL de este script sirve para encontrar chatbot.css en la misma carpeta.
  const urlScript = document.currentScript ? document.currentScript.src : '/chatbot/chatbot.js';

  // ---------------------------------------------------------------------
  // Utilidades para cargar recursos externos
  // ---------------------------------------------------------------------
  function cargarCss(href) {
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = href;
    document.head.appendChild(link);
  }

  function cargarScript(src) {
    return new Promise(resolve => {
      const s = document.createElement('script');
      s.src = src;
      s.async = true;
      s.onload = () => resolve(true);
      s.onerror = () => resolve(false);   // si el CDN falla, el chat sigue andando en texto plano
      document.head.appendChild(s);
    });
  }

  cargarCss(new URL(`chatbot.css?v=${VERSION}`, urlScript).href);
  cargarCss(CDN.hljsCss);
  cargarCss(CDN.katexCss);
  // Se descargan en paralelo; render() los espera antes de dibujar una respuesta.
  const librerias = Promise.all([cargarScript(CDN.marked), cargarScript(CDN.hljs), cargarScript(CDN.katex)])
    .then(() => configurarMarked());

  function configurarMarked() {
    if (!window.marked) return;
    window.marked.use({
      gfm: true,
      breaks: false,
      renderer: {
        // Seguridad: si un .md trae HTML crudo, se muestra como texto y no se ejecuta.
        html(html) {
          return escapar(typeof html === 'string' ? html : html.text || '');
        },
        // Los enlaces relativos de los .md (../../ejercicios/ej01.py) no existen en la web:
        // se muestran como texto. Los enlaces http(s) se abren en otra pestaña.
        link(href, title, text) {
          if (typeof href === 'object' && href) ({ href, title, text } = href);
          if (!/^https?:\/\//i.test(href || '')) return `<span>${text}</span>`;
          const t = title ? ` title="${escapar(title)}"` : '';
          return `<a href="${escapar(href)}"${t} target="_blank" rel="noopener noreferrer">${text}</a>`;
        },
      },
    });
  }

  // Los títulos de los .md a veces traen `código`; para mostrarlos se quitan las comillas invertidas.
  const tituloVisible = texto => String(texto).replace(/`/g, '');

  function escapar(texto) {
    return String(texto).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
  }

  // ---------------------------------------------------------------------
  // Markdown -> HTML
  // ---------------------------------------------------------------------
  // Las fórmulas \( ... \), \[ ... \] y $$ ... $$ se apartan ANTES de pasar por marked,
  // porque marked interpretaría las barras invertidas como escapes y rompería el LaTeX.
  // Después se vuelven a insertar y KaTeX las dibuja.
  const RE_CODIGO = /(```[\s\S]*?```|~~~[\s\S]*?~~~|`[^`\n]+`)/g;
  const RE_FORMULA = /\\\[([\s\S]+?)\\\]|\$\$([\s\S]+?)\$\$|\\\(([\s\S]+?)\\\)/g;

  function apartarFormulas(md) {
    const formulas = [];
    const partes = md.split(RE_CODIGO);   // los índices impares son bloques de código: no se tocan
    const texto = partes.map((parte, i) => (i % 2 === 1 ? parte : parte.replace(RE_FORMULA, (_, bloque, dolares, linea) => {
      formulas.push({ tex: bloque || dolares || linea, display: Boolean(bloque || dolares) });
      return `@@F${formulas.length - 1}@@`;
    }))).join('');
    return { texto, formulas };
  }

  function markdownAHtml(md) {
    const { texto, formulas } = apartarFormulas(md);
    let html = window.marked ? window.marked.parse(texto) : `<p>${escapar(texto).replace(/\n/g, '<br>')}</p>`;
    html = html.replace(/@@F(\d+)@@/g, (_, n) => {
      const f = formulas[Number(n)];
      return `<span class="pe-chat-latex" data-display="${f.display ? 1 : 0}">${escapar(f.tex)}</span>`;
    });
    return html;
  }

  // Aplica KaTeX y highlight.js sobre un elemento ya insertado en la página.
  function decorar(elemento) {
    elemento.querySelectorAll('.pe-chat-latex').forEach(span => {
      if (!window.katex) return;   // sin KaTeX queda el LaTeX como texto, igual se entiende
      try {
        window.katex.render(span.textContent, span, { displayMode: span.dataset.display === '1', throwOnError: false });
      } catch (_) { /* fórmula inválida: se deja el texto original */ }
    });
    if (window.hljs) elemento.querySelectorAll('pre code').forEach(b => window.hljs.highlightElement(b));
  }

  // ---------------------------------------------------------------------
  // Construcción de la interfaz
  // ---------------------------------------------------------------------
  const raiz = document.createElement('div');
  raiz.className = 'pe-chat';
  raiz.innerHTML = `
    <button class="pe-chat-boton" type="button" aria-expanded="false" aria-controls="pe-chat-panel" aria-label="Abrir el asistente de los TPs">
      <svg class="pe-chat-icono-abrir" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 5.75A2.75 2.75 0 0 1 7.75 3h8.5A2.75 2.75 0 0 1 19 5.75v6.5A2.75 2.75 0 0 1 16.25 15H10l-4.5 3v-3.2A2.75 2.75 0 0 1 5 12.25z"/><path d="M9 8h6M9 11h4"/></svg>
      <svg class="pe-chat-icono-cerrar" viewBox="0 0 24 24" aria-hidden="true"><path d="m6 6 12 12M18 6 6 18"/></svg>
    </button>
    <section class="pe-chat-panel" id="pe-chat-panel" role="dialog" aria-labelledby="pe-chat-titulo" hidden>
      <header class="pe-chat-cabecera">
        <span class="pe-chat-cabecera-marca" aria-hidden="true">∑</span>
        <div class="pe-chat-cabecera-texto">
          <h2 id="pe-chat-titulo">Asistente de los TPs</h2>
          <p>Responde con los apuntes del proyecto</p>
        </div>
        <button class="pe-chat-icono" type="button" data-accion="reiniciar" aria-label="Empezar de nuevo" title="Empezar de nuevo">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12a8 8 0 1 0 2.4-5.7M4 4v4h4"/></svg>
        </button>
        <button class="pe-chat-icono" type="button" data-accion="cerrar" aria-label="Cerrar" title="Cerrar">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="m6 6 12 12M18 6 6 18"/></svg>
        </button>
      </header>
      <div class="pe-chat-mensajes" role="log" aria-live="polite"></div>
      <form class="pe-chat-form">
        <label class="pe-chat-oculto" for="pe-chat-input">Escribí tu pregunta</label>
        <input class="pe-chat-input" id="pe-chat-input" type="text" maxlength="${MAX_CARACTERES}" autocomplete="off" placeholder="Preguntá sobre los TPs o el código…">
        <button class="pe-chat-enviar" type="submit" aria-label="Enviar">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h13m-5-5 5 5-5 5"/></svg>
        </button>
      </form>
    </section>`;

  const boton = raiz.querySelector('.pe-chat-boton');
  const panel = raiz.querySelector('.pe-chat-panel');
  const mensajes = raiz.querySelector('.pe-chat-mensajes');
  const form = raiz.querySelector('.pe-chat-form');
  const input = raiz.querySelector('.pe-chat-input');
  const enviar = raiz.querySelector('.pe-chat-enviar');

  let ocupado = false;
  let cacheTemas = null;

  // ---------------------------------------------------------------------
  // Abrir / cerrar
  // ---------------------------------------------------------------------
  function abrir() {
    panel.hidden = false;
    raiz.classList.add('pe-chat--abierto');
    boton.setAttribute('aria-expanded', 'true');
    boton.setAttribute('aria-label', 'Cerrar el asistente');
    if (!mensajes.childElementCount) bienvenida();
    input.focus();
  }

  function cerrar() {
    panel.hidden = true;
    raiz.classList.remove('pe-chat--abierto');
    boton.setAttribute('aria-expanded', 'false');
    boton.setAttribute('aria-label', 'Abrir el asistente de los TPs');
    boton.focus();
  }

  boton.addEventListener('click', () => (panel.hidden ? abrir() : cerrar()));
  raiz.querySelector('[data-accion="cerrar"]').addEventListener('click', cerrar);
  raiz.querySelector('[data-accion="reiniciar"]').addEventListener('click', () => {
    mensajes.replaceChildren();
    bienvenida();
    input.focus();
  });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && !panel.hidden) cerrar(); });

  // ---------------------------------------------------------------------
  // Mensajes
  // ---------------------------------------------------------------------
  function bajarScroll() {
    mensajes.scrollTop = mensajes.scrollHeight;
  }

  function agregarMensaje(tipo) {
    const div = document.createElement('div');
    div.className = `pe-chat-msj pe-chat-msj--${tipo}`;
    mensajes.appendChild(div);
    bajarScroll();
    return div;
  }

  // Crea una fila de botones. Cada opción es { texto, alHacerClick }.
  function crearOpciones(opciones, comoLista = false) {
    const fila = document.createElement('div');
    fila.className = 'pe-chat-opciones' + (comoLista ? ' pe-chat-opciones--lista' : '');
    opciones.forEach(({ texto, alHacerClick }) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'pe-chat-opcion';
      b.textContent = tituloVisible(texto);
      b.addEventListener('click', alHacerClick);
      fila.appendChild(b);
    });
    return fila;
  }

  function botonesRapidos() {
    return crearOpciones(BOTONES_RAPIDOS.map(op => ({
      texto: op.texto,
      alHacerClick: () => (op.tipo === 'temas' ? mostrarTemas(op.texto, op.grupos) : preguntar(op.pregunta)),
    })));
  }

  function bienvenida() {
    const msj = agregarMensaje('bot');
    const p = document.createElement('p');
    p.style.margin = '0';
    p.textContent = '¡Hola! Respondo con el contenido de los TPs, sus glosarios y la explicación de cómo se programó el proyecto. Escribí una pregunta o elegí un tema:';
    msj.append(p, botonesRapidos());
  }

  function mostrarEscribiendo() {
    const msj = agregarMensaje('bot');
    msj.innerHTML = '<span class="pe-chat-escribiendo" aria-label="Escribiendo">escribiendo <span></span><span></span><span></span></span>';
    return msj;
  }

  function bloquear(estado) {
    ocupado = estado;
    enviar.disabled = estado;
  }

  const esperar = ms => new Promise(r => setTimeout(r, ms));

  // ---------------------------------------------------------------------
  // Conversación con el backend
  // ---------------------------------------------------------------------
  async function preguntar(texto) {
    texto = String(texto || '').trim().slice(0, MAX_CARACTERES);
    if (!texto || ocupado) return;
    bloquear(true);

    agregarMensaje('usuario').textContent = texto;   // textContent: lo del usuario nunca se interpreta como HTML
    const escribiendo = mostrarEscribiendo();

    try {
      const [respuesta] = await Promise.all([
        fetch(API, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ pregunta: texto }),
        }).then(r => {
          if (!r.ok) throw new Error(`HTTP ${r.status}`);
          return r.json();
        }),
        esperar(DEMORA_MINIMA_MS),
        librerias,
      ]);
      escribiendo.remove();
      mostrarRespuesta(respuesta);
    } catch (error) {
      escribiendo.remove();
      const msj = agregarMensaje('bot');
      msj.classList.add('pe-chat-msj--aviso');
      msj.textContent = 'No pude conectarme con el servidor. Revisá que la app esté corriendo y probá de nuevo.';
      console.error('[chatbot]', error);
    } finally {
      bloquear(false);
      input.focus();
    }
  }

  function mostrarRespuesta(r) {
    const msj = agregarMensaje('bot');

    if (!r.encontrado) {
      msj.classList.add('pe-chat-msj--aviso');
      const p = document.createElement('p');
      p.style.margin = '0';
      p.textContent = r.respuesta_md;
      msj.append(p, botonesRapidos());
      bajarScroll();
      return;
    }

    // Título de la sección (es el ## / ### del .md, no texto inventado).
    const titulo = document.createElement('h3');
    titulo.className = 'pe-chat-titulo';
    titulo.textContent = tituloVisible(r.titulo);

    // Contenido literal del .md, renderizado.
    const cuerpo = document.createElement('div');
    cuerpo.className = 'pe-chat-md';
    cuerpo.innerHTML = markdownAHtml(r.respuesta_md);

    // Fuente: "📄 TP2 · Medidas de dispersión"
    const fuente = document.createElement('div');
    fuente.className = 'pe-chat-fuente';
    fuente.textContent = `📄 ${r.tp} · ${tituloVisible(r.titulo)}`;
    fuente.title = r.archivo;

    msj.append(titulo, cuerpo, fuente);

    if (r.sugerencias && r.sugerencias.length) {
      const etiqueta = document.createElement('div');
      etiqueta.className = 'pe-chat-fuente';
      etiqueta.style.borderTop = '0';
      etiqueta.textContent = 'También puede interesarte:';
      msj.append(etiqueta, crearOpciones(r.sugerencias.map(s => ({ texto: s, alHacerClick: () => preguntar(s) }))));
    }

    decorar(cuerpo);
    // Se deja visible el comienzo de la respuesta (las secciones pueden ser largas).
    mensajes.scrollTop = msj.offsetTop - 8;
  }

  // Lista de títulos de uno o más grupos (TP1, Programación...), como botones.
  async function mostrarTemas(nombre, grupos) {
    if (ocupado) return;
    agregarMensaje('usuario').textContent = nombre;
    try {
      if (!cacheTemas) {
        const r = await fetch(`${API}/temas`);
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        cacheTemas = await r.json();
      }
      const opciones = [];
      grupos.forEach(grupo => (cacheTemas[grupo] || []).forEach(titulo => {
        const etiqueta = `${grupo} · ${titulo}`;   // el backend reconoce esta forma exacta
        opciones.push({ texto: grupos.length > 1 ? etiqueta : titulo, alHacerClick: () => preguntar(etiqueta) });
      }));

      const msj = agregarMensaje('bot');
      const p = document.createElement('p');
      p.style.margin = '0';
      p.textContent = opciones.length ? `Temas de ${nombre}:` : `No hay temas cargados para ${nombre}.`;
      msj.append(p, crearOpciones(opciones, true));
      bajarScroll();
    } catch (error) {
      const msj = agregarMensaje('bot');
      msj.classList.add('pe-chat-msj--aviso');
      msj.textContent = 'No pude cargar la lista de temas.';
      console.error('[chatbot]', error);
    }
  }

  form.addEventListener('submit', e => {
    e.preventDefault();
    const texto = input.value;
    input.value = '';
    preguntar(texto);
  });

  // El script usa "defer", así que el <body> ya existe cuando se ejecuta.
  document.body.appendChild(raiz);
})();
