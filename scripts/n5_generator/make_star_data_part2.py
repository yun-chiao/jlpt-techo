# -*- coding: utf-8 -*-
"""
make_star_data_part2.py
Builds 75 complete, high-quality JLPT N5 star scramble quizzes (id: n5-star-51 ~ n5-star-125).
Combines DATA_STAR_51_90 and DATA_STAR_91_125.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from star_part2_a import DATA_STAR_51_90
from star_part2_b import DATA_STAR_91_125

def rebalance(chunks, order, desired_star):
    current_star = order[2]
    if current_star == desired_star:
        return chunks, order
    mapping = {current_star: desired_star, desired_star: current_star}
    new_chunks = list(chunks)
    new_chunks[current_star - 1] = chunks[desired_star - 1]
    new_chunks[desired_star - 1] = chunks[current_star - 1]
    new_order = [mapping.get(x, x) for x in order]
    return new_chunks, new_order

def get_star_quizzes_part2():
    all_raw = DATA_STAR_51_90 + DATA_STAR_91_125
    assert len(all_raw) == 75, f"Expected 75 star quizzes, got {len(all_raw)}"

    quizzes = []
    for offset, item in enumerate(all_raw):
        idx = 50 + offset
        pre, post, orig_chunks, orig_order, full_sent, trans, reason = item
        qid = f"n5-star-{idx + 1}"

        desired_star = (idx % 4) + 1
        chunks, order = rebalance(orig_chunks, orig_order, desired_star)

        star_slot_index = 2
        star_chunk_num = order[star_slot_index]
        assert star_chunk_num == desired_star
        star_chunk_text = chunks[star_chunk_num - 1]

        assert sorted(order) == [1, 2, 3, 4], f"Invalid order in {qid}: {order}"
        assert len(chunks) == 4, f"Invalid chunks in {qid}: {chunks}"

        exp = f"文法解構：{reason} 正確語序應為 {order}。因此 ★ 號位置（第 3 格）為 {star_chunk_num} 號「{star_chunk_text}」。"

        quizzes.append({
            "id": qid,
            "preText": pre,
            "postText": post,
            "starIndex": 2,
            "chunks": chunks,
            "correctOrder": order,
            "explanation": exp,
            "fullSentence": full_sent,
            "translation": trans
        })

    return quizzes

if __name__ == "__main__":
    qs = get_star_quizzes_part2()
    print(f"Generated {len(qs)} star scramble quizzes (n5-star-51 ~ n5-star-125).")
    star_counts = {}
    for q in qs:
        star_num = q['correctOrder'][q['starIndex']]
        star_counts[star_num] = star_counts.get(star_num, 0) + 1
    print("Distribution of star chunk number:", star_counts)
