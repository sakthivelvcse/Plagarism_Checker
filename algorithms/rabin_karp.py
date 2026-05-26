def rabin_karp_search(text: str, pattern: str, case_sensitive: bool = True, prime: int = 101, base: int = 256) -> tuple:
    """
    Rabin-Karp pattern searching algorithm using hashing.
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
    
    matches = []
    comparisons = 0
    
    # Hash computation
    pattern_hash = 0
    text_hash = 0
    h = pow(base, m - 1, prime)
    
    # Initial hash values
    for i in range(m):
        pattern_hash = (base * pattern_hash + ord(pattern[i])) % prime
        text_hash = (base * text_hash + ord(text[i])) % prime
    
    # Slide pattern over text
    for i in range(n - m + 1):
        # Check hash match
        if pattern_hash == text_hash:
            # Verify characters
            match = True
            for j in range(m):
                comparisons += 1
                if text[i + j] != pattern[j]:
                    match = False
                    break
            if match:
                matches.append(i)
        else:
            # No hash match, still count a virtual comparison? We'll count 0 extra.
            # For fairness, no char comparisons performed.
            pass
        
        # Compute hash for next window (if not last)
        if i < n - m:
            text_hash = (base * (text_hash - ord(text[i]) * h) + ord(text[i + m])) % prime
            # Handle negative hash
            if text_hash < 0:
                text_hash += prime
    
    return matches, comparisons