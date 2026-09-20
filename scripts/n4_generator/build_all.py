# -*- coding: utf-8 -*-
"""
Main generator for JLPT N4 Quiz Dataset (200 questions):
- sentenceQuizzes: 120 questions (n4-s-1 ~ n4-s-120)
- starQuizzes: 50 questions (n4-star-1 ~ n4-star-50)
- passageQuizzes: 10 passages * 3 = 30 questions (n4-p-1 ~ n4-p-10)
Writes directly to src/data/quiz/n4.json and verifies data integrity.
"""

import json
import os
import sys

from data_n4_sentence import get_sentence_quizzes
from data_n4_star import get_balanced_star_quizzes
from data_n4_passage import get_passage_quizzes

TARGET_FILE = "/usr/local/google/home/yunchiao/jlpt-techo/src/data/quiz/n4.json"

def main():
    print("=== Generating JLPT N4 Quiz Data (200 Questions) ===")
    
    sentence_quizzes = get_sentence_quizzes()
    star_quizzes = get_balanced_star_quizzes()
    passage_quizzes = get_passage_quizzes()
    
    # Assertions
    assert len(sentence_quizzes) == 120, f"Expected 120 sentence quizzes, got {len(sentence_quizzes)}"
    assert len(star_quizzes) == 50, f"Expected 50 star quizzes, got {len(star_quizzes)}"
    assert len(passage_quizzes) == 10, f"Expected 10 passage quizzes, got {len(passage_quizzes)}"
    
    passage_sub_count = sum(len(p["questions"]) for p in passage_quizzes)
    assert passage_sub_count == 30, f"Expected 30 passage sub-questions, got {passage_sub_count}"
    
    total_questions = len(sentence_quizzes) + len(star_quizzes) + passage_sub_count
    assert total_questions == 200, f"Expected 200 total questions, got {total_questions}"
    
    # Verify sentence quizzes integrity
    s_dist = {}
    for i, sq in enumerate(sentence_quizzes):
        expected_id = f"n4-s-{i + 1}"
        assert sq["id"] == expected_id, f"ID mismatch: {sq['id']} != {expected_id}"
        assert len(sq["options"]) == 4, f"Options length error in {sq['id']}"
        assert sq["correctIndex"] in (1, 2, 3, 4), f"correctIndex error in {sq['id']}"
        assert sq["explanation"], f"Empty explanation in {sq['id']}"
        assert sq["targetGrammar"], f"Empty targetGrammar in {sq['id']}"
        s_dist[sq["correctIndex"]] = s_dist.get(sq["correctIndex"], 0) + 1
        
    print(f"✓ 120 Sentence Quizzes verified. Option distribution: {s_dist}")
    
    # Verify star quizzes integrity
    star_dist = {}
    for i, st in enumerate(star_quizzes):
        expected_id = f"n4-star-{i + 1}"
        assert st["id"] == expected_id, f"ID mismatch: {st['id']} != {expected_id}"
        assert len(st["chunks"]) == 4, f"Chunks error in {st['id']}"
        assert sorted(st["correctOrder"]) == [1, 2, 3, 4], f"Order error in {st['id']}"
        assert st["starIndex"] == 2, f"starIndex error in {st['id']}"
        
        # Verify reconstruction
        pre = st["preText"].replace("　", "").replace(" ", "")
        post = st["postText"].replace("　", "").replace(" ", "")
        reconstructed = pre + "".join(st["chunks"][idx - 1] for idx in st["correctOrder"]) + post
        expected_sentence = st["fullSentence"].replace("　", "").replace(" ", "")
        assert reconstructed == expected_sentence, f"Reconstruction mismatch in {st['id']}"
        
        ans = st["correctOrder"][st["starIndex"]]
        star_dist[ans] = star_dist.get(ans, 0) + 1
        
    print(f"✓ 50 Star Quizzes verified. Star answer distribution: {star_dist}")
    
    # Verify passage quizzes integrity
    p_dist = {}
    for i, pq in enumerate(passage_quizzes):
        expected_id = f"n4-p-{i + 1}"
        assert pq["id"] == expected_id, f"ID mismatch: {pq['id']} != {expected_id}"
        assert "【 01 】" in pq["passage"]
        assert "【 02 】" in pq["passage"]
        assert "【 03 】" in pq["passage"]
        assert len(pq["questions"]) == 3, f"Question count in {pq['id']} is not 3"
        for q in pq["questions"]:
            assert len(q["options"]) == 4
            assert q["correctIndex"] in (1, 2, 3, 4)
            p_dist[q["correctIndex"]] = p_dist.get(q["correctIndex"], 0) + 1
            
    print(f"✓ 10 Passage Quizzes (30 sub-questions) verified. Distribution: {p_dist}")
    
    dataset = {
        "level": "n4",
        "levelLabel": "N4 初中級進階",
        "sentenceQuizzes": sentence_quizzes,
        "starQuizzes": star_quizzes,
        "passageQuizzes": passage_quizzes
    }
    
    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
        
    file_size = os.path.getsize(TARGET_FILE)
    print(f"✓ Successfully wrote {TARGET_FILE} ({file_size} bytes)")
    print(f"✓ Total questions in N4 quiz bank: {total_questions}")

if __name__ == "__main__":
    main()
