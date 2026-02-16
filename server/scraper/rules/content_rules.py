from __future__ import annotations

from .content_no_local_reject import content_no_local_reject
from .content_strong_local_pass import content_strong_local_pass
from .content_too_short_reject import content_too_short_reject

CONTENT_RULES = [
    content_too_short_reject,
    content_strong_local_pass,
    content_no_local_reject,
]
