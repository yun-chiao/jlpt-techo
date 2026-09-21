# -*- coding: utf-8 -*-
"""
make_sentence_data_part2.py
Builds 180 complete, high-quality JLPT N5 sentence quizzes (id: n5-s-121 ~ n5-s-300).
Combines DATA_121_180, DATA_181_240, and DATA_241_300.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sentence_part2_a import DATA_121_180
from sentence_part2_b import DATA_181_240
from sentence_part2_c import DATA_241_300

def get_sentence_quizzes_part2():
    all_raw = DATA_121_180 + DATA_181_240 + DATA_241_300
    assert len(all_raw) == 180, f"Expected 180 quizzes, got {len(all_raw)}"

    quizzes = []
    # Start idx at 120 so ID becomes n5-s-121 and target_idx continues cyclically
    for offset, item in enumerate(all_raw):
        idx = 120 + offset
        q_text, opts, orig_ans, exp, tag = item
        qid = f"n5-s-{idx + 1}"

        target_idx = (idx % 4) + 1
        correct_opt = opts[orig_ans - 1]
        other_opts = [o for i, o in enumerate(opts) if i != orig_ans - 1]

        new_opts = []
        other_iter = iter(other_opts)
        for slot in range(1, 5):
            if slot == target_idx:
                new_opts.append(correct_opt)
            else:
                new_opts.append(next(other_iter))

        quizzes.append({
            "id": qid,
            "question": q_text,
            "options": new_opts,
            "correctIndex": target_idx,
            "explanation": exp,
            "targetGrammar": tag
        })

    return quizzes

if __name__ == "__main__":
    qs = get_sentence_quizzes_part2()
    print(f"Generated {len(qs)} sentence quizzes (n5-s-121 ~ n5-s-300).")
    counts = {}
    for q in qs:
        counts[q['correctIndex']] = counts.get(q['correctIndex'], 0) + 1
    print("Distribution of correctIndex:", counts)
