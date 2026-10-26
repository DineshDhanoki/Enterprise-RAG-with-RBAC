"""Deterministic fake identities and documents for local development."""

PERSONAS = {
    "engineering": {
        "display_name": "Demo Engineering",
        "description": "Fake engineering persona; not an authenticated identity.",
    },
    "finance": {
        "display_name": "Demo Finance",
        "description": "Fake finance persona; not an authenticated identity.",
    },
    "people_ops": {
        "display_name": "Demo People Ops",
        "description": "Fake People Ops persona; not an authenticated identity.",
    },
}

DOCUMENTS = [
    {
        "id": "doc-eng-handbook",
        "title": "Engineering handbook",
        "text": "The demo engineering team uses documented code reviews.",
        "audience": ["engineering"],
    },
    {
        "id": "doc-finance-forecast",
        "title": "Finance forecast",
        "text": "The demo finance forecast is illustrative and fictional.",
        "audience": ["finance"],
    },
    {
        "id": "doc-people-guide",
        "title": "People operations guide",
        "text": "The demo People Ops guide describes fictional onboarding.",
        "audience": ["people_ops"],
    },
]


def load_fixtures():
    """Return fresh copies so callers cannot mutate the module fixtures."""
    personas = {key: value.copy() for key, value in PERSONAS.items()}
    documents = [
        {**document, "audience": list(document["audience"])}
        for document in DOCUMENTS
    ]
    return personas, documents
