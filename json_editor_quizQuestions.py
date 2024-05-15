import json

with open("quizQuestions.json", "r") as file:
    data = json.load(file)

chapter_id_map = {
    "introduction_to_2fa": ("understanding_2fa", "introduction_to_2fa"),
    "introduction_to_phishing": (
        "assessing_phishing_knowledge",
        "introduction_to_phishing",
    ),
    "importance_of_strong_passwords": (
        "testing_password_security_knowledge",
        "importance_of_strong_passwords",
    ),
    "creating_strong_passwords": (
        "assessing_password_creation_skills",
        "creating_strong_passwords",
    ),
    "introduction_to_online_privacy": (
        "evaluating_understanding_of_online_privacy",
        "introduction_to_online_privacy",
    ),
    "protecting_online_privacy_measures": (
        "assessing_privacy_protection_knowledge",
        "protecting_online_privacy_measures",
    ),
    "introduction_to_software_updates": (
        "testing_understanding_of_software_updates",
        "introduction_to_software_updates",
    ),
}

with open("quizQuestions.json", "r") as file:
    data = json.load(file)

for question in data["quizQuestions"]:
    # question["isHumanWritten"] = 0
    if question["chapterId"] in chapter_id_map:
        new_chapter_id, from_chapter = chapter_id_map[question["chapterId"]]
        question["chapterId"] = new_chapter_id
        question["fromChapter"] = from_chapter

with open("quizQuestions_updated.json", "w") as file:
    json.dump(data, file, indent=4)
