USER_SKILLS = [
    "python",
    "react",
    "typescript",
    "fastapi",
    "sql",
    "automation",
    "selenium",
    "qa",
]


def calculate_match_score(text: str) -> int:
    text = text.lower()

    score = 0

    for skill in USER_SKILLS:
        if skill in text:
            score += 12

    return min(score, 100)