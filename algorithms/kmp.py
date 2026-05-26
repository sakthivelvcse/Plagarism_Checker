def compute_lps(pattern: str) -> list:
    """Compute Longest Prefix Suffix array for KMP"""
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1
    
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps


def kmp_search(text: str, pattern: str, case_sensitive: bool = True) -> tuple:
    """
    KMP pattern searching algorithm.
    Returns: (list of match start indices, number of character comparisons)
    """
    if not pattern or not text:
        return [], 0
    
    if not case_sensitive:
        text = text.lower()
        pattern = pattern.lower()
    
    n = len(text)
    m = len(pattern)
    
    if m > n:
        return [], 0
    
    lps = compute_lps(pattern)
    matches = []
    comparisons = 0
    i = 0  # index for text
    j = 0  # index for pattern
    
    while i < n:
        comparisons += 1
        if pattern[j] == text[i]:
            i += 1
            j += 1
        
        if j == m:
            matches.append(i - j)
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    
    return matches, comparisons