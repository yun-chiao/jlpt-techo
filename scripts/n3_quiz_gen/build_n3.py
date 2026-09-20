# -*- coding: utf-8 -*-
"""Assembles the complete JLPT N3 200-question quiz database and writes src/data/quiz/n3.json."""

import os
import sys
import json

sys.path.append(os.path.dirname(__file__))

from sentences_part1 import SENTENCES_PART1
from sentences_part2 import SENTENCES_PART2
from sentences_part3 import SENTENCES_PART3
from stars_part1 import STARS_PART1
from stars_part2 import STARS_PART2
from passages import PASSAGES

sentence_quizzes = SENTENCES_PART1 + SENTENCES_PART2 + SENTENCES_PART3
star_quizzes = STARS_PART1 + STARS_PART2
passage_quizzes = PASSAGES

# Assertions and checks
print(f"Loaded sentence quizzes: {len(sentence_quizzes)} (expected 120)")
print(f"Loaded star quizzes: {len(star_quizzes)} (expected 50)")
print(f"Loaded passages: {len(passage_quizzes)} (expected 10)")
total_passage_questions = sum(len(p["questions"]) for p in passage_quizzes)
print(f"Loaded passage questions: {total_passage_questions} (expected 30)")
total_questions = len(sentence_quizzes) + len(star_quizzes) + total_passage_questions
print(f"Total questions count: {total_questions} (expected 200)")

assert len(sentence_quizzes) == 120, "sentence_quizzes must be 120"
assert len(star_quizzes) == 50, "star_quizzes must be 50"
assert len(passage_quizzes) == 10, "passage_quizzes must be 10"
assert total_passage_questions == 30, "passage questions must be 30"
assert total_questions == 200, "total questions must be 200"

# Verify Sentence Quizzes
for i, sq in enumerate(sentence_quizzes):
    expected_id = f"n3-s-{i+1}"
    assert sq["id"] == expected_id, f"Invalid sentence quiz ID {sq['id']}, expected {expected_id}"
    assert "（" in sq["question"] and "）" in sq["question"], f"Missing parenthesis blank in {sq['id']}"
    assert len(sq["options"]) == 4, f"Options length != 4 in {sq['id']}"
    assert len(set(sq["options"])) == 4, f"Duplicate options in {sq['id']}"
    assert 1 <= sq["correctIndex"] <= 4, f"correctIndex out of range in {sq['id']}"
    assert sq["explanation"], f"Empty explanation in {sq['id']}"
    assert sq["targetGrammar"], f"Empty targetGrammar in {sq['id']}"

# Verify Star Quizzes
for i, stq in enumerate(star_quizzes):
    expected_id = f"n3-star-{i+1}"
    assert stq["id"] == expected_id, f"Invalid star quiz ID {stq['id']}, expected {expected_id}"
    assert stq["starIndex"] == 2, f"starIndex must be 2 in {stq['id']}"
    assert len(stq["chunks"]) == 4, f"chunks length != 4 in {stq['id']}"
    assert len(set(stq["chunks"])) == 4, f"Duplicate chunks in {stq['id']}"
    assert sorted(stq["correctOrder"]) == [1, 2, 3, 4], f"Invalid correctOrder in {stq['id']}"
    assert stq["fullSentence"], f"Empty fullSentence in {stq['id']}"
    assert stq["translation"], f"Empty translation in {stq['id']}"
    assert stq["explanation"], f"Empty explanation in {stq['id']}"

# Verify Passage Quizzes
for i, pq in enumerate(passage_quizzes):
    expected_id = f"n3-p-{i+1}"
    assert pq["id"] == expected_id, f"Invalid passage quiz ID {pq['id']}, expected {expected_id}"
    assert pq["title"], f"Empty title in {pq['id']}"
    assert pq["genre"], f"Empty genre in {pq['id']}"
    assert "【 01 】" in pq["passage"] and "【 02 】" in pq["passage"] and "【 03 】" in pq["passage"], f"Missing blanks in {pq['id']}"
    assert len(pq["questions"]) == 3, f"Passage questions length != 3 in {pq['id']}"
    for b_idx, subq in enumerate(pq["questions"]):
        assert subq["blankNumber"] == b_idx + 1, f"Invalid blankNumber in {pq['id']}"
        assert len(subq["options"]) == 4, f"Options length != 4 in {pq['id']} blank {subq['blankNumber']}"
        assert len(set(subq["options"])) == 4, f"Duplicate options in {pq['id']} blank {subq['blankNumber']}"
        assert 1 <= subq["correctIndex"] <= 4, f"Invalid correctIndex in {pq['id']} blank {subq['blankNumber']}"
        assert subq["explanation"], f"Empty explanation in {pq['id']} blank {subq['blankNumber']}"
    assert pq["translation"], f"Empty translation in {pq['id']}"

n3_data = {
    "level": "n3",
    "levelLabel": "N3 中級樞紐",
    "sentenceQuizzes": sentence_quizzes,
    "starQuizzes": star_quizzes,
    "passageQuizzes": passage_quizzes
}

target_file = "/usr/local/google/home/yunchiao/jlpt-techo/src/data/quiz/n3.json"
with open(target_file, "w", encoding="utf-8") as f:
    json.dump(n3_data, f, ensure_ascii=False, indent=2)

print(f"Successfully wrote {target_file}!")
