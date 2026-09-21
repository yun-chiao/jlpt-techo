# -*- coding: utf-8 -*-
"""
make_passage_data_part2.py
Builds 15 complete, high-quality JLPT N5 passage quizzes (id: n5-p-11 ~ n5-p-25),
with 3 questions per passage (45 questions in total).
Combines RAW_PASSAGES_11_18 and RAW_PASSAGES_19_25.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from passage_part2_a import RAW_PASSAGES_11_18
from passage_part2_b import RAW_PASSAGES_19_25

def get_passage_quizzes_part2():
    all_raw = RAW_PASSAGES_11_18 + RAW_PASSAGES_19_25
    assert len(all_raw) == 15, f"Expected 15 passages, got {len(all_raw)}"

    passages = []
    # Start global_q_counter at 30 to continue cyclically from passage 10 (30 questions)
    global_q_counter = 30

    for idx, p in enumerate(all_raw):
        expected_id = f"n5-p-{idx + 11}"
        assert p["id"] == expected_id, f"ID mismatch: {p['id']} vs {expected_id}"
        pid = p["id"]
        title = p["title"]
        genre = p["genre"]
        passage_text = p["passage"]
        translation = p["translation"]

        processed_qs = []
        for q in p["questions"]:
            blank_num = q["blankNumber"]
            correct_opt = q["correct"]
            distractors = q["distractors"]

            # Distribute correctIndex across 1, 2, 3, 4
            target_idx = (global_q_counter % 4) + 1
            global_q_counter += 1

            options = []
            d_iter = iter(distractors)
            for slot in range(1, 5):
                if slot == target_idx:
                    options.append(correct_opt)
                else:
                    options.append(next(d_iter))

            processed_qs.append({
                "blankNumber": blank_num,
                "options": options,
                "correctIndex": target_idx,
                "explanation": q["explanation"]
            })

        passages.append({
            "id": pid,
            "title": title,
            "genre": genre,
            "passage": passage_text,
            "questions": processed_qs,
            "translation": translation
        })

    return passages

if __name__ == "__main__":
    ps = get_passage_quizzes_part2()
    print(f"Generated {len(ps)} passages with {sum(len(p['questions']) for p in ps)} subquestions.")
    counts = {}
    for p in ps:
        for q in p['questions']:
            counts[q['correctIndex']] = counts.get(q['correctIndex'], 0) + 1
    print("Distribution of correctIndex:", counts)
