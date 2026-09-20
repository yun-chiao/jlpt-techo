# -*- coding: utf-8 -*-
"""
make_passage_data.py
Builds 10 complete, high-quality JLPT N5 passage quizzes (id: n5-p-1 ~ n5-p-10),
with 3 questions per passage (30 questions in total).
"""

def get_passage_quizzes():
    raw_passages = [
        # Passage 1
        {
            "id": "n5-p-1",
            "title": "留学生エマさんの日記「はじめての京都旅行」",
            "genre": "日記・隨筆",
            "passage": (
                "先週の土曜日に、友達のリーさんと一緒に京都へ行きました。"
                "東京駅から新幹線に【 01 】、約2時間で京都に着きました。"
                "京都はとても歴史が古い町で、きれいなお寺がたくさんありました。\n"
                "お昼ご飯は、京都で有名な豆腐料理の店に入りました。"
                "料理はとてもおいしかった【 02 】、少し高かったです。\n"
                "午後はずっと雨が降っていました。【 03 】、"
                "傘をさしながら写真をたくさん撮って、とても楽しかったです。また行きたいです。"
            ),
            "translation": (
                "上週六我和朋友李同學一起去了京都。從東京站搭乘新幹線，約2小時到達京都。京都是歷史古城，有許多美麗寺廟。\n"
                "午餐進了一家有名豆腐料理店。料理很好吃，但有點貴。\n"
                "下午一直下雨。但是撐著傘拍了很多照片，非常開心。下次還想再去！"
            ),
            "questions": [
                {
                    "blankNumber": 1,
                    "correct": "乗って",
                    "distractors": ["乗る", "乗った", "乗り"],
                    "explanation": "前後相繼發生的動作，使用動詞て形（乗って）連接後續到達動作。"
                },
                {
                    "blankNumber": 2,
                    "correct": "ですが",
                    "distractors": ["から", "ので", "そして"],
                    "explanation": "「好吃」與「有點貴」為轉折對立關係，接在普通形後選轉折助詞「ですが（雖然...但是...）」最為自然。"
                },
                {
                    "blankNumber": 3,
                    "correct": "しかし",
                    "distractors": ["ですから", "それで", "そして"],
                    "explanation": "前句說明下雨的不便，後句表示撐傘拍照依然很開心，前後句意為轉折關係，使用接續詞「しかし（但是）」首字連接。"
                }
            ]
        },
        # Passage 2
        {
            "id": "n5-p-2",
            "title": "案内「私の日本語学校の１日」",
            "genre": "學校生活介紹",
            "passage": (
                "私の学校の授業は、毎朝9時に【 01 】。午前中は文法と漢字の勉強をします。"
                "先生はいつも優しくて、説明も分かりやすいです。\n"
                "12時になると、みんなで教室でお弁当を食べます。【 02 】、午後は会話の練習をたくさんします。\n"
                "学校が終わった後は、図書館で宿題をします。毎日とても忙しいですが、勉強はとても【 03 】です。"
            ),
            "translation": (
                "我們學校的課每天早上9點開始。上午學習文法與漢字。老師總是親切且解說清楚。\n"
                "到12點大家一起在教室吃便當。然後，下午做很多對話練習。\n"
                "放學後在圖書館寫作業。每天雖然很忙，但學習非常愉快！"
            ),
            "questions": [
                {
                    "blankNumber": 1,
                    "correct": "始まります",
                    "distractors": ["終わります", "あります", "行きます"],
                    "explanation": "每天早上9點課程「開始」，使用自動詞「始まります」。"
                },
                {
                    "blankNumber": 2,
                    "correct": "そして",
                    "distractors": ["しかし", "ですから", "でも"],
                    "explanation": "午前讀書、中午吃便當，接續詞「そして（然後、接著）」順接下午安排的會話練習。"
                },
                {
                    "blankNumber": 3,
                    "correct": "楽しい",
                    "distractors": ["楽しくて", "楽しく", "楽しみ"],
                    "explanation": "形容詞放在丁寧句尾修飾主語「勉強は」，使用基本終止辭書形「楽しいです」。"
                }
            ]
        },
        # Passage 3
        {
            "id": "n5-p-3",
            "title": "手紙「母への近況報告」",
            "genre": "家書・生活近況",
            "passage": (
                "お母さん、お元気ですか。東京は最近だんだん暖かく【 01 】。\n"
                "先週の週末、近所の公園へ桜を見に行きました。たくさんの人が花見をしていて、とてもにぎやかでした。\n"
                "大学の勉強は少し難しいですが、クラスメートがみんな親切【 02 】助かっています。\n"
                "来月は連休がありますから、一度国へ帰ろうと【 03 】。それでは、体に気をつけてください。"
            ),
            "translation": (
                "媽媽您好嗎？東京最近漸漸變溫暖了。\n"
                "上週末我去了附近公園看櫻花。許多人在賞花，非常熱鬧。\n"
                "大學功課有點難，但同學們都很親切，幫了我很多忙。\n"
                "下個月有連假，我想回國一趟。請保重身體。"
            ),
            "questions": [
                {
                    "blankNumber": 1,
                    "correct": "なりました",
                    "distractors": ["しました", "ありました", "きました"],
                    "explanation": "形容氣候自然的狀態演變，使用「暖かくなりました（變得暖和了）」「い形容詞去い＋くなる」。"
                },
                {
                    "blankNumber": 2,
                    "correct": "で",
                    "distractors": ["に", "な", "だ"],
                    "explanation": "な形容詞中頓並列連接後續動詞短語，使用詞幹＋で：「親切で助かっています（既親切又幫了大忙）」。"
                },
                {
                    "blankNumber": 3,
                    "correct": "思っています",
                    "distractors": ["考えています", "言っています", "聞いています"],
                    "explanation": "意志形＋と思っています為日語固定句型，表示說話者當前一段時間內的打算與意願。"
                }
            ]
        },
        # Passage 4
        {
            "id": "n5-p-4",
            "title": "週末の日記「家族みんなで餃子作り」",
            "genre": "家庭生活日記",
            "passage": (
                "昨日の日曜日は、朝から雨が降っていました。どこへも出かけることが【 01 】ので、家で家族と一緒に餃子を作りました。\n"
                "父が野菜とお肉を細かく切って、母が味付けをしました。私は弟と一緒に皮で具を【 02 】包みました。形は少し下手でしたが、焼きたての餃子はとてもおいしかったです。\n"
                "またみんなで一緒に料理を【 03 】と思います。"
            ),
            "translation": (
                "昨天的週日從早上就一直下雨。因為哪裡都無法去，所以在家人一起包餃子。\n"
                "父親把蔬菜和肉切碎，母親調味。我和弟弟一起把餡料包進皮裡。雖然形狀有點醜，但現煎出爐的餃子非常好吃。\n"
                "我想之後大家再一起做菜！"
            ),
            "questions": [
                {
                    "blankNumber": 1,
                    "correct": "できなかった",
                    "distractors": ["できない", "できた", "できる"],
                    "explanation": "「昨日は」為過去時間，全面否定「どこへも出かけることが」搭配過去可能否定「できなかった（無法出門）」。"
                },
                {
                    "blankNumber": 2,
                    "correct": "上手に",
                    "distractors": ["上手な", "上手で", "上手だ"],
                    "explanation": "修飾後續的包餃子動作「包みました」，需使用な形容詞副詞形「上手に」。"
                },
                {
                    "blankNumber": 3,
                    "correct": "作りたい",
                    "distractors": ["作る", "作って", "作った"],
                    "explanation": "第一人稱表達未來的願望想法「〜たいと思います」，填入願望形「作りたい」。"
                }
            ]
        },
        # Passage 5
        {
            "id": "n5-p-5",
            "title": "買い物メモ「近所のスーパーで晩ご飯の買い物」",
            "genre": "日常生活購物",
            "passage": (
                "今日の午後は、晩ご飯の材料を買いに近所のスーパーへ行きました。このスーパーは野菜や魚がとても新鮮【 01 】、値段も安いです。\n"
                "今晩はカレーを作るつもりです。牛肉と玉ねぎとじゃがいもを買いました。【 02 】、デザートに甘いりんごも二つ買いました。\n"
                "レジでお金を払う【 03 】、店員さんが「ポイントカードはありますか」と聞きました。ポイントカードを出して、気分よく買い物をして帰りました。"
            ),
            "translation": (
                "今天下午我去附近的超市買晚餐的食材。這家超市的蔬菜和魚既新鮮又便宜。\n"
                "今晚打算煮咖哩。我買了牛肉、洋蔥和馬鈴薯。接著，還買了兩個甜蘋果當作甜點。\n"
                "在櫃台結帳時，店員問我「請問有集點卡嗎？」。我拿出集點卡，心情愉快地買完東西回家了。"
            ),
            "questions": [
                {
                    "blankNumber": 1,
                    "correct": "で",
                    "distractors": ["に", "な", "だ"],
                    "explanation": "な形容詞「新鮮」中頓形為詞幹＋で：「新鮮で、値段も安いです（既新鮮又便宜）」。"
                },
                {
                    "blankNumber": 2,
                    "correct": "それから",
                    "distractors": ["しかし", "ですから", "ですが"],
                    "explanation": "買好咖哩材料之後，接續詞「それから（接著、還有）」用於順接追加購買甜點蘋果。"
                },
                {
                    "blankNumber": 3,
                    "correct": "とき",
                    "distractors": ["まえ", "あと", "あいだ"],
                    "explanation": "「動詞辭書形＋とき」表示「在...的時候」。「払うとき」表示在結帳付款當下。"
                }
            ]
        },
        # Passage 6
        {
            "id": "n5-p-6",
            "title": "留学生リーさんの作文「大好きな日本の春と桜」",
            "genre": "季節與文化隨筆",
            "passage": (
                "日本に来てから、半年がたちました。日本の四季の中で、私は春が一番【 01 】です。\n"
                "春になると、町中にきれいな桜の花が咲きます。先週の日曜日、友達と一緒に上野公園へ行きました。たくさんの人が桜の木の下でご飯を【 02 】、写真を撮ったりしていました。\n"
                "満開の桜を見て、とても感動しました。国にいる家族にも、このきれいな桜の写真を送って【 03 】です。"
            ),
            "translation": (
                "來到日本之後，已經過了半年。在日本的四季之中，我最喜歡春天。\n"
                "一到春天，整座城鎮都開滿了美麗的櫻花。上週日我和朋友去了上野公園。好多人在櫻花樹下吃便當、拍照。\n"
                "看著盛開的櫻花，我非常感動。我也想寄這美麗櫻花的照片給在母國的家人！"
            ),
            "questions": [
                {
                    "blankNumber": 1,
                    "correct": "好き",
                    "distractors": ["好きな", "好きで", "好きだ"],
                    "explanation": "最高級比較句型「〜が一番好きです」。「好き」為な形容詞詞幹，直接接「です」。"
                },
                {
                    "blankNumber": 2,
                    "correct": "食べたり",
                    "distractors": ["食べて", "食べた", "食べる"],
                    "explanation": "與後文的「撮ったりしていました」呼應，動作列舉句型為「〜たり〜たりする」，選「食べたり」。"
                },
                {
                    "blankNumber": 3,
                    "correct": "あげたい",
                    "distractors": ["くれたい", "もらいたい", "やりたい"],
                    "explanation": "說話者表示想為母國家人做某事的善意，使用授受句型「〜てあげたい（想寄給他們）」。"
                }
            ]
        },
        # Passage 7
        {
            "id": "n5-p-7",
            "title": "メール「ケンさんへのお誘い（動物園へ行こう）」",
            "genre": "朋友交流郵件",
            "passage": (
                "ケンさん、こんにちは。毎日寒いですが、風邪を【 01 】いませんか。\n"
                "さて、今週の土曜日に上野動物園へパンダを見に行きませんか。新しい赤ちゃんパンダが生まれて、今とても人気があるそうです。\n"
                "土曜日の朝10時に、上野駅の公園口の改札で【 02 】ましょう。もし都合が悪かったら、遠慮しないで【 03 】ください。お返事を待っています。"
            ),
            "translation": (
                "健同學，你好。每天雖然很冷，但你沒有感冒吧？\n"
                "話說，這週六要不要一起去上野動物園看熊貓？聽說新生了熊貓寶寶，現在非常受歡迎。\n"
                "我們週六早上10點在上野站公園口的剪票口碰面吧。如果時間不方便的話，請別客氣告訴我。等待你的回信！"
            ),
            "questions": [
                {
                    "blankNumber": 1,
                    "correct": "引いて",
                    "distractors": ["引いた", "引く", "引き"],
                    "explanation": "持續狀態「風邪を引いていませんか（有感冒嗎？）」，使用動詞て形（引いて）。"
                },
                {
                    "blankNumber": 2,
                    "correct": "会い",
                    "distractors": ["会って", "会う", "会った"],
                    "explanation": "提議共同碰面行動句型「動詞ます形去ます＋ましょう」。「会う」去ます為「会い」。"
                },
                {
                    "blankNumber": 3,
                    "correct": "言って",
                    "distractors": ["言う", "言わないで", "言った"],
                    "explanation": "請求句型「動詞て形＋ください」。「言ってください」表示「請告訴我、請說」。"
                }
            ]
        },
        # Passage 8
        {
            "id": "n5-p-8",
            "title": "アルバイト体験記「大学近くのコンビニでの仕事」",
            "genre": "工作與生活體驗",
            "passage": (
                "私は先月から、大学の近くのコンビニでアルバイトを【 01 】。\n"
                "仕事はレジでお金を計算したり、商品を棚に並べたりすることです。初めは日本語で接客するのが少し怖かったですが、店長が親切に【 02 】くれました。\n"
                "今はお客さんに「いらっしゃいませ」や「ありがとうございました」と大きな声で言うことができます。これからも一生懸命【 03 】と思います。"
            ),
            "translation": (
                "我從上個月開始在大學附近的便利商店打工。\n"
                "工作內容是在櫃台結帳，以及把商品擺到貨架上。起初用日語接待客人有點害怕，但店長很親切地指導了我。\n"
                "現在我已經能夠大聲對客人說「歡迎光臨」和「非常感謝」。今後我也想繼續全力以赴！"
            ),
            "questions": [
                {
                    "blankNumber": 1,
                    "correct": "始めました",
                    "distractors": ["始まります", "始めて", "始まる"],
                    "explanation": "「先月から」表示上個月已發生的動作，主動開始打工使用他動詞過去式「始めました」。"
                },
                {
                    "blankNumber": 2,
                    "correct": "教えて",
                    "distractors": ["教える", "教え", "教えた"],
                    "explanation": "他人為我方提供指導的授受表達「動詞て形＋くれました」，使用「教えてくれました」。"
                },
                {
                    "blankNumber": 3,
                    "correct": "頑張りたい",
                    "distractors": ["頑張る", "頑張って", "頑張った"],
                    "explanation": "第一人稱表達今後決心與想法「〜たいと思います」，填入願望形「頑張りたい」。"
                }
            ]
        },
        # Passage 9
        {
            "id": "n5-p-9",
            "title": "初めての体験「ひとりで地下鉄に乗った日」",
            "genre": "生活記事・交通體驗",
            "passage": (
                "日本に来たばかりの時、私はひとりで東京の地下鉄に【 01 】行きました。東京の駅はとても広くて、線がたくさんあって驚きました。\n"
                "切符の買い方が分からなかったので、駅員さんに【 02 】みました。駅員さんは自動券売機の使い方を丁寧に教えてくれました。\n"
                "無事に目的地に着くことができて、とても安心しました。自分ひとりで地下鉄に乗ることが【 03 】、少し自信がつきました。"
            ),
            "translation": (
                "剛來日本的時候，我一個人搭乘東京的地下鐵出門。東京的車站非常大，線路繁多，令我非常驚訝。\n"
                "因為不知道怎麼買票，所以我試著問了站務員。站務員非常親切地教我如何使用自動售票機。\n"
                "最後平安到達了目的地，非常安心。自己能夠一個人搭乘地下鐵，也讓我增添了一點自信！"
            ),
            "questions": [
                {
                    "blankNumber": 1,
                    "correct": "乗って",
                    "distractors": ["乗る", "乗り", "乗った"],
                    "explanation": "搭乘地下鐵前往，前後動作相繼「動詞て形＋行く」：「乗って行きました」。"
                },
                {
                    "blankNumber": 2,
                    "correct": "聞いて",
                    "distractors": ["聞く", "聞き", "聞いた"],
                    "explanation": "嘗試進行某動作「動詞て形＋みる」。「聞く」的て形為「聞いてみました（試著詢問）」。"
                },
                {
                    "blankNumber": 3,
                    "correct": "できて",
                    "distractors": ["できる", "できた", "でき"],
                    "explanation": "表示「成功做到了這件事」並作為中頓連接後續心境，使用可能動詞て形「できて」。"
                }
            ]
        },
        # Passage 10
        {
            "id": "n5-p-10",
            "title": "年末の日記「日本のお正月と大掃除の準備」",
            "genre": "節日文化與年末日記",
            "passage": (
                "もうすぐ12月が終わります。日本では年末になると、家の中をきれいに掃除【 01 】習慣があります。\n"
                "今日は朝から自分の部屋を大掃除しました。机の上やベッドの下を掃除して、いらない服や古い雑誌を【 02 】。\n"
                "部屋がとてもきれいになって、気持ちがすっきりしました。明日は友達と一緒に年越しそばを【 03 】予定です。よい新年を迎えたいです。"
            ),
            "translation": (
                "12月馬上就要結束了。在日本一到年末，就有把家裡打掃得乾乾淨淨的習慣。\n"
                "今天從早上就開始大掃除自己的房間。打掃了桌面上和床底下，把不需要的衣服和舊雜誌扔掉了。\n"
                "房間變得非常乾淨，心情十分舒暢。明天預計和朋友一起吃跨年蕎麥麵。希望能迎接美好的一年！"
            ),
            "questions": [
                {
                    "blankNumber": 1,
                    "correct": "する",
                    "distractors": ["して", "した", "します"],
                    "explanation": "修飾名詞「習慣」需使用動詞連體形（辭書形）：「掃除する習慣（打掃的習慣）」。"
                },
                {
                    "blankNumber": 2,
                    "correct": "捨てました",
                    "distractors": ["捨てて", "捨てる", "捨てます"],
                    "explanation": "今天早上完成的大掃除過去動作，句尾丁寧過去形為「捨てました（扔掉了）」。"
                },
                {
                    "blankNumber": 3,
                    "correct": "食べる",
                    "distractors": ["食べて", "食べた", "食べます"],
                    "explanation": "計劃預定句型「動詞辭書形＋予定です」。「食べる予定です」表示「打算吃、預計吃」。"
                }
            ]
        }
    ]

    assert len(raw_passages) == 10, f"Expected 10 passages, got {len(raw_passages)}"

    passages = []
    global_q_counter = 0

    for p in raw_passages:
        pid = p["id"]
        title = p["title"]
        genre = p["genre"]
        passage_text = p["passage"]
        translation = p["translation"]
        raw_qs = p["questions"]
        assert len(raw_qs) == 3, f"Passage {pid} does not have 3 questions"

        processed_qs = []
        for q in raw_qs:
            blank_num = q["blankNumber"]
            correct_opt = q["correct"]
            distractors = q["distractors"]
            assert len(distractors) == 3, f"Distractors not 3 in {pid} blank {blank_num}"
            assert correct_opt not in distractors, f"Duplicate option in {pid} blank {blank_num}"

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
    ps = get_passage_quizzes()
    print(f"Generated {len(ps)} passages with {sum(len(p['questions']) for p in ps)} subquestions.")
    counts = {}
    for p in ps:
        for q in p['questions']:
            counts[q['correctIndex']] = counts.get(q['correctIndex'], 0) + 1
    print("Distribution of correctIndex:", counts)
