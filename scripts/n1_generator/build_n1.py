# -*- coding: utf-8 -*-
"""
Builds and writes /usr/local/google/home/yunchiao/jlpt-techo/src/data/quiz/n1.json
Total: 300 sentence quizzes + 125 star quizzes + 25 passages (75 sub-questions) = 500 questions.
"""
import json
import os
import sys

# Ensure local imports work whether run from repo root or scripts/n1_generator/
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from create_sentences import generate_sentence_quizzes
from create_stars import generate_star_quizzes, PERMS
from create_passages import generate_passage_quizzes

from sentence_part2 import SENTENCES_PART2
from sentence_part3 import SENTENCES_PART3
from create_stars_part2 import RAW_STARS_PART2
from create_passages_part2 import RAW_PASSAGES_PART2

def build_all_sentence_quizzes():
    quizzes = generate_sentence_quizzes()
    assert len(quizzes) == 120, f"Expected 120 original sentences, got {len(quizzes)}"
    
    new_raw = SENTENCES_PART2 + SENTENCES_PART3
    assert len(new_raw) == 180, f"Expected 180 new sentences, got {len(new_raw)}"
    
    for i, q in enumerate(new_raw):
        idx = 120 + i
        correct_idx = (i % 4) + 1  # 1, 2, 3, 4 evenly distributed
        opts = [None] * 4
        opts[correct_idx - 1] = q["ans"]
        d_idx = 0
        for j in range(4):
            if opts[j] is None:
                opts[j] = q["distractors"][d_idx]
                d_idx += 1
        quizzes.append({
            "id": f"n1-s-{idx + 1}",
            "question": q["q"],
            "options": opts,
            "correctIndex": correct_idx,
            "explanation": q["exp"],
            "targetGrammar": q["grammar"]
        })
    assert len(quizzes) == 300, f"Expected 300 total sentences, got {len(quizzes)}"
    return quizzes

def build_all_star_quizzes():
    quizzes = generate_star_quizzes()
    assert len(quizzes) == 50, f"Expected 50 original stars, got {len(quizzes)}"
    
    assert len(RAW_STARS_PART2) == 75, f"Expected 75 new stars, got {len(RAW_STARS_PART2)}"
    for i, s in enumerate(RAW_STARS_PART2):
        idx = 50 + i
        target_star = (i % 4) + 1
        perm = PERMS[target_star]
        assert perm[2] == target_star
        p = s["pieces"]
        assert len(p) == 4
        
        chunks = [None] * 4
        for slot in range(4):
            chunks[perm[slot] - 1] = p[slot]
            
        reconstructed = (s["pre"].strip() + "".join(chunks[perm[slot]-1] for slot in range(4)) + s["post"].strip()).replace(" ", "").replace("　", "")
        expected = s["full"].replace(" ", "").replace("　", "")
        assert reconstructed == expected, f"Star Item {idx+1} mismatch:\nGot:  {reconstructed}\nWant: {expected}"
        
        star_num = perm[2]
        star_chunk = chunks[star_num - 1]
        step_arrows = f"{p[0]} ({perm[0]}) ➔ {p[1]} ({perm[1]}) ➔ {p[2]} ({perm[2]}) ➔ {p[3]} ({perm[3]})。★ 為 {star_num} 號【{star_chunk}】。{s['note']}"
        
        quizzes.append({
            "id": f"n1-star-{idx+1}",
            "preText": s["pre"],
            "postText": s["post"],
            "starIndex": 2,
            "chunks": chunks,
            "correctOrder": perm,
            "explanation": step_arrows,
            "fullSentence": s["full"],
            "translation": s["trans"]
        })
    assert len(quizzes) == 125, f"Expected 125 total stars, got {len(quizzes)}"
    return quizzes

def build_all_passage_quizzes():
    quizzes, _ = generate_passage_quizzes()
    assert len(quizzes) == 10, f"Expected 10 original passages, got {len(quizzes)}"
    
    assert len(RAW_PASSAGES_PART2) == 15, f"Expected 15 new passages, got {len(RAW_PASSAGES_PART2)}"
    for p in RAW_PASSAGES_PART2:
        assert "【 01 】" in p["passage"]
        assert "【 02 】" in p["passage"]
        assert "【 03 】" in p["passage"]
        assert len(p["questions"]) == 3
        
        q_items = []
        for q in p["questions"]:
            target_idx = q["target_idx"]
            opts = [None] * 4
            opts[target_idx - 1] = q["ans"]
            d_idx = 0
            for j in range(4):
                if opts[j] is None:
                    opts[j] = q["distractors"][d_idx]
                    d_idx += 1
            q_items.append({
                "blankNumber": q["blankNumber"],
                "options": opts,
                "correctIndex": target_idx,
                "explanation": q["exp"]
            })
        quizzes.append({
            "id": p["id"],
            "title": p["title"],
            "genre": p["genre"],
            "passage": p["passage"],
            "questions": q_items,
            "translation": p["translation"]
        })
    assert len(quizzes) == 25, f"Expected 25 total passages, got {len(quizzes)}"
    return quizzes

