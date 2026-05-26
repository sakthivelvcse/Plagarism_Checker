# Intelligent Pattern Searching System for Plagiarism Detection

[![Flask](https://img.shields.io/badge/Flask-3.0-blue)](https://flask.palletsprojects.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple)](https://getbootstrap.com/)
[![Chart.js](https://img.shields.io/badge/Chart.js-4.4-red)](https://www.chartjs.org/)

A comprehensive web application for academic plagiarism detection using classical string matching algorithms. The system supports multiple pattern search, real-time highlighting, and performance comparison of four algorithms: Naïve, KMP, Rabin-Karp, and Boyer-Moore.

## Features

- **Multiple Pattern Search** – Search one or more phrases simultaneously
- **Four String Matching Algorithms**:
  - Naïve Pattern Matching
  - Knuth–Morris–Pratt (KMP)
  - Rabin-Karp (Rolling Hash)
  - Boyer-Moore (Bad Character Heuristic)
- **Case-Sensitive/Insensitive Search** – Toggle as needed
- **Performance Metrics**:
  - Execution time (ms)
  - Number of character comparisons
  - Memory usage estimation
  - Time complexity visualization
- **Interactive Highlighting** – Matched patterns highlighted in document preview
- **Algorithm Benchmarking** – Compare all algorithms on the same text/pattern
- **File Upload Support** – Upload .txt files (up to 10MB)
- **Responsive UI** – Built with Bootstrap 5

## Technology Stack

| Component       | Technology                          |
|----------------|-------------------------------------|
| Backend        | Python 3.10+ / Flask                |
| Frontend       | HTML5, CSS3, JavaScript (ES6)       |
| Visualization  | Chart.js                            |
| Styling        | Bootstrap 5 + Custom CSS            |
| IDE            | Visual Studio Code                  |

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/plagiarism-pattern-search.git
   cd plagiarism-pattern-search