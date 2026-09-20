# -*- coding: utf-8 -*-
"""Master Build Script for JLPT N2 Quiz Dataset (200 Questions Total)"""

import json
import os
import sys

# Add current script directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from sentence_part1 import get_sentence_part1
from sentence_part2 import get_sentence_part2
from sentence_part3 import get_sentence_part3
from star_quizzes import get_star_quizzes
from passage_quizzes import get_passage_quizzes

def build():
    # 1. Gather all sentence quizzes
    sq1 = get_sentence_part1()
    sq2 = get_sentence_part2()
    sq3 = get_sentence_part3()
    sentence_quizzes = sq1 + sq2 + sq3

    assert len(sentence_quizzes) == 120, f"Expected 120 sentence quizzes, got {len(sentence_quizzes)}"

    # 2. Gather star quizzes
    star_quizzes = get_star_quizzes()
    assert len(star_quizzes) == 50, f"Expected 50 star quizzes, got {len(star_quizzes)}"

    # 3. Gather passage quizzes
    passage_quizzes = get_passage_quizzes()
    assert len(passage_quizzes) == 10, f"Expected 10 passages, got {len(passage_quizzes)}"

    # Total questions
    total_questions = len(sentence_quizzes) + len(star_quizzes) + sum(len(p["questions"]) for p in passage_quizzes)
    assert total_questions == 200, f"Expected 200 total questions, got {total_questions}"

    print(f"Collected: {len(sentence_quizzes)} sentence + {len(star_quizzes)} star + {len(passage_quizzes)} passages (30 subQ) = {total_questions} total questions.")

    # Validation: Sentence quizzes
    for idx, q in enumerate(sentence_quizzes):
        expected_id = f"n2-s-{idx + 1}"
        assert q["id"] == expected_id, f"Sentence id mismatch: expected {expected_id}, got {q['id']}"
        assert "（　　）" in q["question"] or "（　）" in q["question"], f"Missing blank in {q['id']}"
        assert len(q["options"]) == 4, f"Options length not 4 in {q['id']}"
        assert len(set(q["options"])) == 4, f"Duplicate options in {q['id']}"
        assert q["correctIndex"] in [1, 2, 3, 4], f"Invalid correctIndex in {q['id']}"
        assert len(q["explanation"].strip()) > 0, f"Empty explanation in {q['id']}"
        assert len(q.get("targetGrammar", "").strip()) > 0, f"Empty targetGrammar in {q['id']}"

    # Validation: Star quizzes
    for idx, q in enumerate(star_quizzes):
        expected_id = f"n2-star-{idx + 1}"
        assert q["id"] == expected_id, f"Star id mismatch: expected {expected_id}, got {q['id']}"
        assert q["starIndex"] == 2, f"starIndex must be 2 in {q['id']}"
        assert len(q["chunks"]) == 4, f"chunks length not 4 in {q['id']}"
        assert len(set(q["chunks"])) == 4, f"Duplicate chunks in {q['id']}"
        assert sorted(q["correctOrder"]) == [1, 2, 3, 4], f"Invalid permutation in {q['id']}"
        reconstructed = q["preText"].strip() + "".join(q["chunks"][i - 1] for i in q["correctOrder"]) + q["postText"].strip()
        assert reconstructed == q["fullSentence"].strip(), f"Mismatch in {q['id']}: {reconstructed} != {q['fullSentence']}"
        star_num = q["correctOrder"][q["starIndex"]]
        assert f"★ 為 {star_num} 號" in q["explanation"], f"Star number explanation missing in {q['id']}"
        assert len(q["translation"].strip()) > 0, f"Empty translation in {q['id']}"

    # Validation: Passage quizzes
    for idx, p in enumerate(passage_quizzes):
        expected_id = f"n2-p-{idx + 1}"
        assert p["id"] == expected_id, f"Passage id mismatch: expected {expected_id}, got {p['id']}"
        assert "【 01 】" in p["passage"] and "【 02 】" in p["passage"] and "【 03 】" in p["passage"], f"Missing blanks in {p['id']}"
        assert len(p["questions"]) == 3, f"Passage {p['id']} does not have 3 questions"
        for sub_idx, sub_q in enumerate(p["questions"]):
            assert sub_q["blankNumber"] == sub_idx + 1, f"blankNumber mismatch in {p['id']} question {sub_idx}"
            assert len(sub_q["options"]) == 4, f"Options length not 4 in {p['id']} question {sub_idx}"
            assert len(set(sub_q["options"])) == 4, f"Duplicate options in {p['id']} question {sub_idx}"
            assert sub_q["correctIndex"] in [1, 2, 3, 4], f"Invalid correctIndex in {p['id']} question {sub_idx}"
            assert len(sub_q["explanation"].strip()) > 0, f"Empty explanation in {p['id']} question {sub_idx}"
        assert len(p["translation"].strip()) > 0, f"Empty translation in {p['id']}"

    # Build final object
    final_data = {
        "level": "n2",
        "levelLabel": "N2 商務實務中高級",
        "sentenceQuizzes": sentence_quizzes,
        "starQuizzes": star_quizzes,
        "passageQuizzes": passage_quizzes
    }

    target_path = os.path.abspath(os.path.join(script_dir, "../../src/data/quiz/n2.json"))
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)

    print(f"Successfully generated and wrote {target_path} ({os.path.getsize(target_path)} bytes)")

if __name__ == "__main__":
    build()