def main():
    sentence_quizzes = build_all_sentence_quizzes()
    star_quizzes = build_all_star_quizzes()
    passage_quizzes = build_all_passage_quizzes()
    
    # Rigorous Validation checks
    assert len(sentence_quizzes) == 300, f"Expected 300 sentence quizzes, got {len(sentence_quizzes)}"
    assert len(star_quizzes) == 125, f"Expected 125 star quizzes, got {len(star_quizzes)}"
    assert len(passage_quizzes) == 25, f"Expected 25 passage quizzes, got {len(passage_quizzes)}"
    
    # Check IDs
    for idx, sq in enumerate(sentence_quizzes):
        expected_id = f"n1-s-{idx + 1}"
        assert sq["id"] == expected_id, f"Wrong ID: {sq['id']} != {expected_id}"
        assert len(sq["options"]) == 4, f"{sq['id']} options != 4"
        assert len(set(sq["options"])) == 4, f"{sq['id']} duplicate options"
        assert sq["correctIndex"] in (1, 2, 3, 4), f"{sq['id']} invalid correctIndex"
        assert sq["explanation"], f"{sq['id']} empty explanation"
        assert sq["targetGrammar"], f"{sq['id']} empty targetGrammar"
        assert "（　　）" in sq["question"] or "（　" in sq["question"], f"{sq['id']} missing blank"
        
    for idx, st in enumerate(star_quizzes):
        expected_id = f"n1-star-{idx + 1}"
        assert st["id"] == expected_id, f"Wrong ID: {st['id']} != {expected_id}"
        assert len(st["chunks"]) == 4, f"{st['id']} chunks != 4"
        assert len(set(st["chunks"])) == 4, f"{st['id']} duplicate chunks"
        assert len(st["correctOrder"]) == 4, f"{st['id']} correctOrder != 4"
        assert set(st["correctOrder"]) == {1, 2, 3, 4}, f"{st['id']} correctOrder not permutation of 1..4"
        assert st["starIndex"] == 2, f"{st['id']} starIndex != 2"
        recon = (st["preText"].strip() + "".join(st["chunks"][c-1] for c in st["correctOrder"]) + st["postText"].strip()).replace(" ", "").replace("　", "")
        exp = st["fullSentence"].replace(" ", "").replace("　", "")
        assert recon == exp, f"Star {st['id']} reconstruction mismatch:\nRecon: {recon}\nExp:   {exp}"
        assert st["translation"], f"{st['id']} empty translation"
        assert st["explanation"], f"{st['id']} empty explanation"
        
    total_passage_subquestions = 0
    for idx, pq in enumerate(passage_quizzes):
        expected_id = f"n1-p-{idx + 1}"
        assert pq["id"] == expected_id, f"Wrong ID: {pq['id']} != {expected_id}"
        assert len(pq["questions"]) == 3, f"{pq['id']} questions != 3"
        for q_idx, q in enumerate(pq["questions"]):
            total_passage_subquestions += 1
            assert q["blankNumber"] == q_idx + 1
            assert len(q["options"]) == 4, f"{pq['id']} Q{q_idx+1} options != 4"
            assert len(set(q["options"])) == 4, f"{pq['id']} Q{q_idx+1} duplicate options"
            assert q["correctIndex"] in (1, 2, 3, 4), f"{pq['id']} Q{q_idx+1} invalid correctIndex"
            assert q["explanation"], f"{pq['id']} Q{q_idx+1} empty explanation"
        assert "【 01 】" in pq["passage"]
        assert "【 02 】" in pq["passage"]
        assert "【 03 】" in pq["passage"]
        assert pq["translation"]

    total_questions = len(sentence_quizzes) + len(star_quizzes) + total_passage_subquestions
    print(f"Total verified questions: {total_questions} (300 sentences + 125 stars + {total_passage_subquestions} passage sub-questions)")
    assert total_questions == 500, f"Expected 500 questions, got {total_questions}"
    
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
