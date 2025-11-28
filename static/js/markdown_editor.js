(function(){
  // Undo/Redo history management
  let history = [];
  let historyIndex = -1;
  let isUndoRedo = false;

  function saveState(){
    if(isUndoRedo) return;
    
    const currentState = {
      text: input.value,
      cursor: input.selectionStart
    };
    
    // Remove any future states if we're not at the end
    if(historyIndex < history.length - 1){
      history = history.slice(0, historyIndex + 1);
    }
    
    // Only save if different from last state
    if(history.length === 0 || history[historyIndex].text !== currentState.text){
      history.push(currentState);
      historyIndex++;
      
      // Limit history to 100 states
      if(history.length > 100){
        history.shift();
        historyIndex--;
      }
    }
  }

  function undo(){
    if(historyIndex > 0){
      historyIndex--;
      isUndoRedo = true;
      const state = history[historyIndex];
      input.value = state.text;
      input.selectionStart = input.selectionEnd = state.cursor;
      render();
      isUndoRedo = false;
    }
  }

  function redo(){
    if(historyIndex < history.length - 1){
      historyIndex++;
      isUndoRedo = true;
      const state = history[historyIndex];
      input.value = state.text;
      input.selectionStart = input.selectionEnd = state.cursor;
      render();
      isUndoRedo = false;
    }
  }

  // Debounce helper
  function debounce(fn, delay){
    let t;
    return function(){
      clearTimeout(t);
      const args = arguments;
      t = setTimeout(()=>fn.apply(null, args), delay);
    }
  }

  const saveStateDebounced = debounce(saveState, 100);

  // Initialize markdown-it with code syntax highlighting
  const md = window.markdownit({
    html: true,
    linkify: true,
    typographer: true,
    highlight: function(str, lang){
      if(lang && hljs.getLanguage(lang)){
        try{
          return '<pre class="hljs"><code>' +
                 hljs.highlight(str, {language: lang, ignoreIllegals: true}).value +
                 '</code></pre>';
        }catch(e){}
      }
      return '<pre class="hljs"><code>' + md.utils.escapeHtml(str) + '</code></pre>';
    }
  });

  const input = document.getElementById('mdInput');
  const preview = document.getElementById('previewContent');
  const downloadBtn = document.getElementById('downloadPdf');
  const previewContainer = document.getElementById('previewContainer');
  const fileInput = document.getElementById('fileInputHidden');

  // Toolbar buttons
  const btnBold = document.getElementById('btnBold');
  const btnItalic = document.getElementById('btnItalic');
  const btnHeading = document.getElementById('btnHeading');
  const btnLink = document.getElementById('btnLink');
  const btnCode = document.getElementById('btnCode');
  const btnList = document.getElementById('btnList');
  const openFile = document.getElementById('openFile');
  const saveFile = document.getElementById('saveFile');

  function render(){
    const text = input.value || '';
    const html = md.render(text);
    preview.innerHTML = html;
  }

  const renderDebounced = debounce(render, 150);

  // Wire events
  input.addEventListener('input', function(){
    renderDebounced();
    saveStateDebounced();
  });

  // Helper: Insert text at cursor
  function insertAtCursor(before, after=''){
    const start = input.selectionStart;
    const end = input.selectionEnd;
    const text = input.value;
    const selected = text.substring(start, end);
    
    const replacement = before + selected + after;
    input.value = text.substring(0, start) + replacement + text.substring(end);
    
    // Restore cursor position
    const newPos = start + before.length + selected.length;
    input.selectionStart = input.selectionEnd = newPos;
    input.focus();
    render();
    saveState();
  }

  // Toolbar actions
  btnBold.addEventListener('click', ()=>insertAtCursor('**', '**'));
  btnItalic.addEventListener('click', ()=>insertAtCursor('*', '*'));
  btnHeading.addEventListener('click', ()=>{
    const start = input.selectionStart;
    const text = input.value;
    const lineStart = text.lastIndexOf('\n', start-1) + 1;
    input.value = text.substring(0, lineStart) + '## ' + text.substring(lineStart);
    input.selectionStart = input.selectionEnd = lineStart + 3;
    input.focus();
    render();
    saveState();
  });
  btnLink.addEventListener('click', ()=>insertAtCursor('[', '](url)'));
  btnCode.addEventListener('click', ()=>insertAtCursor('`', '`'));
  btnList.addEventListener('click', ()=>{
    const start = input.selectionStart;
    const text = input.value;
    const lineStart = text.lastIndexOf('\n', start-1) + 1;
    input.value = text.substring(0, lineStart) + '- ' + text.substring(lineStart);
    input.selectionStart = input.selectionEnd = lineStart + 2;
    input.focus();
    render();
    saveState();
  });

  // Keyboard shortcuts
  input.addEventListener('keydown', function(e){
    if(e.ctrlKey || e.metaKey){
      if(e.key === 'z'){
        e.preventDefault();
        undo();
      }else if(e.key === 'y' || (e.shiftKey && e.key === 'Z')){
        e.preventDefault();
        redo();
      }else if(e.key === 'b'){
        e.preventDefault();
        insertAtCursor('**', '**');
      }else if(e.key === 'i'){
        e.preventDefault();
        insertAtCursor('*', '*');
      }
      // Ctrl+C, Ctrl+V, Ctrl+X are native browser shortcuts
    }
  });

  // File operations
  openFile.addEventListener('click', ()=>fileInput.click());
  
  fileInput.addEventListener('change', function(){
    const file = this.files[0];
    if(!file) return;
    
    const reader = new FileReader();
    reader.onload = function(e){
      input.value = e.target.result;
      render();
      saveState();
    };
    reader.readAsText(file);
  });

  saveFile.addEventListener('click', function(){
    const text = input.value;
    const blob = new Blob([text], {type:'text/markdown'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'document.md';
    a.click();
    URL.revokeObjectURL(url);
  });

  // Initial sample content
  const sample = `# Welcome to ConverterAI Editor

This is a **live Markdown editor** with PDF export capability.

## Features

- 📝 Real-time preview
- 🎨 Syntax highlighting
- 📄 PDF export
- 💾 Save/Load .md files
- ⌨️ Keyboard shortcuts (Ctrl+B, Ctrl+I)
- ↩️ Undo/Redo (Ctrl+Z, Ctrl+Y)

## Code Example

\`\`\`python
def hello_world():
    print("Hello from ConverterAI!")
\`\`\`

## Try It Out

Select text and use the toolbar buttons, or type naturally. The preview updates instantly!

**Enjoy!** 🚀`;

  input.value = sample;
  render();
  saveState();

  // PDF download handler
  downloadBtn.addEventListener('click', function(){
    const opt = {
      margin:       10,
      filename:     'document.pdf',
      image:        { type: 'jpeg', quality: 0.98 },
      html2canvas:  { scale: 2, useCORS: true },
      jsPDF:        { unit: 'pt', format: 'a4', orientation: 'portrait' }
    };

    const clone = previewContainer.cloneNode(true);
    clone.style.boxShadow = 'none';
    clone.style.margin = '0';
    clone.style.transform = 'none';

    const wrapper = document.createElement('div');
    wrapper.style.background = '#fff';
    wrapper.appendChild(clone);

    html2pdf().set(opt).from(wrapper).save();
  });

})();
