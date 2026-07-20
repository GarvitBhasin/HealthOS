from helpers.assessment_logic.attach_results import *
from helpers.assessment_logic.assessment import *

WEAKNESS_THRESHOLD = 40

def calculate(responses):
    answers = attach_results(responses)
    weight_skipped = 0

    scores = {
        "strength": 0,
        "cardio": 0,
        "flexibility": 0,
        "nutrition": 0,
        "recovery": 0,
        "metabolic": 0,
    }

    weights = {
        "strength": 1,
        "cardio": 1,
        "flexibility": 1,
        "nutrition": 1,
        "recovery": 1,
        "metabolic": 1,
    }

    blindspots = {
        "strength": [],
        "cardio": [],
        "flexibility": [],
        "nutrition": [],
        "recovery": [],
        "metabolic": [],
    }

    weaknesses = {
        "strength": [],
        "cardio": [],
        "flexibility": [],
        "nutrition": [],
        "recovery": [],
        "metabolic": [],
    }

    for section in assessment:
        for question in section["questions"]:

            if "curve" not in question:
                continue

            category = question["category"]
            answer = answers[question["id"]]
            score = question["curve"][answer]

            if score is None:
                blindspots[category].append(question["insight"])
                weights[category] -= question["weight"]
                weight_skipped += question["weight"]
                continue

            if score < WEAKNESS_THRESHOLD:
                weaknesses[category].append(question["insight"])
            
            scores[category] += (score * question["weight"])

    for category in scores:
        if weights[category] == 0:
            scores[category] = "Not enough information"
        else:
            scores[category] /= weights[category]

    confidence = 100 - (weight_skipped / 6) * 100

    return {
        "scores": scores, 
        "blindspots": blindspots, 
        "weaknesses": weaknesses,
        "confidence": confidence
    }