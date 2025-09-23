import re
from typing import Tuple, Dict

# Simple demo patterns; extend with Comprehend Medical or custom rules for production
DATE_PATTERN = re.compile(r"""\b(?:\d{2}[/-]\d{2}[/-]\d{4}|\d{4}-\d{2}-\d{2})\b""")
# Very naive first-name list for demo only
NAMES = ["John", "Jane", "Alice", "Bob", "Mary", "David"]

def mask_phi(text: str, name_token: str = "[NAME]", date_token: str = "[DATE]") -> Tuple[str, Dict[str, str]]:
    mapping = {}
    # Dates
    def _date_sub(m):
        val = m.group(0)
        mapping.setdefault(val, date_token)
        return date_token

    masked = DATE_PATTERN.sub(_date_sub, text)

    # Names (word boundaries, case-insensitive)
    for n in NAMES:
        pattern = re.compile(rf"\b{re.escape(n)}\b", re.IGNORECASE)
        if pattern.search(masked):
            mapping.setdefault(n, name_token)
            masked = pattern.sub(name_token, masked)

    return masked, mapping
