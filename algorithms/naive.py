def naive_search(text: str, pattern: str, case_sensitive: bool = True) -> tuple:
    """
    Naïve pattern searching algorithm.
    Returns: (list of match start indices, number of character comparisons)
    """
    if not pattern or not text:
        return [], 0
    
    if not case_sensitive:
        text = text.lower()
        pattern = pattern.lower()
    
    n = len(text)
    m = len(pattern)
    matches = []
    comparisons = 0
    
    for i in range(n - m + 1):
        match = True
        for j in range(m):
            comparisons += 1
            if text[i + j] != pattern[j]:
                match = False
                break
        if match:
            matches.append(i)
    
    return matches, comparisons