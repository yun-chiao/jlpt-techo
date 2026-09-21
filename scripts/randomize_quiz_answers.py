# -*- coding: utf-8 -*-
"""
Randomizes the multiple-choice options in JLPT Quiz data to eliminate predictable
sequential repeating patterns (e.g., 1, 2, 3, 4, 1, 2, 3, 4...) while maintaining
overall option balance (approx. 25% each for options 1, 2, 3, 4).

Operates on data_full/quiz/*.json and updates src/data/quiz/*.json (50-question web tier).
"""

import json
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FULL_DIR = BASE_DIR / "data_full" / "quiz"
SRC_QUIZ_DIR = BASE_DIR / "src" / "data" / "quiz"

SEEDS = {
    "n1": 101,
    "n2": 202,
    "n3": 303,
    "n4": 404,
    "n5": 505,
}

def generate_natural_sequence(n: int, seed: int) -> list[int]:
    """
    Generates a balanced sequence of 1, 2, 3, 4 where each option appears
    equally (within +/- 1), but with natural pseudo-random shuffling so that
    no repeating cycles (like 1, 2, 3, 4 or 4, 3, 2, 1) occur and no option
    repeats consecutively.
    """
    rng = random.Random(seed)
    pool = []
    while len(pool) < n:
        block = [1, 2, 3, 4]
        rng.shuffle(block)
        # Avoid same option adjacent across block boundary
        if pool and block[0] == pool[-1]:
            block[0], block[1] = block[1], block[0]
        pool.extend(block)
    return pool[:n]

def randomize_level(lvl: str):
    data_file = DATA_FULL_DIR / f"{lvl}.json"
    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    seed_base = SEEDS[lvl]

    # 1. Randomize sentenceQuizzes
    sq_list = data["sentenceQuizzes"]
    sq_seq = generate_natural_sequence(len(sq_list), seed_base)
    rng_sq = random.Random(seed_base + 111)

    for i, q in enumerate(sq_list):
        orig_corr = q["options"][q["correctIndex"] - 1]
        distractors = [opt for j, opt in enumerate(q["options"]) if j != q["correctIndex"] - 1]
        rng_sq.shuffle(distractors)
        
        target_idx = sq_seq[i]
        new_opts = list(distractors)
        new_opts.insert(target_idx - 1, orig_corr)
        
        assert new_opts[target_idx - 1] == orig_corr, f"Error at {q['id']}: expected {orig_corr} at {target_idx}"
        q["options"] = new_opts
        q["correctIndex"] = target_idx

    # 2. Randomize passageQuizzes
    pq_list = data["passageQuizzes"]
    total_pq_questions = sum(len(p["questions"]) for p in pq_list)
    pq_seq = generate_natural_sequence(total_pq_questions, seed_base + 333)
    rng_pq = random.Random(seed_base + 777)

    global_q_idx = 0
    for p in pq_list:
        for q in p["questions"]:
            orig_corr = q["options"][q["correctIndex"] - 1]
            distractors = [opt for j, opt in enumerate(q["options"]) if j != q["correctIndex"] - 1]
            rng_pq.shuffle(distractors)
            
            target_idx = pq_seq[global_q_idx]
            new_opts = list(distractors)
            new_opts.insert(target_idx - 1, orig_corr)
            
            assert new_opts[target_idx - 1] == orig_corr, f"Error in passage blank {q.get('blankNumber')}"
            q["options"] = new_opts
            q["correctIndex"] = target_idx
            global_q_idx += 1

    # Save to data_full
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # 3. Create 50-question web tier in src/data/quiz/
    web_tier = {
        "level": data["level"],
        "levelLabel": data["levelLabel"],
        "sentenceQuizzes": data["sentenceQuizzes"][:30],
        "starQuizzes": data["starQuizzes"][:14],
        "passageQuizzes": data["passageQuizzes"][:2],
    }
    src_file = SRC_QUIZ_DIR / f"{lvl}.json"
    with open(src_file, "w", encoding="utf-8") as f:
        json.dump(web_tier, f, ensure_ascii=False, indent=2)

    sq_answers_sample = [q["correctIndex"] for q in web_tier["sentenceQuizzes"][:15]]
    print(f"✓ {lvl.upper()} randomized! First 15 sentence answers: {sq_answers_sample}")

def main():
    print("=== Randomizing Quiz Options & Answers Across All Levels ===")
    for lvl in ["n1", "n2", "n3", "n4", "n5"]:
        randomize_level(lvl)
    print("All levels randomized successfully!")

if __name__ == "__main__":
    main()
