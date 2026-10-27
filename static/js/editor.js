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
});
