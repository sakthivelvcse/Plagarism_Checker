from flask import Flask, render_template, request, jsonify
import time
import os
from algorithms import naive_search, kmp_search, rabin_karp_search, boyer_moore_search

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB limit

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Algorithm metadata
ALGORITHMS = {
    'naive': {
        'name': 'Naïve Pattern Matching',
        'func': naive_search,
        'best_case': 'O(n)',
        'worst_case': 'O(nm)',
        'technique': 'Sequential Comparison'
    },
    'kmp': {
        'name': "Knuth-Morris-Pratt (KMP)",
        'func': kmp_search,
        'best_case': 'O(n)',
        'worst_case': 'O(n+m)',
        'technique': 'Prefix Table (LPS)'
    },
    'rabin_karp': {
        'name': 'Rabin-Karp',
        'func': rabin_karp_search,
        'best_case': 'O(n+m)',
        'worst_case': 'O(nm)',
        'technique': 'Rolling Hash'
    },
    'boyer_moore': {
        'name': 'Boyer-Moore',
        'func': boyer_moore_search,
        'best_case': 'O(n/m)',
        'worst_case': 'O(nm)',
        'technique': 'Bad Character Heuristic'
    }
}


def merge_match_intervals(matches_per_pattern: list) -> list:
    """Merge overlapping match intervals from multiple patterns"""
    # Expect matches_per_pattern as iterable of (start, length) pairs
    intervals = []
    for item in matches_per_pattern:
        if isinstance(item, tuple) and len(item) == 2:
            start, plen = item
            intervals.append((start, start + plen))
        else:
            # If only start provided, treat length as 1
            try:
                start = int(item)
                intervals.append((start, start + 1))
            except Exception:
                continue

    # Merge overlapping intervals
    if not intervals:
        return []
    intervals.sort()
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))
    return merged


def highlight_text(text: str, all_matches: list, pattern_lengths: list = None) -> str:
    """Highlight matches in text using <mark> tags, merging overlapping intervals"""
    if not all_matches:
        return text
    
    # Create intervals (start, end)
    intervals = []
    # all_matches is list of (start, pattern_len) for each match
    for start, plen in all_matches:
        intervals.append((start, start + plen))
    
    # Sort and merge overlapping intervals
    intervals.sort()
    merged = []
    for start, end in intervals:
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    
    # Build highlighted HTML
    result = []
    last_idx = 0
    for start, end in merged:
        result.append(text[last_idx:start])
        result.append(f'<mark class="highlight">{text[start:end]}</mark>')
        last_idx = end
    result.append(text[last_idx:])
    
    return ''.join(result)


@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html', algorithms=ALGORITHMS)


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle text file upload"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400
    
    if file and file.filename.endswith('.txt'):
        text = file.read().decode('utf-8')
        return jsonify({'text': text})
    else:
        return jsonify({'error': 'Only .txt files supported'}), 400


@app.route('/search', methods=['POST'])
def search():
    """Execute pattern search with selected algorithm"""
    data = request.json
    text = data.get('text', '')
    patterns = data.get('patterns', [])
    algorithm_key = data.get('algorithm', 'naive')
    case_sensitive = data.get('case_sensitive', True)
    
    if not text or not patterns:
        return jsonify({'error': 'Text and patterns required'}), 400
    
    if algorithm_key not in ALGORITHMS:
        return jsonify({'error': 'Invalid algorithm'}), 400
    
    algo = ALGORITHMS[algorithm_key]
    search_func = algo['func']
    
    results = {}
    all_matches_with_len = []  # For highlighting
    total_matches = 0
    
    for pattern in patterns:
        if not pattern:
            continue
        
        # Measure execution time
        start_time = time.perf_counter()
        matches, comparisons = search_func(text, pattern, case_sensitive)
        end_time = time.perf_counter()
        exec_time = (end_time - start_time) * 1000  # Convert to ms
        
        match_positions = matches
        total_matches += len(matches)
        
        # Store pattern results
        results[pattern] = {
            'matches': len(matches),
            'positions': match_positions,
            'comparisons': comparisons,
            'execution_time_ms': round(exec_time, 4)
        }
        
        # Store for highlighting
        for pos in match_positions:
            all_matches_with_len.append((pos, len(pattern)))
    
    # Generate highlighted HTML
    highlighted_html = highlight_text(text, all_matches_with_len)
    
    return jsonify({
        'success': True,
        'total_matches': total_matches,
        'results': results,
        'highlighted_html': highlighted_html,
        'algorithm_info': {
            'name': algo['name'],
            'best_case': algo['best_case'],
            'worst_case': algo['worst_case'],
            'technique': algo['technique']
        }
    })


@app.route('/compare', methods=['POST'])
def compare_algorithms():
    """Compare all algorithms on same text and pattern"""
    data = request.json
    text = data.get('text', '')
    pattern = data.get('pattern', '')
    case_sensitive = data.get('case_sensitive', True)
    
    if not text or not pattern:
        return jsonify({'error': 'Text and pattern required'}), 400
    
    comparison_results = []
    
    for key, algo in ALGORITHMS.items():
        search_func = algo['func']
        
        # Measure time and comparisons
        start_time = time.perf_counter()
        matches, comparisons = search_func(text, pattern, case_sensitive)
        end_time = time.perf_counter()
        exec_time = (end_time - start_time) * 1000
        
        # Memory overhead estimation (simplified)
        if key == 'kmp':
            memory_kb = len(pattern) * 8 / 1024  # LPS array
        elif key == 'boyer_moore':
            memory_kb = len(set(pattern)) * 8 / 1024  # Bad char table
        elif key == 'rabin_karp':
            memory_kb = 0.5  # Minimal
        else:
            memory_kb = 0.1
        
        comparison_results.append({
            'algorithm': algo['name'],
            'algorithm_key': key,
            'matches': len(matches),
            'comparisons': comparisons,
            'execution_time_ms': round(exec_time, 4),
            'memory_estimate_kb': round(memory_kb, 2),
            'best_case': algo['best_case'],
            'worst_case': algo['worst_case']
        })
    
    return jsonify({'success': True, 'comparison': comparison_results})


if __name__ == '__main__':
    app.run(debug=True, port=5000)