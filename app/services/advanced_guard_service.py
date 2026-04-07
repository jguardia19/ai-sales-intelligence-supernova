import re
from typing import Dict, List


def detect_pii(text: str) -> Dict:
    """Detecta información personal identificable (PII)"""
    patterns = {
        "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        "phone": r'\b(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3,4}[-.\s]?\d{4}\b',
        "credit_card": r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
        "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
        "curp": r'\b[A-Z]{4}\d{6}[HM][A-Z]{5}[0-9A-Z]\d\b',
        "rfc": r'\b[A-Z&Ñ]{3,4}\d{6}[A-Z0-9]{3}\b',
    }
    
    found = {}
    for pii_type, pattern in patterns.items():
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            found[pii_type] = len(matches)
    
    return {
        "contains_pii": len(found) > 0,
        "types": found
    }


def check_rate_limit_indicators(text: str) -> Dict:
    """Detecta patrones de abuso o spam"""
    indicators = {
        "excessive_length": len(text) > 5000,
        "excessive_repetition": has_excessive_repetition(text),
        "all_caps": text.isupper() and len(text) > 50,
        "excessive_special_chars": count_special_chars(text) > len(text) * 0.3,
    }
    
    return {
        "is_suspicious": any(indicators.values()),
        "indicators": {k: v for k, v in indicators.items() if v}
    }


def has_excessive_repetition(text: str, threshold: int = 5) -> bool:
    """Detecta repetición excesiva de palabras"""
    words = text.lower().split()
    if len(words) < 10:
        return False
    
    word_counts = {}
    for word in words:
        if len(word) > 3:
            word_counts[word] = word_counts.get(word, 0) + 1
    
    max_repetition = max(word_counts.values()) if word_counts else 0
    return max_repetition > threshold


def count_special_chars(text: str) -> int:
    """Cuenta caracteres especiales sospechosos"""
    special = r'[!@#$%^&*()_+=\[\]{};:"|<>?/\\~`]'
    return len(re.findall(special, text))


def detect_jailbreak_attempts(text: str) -> Dict:
    """Detecta intentos avanzados de jailbreak"""
    jailbreak_patterns = [
        r"pretend\s+you\s+are",
        r"imagine\s+you\s+are",
        r"roleplay\s+as",
        r"simulate\s+being",
        r"act\s+like\s+you're",
        r"from\s+now\s+on",
        r"new\s+instructions",
        r"override\s+previous",
        r"disregard\s+all",
        r"ignore\s+your\s+programming",
        r"you\s+are\s+now\s+in\s+developer\s+mode",
        r"DAN\s+mode",
        r"do\s+anything\s+now",
        r"evil\s+mode",
        r"unrestricted\s+mode",
    ]
    
    lowered = text.lower()
    matches = []
    
    for pattern in jailbreak_patterns:
        if re.search(pattern, lowered):
            matches.append(pattern)
    
    return {
        "is_jailbreak": len(matches) > 0,
        "patterns": matches
    }


def validate_business_context(text: str) -> Dict:
    """Valida que la consulta tenga contexto de negocio válido"""
    # Palabras que indican consultas fuera de contexto
    off_topic_keywords = [
        "receta", "cocina", "película", "música", "deporte",
        "política", "religión", "medicina", "legal", "abogado",
        "doctor", "enfermedad", "tratamiento", "diagnóstico",
        "inversión personal", "criptomoneda", "bitcoin",
        "hack", "crackear", "piratear", "ilegal",
    ]
    
    lowered = text.lower()
    found_off_topic = [kw for kw in off_topic_keywords if kw in lowered]
    
    return {
        "is_off_topic": len(found_off_topic) > 0,
        "keywords": found_off_topic
    }


def check_output_manipulation(text: str) -> Dict:
    """Detecta intentos de manipular la salida del modelo"""
    manipulation_patterns = [
        r"output\s+in\s+format",
        r"respond\s+only\s+with",
        r"answer\s+must\s+be",
        r"you\s+must\s+say",
        r"always\s+respond",
        r"never\s+mention",
        r"don't\s+tell",
        r"hide\s+the\s+fact",
        r"pretend\s+that",
    ]
    
    lowered = text.lower()
    matches = []
    
    for pattern in manipulation_patterns:
        if re.search(pattern, lowered):
            matches.append(pattern)
    
    return {
        "is_manipulation": len(matches) > 0,
        "patterns": matches
    }


def comprehensive_validation(text: str) -> Dict:
    """Validación completa combinando todas las verificaciones"""
    pii_check = detect_pii(text)
    rate_check = check_rate_limit_indicators(text)
    jailbreak_check = detect_jailbreak_attempts(text)
    context_check = validate_business_context(text)
    manipulation_check = check_output_manipulation(text)
    
    is_blocked = (
        pii_check["contains_pii"] or
        rate_check["is_suspicious"] or
        jailbreak_check["is_jailbreak"] or
        context_check["is_off_topic"] or
        manipulation_check["is_manipulation"]
    )
    
    return {
        "is_blocked": is_blocked,
        "pii": pii_check,
        "rate_limit": rate_check,
        "jailbreak": jailbreak_check,
        "business_context": context_check,
        "output_manipulation": manipulation_check,
    }