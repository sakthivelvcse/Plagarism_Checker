def build_bad_char_table(pattern: str) -> dict:
    """Build bad character shift table for Boyer-Moore"""
    m = len(pattern)
    bad_char = {}
    for i in range(m - 1):
        bad_char[pattern[i]] = m - 1 - i
    return bad_char


def boyer_moore_search(text: str, pattern: str, case_sensitive: bool = True) -> tuple:
    """
    Boyer-Moore pattern searching algorithm with bad character heuristic.
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
    
    bad_char = build_bad_char_table(pattern)
    matches = []
    comparisons = 0
    shift = 0
    
    while shift <= n - m:
        j = m - 1
        
        # Compare from right to left
        while j >= 0:
            comparisons += 1
            if pattern[j] == text[shift + j]:
                j -= 1
            else:
                break
        
        if j < 0:  # Match found
            matches.append(shift)
            # Shift by 1 (or use good suffix, but we implement basic bad char)
            shift += 1
        else:
            # Bad character shift
            bad_char_shift = bad_char.get(text[shift + j], m)
            shift += max(1, j - bad_char_shift)
    
    return matches, comparisons