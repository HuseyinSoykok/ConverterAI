// ConverterAI Frontend Application

const API_BASE = '';

// State
let state = {
    fileId: null,
    fileName: null,
    fileFormat: null,
    outputFormat: null,
    taskId: null,
    useOcr: false,
    useLlm: false,
    llmProvider: 'auto'
};

// Format icons and labels
const formatInfo = {
    'pdf': { icon: 'fa-solid fa-file-pdf', label: 'PDF', color: '#ef4444' },
    'docx': { icon: 'fa-solid fa-file-word', label: 'DOCX', color: '#2563eb' },
    'markdown': { icon: 'fa-brands fa-markdown', label: 'Markdown', color: '#6b7280' },
    'html': { icon: 'fa-brands fa-html5', label: 'HTML', color: '#f97316' }
};

// DOM Elements
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const fileFormat = document.getElementById('fileFormat');
const fileSize = document.getElementById('fileSize');
const removeFileBtn = document.getElementById('removeFile');

const conversionSection = document.getElementById('conversionSection');
const formatButtons = document.getElementById('formatButtons');
const qualityCheckbox = document.getElementById('qualityCheck');
const convertBtn = document.getElementById('convertBtn');

const progressSection = document.getElementById('progressSection');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');

const resultSection = document.getElementById('resultSection');
const processingTime = document.getElementById('processingTime');
const qualityResult = document.getElementById('qualityResult');
const qualityScore = document.getElementById('qualityScore');
const warnings = document.getElementById('warnings');
const warningsList = document.getElementById('warningsList');
const downloadBtn = document.getElementById('downloadBtn');
const newConversionBtn = document.getElementById('newConversionBtn');

const errorSection = document.getElementById('errorSection');
const errorMessage = document.getElementById('errorMessage');
const retryBtn = document.getElementById('retryBtn');

// OCR/LLM options
const ocrOption = document.getElementById('ocrOption');
const useOcrCheckbox = document.getElementById('useOcr');
const llmOption = document.getElementById('llmOption');
const useLlmCheckbox = document.getElementById('useLlm');
const llmProviderSelect = document.getElementById('llmProviderSelect');
const llmProviderDropdown = document.getElementById('llmProvider');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    ensureFontAwesome();
    loadSupportedConversions();
    initEventListeners();
});

// Ensure Font Awesome is loaded
function ensureFontAwesome() {
    if (!document.querySelector('link[href*="font-awesome"]') && !document.querySelector('link[href*="fontawesome"]')) {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css';
        link.crossOrigin = 'anonymous';
        document.head.appendChild(link);
    }
}

// Event Listeners
function initEventListeners() {
    // Drop zone
    dropZone.addEventListener('click', () => fileInput.click());
    dropZone.addEventListener('dragover', handleDragOver);
    dropZone.addEventListener('dragleave', handleDragLeave);
    dropZone.addEventListener('drop', handleDrop);
    
    // File input
    fileInput.addEventListener('change', handleFileSelect);
    
    // Remove file
    removeFileBtn.addEventListener('click', resetUpload);
    
    // Convert button
    convertBtn.addEventListener('click', startConversion);
    
    // Download button
    downloadBtn.addEventListener('click', downloadFile);
    
    // New conversion button
    newConversionBtn.addEventListener('click', resetAll);
    
    // Retry button
    retryBtn.addEventListener('click', resetAll);
    
    // OCR checkbox
    if (useOcrCheckbox) {
        useOcrCheckbox.addEventListener('change', (e) => {
            state.useOcr = e.target.checked;
            // Show LLM option when OCR is enabled
            if (llmOption) {
                llmOption.style.display = e.target.checked ? 'flex' : 'none';
                if (!e.target.checked) {
                    useLlmCheckbox.checked = false;
                    state.useLlm = false;
                    llmProviderSelect.style.display = 'none';
                }
            }
        });
    }
    
    // LLM checkbox
    if (useLlmCheckbox) {
        useLlmCheckbox.addEventListener('change', (e) => {
            state.useLlm = e.target.checked;
            // Show provider select when LLM is enabled
            if (llmProviderSelect) {
                llmProviderSelect.style.display = e.target.checked ? 'block' : 'none';
            }
        });
    }
    
    // LLM provider select
    if (llmProviderDropdown) {
        llmProviderDropdown.addEventListener('change', (e) => {
            state.llmProvider = e.target.value;
        });
    }
}

