from typing import Dict

def restore_placeholders(text: str, mapping: Dict[str, str]) -> str:
    """Replace tokens back with original values based on mapping.
    NOTE: This is optional and should be scoped to non-sensitive contexts only.
    """
    restored = text
    # invert mapping: token -> original (choose first original for each token)
    inverse = {}
    for original, token in mapping.items():
        inverse.setdefault(token, original)
    for token, original in inverse.items():
        restored = restored.replace(token, original)
    return restored
