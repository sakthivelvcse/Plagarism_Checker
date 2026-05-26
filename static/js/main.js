let performanceChart = null;

// Handle file upload
document.getElementById('fileUpload').addEventListener('change', async function(e) {
    const file = e.target.files[0];
    if (!file) return;
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch('/upload', { method: 'POST', body: formData });
        const data = await response.json();
        if (data.text) {
            document.getElementById('documentText').value = data.text;
            showToast('File loaded successfully!', 'success');
        } else if (data.error) {
            showToast(data.error, 'danger');
        }
    } catch (err) {
        showToast('Error uploading file', 'danger');
    }
});

// Load sample document
document.getElementById('loadSampleBtn').addEventListener('click', function() {
    const sampleText = `The concept of artificial intelligence has revolutionized modern computing. Machine learning algorithms enable systems to learn from data without explicit programming. Pattern matching is fundamental to many AI applications including natural language processing and computer vision. String matching algorithms like KMP and Boyer-Moore provide efficient search capabilities for large text databases. Plagiarism detection systems rely on these algorithms to identify copied content across academic documents. The efficiency of pattern searching directly impacts the performance of digital libraries and search engines.`;
    document.getElementById('documentText').value = sampleText;
    showToast('Sample document loaded', 'info');
});

// Dynamic pattern management
document.getElementById('addPatternBtn').addEventListener('click', function() {
    const container = document.getElementById('patternsContainer');
    const newPatternDiv = document.createElement('div');
    newPatternDiv.className = 'input-group mb-2 pattern-group';
    newPatternDiv.innerHTML = `
        <input type="text" class="form-control pattern-input" placeholder="Enter pattern">
        <button class="btn btn-danger remove-pattern" type="button">
            <i class="fas fa-times"></i>
        </button>
    `;
    container.appendChild(newPatternDiv);
    
    // Show remove buttons for all except first
    document.querySelectorAll('.remove-pattern').forEach(btn => btn.style.display = 'inline-block');
});

document.getElementById('patternsContainer').addEventListener('click', function(e) {
    if (e.target.closest('.remove-pattern')) {
        const patternGroup = e.target.closest('.pattern-group');
        if (document.querySelectorAll('.pattern-group').length > 1) {
            patternGroup.remove();
        } else {
            showToast('At least one pattern required', 'warning');
        }
    }
});

// Get all patterns
function getPatterns() {
    const inputs = document.querySelectorAll('.pattern-input');
    return Array.from(inputs).map(inp => inp.value.trim()).filter(p => p !== '');
}

