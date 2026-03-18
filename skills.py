import re

def extract_skills(text):

    skills = [
        "python","java","c","c++","html","css","javascript",
        "react","node","sql","mysql","mongodb",
        "machine learning","deep learning","pandas","numpy"
    ]

    text = text.lower()
    found = []

    for skill in skills:
        if re.search(r"\b" + re.escape(skill) + r"\b", text):
            found.append(skill)

    return list(set(found))