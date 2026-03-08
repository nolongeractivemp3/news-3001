from dataclasses import dataclass, field


@dataclass
class ArticleInput:
    source: str
    title: str
    description: str
    link: str
    full_text: str = ""
    extra: dict = field(default_factory=dict)
