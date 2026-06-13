const API_BASE = 'https://ai-projects-production-f96b.up.railway.app';

const form = document.getElementById('classifierForm');
const descriptionInput = document.getElementById('description');
const loadingDiv = document.getElementById('loading');
const resultDiv = document.getElementById('result');
const errorDiv = document.getElementById('error');
const closeResultBtn = document.getElementById('closeResult');
const closeErrorBtn = document.getElementById('closeError');

// Form submission
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const description = descriptionInput.value.trim();
    if (!description) return;
    
    // Hide previous results
    resultDiv.classList.add('hidden');
    errorDiv.classList.add('hidden');
    
    // Show loading
    loadingDiv.classList.remove('hidden');
    
    try {
        const response = await fetch(`${API_BASE}/classify`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ description })
        });
        
        const data = await response.json();
        loadingDiv.classList.add('hidden');
        
        if (data.success) {
            displayResult(data.data);
        } else {
            displayError(data.error || 'Classification failed');
        }
    } catch (error) {
        loadingDiv.classList.add('hidden');
        displayError(error.message || 'Network error');
    }
});

function displayResult(data) {
    document.getElementById('docType').textContent = data.doc_type;
    document.getElementById('docTypeConf').textContent = `(${(data.doc_type_confidence * 100).toFixed(0)}%)`;
    
    document.getElementById('name').textContent = data.name || '—';
    document.getElementById('nameConf').textContent = `(${(data.name_confidence * 100).toFixed(0)}%)`;
    
    document.getElementById('dob').textContent = data.dob || '—';
    document.getElementById('dobConf').textContent = `(${(data.dob_confidence * 100).toFixed(0)}%)`;
    
    const actionEl = document.getElementById('action');
    actionEl.textContent = data.action.toUpperCase();
    actionEl.className = `value action ${data.action}`;
    
    document.getElementById('rawJson').textContent = JSON.stringify(data, null, 2);
    
    resultDiv.classList.remove('hidden');
}

function displayError(message) {
    document.getElementById('errorMessage').textContent = message;
    errorDiv.classList.remove('hidden');
}

closeResultBtn.addEventListener('click', () => {
    resultDiv.classList.add('hidden');
});

closeErrorBtn.addEventListener('click', () => {
    errorDiv.classList.add('hidden');
});