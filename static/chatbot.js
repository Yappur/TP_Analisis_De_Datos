(() => {
  const panel = document.getElementById('chatbot-panel');
  const toggle = document.getElementById('chatbot-toggle');
  const close = document.getElementById('chatbot-close');
  const fresh = document.getElementById('chatbot-new');
  const form = document.getElementById('chatbot-form');
  const input = document.getElementById('chatbot-input');
  const send = document.getElementById('chatbot-send');
  const messages = document.getElementById('chatbot-messages');
  const status = document.getElementById('chatbot-status');
  const statusDot = document.querySelector('.chatbot-status-dot');
  const welcomeHTML = messages.innerHTML;
  let pending = false;
  let lastQuestion = '';

  const escapeHTML = value => String(value).replace(/[&<>"']/g, char => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  })[char]);

  function readableMath(value) {
    const subscripts = { '0':'₀','1':'₁','2':'₂','3':'₃','4':'₄','5':'₅','6':'₆','7':'₇','8':'₈','9':'₉','i':'ᵢ','n':'ₙ','x':'ₓ','t':'ₜ','+':'₊','-':'₋' };
    const superscripts = { '0':'⁰','1':'¹','2':'²','3':'³','4':'⁴','5':'⁵','6':'⁶','7':'⁷','8':'⁸','9':'⁹','n':'ⁿ','i':'ⁱ','2':'²','+':'⁺','-':'⁻' };
    return String(value)
      .replace(/\\(?:d?frac)\{([^{}]+)\}\{([^{}]+)\}/g, '($1) / ($2)')
      .replace(/\\sqrt\{([^{}]+)\}/g, '√($1)')
      .replace(/\\(?:bar|overline)\{([^{}]+)\}/g, '$1̄')
      .replace(/\\text\{([^{}]+)\}/g, '$1')
      .replace(/\\sum\b/g, 'Σ').replace(/\\prod\b/g, 'Π')
      .replace(/\\alpha\b/g, 'α').replace(/\\beta\b/g, 'β').replace(/\\mu\b/g, 'μ')
      .replace(/\\sigma\b/g, 'σ').replace(/\\pi\b/g, 'π').replace(/\\theta\b/g, 'θ')
      .replace(/\\cdot\b/g, '·').replace(/\\times\b/g, '×').replace(/\\leq?\b/g, '≤')
      .replace(/\\geq?\b/g, '≥').replace(/\\neq\b/g, '≠').replace(/\\infty\b/g, '∞')
      .replace(/\\%/g, '%').replace(/\\,/g, ' ')
      .replace(/_\{?([0-9inx+-])\}?/g, (_, char) => subscripts[char] || char)
      .replace(/\^\{?([0-9in+-])\}?/g, (_, char) => superscripts[char] || char);
  }

  // Convierte un subconjunto de Markdown a nodos generados por la aplicación.
  // Todo el texto externo se escapa antes de insertar etiquetas permitidas.
  function renderMarkdown(source) {
    const codeBlocks = [];
    let text = String(source).replace(/```([^\n`]*)\n([\s\S]*?)```/g, (_, language, code) => {
      const placeholder = `@@CODE${codeBlocks.length}@@`;
      codeBlocks.push(`<pre><code>${escapeHTML(code.replace(/\n$/, ''))}</code></pre>`);
      return `\n${placeholder}\n`;
    });
    const math = [];
    text = text.replace(/\\\[([\s\S]+?)\\\]|\\\(([^\n]+?)\\\)|\$\$([\s\S]+?)\$\$|\$([^$\n]+)\$/g, (_, displayBlock, inlineParen, displayDollar, inlineDollar) => {
      const placeholder = `@@MATH${math.length}@@`;
      const displayClass = displayBlock || displayDollar ? ' chatbot-math--display' : '';
      math.push(`<span class="chatbot-math${displayClass}">${escapeHTML(readableMath(displayBlock || inlineParen || displayDollar || inlineDollar))}</span>`);
      return placeholder;
    });
    text = escapeHTML(text);
    text = text.replace(/`([^`\n]+)`/g, '<code>$1</code>')
      .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
      .replace(/\*([^*\n]+)\*/g, '<em>$1</em>');
    const blocks = text.split(/\n{2,}/).map(block => {
      const codeMatch = block.trim().match(/^@@CODE(\d+)@@$/);
      if (codeMatch) return codeBlocks[Number(codeMatch[1])];
      const lines = block.split('\n');
      if (lines.every(line => /^\s*[-*]\s+/.test(line))) {
        return `<ul>${lines.map(line => `<li>${line.replace(/^\s*[-*]\s+/, '')}</li>`).join('')}</ul>`;
      }
      if (lines.every(line => /^\s*\d+[.)]\s+/.test(line))) {
        return `<ol>${lines.map(line => `<li>${line.replace(/^\s*\d+[.)]\s+/, '')}</li>`).join('')}</ol>`;
      }
      return `<p>${block.replace(/\n/g, '<br>')}</p>`;
    });
    return blocks.join('').replace(/@@MATH(\d+)@@/g, (_, n) => math[Number(n)] || '');
  }

  function scrollDown() { messages.scrollTop = messages.scrollHeight; }
  function addUser(text) {
    const row = document.createElement('div');
    row.className = 'chatbot-message-row user';
    const bubble = document.createElement('div');
    bubble.className = 'chatbot-message';
    bubble.textContent = text;
    row.append(bubble);
    messages.append(row);
    scrollDown();
  }
  function addTyping() {
    const row = document.createElement('div');
    row.className = 'chatbot-message-row assistant';
    row.id = 'chatbot-typing-row';
    row.setAttribute('aria-label', 'El asistente está escribiendo');
    row.innerHTML = '<div class="chatbot-typing"><span></span><span></span><span></span></div>';
    messages.append(row);
    scrollDown();
  }
  function addError(message) {
    const row = document.createElement('div');
    row.className = 'chatbot-message-row assistant';
    const bubble = document.createElement('div');
    bubble.className = 'chatbot-message';
    const error = document.createElement('p');
    error.className = 'chatbot-error';
    error.textContent = message;
    const retry = document.createElement('button');
    retry.className = 'chatbot-retry';
    retry.type = 'button';
    retry.textContent = 'Reintentar';
    retry.addEventListener('click', () => { row.remove(); submitQuestion(lastQuestion, false); });
    bubble.append(error, retry);
    row.append(bubble);
    messages.append(row);
    scrollDown();
  }
  function addAssistant(data) {
    const row = document.createElement('div');
    row.className = 'chatbot-message-row assistant';
    const bubble = document.createElement('div');
    bubble.className = 'chatbot-message';
    bubble.innerHTML = renderMarkdown(data.answer || '');
    if (Array.isArray(data.sources) && data.sources.length) {
      const sources = document.createElement('div');
      sources.className = 'chatbot-sources';
      const heading = document.createElement('strong');
      heading.textContent = 'Fuentes consultadas:';
      const list = document.createElement('ul');
      data.sources.forEach(source => {
        const item = document.createElement('li');
        item.textContent = `${source.category} → ${source.section} (${source.file})`;
        list.append(item);
      });
      sources.append(heading, list);
      bubble.append(sources);
    }
    row.append(bubble);
    messages.append(row);
    scrollDown();
  }
  async function submitQuestion(raw, addBubble = true) {
    const message = String(raw || '').trim();
    if (!message || pending) return;
    pending = true;
    lastQuestion = message;
    input.value = '';
    input.style.height = 'auto';
    if (addBubble) addUser(message);
    addTyping();
    send.disabled = true;
    input.disabled = true;
    fresh.disabled = true;
    try {
      const response = await fetch('/api/chat', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
      });
      const data = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(data.detail || 'No se pudo conectar con el asistente.');
      addAssistant(data);
    } catch (error) {
      addError(error.message || 'Error de conexión. Revisá tu conexión e intentá nuevamente.');
    } finally {
      document.getElementById('chatbot-typing-row')?.remove();
      pending = false;
      send.disabled = false;
      input.disabled = false;
      fresh.disabled = false;
      if (!panel.hidden) input.focus();
    }
  }
  async function checkHealth() {
    try {
      const response = await fetch('/api/chat/health');
      const data = await response.json();
      const ready = response.ok && data.index_ready && data.model_configured && !data.missing_documents?.length;
      status.textContent = ready ? 'Disponible' : 'Configuración pendiente';
      statusDot.classList.toggle('offline', !ready);
    } catch {
      status.textContent = 'Sin conexión';
      statusDot.classList.add('offline');
    }
  }
  function setOpen(open) {
    panel.hidden = !open;
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Cerrar Asistente Académico' : 'Abrir Asistente Académico');
    if (open) { input.focus(); scrollDown(); }
    else toggle.focus();
  }

  toggle.addEventListener('click', () => setOpen(panel.hidden));
  close.addEventListener('click', () => setOpen(false));
  fresh.addEventListener('click', () => {
    messages.innerHTML = welcomeHTML;
    bindSuggestions();
    input.value = '';
    input.focus();
  });
  function bindSuggestions() {
    messages.querySelectorAll('.chatbot-suggestions button').forEach(button => {
      button.addEventListener('click', () => submitQuestion(button.textContent));
    });
  }
  bindSuggestions();
  form.addEventListener('submit', event => { event.preventDefault(); submitQuestion(input.value); });
  input.addEventListener('keydown', event => {
    if (event.key === 'Enter' && !event.shiftKey) { event.preventDefault(); form.requestSubmit(); }
  });
  input.addEventListener('input', () => {
    input.style.height = 'auto';
    input.style.height = `${Math.min(input.scrollHeight, 120)}px`;
  });
  document.addEventListener('keydown', event => { if (event.key === 'Escape' && !panel.hidden) setOpen(false); });
  checkHealth();
})();