// Drag and Drop Handlers
function handleDragOver(e) {
    e.preventDefault();
    dropZone.classList.add('drag-over');
}

function handleDragLeave(e) {
    e.preventDefault();
    dropZone.classList.remove('drag-over');
}

function handleDrop(e) {
    e.preventDefault();
    dropZone.classList.remove('drag-over');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        uploadFile(files[0]);
    }
}

function handleFileSelect(e) {
    const files = e.target.files;
    if (files.length > 0) {
        uploadFile(files[0]);
    }
}

// File Upload
async function uploadFile(file) {
    showProgress('Dosya yükleniyor...', 20);
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch(`${API_BASE}/api/upload`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            state.fileId = data.file_id;
            state.fileName = data.original_name;
            state.fileFormat = data.format;
            
            displayFileInfo(data);
            hideProgress();
            showConversionOptions(data.format);
        } else {
            showError(data.error || 'Dosya yüklenirken hata oluştu');
        }
    } catch (error) {
        showError('Dosya yüklenirken hata oluştu: ' + error.message);
    }
}

// Display File Info
function displayFileInfo(data) {
    fileName.textContent = data.original_name;
    fileFormat.textContent = formatInfo[data.format]?.label || data.format.toUpperCase();
    fileSize.textContent = data.size_mb + ' MB';
    
    document.querySelector('.drop-zone').style.display = 'none';
    fileInfo.style.display = 'flex';
}

// Show Conversion Options
async function showConversionOptions(inputFormat) {
    conversionSection.style.display = 'block';
    
    // Show OCR option for PDF and image files
    if (ocrOption && ['pdf', 'png', 'jpg', 'jpeg', 'image'].includes(inputFormat.toLowerCase())) {
        ocrOption.style.display = 'flex';
    } else if (ocrOption) {
        ocrOption.style.display = 'none';
    }
    
    try {
        const response = await fetch(`${API_BASE}/api/supported-conversions`);
        const data = await response.json();
        
        if (data.success) {
            const supportedFormats = data.conversions[inputFormat] || [];
            renderFormatButtons(supportedFormats);
        }
    } catch (error) {
        console.error('Failed to load conversions:', error);
    }
}

// Render Format Buttons
function renderFormatButtons(formats) {
    formatButtons.innerHTML = '';
    
    formats.forEach(format => {
        const info = formatInfo[format];
        if (!info) return;
        
        const button = document.createElement('button');
        button.className = 'format-btn';
        button.dataset.format = format;
        button.innerHTML = `
            <i class="fas ${info.icon}"></i>
            <span>${info.label}</span>
        `;
        
        button.addEventListener('click', () => selectFormat(format));
        formatButtons.appendChild(button);
    });
}

