"""
Compatibility re-export module.

Historicamente o código importava `IdentityRequestRecord` de
`domain.models.identity_request_record`. O ficheiro actual chama-se
`identity_request.py` e define `IdentityRequest`. Para evitar alterar
várias importações, expomos `IdentityRequestRecord` como alias.
"""
from .identity_request import IdentityRequest as IdentityRequestRecord

__all__ = ["IdentityRequestRecord"]
