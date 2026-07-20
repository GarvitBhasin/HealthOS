from helpers.assessment_logic.question_key import *

def attach_results(responses):
    answers = {}
    for section_index, section in enumerate(QUESTION_KEYS):
        answers.update(
            dict(
                zip(
                    QUESTION_KEYS[section], responses[section_index]
                )
            )
        )
    return answers