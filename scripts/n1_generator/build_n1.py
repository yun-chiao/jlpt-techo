# -*- coding: utf-8 -*-
"""
Builds and writes /usr/local/google/home/yunchiao/jlpt-techo/src/data/quiz/n1.json
"""
import json
import os
import sys

from create_sentences import generate_sentence_quizzes
from create_stars import generate_star_quizzes
from create_passages import generate_passage_quizzes

def main():
    sentence_quizzes = generate_sentence_quizzes()
    star_quizzes = generate_star_quizzes()
    passage_quizzes, p_dist = generate_passage_quizzes()
    
    # Validation checks
    assert len(sentence_quizzes) == 120, f"Expected 120 sentence quizzes, got {len(sentence_quizzes)}"
    assert len(star_quizzes) == 50, f"Expected 50 star quizzes, got {len(star_quizzes)}"
    assert len(passage_quizzes) == 10, f"Expected 10 passage quizzes, got {len(passage_quizzes)}"
    
    # Check IDs
    for idx, sq in enumerate(sentence_quizzes):
        expected_id = f"n1-s-{idx + 1}"
        assert sq["id"] == expected_id, f"Wrong ID: {sq['id']} != {expected_id}"
        assert len(sq["options"]) == 4
        assert sq["correctIndex"] in (1, 2, 3, 4)
        assert sq["explanation"]
        assert sq["targetGrammar"]
        assert "（　　）" in sq["question"] or "（　" in sq["question"]
        
    for idx, st in enumerate(star_quizzes):
        expected_id = f"n1-star-{idx + 1}"
        assert st["id"] == expected_id, f"Wrong ID: {st['id']} != {expected_id}"
        assert len(st["chunks"]) == 4
        assert len(st["correctOrder"]) == 4
        assert set(st["correctOrder"]) == {1, 2, 3, 4}
        assert st["starIndex"] == 2
        # Check fullSentence reconstruction
        recon = (st["preText"].strip() + "".join(st["chunks"][c-1] for c in st["correctOrder"]) + st["postText"].strip()).replace(" ", "").replace("　", "")
        exp = st["fullSentence"].replace(" ", "").replace("　", "")
        assert recon == exp, f"Star {st['id']} reconstruction mismatch:\nRecon: {recon}\nExp:   {exp}"
        assert st["translation"]
        assert st["explanation"]
        
    total_passage_subquestions = 0
    for idx, pq in enumerate(passage_quizzes):
        expected_id = f"n1-p-{idx + 1}"
        assert pq["id"] == expected_id, f"Wrong ID: {pq['id']} != {expected_id}"
        assert len(pq["questions"]) == 3
        for q_idx, q in enumerate(pq["questions"]):
            total_passage_subquestions += 1
            assert q["blankNumber"] == q_idx + 1
            assert len(q["options"]) == 4
            assert q["correctIndex"] in (1, 2, 3, 4)
            assert q["explanation"]
        assert "【 01 】" in pq["passage"]
        assert "【 02 】" in pq["passage"]
        assert "【 03 】" in pq["passage"]
        assert pq["translation"]

    total_questions = len(sentence_quizzes) + len(star_quizzes) + total_passage_subquestions
    print(f"Total verified questions: {total_questions} (120 sentences + 50 stars + {total_passage_subquestions} passage sub-questions)")
    
    data = {
        "level": "n1",
        "levelLabel": "N1 最高殿堂精通",
        "sentenceQuizzes": sentence_quizzes,
        "starQuizzes": star_quizzes,
        "passageQuizzes": passage_quizzes
    }
    
    target_path = "/usr/local/google/home/yunchiao/jlpt-techo/src/data/quiz/n1.json"
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Successfully wrote data to {target_path}")

if __name__ == "__main__":
    main()
