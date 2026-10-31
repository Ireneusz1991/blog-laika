document.addEventListener('DOMContentLoaded', () => {
  const titleInput = document.getElementById('post-title');
  const slugInput = document.getElementById('post-slug');
  const contentInput = document.getElementById('post-content');
  const previewPane = document.getElementById('preview-pane');
  const wordCountElem = document.getElementById('word-count');
  const readTimeElem = document.getElementById('read-time');

  // Slug generator helper
  function slugify(text) {
    return text.toString().toLowerCase().trim()
      .replace(/ą/g, 'a').replace(/ć/g, 'c').replace(/ę/g, 'e').replace(/ł/g, 'l')
      .replace(/ń/g, 'n').replace(/ó/g, 'o').replace(/ś/g, 's').replace(/ź/g, 'z').replace(/ż/g, 'z')
      .replace(/\s+/g, '-')
      .replace(/[^\w\-]+/g, '')
      .replace(/\-\-+/g, '-')
      .replace(/^-+/, '')
      .replace(/-+$/, '');
  }

  // Auto update slug if user hasn't explicitly edited slug
  let slugUserEdited = slugInput && slugInput.value.length > 0;
  if (slugInput) {
    slugInput.addEventListener('input', () => {
      slugUserEdited = true;
    });
  }

  if (titleInput && slugInput) {
    titleInput.addEventListener('input', () => {
      if (!slugUserEdited) {
        slugInput.value = slugify(titleInput.value);
      }
    });
  }

  // Live markdown preview
  function updateStatsAndPreview() {
    if (!contentInput) return;
    const text = contentInput.value;
    
    // Word count & read time
    const words = text.trim() ? text.trim().split(/\s+/).length : 0;
    const readMin = Math.max(1, Math.round(words / 200));
    
    if (wordCountElem) wordCountElem.innerText = `${words} słów`;
    if (readTimeElem) readTimeElem.innerText = `~${readMin} min czytania`;

    // Preview
    if (previewPane && window.marked) {
      previewPane.innerHTML = window.marked.parse(text);
    }
  }

  if (contentInput) {
    contentInput.addEventListener('input', updateStatsAndPreview);
    updateStatsAndPreview();

    // Editor keyboard shortcuts
    contentInput.addEventListener('keydown', (e) => {
      // Tab key indent
      if (e.key === 'Tab') {
        e.preventDefault();
        const start = contentInput.selectionStart;
        const end = contentInput.selectionEnd;
        contentInput.value = contentInput.value.substring(0, start) + '  ' + contentInput.value.substring(end);
        contentInput.selectionStart = contentInput.selectionEnd = start + 2;
        updateStatsAndPreview();
      }
      
      // Ctrl+S to submit form
      if ((e.ctrlKey || e.metaKey) && e.key === 's') {
        e.preventDefault();
        const form = contentInput.closest('form');
        if (form) form.submit();
      }
    });
  }

  // Formatting Toolbar for Editor
  window.formatEditorText = function(type) {
    if (!contentInput) return;
    const start = contentInput.selectionStart;
    const end = contentInput.selectionEnd;
    const selected = contentInput.value.substring(start, end);
    let replacement = '';
    let offset = 0;

    switch (type) {
      case 'bold':
        replacement = selected ? `**${selected}**` : '**pogrubiony tekst**';
        offset = selected ? replacement.length : 2;
        break;
      case 'italic':
        replacement = selected ? `*${selected}*` : '*pochylony tekst*';
        offset = selected ? replacement.length : 1;
        break;
      case 'h2':
        replacement = `\n\n## ${selected || 'Tytuł sekcji'}\n\n`;
        offset = replacement.length;
        break;
      case 'h3':
        replacement = `\n\n### ${selected || 'Śródtytuł'}\n\n`;
        offset = replacement.length;
        break;
      case 'quote':
        replacement = `\n\n> ${selected || 'Ważny cytat lub myśl przewodnia'}\n\n`;
        offset = replacement.length;
        break;
      case 'ul':
        replacement = selected ? selected.split('\n').map(l => `- ${l}`).join('\n') : '\n- Punkt pierwszy\n- Punkt drugi\n';
        offset = replacement.length;
        break;
      case 'ol':
        replacement = selected ? selected.split('\n').map((l, i) => `${i+1}. ${l}`).join('\n') : '\n1. Krok pierwszy\n2. Krok drugi\n';
        offset = replacement.length;
        break;
      case 'link':
        const url = prompt('Podaj adres URL:', 'https://');
        if (!url) return;
        replacement = `[${selected || 'Tekst linku'}](${url})`;
        offset = replacement.length;
        break;
      case 'image':
        const imgUrl = prompt('Podaj adres URL obrazka:', 'https://images.unsplash.com/...');
        if (!imgUrl) return;
        const alt = prompt('Podaj podpis obrazka:', selected || 'Zdjęcie ilustracyjne');
        replacement = `\n\n![${alt || 'Obraz'}](${imgUrl})\n\n`;
        offset = replacement.length;
        break;
      case 'code':
        replacement = selected.includes('\n') ? `\n\`\`\`python\n${selected}\n\`\`\`\n` : `\`${selected || 'kod'}\``;
        offset = replacement.length;
        break;
      case 'hr':
        replacement = '\n\n---\n\n';
        offset = replacement.length;
        break;
    }

    contentInput.value = contentInput.value.substring(0, start) + replacement + contentInput.value.substring(end);
    contentInput.focus();
    contentInput.selectionStart = contentInput.selectionEnd = start + offset;
    updateStatsAndPreview();
  };

  // Import .md file into Editor
  window.importMdToLocalEditor = function(e) {
    const file = e.target.files && e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function(evt) {
      const text = evt.target.result;
      let title = '';
      let category = '';
      let summary = '';
      let slug = '';
      let body = text;

      if (text.startsWith('---')) {
        const parts = text.split('---');
        if (parts.length >= 3) {
          const front = parts[1].trim();
          body = parts.slice(2).join('---').trim();
          front.split('\n').forEach(line => {
            const idx = line.indexOf(':');
            if (idx > -1) {
              const k = line.substring(0, idx).trim().toLowerCase();
              const v = line.substring(idx + 1).trim().replace(/^["']|["']$/g, '');
              if (k === 'title') title = v;
              if (k === 'category') category = v;
              if (k === 'summary') summary = v;
              if (k === 'slug') slug = v;
            }
          });
        }
      }

      if (!title) {
        for (let l of body.split('\n')) {
          if (l.startsWith('# ')) {
            title = l.replace('# ', '').trim();
            break;
          }
        }
      }

      if (title && titleInput) titleInput.value = title;
      if (slug && slugInput) { slugInput.value = slug; slugUserEdited = true; }
      if (category) {
        const catSelect = document.getElementById('category');
        if (catSelect) catSelect.value = category;
      }
      if (summary) {
        const summaryInput = document.getElementById('summary');
        if (summaryInput) summaryInput.value = summary;
      }

      if (contentInput) {
        contentInput.value = body;
        updateStatsAndPreview();
      }
    };
    reader.readAsText(file, 'UTF-8');
  };
});
