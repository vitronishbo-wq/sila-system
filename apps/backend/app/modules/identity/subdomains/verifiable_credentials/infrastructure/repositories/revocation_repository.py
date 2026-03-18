import zlib
import base64

class RevocationRepository:
    """Gerencia o Status List em formato Bitmap comprimido para alta performance."""

    def __init__(self, size_bytes: int=128):
        self._status_bitmap = bytearray(size_bytes)

    def revoke(self, index: int):
        if index >= len(self._status_bitmap) * 8:
            raise ValueError(f'Indice {index} fora do limite do registro.')
        byte_idx = index // 8
        bit_idx = index % 8
        self._status_bitmap[byte_idx] |= 1 << bit_idx

    def is_revoked(self, index: int) -> bool:
        byte_idx = index // 8
        bit_idx = index % 8
        return bool(self._status_bitmap[byte_idx] & 1 << bit_idx)

    def get_compressed_status_list(self) -> str:
        """Gera a string Base64 do bitmap comprimido (padrao W3C StatusList2021)."""
        compressed = zlib.compress(self._status_bitmap)
        return base64.b64encode(compressed).decode('utf-8')
DEFAULT_REVOCATION_REPOSITORY = RevocationRepository()