// Select Format
function selectFormat(format) {
    // Remove active class from all buttons
    document.querySelectorAll('.format-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Add active class to selected button
    const selectedBtn = document.querySelector(`[data-format="${format}"]`);
    if (selectedBtn) {
        selectedBtn.classList.add('active');
        state.outputFormat = format;
    }
}

// Start Conversion
async function startConversion() {
    if (!state.outputFormat) {
        alert('Lütfen hedef format seçin');
        return;
    }
    
    const qualityCheck = qualityCheckbox.checked;
    const useOcr = useOcrCheckbox ? useOcrCheckbox.checked : false;
    const useLlm = useLlmCheckbox ? useLlmCheckbox.checked : false;
    const llmProvider = llmProviderDropdown ? llmProviderDropdown.value : 'auto';
    
    let progressMessage = 'Dönüştürme başlatılıyor...';
    if (useOcr && useLlm) {
        progressMessage = 'OCR + LLM ile dönüştürülüyor... (Bu işlem biraz zaman alabilir)';
    } else if (useOcr) {
        progressMessage = 'OCR ile dönüştürülüyor...';
    } else if (useLlm) {
        progressMessage = 'LLM ile iyileştiriliyor...';
    }
    
    showProgress(progressMessage, 30);
    
    try {
        const response = await fetch(`${API_BASE}/api/convert`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                file_id: state.fileId,
                output_format: state.outputFormat,
                quality_check: qualityCheck,
                use_ocr: useOcr,
                use_llm: useLlm,
                llm_provider: llmProvider
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            state.taskId = data.task_id;
            showProgress('Dönüştürme tamamlandı!', 100);
            
            setTimeout(() => {
                hideProgress();
                showResult(data);
            }, 500);
        } else {
            showError(data.error || 'Dönüştürme sırasında hata oluştu');
        }
    } catch (error) {
        showError('Dönüştürme sırasında hata oluştu: ' + error.message);
    }
}

// Show Result
function showResult(data) {
    conversionSection.style.display = 'none';
    resultSection.style.display = 'block';
    
    processingTime.textContent = data.processing_time;
    
    // Quality score
    if (data.quality_score !== null && data.quality_score !== undefined) {
        qualityResult.style.display = 'flex';
        const scorePercent = (data.quality_score * 100).toFixed(0);
        qualityScore.textContent = scorePercent + '%';
        
        // Color code based on quality
        const scoreElem = qualityScore.parentElement;
        if (data.quality_score >= 0.9) {
            scoreElem.style.color = '#10b981';
        } else if (data.quality_score >= 0.7) {
            scoreElem.style.color = '#f59e0b';
        } else {
            scoreElem.style.color = '#ef4444';
        }
    }
    
    // Warnings
    if (data.warnings && data.warnings.length > 0) {
        warnings.style.display = 'block';
        warningsList.innerHTML = '';
        data.warnings.forEach(warning => {
            const li = document.createElement('li');
            li.textContent = warning;
            warningsList.appendChild(li);
        });
    }
    
    // Store output file for download
    state.outputFile = data.output_file;
}

// Download File
function downloadFile() {
    if (state.outputFile) {
        window.location.href = `${API_BASE}/api/download/${state.outputFile}`;
    }
}

// Show Progress
function showProgress(message, percent) {
    conversionSection.style.display = 'none';
    progressSection.style.display = 'block';
    progressText.textContent = message;
    progressFill.style.width = percent + '%';
}

// Hide Progress
function hideProgress() {
    progressSection.style.display = 'none';
}

// Show Error
function showError(message) {
    hideProgress();
    conversionSection.style.display = 'none';
    resultSection.style.display = 'none';
    errorSection.style.display = 'block';
    errorMessage.textContent = message;
}

// Reset Upload
function resetUpload() {
    document.querySelector('.drop-zone').style.display = 'block';
    fileInfo.style.display = 'none';
    conversionSection.style.display = 'none';
    fileInput.value = '';
    
    state.fileId = null;
    state.fileName = null;
    state.fileFormat = null;
    state.outputFormat = null;
}

// Reset All
function resetAll() {
    resetUpload();
    hideProgress();
    resultSection.style.display = 'none';
    errorSection.style.display = 'none';
    
    // Reset OCR/LLM options
    if (ocrOption) ocrOption.style.display = 'none';
    if (llmOption) llmOption.style.display = 'none';
    if (llmProviderSelect) llmProviderSelect.style.display = 'none';
    if (useOcrCheckbox) useOcrCheckbox.checked = false;
    if (useLlmCheckbox) useLlmCheckbox.checked = false;
    if (llmProviderDropdown) llmProviderDropdown.value = 'auto';
    
    state = {
        fileId: null,
        fileName: null,
        fileFormat: null,
        outputFormat: null,
        taskId: null,
        outputFile: null,
        useOcr: false,
        useLlm: false,
        llmProvider: 'auto'
    };
}

// Load Supported Conversions
async function loadSupportedConversions() {
    try {
        const response = await fetch(`${API_BASE}/api/supported-conversions`);
        const data = await response.json();
        console.log('Supported conversions:', data.conversions);
    } catch (error) {
        console.error('Failed to load supported conversions:', error);
    }
}
