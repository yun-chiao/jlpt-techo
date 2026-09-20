# -*- coding: utf-8 -*-
"""
build_all.py
Assembles 200 JLPT N5 questions:
- 120 sentenceQuizzes (n5-s-1 ~ n5-s-120)
- 50 starQuizzes (n5-star-1 ~ n5-star-50)
- 10 passageQuizzes (n5-p-1 ~ n5-p-10, 30 subquestions)
Writes to /usr/local/google/home/yunchiao/jlpt-techo/src/data/quiz/n5.json
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_sentence_data import get_sentence_quizzes
from make_star_data import get_star_quizzes
from make_passage_data import get_passage_quizzes

def main():
    sentence_quizzes = get_sentence_quizzes()
    star_quizzes = get_star_quizzes()
    passage_quizzes = get_passage_quizzes()

    # Integrity assertions
    assert len(sentence_quizzes) == 120, f"Expected 120 sentence quizzes, got {len(sentence_quizzes)}"
    assert len(star_quizzes) == 50, f"Expected 50 star quizzes, got {len(star_quizzes)}"
    assert len(passage_quizzes) == 10, f"Expected 10 passage quizzes, got {len(passage_quizzes)}"
    total_passage_subquestions = sum(len(p["questions"]) for p in passage_quizzes)
    assert total_passage_subquestions == 30, f"Expected 30 passage subquestions, got {total_passage_subquestions}"

    total_questions = len(sentence_quizzes) + len(star_quizzes) + total_passage_subquestions
    print(f"Total questions: {total_questions} (120 sentence + 50 star + 30 passage)")

    # Check ID sequences
    for i, q in enumerate(sentence_quizzes, 1):
        expected_id = f"n5-s-{i}"
        assert q["id"] == expected_id, f"Sentence quiz id mismatch: {q['id']} vs {expected_id}"
        assert len(q["options"]) == 4, f"Options length != 4 in {q['id']}"
        assert 1 <= q["correctIndex"] <= 4, f"correctIndex invalid in {q['id']}"
        assert "（　　）" in q["question"], f"Blank missing in {q['id']}"

    for i, q in enumerate(star_quizzes, 1):
        expected_id = f"n5-star-{i}"
        assert q["id"] == expected_id, f"Star quiz id mismatch: {q['id']} vs {expected_id}"
        assert len(q["chunks"]) == 4, f"Chunks length != 4 in {q['id']}"
        assert sorted(q["correctOrder"]) == [1, 2, 3, 4], f"correctOrder invalid in {q['id']}"
        assert q["starIndex"] == 2, f"starIndex != 2 in {q['id']}"

    for i, p in enumerate(passage_quizzes, 1):
        expected_id = f"n5-p-{i}"
        assert p["id"] == expected_id, f"Passage quiz id mismatch: {p['id']} vs {expected_id}"
        for b in ["【 01 】", "【 02 】", "【 03 】"]:
            assert b in p["passage"], f"{b} missing in {p['id']}"
        assert len(p["questions"]) == 3, f"Passage questions length != 3 in {p['id']}"
        for qi, sq in enumerate(p["questions"], 1):
            assert sq["blankNumber"] == qi
            assert len(sq["options"]) == 4
            assert 1 <= sq["correctIndex"] <= 4

    dataset = {
        "level": "n5",
        "levelLabel": "N5 初級基礎",
        "sentenceQuizzes": sentence_quizzes,
        "starQuizzes": star_quizzes,
        "passageQuizzes": passage_quizzes
    }

    target_path = "/usr/local/google/home/yunchiao/jlpt-techo/src/data/quiz/n5.json"
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)

    print(f"Successfully wrote {target_path}")

if __name__ == "__main__":
    main()
