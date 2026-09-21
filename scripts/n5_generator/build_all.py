# -*- coding: utf-8 -*-
"""
build_all.py
Assembles 500 JLPT N5 questions:
- 300 sentenceQuizzes (n5-s-1 ~ n5-s-300)
- 125 starQuizzes (n5-star-1 ~ n5-star-125)
- 25 passageQuizzes (n5-p-1 ~ n5-p-25, 75 subquestions)
Total = 300 + 125 + 75 = 500 questions.
Writes to /usr/local/google/home/yunchiao/jlpt-techo/src/data/quiz/n5.json
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_sentence_data import get_sentence_quizzes
from make_sentence_data_part2 import get_sentence_quizzes_part2
from make_star_data import get_star_quizzes
from make_star_data_part2 import get_star_quizzes_part2
from make_passage_data import get_passage_quizzes
from make_passage_data_part2 import get_passage_quizzes_part2

def main():
    sentence_quizzes = get_sentence_quizzes() + get_sentence_quizzes_part2()
    star_quizzes = get_star_quizzes() + get_star_quizzes_part2()
    passage_quizzes = get_passage_quizzes() + get_passage_quizzes_part2()

    # Integrity assertions
    assert len(sentence_quizzes) == 300, f"Expected 300 sentence quizzes, got {len(sentence_quizzes)}"
    assert len(star_quizzes) == 125, f"Expected 125 star quizzes, got {len(star_quizzes)}"
    assert len(passage_quizzes) == 25, f"Expected 25 passage quizzes, got {len(passage_quizzes)}"
    total_passage_subquestions = sum(len(p["questions"]) for p in passage_quizzes)
    assert total_passage_subquestions == 75, f"Expected 75 passage subquestions, got {total_passage_subquestions}"

    total_questions = len(sentence_quizzes) + len(star_quizzes) + total_passage_subquestions
    assert total_questions == 500, f"Expected 500 total questions, got {total_questions}"
    print(f"Total questions: {total_questions} (300 sentence + 125 star + 75 passage)")

    # Check Sentence ID sequences & fields
    s_dist = {}
    for i, q in enumerate(sentence_quizzes, 1):
        expected_id = f"n5-s-{i}"
        assert q["id"] == expected_id, f"Sentence quiz id mismatch: {q['id']} vs {expected_id}"
        assert len(q["options"]) == 4, f"Options length != 4 in {q['id']}"
        assert len(set(q["options"])) == 4, f"Duplicate options in {q['id']}"
        assert 1 <= q["correctIndex"] <= 4, f"correctIndex invalid in {q['id']}"
        assert "（　　）" in q["question"], f"Blank missing in {q['id']}"
        assert len(q["explanation"].strip()) > 0, f"Empty explanation in {q['id']}"
        assert len(q.get("targetGrammar", "").strip()) > 0, f"Empty targetGrammar in {q['id']}"
        s_dist[q["correctIndex"]] = s_dist.get(q["correctIndex"], 0) + 1
    print(f"✓ Sentence quizzes options distribution: {s_dist}")

    # Check Star ID sequences & fields
    star_dist = {}
    for i, q in enumerate(star_quizzes, 1):
        expected_id = f"n5-star-{i}"
        assert q["id"] == expected_id, f"Star quiz id mismatch: {q['id']} vs {expected_id}"
        assert len(q["chunks"]) == 4, f"Chunks length != 4 in {q['id']}"
        assert len(set(q["chunks"])) == 4, f"Duplicate chunks in {q['id']}"
        assert sorted(q["correctOrder"]) == [1, 2, 3, 4], f"correctOrder invalid in {q['id']}"
        assert q["starIndex"] == 2, f"starIndex != 2 in {q['id']}"
        assert len(q["explanation"].strip()) > 0, f"Empty explanation in {q['id']}"
        assert len(q["fullSentence"].strip()) > 0, f"Empty fullSentence in {q['id']}"
        assert len(q["translation"].strip()) > 0, f"Empty translation in {q['id']}"
        star_num = q["correctOrder"][q["starIndex"]]
        star_dist[star_num] = star_dist.get(star_num, 0) + 1
    print(f"✓ Star quizzes answers distribution: {star_dist}")

    # Check Passage ID sequences & fields
    p_dist = {}
    for i, p in enumerate(passage_quizzes, 1):
        expected_id = f"n5-p-{i}"
        assert p["id"] == expected_id, f"Passage quiz id mismatch: {p['id']} vs {expected_id}"
        for b in ["【 01 】", "【 02 】", "【 03 】"]:
            assert b in p["passage"], f"{b} missing in {p['id']}"
        assert len(p["questions"]) == 3, f"Passage questions length != 3 in {p['id']}"
        assert len(p["title"].strip()) > 0, f"Empty title in {p['id']}"
        assert len(p["genre"].strip()) > 0, f"Empty genre in {p['id']}"
        assert len(p["translation"].strip()) > 0, f"Empty translation in {p['id']}"
        for qi, sq in enumerate(p["questions"], 1):
            assert sq["blankNumber"] == qi
            assert len(sq["options"]) == 4
            assert len(set(sq["options"])) == 4, f"Duplicate options in {p['id']} Q{qi}"
            assert 1 <= sq["correctIndex"] <= 4
            assert len(sq["explanation"].strip()) > 0
            p_dist[sq["correctIndex"]] = p_dist.get(sq["correctIndex"], 0) + 1
    print(f"✓ Passage subquestions distribution: {p_dist}")

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