// Show toast notification
function showToast(message, type) {
    const toastContainer = document.getElementById('toastContainer') || createToastContainer();
    const toastId = 'toast-' + Date.now();
    const toastHtml = `
        <div id="${toastId}" class="toast align-items-center text-white bg-${type} border-0" role="alert" data-bs-autohide="true" data-bs-delay="3000">
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    toastContainer.insertAdjacentHTML('beforeend', toastHtml);
    const toastEl = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastEl);
    toast.show();
    toastEl.addEventListener('hidden.bs.toast', () => toastEl.remove());
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toastContainer';
    container.style.position = 'fixed';
    container.style.bottom = '20px';
    container.style.right = '20px';
    container.style.zIndex = '1100';
    document.body.appendChild(container);
    return container;
}

// Display search results
function displayResults(data) {
    const resultsDiv = document.getElementById('resultsArea');
    let html = `
        <div class="alert alert-success">
            <i class="fas fa-check-circle"></i> <strong>Total Matches Found: ${data.total_matches}</strong>
        </div>
        <div class="card mb-3">
            <div class="card-header bg-info text-white">
                Algorithm: ${data.algorithm_info.name}
                <span class="badge bg-light text-dark ms-2">Best: ${data.algorithm_info.best_case} | Worst: ${data.algorithm_info.worst_case}</span>
            </div>
            <div class="card-body">
                <p><strong>Technique:</strong> ${data.algorithm_info.technique}</p>
                <hr>
                <h6>Pattern-wise Results:</h6>
                <table class="table table-sm table-bordered">
                    <thead>
                        <tr><th>Pattern</th><th>Matches</th><th>Positions</th><th>Comparisons</th><th>Time (ms)</th></tr>
                    </thead>
                    <tbody>
    `;
    
    for (const [pattern, res] of Object.entries(data.results)) {
        const positions = res.positions.slice(0, 10).join(', ') + (res.positions.length > 10 ? ', ...' : '');
        html += `<tr>
            <td><code>${escapeHtml(pattern)}</code></td>
            <td>${res.matches}</td>
            <td style="max-width: 300px; overflow-x: auto;">[${positions}]</td>
            <td>${res.comparisons}</td>
            <td>${res.execution_time_ms} ms</td>
        </tr>`;
    }
    
    html += `</tbody>}</div></div>`;
    resultsDiv.innerHTML = html;
}

// Execute search
document.getElementById('searchBtn').addEventListener('click', async function() {
    const text = document.getElementById('documentText').value;
    const patterns = getPatterns();
    const algorithm = document.getElementById('algorithmSelect').value;
    const caseSensitive = document.getElementById('caseSensitive').checked;
    
    if (!text) {
        showToast('Please enter document text or upload a file', 'warning');
        return;
    }
    
    if (patterns.length === 0) {
        showToast('Please enter at least one search pattern', 'warning');
        return;
    }
    
    // Show loading
    const resultsDiv = document.getElementById('resultsArea');
    resultsDiv.innerHTML = '<div class="alert alert-info"><i class="fas fa-spinner fa-spin"></i> Searching...</div>';
    
    try {
        const response = await fetch('/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
    text, 
    patterns, 
    case_sensitive: caseSensitive 
})
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayResults(data);
            document.getElementById('previewArea').innerHTML = data.highlighted_html || '<div class="text-muted">No matches found</div>';
        } else {
            resultsDiv.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
        }
    } catch (err) {
        console.error('Caught error:', err);
        resultsDiv.innerHTML = `<div class="alert alert-danger">Error: ${err.message}</div>`;
    }
});

// Benchmark all algorithms - FIXED VERSION
document.getElementById('benchmarkBtn').addEventListener('click', async function() {
    const text = document.getElementById('documentText').value;
    const pattern = document.getElementById('benchmarkPattern').value;
    const caseSensitive = document.getElementById('caseSensitive').checked; // FIXED: define case_sensitive here
    
    if (!text) {
        showToast('Please enter document text', 'warning');
        return;
    }
    if (!pattern) {
        showToast('Please enter a pattern for benchmarking', 'warning');
        return;
    }
    
    const resultsDiv = document.getElementById('resultsArea');
    resultsDiv.innerHTML = '<div class="alert alert-info"><i class="fas fa-chart-line"></i> Running benchmark on all algorithms...</div>';
    console.log(document.getElementById('algorithmSelect'));
     const algorithm = document.getElementById('algorithmSelect').value;
    try {
       
        const response = await fetch('/compare', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
body: JSON.stringify({ 
    text, 
    pattern, 
    algorithm, 
    case_sensitive: caseSensitive 
})        });
        const data = await response.json();
        
        if (data.success) {
            displayBenchmark(data.comparison, pattern);
        } else {
            resultsDiv.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
        }
    } catch (err) {
        console.error('Benchmark error:', err);
        resultsDiv.innerHTML = `<div class="alert alert-danger">Benchmark error: ${err.message}</div>`;
    }
});

function displayBenchmark(comparison, pattern) {
    let html = `
        <div class="alert alert-secondary">
            <strong>Performance Benchmark for Pattern: </strong><code>${escapeHtml(pattern)}</code>
        </div>
        <table class="table table-striped table-bordered comparison-table">
            <thead class="table-dark">
                <tr><th>Algorithm</th><th>Matches</th><th>Comparisons</th><th>Time (ms)</th><th>Memory (KB)</th><th>Complexity</th></tr>
            </thead>
            <tbody>
    `;
    
    comparison.forEach(algo => {
        html += `<tr>
            <td><strong>${algo.algorithm}</strong></td>
            <td>${algo.matches}</td>
            <td>${algo.comparisons}</td>
            <td>${algo.execution_time_ms} ms</td>
            <td>${algo.memory_estimate_kb} KB</td>
            <td>${algo.best_case} / ${algo.worst_case}</td>
        </tr>`;
    });
    
html += `</tbody></table><canvas id="benchmarkChart"></canvas>`;    
    const resultsDiv = document.getElementById('resultsArea');
    resultsDiv.innerHTML = html;
    
    // Create chart
    const ctx = document.getElementById('benchmarkChart').getContext('2d');
    if (performanceChart) performanceChart.destroy();
    
    performanceChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: comparison.map(a => a.algorithm.split(' ')[0]),
            datasets: [
                {
                    label: 'Execution Time (ms)',
                    data: comparison.map(a => a.execution_time_ms),
                    backgroundColor: 'rgba(54, 162, 235, 0.6)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1,
                    yAxisID: 'y'
                },
                {
                    label: 'Comparisons (x100)',
                    data: comparison.map(a => a.comparisons / 100),
                    backgroundColor: 'rgba(255, 99, 132, 0.6)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1,
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            responsive: true,
            interaction: { mode: 'index', intersect: false },
            scales: {
                y: { title: { display: true, text: 'Time (ms)' }, beginAtZero: true },
                y1: { title: { display: true, text: 'Comparisons (hundreds)' }, position: 'right', beginAtZero: true }
            }
        }
    });
}

function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/[&<>]/g, function(m) {
        if (m === '&') return '&amp;';
        if (m === '<') return '&lt;';
        if (m === '>') return '&gt;';
        return m;
    });
}