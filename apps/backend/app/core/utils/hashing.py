"""Hashing helpers para deduplicação e chaves determinísticas."""
from hashlib import md5, sha256

def hash_text(value: str, algorithm: str='sha256') -> str:
    """Gera hash textual com algoritmo configurável."""
    data = value.encode('utf-8')
    if algorithm == 'md5':
        return md5(data, usedforsecurity=False).hexdigest()
    if algorithm == 'sha256':
        return sha256(data).hexdigest()
    raise ValueError(f'Unsupported hashing algorithm: {algorithm}')

def stable_hash(*parts: object) -> str:
    """Hash determinístico de múltiplos campos."""
    base = '|'.join(('' if p is None else str(p) for p in parts))
    return hash_text(base, algorithm='sha256')