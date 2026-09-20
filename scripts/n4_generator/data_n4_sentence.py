# -*- coding: utf-8 -*-
"""
120 JLPT N4 Sentence Grammar Quizzes (n4-s-1 to n4-s-120)
"""

RAW_SENTENCE_QUIZZES = [
    # 1-12: 授受動詞與請託
    {
        "id": "n4-s-1",
        "question": "熱が　あるので、今日は　早く　帰って（　　）いいですか。",
        "correct": "も",
        "distractors": ["は", "で", "に"],
        "explanation": "「動詞て形＋もいいですか」表示請求許可（可以...嗎？）。",
        "targetGrammar": "許可「〜てもいいですか」"
    },
    {
        "id": "n4-s-2",
        "question": "すみませんが、この言葉の読み方を教えて（　　）いただけませんか。",
        "correct": "（無）",
        "distractors": ["くださって", "て", "くださり"],
        "explanation": "禮貌請求句型「動詞て形＋いただけませんか」。「教えて」已是て形，後方直接接「いただけませんか」。",
        "targetGrammar": "客氣請求「〜ていただけませんか」"
    },
    {
        "id": "n4-s-3",
        "question": "弟の誕生日に　新しい自転車を　買って（　　）。",
        "correct": "あげた",
        "distractors": ["もらった", "くれた", "いただいた"],
        "explanation": "「〜てあげる」表示說話者為他人（弟弟）做某事，給予恩惠。",
        "targetGrammar": "授受「〜てあげる」"
    },
    {
        "id": "n4-s-4",
        "question": "荷物が重かったので、親切な駅員さんに　手伝って（　　）。",
        "correct": "もらった",
        "distractors": ["あげた", "くれた", "やった"],
        "explanation": "「〜に…てもらう」表示請某人為自己做某事或蒙受他人幫助（駅員さんに手伝ってもらった）。",
        "targetGrammar": "授受「〜てもらう」"
    },
    {
        "id": "n4-s-5",
        "question": "急に雨が降ってきたとき、見知らぬ人が　傘を　貸して（　　）。",
        "correct": "くれました",
        "distractors": ["あげました", "もらいました", "やりました"],
        "explanation": "他人為主語且為我做某事時，恩惠流向自己，動詞使用「〜てくれる」。",
        "targetGrammar": "授受「〜てくれる」"
    },
    {
        "id": "n4-s-6",
        "question": "先生が　私の日本語の作文を　直して（　　）。",
        "correct": "くださいました",
        "distractors": ["さしあげました", "いただきました", "あげました"],
        "explanation": "長輩尊長（先生）為我做某事時，動詞「くれる」的尊敬語為「くださる」。",
        "targetGrammar": "敬語授受「〜てくださる」"
    },
    {
        "id": "n4-s-7",
        "question": "部長に　日本の伝統文化について　詳しく　教えて（　　）。",
        "correct": "いただきました",
        "distractors": ["さしあげました", "やりました", "あげました"],
        "explanation": "「尊長に…ていただく」為「てもらう」的謙讓表現，表示從尊長處獲益或承蒙指教。",
        "targetGrammar": "敬語授受「〜ていただく」"
    },
    {
        "id": "n4-s-8",
        "question": "重そうですね。先生のお荷物を　職員室まで　お持ち（　　）。",
        "correct": "しましょう",
        "distractors": ["になりましょう", "なさいましょう", "いただきましょう"],
        "explanation": "自謙句型「お＋動詞ます形去ます＋する」：「お持ちしましょう」表示由我替老師拿行李。",
        "targetGrammar": "自謙語「お〜する」"
    },
    {
        "id": "n4-s-9",
        "question": "すみませんが、もう少し　ゆっくり　話して（　　）ませんか。",
        "correct": "ください",
        "distractors": ["くださり", "くださら", "くださる"],
        "explanation": "「動詞て形＋くださいませんか」為向對方提出客氣請求的常用句型。",
        "targetGrammar": "客氣請託「〜てくださいませんか」"
    },
    {
        "id": "n4-s-10",
        "question": "田中君、この辞書を　ちょっと　貸して（　　）ない？",
        "correct": "もらえ",
        "distractors": ["あげ", "やら", "さしあげ"],
        "explanation": "平輩日常對話請託「〜てもらえない？」（能否借我一下？），為「てもらう」之可能形否定疑問句。",
        "targetGrammar": "口語請託「〜てもらえない」"
    },
    {
        "id": "n4-s-11",
        "question": "部屋が暑いので、窓を　開けて（　　）ない？",
        "correct": "くれ",
        "distractors": ["もらい", "あげ", "やり"],
        "explanation": "平輩親近請求「動詞て形＋くれない？」（能幫我開個窗嗎？）。",
        "targetGrammar": "日常請求「〜てくれない」"
    },
    {
        "id": "n4-s-12",
        "question": "道に迷って困ったので、交番の警察官（　　）道を尋ねました。",
        "correct": "に",
        "distractors": ["を", "で", "が"],
        "explanation": "向人詢問或打聽時，對象助詞使用「に」（人に尋ねる）。",
        "targetGrammar": "助詞用法「人に尋ねる」"
    },

    # 13-24: 條件形與假定
    {
        "id": "n4-s-13",
        "question": "この薬を　（　　）ば、熱は　すぐに　下がりますよ。",
        "correct": "飲め",
        "distractors": ["飲む", "飲んだ", "飲もう"],
        "explanation": "五段動詞假定形（ば形）：詞尾「u」段改「e」段加「ば」（飲む ➔ 飲めば）。",
        "targetGrammar": "假定「〜ば」"
    },
    {
        "id": "n4-s-14",
        "question": "値段が　安く（　　）ば、この新しいパソコンを　買いたいです。",
        "correct": "なけれ",
        "distractors": ["ない", "なくて", "なさ"],
        "explanation": "否定形容詞ない的ば形變化為「なけれ＋ば」（安くなければ＝如果不便宜的話；若便宜則為安ければ）。",
        "targetGrammar": "否定假定「〜なければ」"
    },
    {
        "id": "n4-s-15",
        "question": "春に　（　　）たら、公園の桜を見に行きましょう。",
        "correct": "なっ",
        "distractors": ["なる", "なり", "なれ"],
        "explanation": "「〜たら」接在動詞た形後面：なる ➔ なった ➔ なったら（到了春天）。",
        "targetGrammar": "確定條件「〜たら」"
    },
    {
        "id": "n4-s-16",
        "question": "家に　帰っ（　　）、まず　うがいと手洗いをします。",
        "correct": "たら",
        "distractors": ["なら", "ば", "と"],
        "explanation": "前項動作完成後接著進行後項意志動作，四條件中以「〜たら」最自然合適（帰ったら）。",
        "targetGrammar": "接續條件「〜たら」"
    },
    {
        "id": "n4-s-17",
        "question": "駅に　着い（　　）、定期券を　家に忘れたことに気がつきました。",
        "correct": "たら",
        "distractors": ["ば", "なら", "ても"],
        "explanation": "「動詞た形＋ら」可表示動作完成後「意外發現」新狀況（到了車站才發現忘了定期票）。",
        "targetGrammar": "發現「〜たら」"
    },
    {
        "id": "n4-s-18",
        "question": "この交差点を　左へ　曲がる（　　）、右側に大きな銀行があります。",
        "correct": "と",
        "distractors": ["ば", "たら", "なら"],
        "explanation": "道案内（路線指引）的必然結果使用「動詞辭書形＋と」（一轉過去就會看到）。",
        "targetGrammar": "恆常必然「〜と」"
    },
    {
        "id": "n4-s-19",
        "question": "この赤いボタンを　押す（　　）、切符とおつりが出ます。",
        "correct": "と",
        "distractors": ["たら", "なら", "ば"],
        "explanation": "機械操作的自然必然結果句型為「辭書形＋と」（押すと）。",
        "targetGrammar": "機械操作「〜と」"
    },
    {
        "id": "n4-s-20",
        "question": "おいしい寿司を　食べる（　　）、駅前の店がおすすめですよ。",
        "correct": "なら",
        "distractors": ["と", "ば", "たら"],
        "explanation": "話題承接假定「〜なら」（如果要吃美味壽司的話，推薦站前那家）。",
        "targetGrammar": "話題承接「〜なら」"
    },
    {
        "id": "n4-s-21",
        "question": "雨が　降っ（　　）、明日の運動会は予定通り行われます。",
        "correct": "ても",
        "distractors": ["たら", "れば", "なら"],
        "explanation": "逆接假定條件「動詞て形＋も」（即使下雨，運動會也照常舉行）。",
        "targetGrammar": "逆接條件「〜ても」"
    },
    {
        "id": "n4-s-22",
        "question": "いくら　（　　）ても、途中で諦めてはいけません。",
        "correct": "大変で",
        "distractors": ["大変だっ", "大変", "大変な"],
        "explanation": "な形容詞的て形為「語幹＋で」：大変 ➔ 大変で ➔ いくら大変でも（無論多辛苦）。",
        "targetGrammar": "讓步「いくら〜ても」"
    },
    {
        "id": "n4-s-23",
        "question": "少し熱があるようですね。今日は早く帰って休ん（　　）どうですか。",
        "correct": "だら",
        "distractors": ["でば", "だなら", "だと"],
        "explanation": "委婉建議「動詞た形＋らどうですか」：休む ➔ 休んだ ➔ 休んだらどうですか。",
        "targetGrammar": "建議「〜たらどうですか」"
    },
    {
        "id": "n4-s-24",
        "question": "こんなに難しいなら、もっと早く先生に質問すれ（　　）よかったです。",
        "correct": "ば",
        "distractors": ["たら", "なら", "と"],
        "explanation": "「動詞ば形＋よかった」表示對過去行為的懊悔（早知道早點請教老師就好了）。",
        "targetGrammar": "後悔「〜ばよかった」"
    },

    # 25-39: 受身・使役・使役受身
    {
        "id": "n4-s-25",
        "question": "昨日のスピーチ大会で、校長先生に　（　　）とても嬉しかったです。",
        "correct": "褒められて",
        "distractors": ["褒めて", "褒めさせて", "褒めさせられて"],
        "explanation": "二類動詞「褒める」之被動形為「褒められる」（被校長稱讚）。",
        "targetGrammar": "直接受身「〜られる」"
    },
    {
        "id": "n4-s-26",
        "question": "混雑したバスの中で、見知らぬ人に　足を　（　　）痛かったです。",
        "correct": "踏まれて",
        "distractors": ["踏まされて", "踏ませて", "踏んで"],
        "explanation": "所有物受身（持ち主の受身）：人に＋足を＋踏まれる（被別人踩到腳）。",
        "targetGrammar": "所有物受身「〜を…られる」"
    },
    {
        "id": "n4-s-27",
        "question": "傘を持たずに出かけたら、途中で雨に（　　）風邪をひいてしまいました。",
        "correct": "降られて",
        "distractors": ["降らせて", "降らされて", "降って"],
        "explanation": "迷惑受身（間接受害被動）：「雨に降られる」（被雨淋了而深受其害）。",
        "targetGrammar": "迷惑受身「雨に降られる」"
    },
    {
        "id": "n4-s-28",
        "question": "この歴史ある建物は、今から約300年前に　（　　）。",
        "correct": "建てられました",
        "distractors": ["建てさせました", "建てました", "建てさせられました"],
        "explanation": "無生物主語（建築物等）通常以被動語態表示建造：建てる ➔ 建てられる（建てられました）。",
        "targetGrammar": "無生物受身「〜られる」"
    },
    {
        "id": "n4-s-29",
        "question": "「坊っちゃん」は夏目漱石（　　）書かれた有名な小説です。",
        "correct": "によって",
        "distractors": ["について", "にとって", "に対して"],
        "explanation": "無生物受身中，表示創作、發明、建造之主體通常使用「〜によって」（由夏目漱石所撰寫）。",
        "targetGrammar": "受身作者「〜によって」"
    },
    {
        "id": "n4-s-30",
        "question": "先生は　明日の懇親会に　（　　）ますか。",
        "correct": "来られ",
        "distractors": ["来させ", "来させられ", "参られ"],
        "explanation": "動詞受身形可用於表達對尊長的敬意（尊敬受身）：来る ➔ 来られる（先生會前來嗎？）。",
        "targetGrammar": "尊敬受身「〜られる」"
    },
    {
        "id": "n4-s-31",
        "question": "お母さんは　子供に　毎日ニンジンを　（　　）。",
        "correct": "食べさせました",
        "distractors": ["食べられました", "食べさせられました", "食べました"],
        "explanation": "使役形（讓/叫某人做）：二類動詞食べる ➔ 食べさせる（叫孩子吃胡蘿蔔）。",
        "targetGrammar": "使役「〜させる」"
    },
    {
        "id": "n4-s-32",
        "question": "先生は　グラウンドで　生徒たちを　1キロ　（　　）。",
        "correct": "走らせた",
        "distractors": ["走られた", "走らさせた", "走った"],
        "explanation": "一類動詞「走る」的使役形為詞尾改「a」加「せる」：走る ➔ 走らせる（讓學生跑了1公里）。",
        "targetGrammar": "使役「〜せる」"
    },
    {
        "id": "n4-s-33",
        "question": "連絡もせずに夜遅くまで遊び、両親を　（　　）しまいました。",
        "correct": "心配させて",
        "distractors": ["心配して", "心配されて", "心配させられて"],
        "explanation": "感情誘發使役：「〜を心配させる」（讓父母擔憂焦急了）。",
        "targetGrammar": "感情使役「〜を…させる」"
    },
    {
        "id": "n4-s-34",
        "question": "体調がすぐれませんので、今日は早く　（　　）てください。",
        "correct": "帰らせ",
        "distractors": ["帰られ", "帰らされ", "帰り"],
        "explanation": "「動詞使役て形＋ください」（請讓我...）：帰る ➔ 帰らせてください（請准許我早退）。",
        "targetGrammar": "許可使役「〜させてください」"
    },
    {
        "id": "n4-s-35",
        "question": "新入社員の紹介を　（　　）いただきます。",
        "correct": "させて",
        "distractors": ["されて", "させられて", "して"],
        "explanation": "自謙表達「動詞使役て形＋いただきます」：する ➔ させていただきます（容我向大家介紹）。",
        "targetGrammar": "自謙表現「〜させていただきます」"
    },
    {
        "id": "n4-s-36",
        "question": "友達が約束の時間に大幅に遅れ、雨の中で1時間も　（　　）。",
        "correct": "待たされた",
        "distractors": ["待たせた", "待たせられた", "待たれた"],
        "explanation": "一類動詞使役受身縮約形：待つ ➔ 待たせる ➔ 待たされる（被迫苦等了1小時）。",
        "targetGrammar": "使役受身「〜される」"
    },
    {
        "id": "n4-s-37",
        "question": "子供の頃、嫌いな野菜を　無理やり　（　　）泣いたことがあります。",
        "correct": "食べさせられて",
        "distractors": ["食べさせて", "食べられて", "食べて"],
        "explanation": "二類動詞使役受身形：食べる ➔ 食べさせる ➔ 食べさせられる（被迫吃討厭的蔬菜）。",
        "targetGrammar": "使役受身「〜させられる」"
    },
    {
        "id": "n4-s-38",
        "question": "急なトラブルで、昨日は終電まで　（　　）。",
        "correct": "残業させられました",
        "distractors": ["残業されました", "残業させました", "残業いたしました"],
        "explanation": "三類動詞使役受身形：残業する ➔ 残業させられる（被迫加班到末班車）。",
        "targetGrammar": "使役受身「〜させられる」"
    },
    {
        "id": "n4-s-39",
        "question": "兄の買い物に半日も　（　　）、足が棒のようになりました。",
        "correct": "付き合わされて",
        "distractors": ["付き合わせて", "付き合われて", "付き合って"],
        "explanation": "一類動詞使役受身：付き合う ➔ 付き合わされる（被迫陪哥哥逛街買東西）。",
        "targetGrammar": "使役受身「〜わされる」"
    },

    # 40-53: 樣態・傳聞・推量・比喻
    {
        "id": "n4-s-40",
        "question": "空が真っ暗になってきました。今にも雨が　（　　）そうですね。",
        "correct": "降り",
        "distractors": ["降る", "降った", "降って"],
        "explanation": "動詞ます形去ます＋そう表示樣態推測（看起來快要下雨了）：降る ➔ 降り ➔ 降りそう。",
        "targetGrammar": "樣態「〜そう」"
    },
    {
        "id": "n4-s-41",
        "question": "ショーケースに並んでいるケーキは、どれも　とても　（　　）そうでした。",
        "correct": "美味し",
        "distractors": ["美味しい", "美味しく", "美味しさ"],
        "explanation": "い形容詞去掉「い」加「そう」表示外觀樣態：美味しい ➔ 美味しそう（看起來很美味）。",
        "targetGrammar": "樣態「〜そう」"
    },
    {
        "id": "n4-s-42",
        "question": "この映画は　評判が　とても　（　　）そうですね。ぜひ見に行きましょう。",
        "correct": "よさ",
        "distractors": ["いい", "よく", "いいさ"],
        "explanation": "「いい」的樣態推量為特殊變化「よさそう」（看起來很棒）。",
        "targetGrammar": "樣態特殊「よさそう」"
    },
    {
        "id": "n4-s-43",
        "question": "渋滞がひどいので、開演時間には　間に合い（　　）そうにありません。",
        "correct": "（無）",
        "distractors": ["る", "た", "て"],
        "explanation": "動詞樣態否定「動詞ます形去ます＋そうにない」：間に合い＋そうにありません（看來趕不上了）。",
        "targetGrammar": "樣態否定「〜そうにない」"
    },
    {
        "id": "n4-s-44",
        "question": "天気予報によると、明日は午後から激しい雨が　（　　）そうです。",
        "correct": "降る",
        "distractors": ["降り", "降った", "降ろう"],
        "explanation": "情報源（天気予報によると）接傳聞「動詞普通形＋そうです」：降るそうです（聽說會下雨）。",
        "targetGrammar": "傳聞「〜そうだ」"
    },
    {
        "id": "n4-s-45",
        "question": "噂では、山田先生の担当するテストは　とても　（　　）そうです。",
        "correct": "大変だ",
        "distractors": ["大変", "大変で", "大変な"],
        "explanation": "な形容詞接傳聞「〜そうです」時需保留「だ」：語幹＋だそうです（大変だそうです）。",
        "targetGrammar": "傳聞接續「な形＋だそう」"
    },
    {
        "id": "n4-s-46",
        "question": "赤ちゃんのほっぺたは柔らかく、まるで　マシュマロの（　　）です。",
        "correct": "よう",
        "distractors": ["そう", "らしい", "みたい"],
        "explanation": "「まるで＋名詞＋の＋ようだ」比喻句型（宛如棉花糖一般）。",
        "targetGrammar": "比喻「まるで〜のようだ」"
    },
    {
        "id": "n4-s-47",
        "question": "隣の部屋から楽しそうな声が聞こえます。パーティーを　している（　　）です。",
        "correct": "よう",
        "distractors": ["そう", "はず", "わけ"],
        "explanation": "透過現場所見所聞的感官線索推測客觀事態，使用「〜ようだ」（好像在辦派對）。",
        "targetGrammar": "觀察推量「〜ようだ」"
    },
    {
        "id": "n4-s-48",
        "question": "あの兄弟は、声も仕草も　父親（　　）そっくりです。",
        "correct": "みたいに",
        "distractors": ["そうに", "らしく", "ようにで"],
        "explanation": "口語比喻修飾用言：「名詞＋みたいに」（像父親一樣一模一樣）。",
        "targetGrammar": "比喻修飾「〜みたいに」"
    },
    {
        "id": "n4-s-49",
        "question": "3月中旬なのに、今日は真冬（　　）寒い一日でした。",
        "correct": "らしい",
        "distractors": ["そう", "みたい", "よう"],
        "explanation": "「名詞＋らしい」表示具備該名詞的典型本質特徵（像嚴冬一樣寒冷）。",
        "targetGrammar": "典型特徵「〜らしい」"
    },
    {
        "id": "n4-s-50",
        "question": "明日は祝日ですから、市役所の窓口は　休み（　　）でしょう。",
        "correct": "（無）",
        "distractors": ["な", "だ", "で"],
        "explanation": "名詞接推量助動詞「でしょう」時直接連接，無需加「だ」或「な」：休みでしょう。",
        "targetGrammar": "推量接續「名詞＋でしょう」"
    },
    {
        "id": "n4-s-51",
        "question": "道が混雑しているので、待ち合わせの時間に　少し（　　）かもしれません。",
        "correct": "遅れる",
        "distractors": ["遅れて", "遅れたり", "遅れ"],
        "explanation": "動詞普通形＋かもしれません（說不定會遲到）。",
        "targetGrammar": "推測「〜かもしれない」"
    },
    {
        "id": "n4-s-52",
        "question": "毎日欠かさず勉強しているのだから、田中さんは試験に　合格する（　　）です。",
        "correct": "はず",
        "distractors": ["わけ", "こと", "もの"],
        "explanation": "「動詞普通形＋はずです」表示有充分理由推斷某事理所當然會發生（理應合格）。",
        "targetGrammar": "推斷「〜はずだ」"
    },
    {
        "id": "n4-s-53",
        "question": "彼は今朝ハワイへ出発したのだから、今日本に　いる（　　）がありません。",
        "correct": "はず",
        "distractors": ["わけ", "つもり", "こと"],
        "explanation": "「〜はずがありません」表示強烈的否定推斷（絕不可能在日本）。",
        "targetGrammar": "否定推斷「〜はずがない」"
    },

    # 54-65: 目的・理由・逆接・並列
    {
        "id": "n4-s-54",
        "question": "将来自分の家を　建てる（　　）に、毎月貯金をしています。",
        "correct": "ため",
        "distractors": ["よう", "こと", "の"],
        "explanation": "意志動詞辭書形＋ために表示目的（為了建自己的房子）。前後主語同一。",
        "targetGrammar": "目的「〜ために」"
    },
    {
        "id": "n4-s-55",
        "question": "会場の後ろの席の人にも　よく　聞こえる（　　）に、大きな声で話してください。",
        "correct": "よう",
        "distractors": ["ため", "こと", "そう"],
        "explanation": "接可能動詞或非意志動詞時，表示實現某期望目標，必須用「〜ように」（為了聽得清）。",
        "targetGrammar": "目的「〜ように」"
    },
    {
        "id": "n4-s-56",
        "question": "大切な約束を　忘れない（　　）に、手帳にメモしておきました。",
        "correct": "よう",
        "distractors": ["ため", "こと", "はず"],
        "explanation": "否定形式表目的預防時，慣用「動詞ない形＋ように」（為了不忘記）。",
        "targetGrammar": "否定目的「〜ないように」"
    },
    {
        "id": "n4-s-57",
        "question": "このハサミは、厚いダンボールを　切る（　　）とても便利です。",
        "correct": "のに",
        "distractors": ["ために", "ように", "ので"],
        "explanation": "「動詞辭書形＋のに＋便利だ/役に立つ」表示在特定用途、目的上的評價（剪紙箱很好用）。",
        "targetGrammar": "用途評價「〜のに」"
    },
    {
        "id": "n4-s-58",
        "question": "新しいスマートフォンの使い方を　覚える（　　）一週間かかりました。",
        "correct": "のに",
        "distractors": ["ために", "ように", "ので"],
        "explanation": "達成某事所需之時間、金錢消耗接續「動詞辭書形＋のに」（花了整整一週）。",
        "targetGrammar": "時間花費「〜のに」"
    },
    {
        "id": "n4-s-59",
        "question": "急な用事が　できた（　　）で、今日の打ち合わせに参加できなくなりました。",
        "correct": "の",
        "distractors": ["こと", "もの", "よう"],
        "explanation": "「〜ので」表示客觀原因理由，動詞普通形接「ので」（題目已有「で」，故填「の」）。",
        "targetGrammar": "原因理由「〜ので」"
    },
    {
        "id": "n4-s-60",
        "question": "危ない（　　）、線路の内側には立ち入らないでください。",
        "correct": "から",
        "distractors": ["のに", "けど", "なら"],
        "explanation": "說明主觀警告之理由，接在形容詞後使用「から」（因為危險）。",
        "targetGrammar": "主觀理由「〜から」"
    },
    {
        "id": "n4-s-61",
        "question": "このレストランは、料理が美味しい（　　）、値段も安くていつも混んでいます。",
        "correct": "し",
        "distractors": ["て", "で", "と"],
        "explanation": "列舉複數同類理由：「〜し、〜し」（菜好吃，而且價格也便宜）。",
        "targetGrammar": "並列理由「〜し」"
    },
    {
        "id": "n4-s-62",
        "question": "何回も　丁寧に説明した（　　）、彼は全く理解してくれませんでした。",
        "correct": "のに",
        "distractors": ["ので", "から", "ため"],
        "explanation": "「普通形＋のに」表示與預期相反的逆接轉折，帶有不滿或遺憾語氣（明明解釋了好幾遍卻...）。",
        "targetGrammar": "逆接遺憾「〜のに」"
    },
    {
        "id": "n4-s-63",
        "question": "電車が　遅延した（　　）で、大切な会議に遅刻してしまいました。",
        "correct": "せい",
        "distractors": ["おかげ", "ため", "よう"],
        "explanation": "表示招致不良後果的消極原因：「〜せいで」（都是電車誤點害的）。",
        "targetGrammar": "負面因果「〜せいで」"
    },
    {
        "id": "n4-s-64",
        "question": "先輩が　親切に指導してくれた（　　）で、無事に仕事を覚えられました。",
        "correct": "おかげ",
        "distractors": ["せい", "ため", "よう"],
        "explanation": "表示託福、帶來積極好結果的原因：「〜おかげで」（多虧前輩耐心指導）。",
        "targetGrammar": "恩惠因果「〜おかげで」"
    },
    {
        "id": "n4-s-65",
        "question": "休日は　家で　本を　読ん（　　）、音楽を聴いたりしてのんびり過ごします。",
        "correct": "だり",
        "distractors": ["だら", "で", "し"],
        "explanation": "動作列舉「動詞た形＋り、動詞た形＋りする」：読む ➔ 読んだ ➔ 読んだり。",
        "targetGrammar": "動作列舉「〜たり〜たりする」"
    },

    # 66-76: 許可・禁止・義務・忠告
    {
        "id": "n4-s-66",
        "question": "図書館の中では、大きな声で　話して（　　）いけません。",
        "correct": "は",
        "distractors": ["も", "で", "に"],
        "explanation": "「動詞て形＋はいけません」為禁止句型（不得大聲說話）。",
        "targetGrammar": "禁止「〜てはいけない」"
    },
    {
        "id": "n4-s-67",
        "question": "明日は　祝日ですから、学校へ　（　　）もいいですよ。",
        "correct": "来なくて",
        "distractors": ["来ないで", "来ず", "来なしに"],
        "explanation": "「動詞ない形去い＋くてもいい」表示不必、不做也可以（不來也沒關係）。",
        "targetGrammar": "無須義務「〜なくてもいい」"
    },
    {
        "id": "n4-s-68",
        "question": "借りた本は、来週の月曜日までに　図書館へ　返さ（　　）なりません。",
        "correct": "なければ",
        "distractors": ["なくては", "ないでは", "ずには"],
        "explanation": "義務句型「動詞ない形去い＋なければなりません」（必須歸還）。",
        "targetGrammar": "義務「〜なければならない」"
    },
    {
        "id": "n4-s-69",
        "question": "健康のために、毎日野菜を　食べ（　　）いけませんよ。",
        "correct": "なくては",
        "distractors": ["ないで", "なければ", "ずには"],
        "explanation": "義務句型「動詞ない形去い＋なくてはいけません」（必須吃蔬菜）。常搭配いけない。",
        "targetGrammar": "義務「〜なくてはいけない」"
    },
    {
        "id": "n4-s-70",
        "question": "熱があるなら、無理をしないで　早く　（　　）ほうがいいですよ。",
        "correct": "休んだ",
        "distractors": ["休む", "休んで", "休みたい"],
        "explanation": "肯定忠告建議「動詞た形＋ほうがいい」（最好早點休息）。",
        "targetGrammar": "忠告「〜たほうがいい」"
    },
    {
        "id": "n4-s-71",
        "question": "夜遅くに　コーヒーを　（　　）ほうがいいですよ。眠れなくなります。",
        "correct": "飲まない",
        "distractors": ["飲んだ", "飲まなかった", "飲まず"],
        "explanation": "否定忠告「動詞ない形＋ほうがいい」（最好不要喝）。",
        "targetGrammar": "否定忠告「〜ないほうがいい」"
    },
    {
        "id": "n4-s-72",
        "question": "もうすぐご飯だから、テレビを消して手を洗い（　　）。",
        "correct": "なさい",
        "distractors": ["てください", "な", "なさいよ"],
        "explanation": "長輩對晚輩之柔性命令句型「動詞ます形去ます＋なさい」（去洗手）。",
        "targetGrammar": "柔性命令「〜なさい」"
    },
    {
        "id": "n4-s-73",
        "question": "「ペンキ塗りたて」と書いてあるから、壁に　（　　）な！",
        "correct": "触る",
        "distractors": ["触り", "触って", "触った"],
        "explanation": "動詞辭書形＋な為嚴格禁止形（觸るな＝不准碰！）。",
        "targetGrammar": "禁止形「〜な」"
    },
    {
        "id": "n4-s-74",
        "question": "発車のベルが鳴っているぞ！早く　（　　）！",
        "correct": "急げ",
        "distractors": ["急ぎ", "急ぐ", "急ごう"],
        "explanation": "一類五段動詞命令形：詞尾改「e」段音（急ぐ ➔ 急げ！）。",
        "targetGrammar": "命令形「急げ」"
    },
    {
        "id": "n4-s-75",
        "question": "テストの最中に　スマートフォンを　見（　　）だめです。",
        "correct": "ては",
        "distractors": ["たら", "ても", "て"],
        "explanation": "口語禁止句型「動詞て形＋はだめです」（不可看手機）。",
        "targetGrammar": "口語禁止「〜てはだめ」"
    },
    {
        "id": "n4-s-76",
        "question": "ここでは　タバコを　吸っ（　　）かまいませんか。",
        "correct": "ても",
        "distractors": ["ては", "たら", "てもで"],
        "explanation": "「動詞て形＋もかまいません（か）」表示許可（抽菸也無妨嗎？/可以抽菸嗎？）。",
        "targetGrammar": "許可「〜てもかまわない」"
    },

    # 77-88: て形相關表現
    {
        "id": "n4-s-77",
        "question": "教室のホワイトボードに、本日の連絡事項が　書いて（　　）。",
        "correct": "あります",
        "distractors": ["います", "おきます", "みます"],
        "explanation": "他動詞て形＋ある表示人為動作完成後結果狀態的存續（寫著通知事項）。",
        "targetGrammar": "存續態「〜てある」"
    },
    {
        "id": "n4-s-78",
        "question": "風が吹き込んできたと思ったら、窓が　（　　）いました。",
        "correct": "開いて",
        "distractors": ["開けて", "開けられて", "開かせて"],
        "explanation": "自動詞＋ている表示自然結果狀態的留存（窗戶開著）。",
        "targetGrammar": "自動詞結果狀態「〜ている」"
    },
    {
        "id": "n4-s-79",
        "question": "旅行へ行く前に、新幹線の切符を　予約し（　　）ました。",
        "correct": "ておき",
        "distractors": ["てしまい", "てあり", "てみ"],
        "explanation": "為了之後的活動預先處置：「動詞て形＋おく」（預先訂好了車票）。",
        "targetGrammar": "事先準備「〜ておく」"
    },
    {
        "id": "n4-s-80",
        "question": "部屋の空気を入れ替えたいので、窓を　開け（　　）おいてください。",
        "correct": "て",
        "distractors": ["で", "た", "る"],
        "explanation": "動詞て形＋おく表示使某狀態繼續保持（請讓窗戶開著）。",
        "targetGrammar": "保持狀態「〜ておく」"
    },
    {
        "id": "n4-s-81",
        "question": "お気に入りの小説を、面白くて一日で全部　読ん（　　）しまいました。",
        "correct": "で",
        "distractors": ["だ", "て", "に"],
        "explanation": "動詞て形＋しまう表示動作完全結束（讀完了）。読む ➔ 読んで。",
        "targetGrammar": "完了「〜てしまう」"
    },
    {
        "id": "n4-s-82",
        "question": "大切なパスポートを　電車の網棚に　置き（　　）ました。",
        "correct": "忘れてしまい",
        "distractors": ["忘れておき", "忘れてあり", "忘れてみ"],
        "explanation": "「動詞て形＋しまう」表示非刻意發生的遺憾後悔情事（不小心遺忘在車架上）。",
        "targetGrammar": "遺憾「〜てしまう」"
    },
    {
        "id": "n4-s-83",
        "question": "この日本の伝統的な着物を、一度　着（　　）みたいです。",
        "correct": "て",
        "distractors": ["た", "る", "ます"],
        "explanation": "動詞て形＋みる表示嘗試體驗（想試穿看看）。着る ➔ 着て。",
        "targetGrammar": "嘗試「〜てみる」"
    },
    {
        "id": "n4-s-84",
        "question": "夕方になり、子供たちが楽しそうに家に　帰っ（　　）いきました。",
        "correct": "て",
        "distractors": ["た", "たら", "で"],
        "explanation": "「動詞て形＋いく」表示動作由近處向遠處離去的移動趨向（走回去了）。",
        "targetGrammar": "移動趨向「〜ていく」"
    },
    {
        "id": "n4-s-85",
        "question": "空が曇ってきて、ポツポツと雨が　降っ（　　）きました。",
        "correct": "て",
        "distractors": ["で", "た", "たら"],
        "explanation": "「動詞て形＋くる」表示自然現象或新事態開始浮現（下起雨來了）。",
        "targetGrammar": "趨向出現「〜てくる」"
    },
    {
        "id": "n4-s-86",
        "question": "日本に留学していた頃、富士山に　登っ（　　）があります。",
        "correct": "たこと",
        "distractors": ["ること", "たとき", "るため"],
        "explanation": "過去經驗句型「動詞た形＋ことがある」（曾經爬過富士山）。",
        "targetGrammar": "經驗「〜たことがある」"
    },
    {
        "id": "n4-s-87",
        "question": "私は今までに一度も歌舞伎を　見（　　）ことがありません。",
        "correct": "た",
        "distractors": ["る", "ない", "て"],
        "explanation": "否定經驗句型「動詞た形＋ことがありません」（從未看過歌舞伎）。",
        "targetGrammar": "無經驗「〜たことがない」"
    },
    {
        "id": "n4-s-88",
        "question": "部屋の隅に、花瓶が　綺麗に　飾っ（　　）あります。",
        "correct": "て",
        "distractors": ["で", "た", "る"],
        "explanation": "他動詞て形＋ある：飾る ➔ 飾ってあります（裝飾擺設著花瓶）。",
        "targetGrammar": "存續態「〜てある」"
    },

    # 89-100: 變化・決定・意向・預定
    {
        "id": "n4-s-89",
        "question": "4月になって、気候がだんだん　暖かく（　　）なりました。",
        "correct": "（無）",
        "distractors": ["く", "に", "で"],
        "explanation": "い形容詞接「なる」時詞尾改「く」：暖かく＋なる。題目已有「暖かく」，故無需冗字。",
        "targetGrammar": "變化「〜くなる」"
    },
    {
        "id": "n4-s-90",
        "question": "毎日日本語を練習して、ニュースが少し聞き取れる（　　）なりました。",
        "correct": "ように",
        "distractors": ["ために", "ことに", "そうに"],
        "explanation": "可能動詞＋ようになる表示能力或狀態的新轉變（變得聽得懂了）。",
        "targetGrammar": "能力轉變「〜ようになる」"
    },
    {
        "id": "n4-s-91",
        "question": "年を取ってから、油っこい料理をあまり　（　　）なりました。",
        "correct": "食べなく",
        "distractors": ["食べる", "食べた", "食べない"],
        "explanation": "習慣的否定變化：動詞ない形去い＋なくなる（變得不太吃了）。",
        "targetGrammar": "否定轉變「〜なくなる」"
    },
    {
        "id": "n4-s-92",
        "question": "健康を維持するために、毎朝散歩を　する（　　）にしています。",
        "correct": "よう",
        "distractors": ["こと", "ため", "はず"],
        "explanation": "努力養成並維持某生活習慣：「動詞辭書形＋ようにしている」（盡量每天散步）。",
        "targetGrammar": "習慣養成「〜ようにする」"
    },
    {
        "id": "n4-s-93",
        "question": "夜遅くには甘いお菓子を　（　　）ようにしています。",
        "correct": "食べない",
        "distractors": ["食べる", "食べた", "食べよう"],
        "explanation": "努力避免某行為的習慣：「動詞ない形＋ようにしている」（盡量不吃）。",
        "targetGrammar": "習慣避免「〜ないようにする」"
    },
    {
        "id": "n4-s-94",
        "question": "今年こそ日本語能力試験N4に合格する（　　）に決めました。",
        "correct": "こと",
        "distractors": ["よう", "ため", "そう"],
        "explanation": "動詞名詞化做決定：「動詞辭書形＋ことに決める／ことにする」（下定決心）。",
        "targetGrammar": "個人決定「〜ことにする」"
    },
    {
        "id": "n4-s-95",
        "question": "私は毎晩寝る前に、必ず日記を　書く（　　）にしています。",
        "correct": "こと",
        "distractors": ["よう", "そう", "はず"],
        "explanation": "「動詞辭書形＋ことにしている」表示個人自行決定後持續奉行的行為規則（堅持每晚寫日記）。",
        "targetGrammar": "生活規則「〜ことにしている」"
    },
    {
        "id": "n4-s-96",
        "question": "会社の方針で、来期から新規事業を　担当する（　　）になりました。",
        "correct": "こと",
        "distractors": ["よう", "ため", "そう"],
        "explanation": "「動詞辭書形＋ことになる」表示外部組織決定或非由個人全權掌控的客觀結果（確定負責新專案）。",
        "targetGrammar": "客觀決定「〜ことになる」"
    },
    {
        "id": "n4-s-97",
        "question": "今週末は図書館へ行って、試験の勉強を　（　　）と思っています。",
        "correct": "しよう",
        "distractors": ["する", "した", "すれば"],
        "explanation": "三類動詞する之意向形為「しよう」。「意向形＋と思っている」（打算去讀書）。",
        "targetGrammar": "意向打算「〜ようと思う」"
    },
    {
        "id": "n4-s-98",
        "question": "エレベーターのドアが　（　　）とした時、誰かが走ってきました。",
        "correct": "閉まろう",
        "distractors": ["閉まる", "閉まって", "閉まれば"],
        "explanation": "「動詞意向形＋とする」表示某動作即將發生的瞬間（電梯門正要關上的時候）。",
        "targetGrammar": "即將動作「〜ようとする」"
    },
    {
        "id": "n4-s-99",
        "question": "大学を卒業したら、父の会社を　手伝う（　　）です。",
        "correct": "つもり",
        "distractors": ["予定", "はず", "こと"],
        "explanation": "「動詞辭書形＋つもりです」表示個人堅定的意志打算（打算幫父親的忙）。",
        "targetGrammar": "意圖打算「〜つもりだ」"
    },
    {
        "id": "n4-s-100",
        "question": "明日の午前中は、海外からのお客様を　案内する（　　）になっています。",
        "correct": "予定",
        "distractors": ["つもり", "はず", "わけ"],
        "explanation": "「〜予定になっている」表示排定的既定公務行程（預定接待引導貴賓）。",
        "targetGrammar": "既定時程「〜予定だ」"
    },

    # 101-110: 敬語（尊敬・謙讓・丁寧）
    {
        "id": "n4-s-101",
        "question": "先生は　先ほど職員室へ　お戻り（　　）ました。",
        "correct": "になり",
        "distractors": ["し", "いただき", "さしあげ"],
        "explanation": "尊敬語句型「お＋動詞ます形去ます＋になる」：お戻りになりました（老師回去了）。",
        "targetGrammar": "尊敬語「お〜になる」"
    },
    {
        "id": "n4-s-102",
        "question": "社長は　ただいま外出（　　）おります。",
        "correct": "されて",
        "distractors": ["いたして", "なられて", "させて"],
        "explanation": "尊敬表達：「する」之尊敬形「される」（社長現在外出中）。",
        "targetGrammar": "尊敬語「される」"
    },
    {
        "id": "n4-s-103",
        "question": "先生は　今　どちらに　（　　）ますか。",
        "correct": "いらっしゃい",
        "distractors": ["まいり", "いただき", "存じ"],
        "explanation": "動詞「いる／来る／行く」之特殊尊敬語為「いらっしゃる」（老師人在何處？）。",
        "targetGrammar": "特殊尊敬「いらっしゃる」"
    },
    {
        "id": "n4-s-104",
        "question": "校長先生が　朝礼で　そう　（　　）ました。",
        "correct": "おっしゃい",
        "distractors": ["申し", "伺い", "いたし"],
        "explanation": "動詞「言う」之特殊尊敬語為「おっしゃる」（校長是這麼說的）。「申す」為自謙語。",
        "targetGrammar": "特殊尊敬「おっしゃる」"
    },
    {
        "id": "n4-s-105",
        "question": "どうぞ　こちらの温かいお茶を　（　　）上がってください。",
        "correct": "召し",
        "distractors": ["いただき", "飲み", "上がり"],
        "explanation": "動詞「飲む／食べる」之特殊尊敬語為「召し上がる」（請喝茶）。",
        "targetGrammar": "特殊尊敬「召し上がる」"
    },
    {
        "id": "n4-s-106",
        "question": "先生、昨日送っていただいたメールを　（　　）になりましたか。",
        "correct": "ご覧",
        "distractors": ["拝見", "お見せ", "ご覧入れ"],
        "explanation": "動詞「見る」之特殊尊敬語為「ご覧になる」（您看了信件嗎？）。「拝見」為自謙語。",
        "targetGrammar": "特殊尊敬「ご覧になる」"
    },
    {
        "id": "n4-s-107",
        "question": "明日　午後3時に　御社へ　（　　）ます。",
        "correct": "まいり",
        "distractors": ["いらっしゃい", "お越しになり", "見え"],
        "explanation": "動詞「行く／来る」之自謙語為「参る（まいる）」（明天會去貴公司）。",
        "targetGrammar": "特殊謙讓「参る」"
    },
    {
        "id": "n4-s-108",
        "question": "初めまして。私、営業部の田中と　（　　）ます。",
        "correct": "申し",
        "distractors": ["おっしゃい", "伺い", "存じ"],
        "explanation": "自稱姓名時，動詞「言う」之自謙語為「申す（もうす）」（我名叫田中）。",
        "targetGrammar": "特殊謙讓「申す」"
    },
    {
        "id": "n4-s-109",
        "question": "いただいた企画書の資料を　しっかりと　（　　）いたしました。",
        "correct": "拝見",
        "distractors": ["ご覧", "お見せ", "ご覧入れ"],
        "explanation": "動詞「見る」之自謙語為「拝見する（はいけんする）」（拜讀了企劃書資料）。",
        "targetGrammar": "特殊謙讓「拝見する」"
    },
    {
        "id": "n4-s-110",
        "question": "先生の最新のご研究について　お話を　（　　）たいのですが。",
        "correct": "伺い",
        "distractors": ["おっしゃい", "申され", "ご覧になり"],
        "explanation": "動詞「聞く／尋ねる／訪ねる」之自謙語為「伺う（うかがう）」（想請教拜聽老師的見解）。",
        "targetGrammar": "特殊謙讓「伺う」"
    },

    # 111-120: 難易・程度・時間・限定與形式名詞
    {
        "id": "n4-s-111",
        "question": "このペンは　軽くて　とても　字が　書き（　　）です。",
        "correct": "やすい",
        "distractors": ["にくい", "そう", "すぎ"],
        "explanation": "「動詞ます形去ます＋やすい」表示易於執行某動作、好寫（書きやすい）。",
        "targetGrammar": "易難「〜やすい」"
    },
    {
        "id": "n4-s-112",
        "question": "この本は　専門用語が多くて、初心者には　分かり（　　）です。",
        "correct": "にくい",
        "distractors": ["やすい", "そう", "すぎ"],
        "explanation": "「動詞ます形去ます＋にくい」表示難以執行或理解（分かりにくい＝不易理解）。",
        "targetGrammar": "易難「〜にくい」"
    },
    {
        "id": "n4-s-113",
        "question": "昨日は　カラオケで　歌い（　　）て、喉が痛くなってしまいました。",
        "correct": "すぎ",
        "distractors": ["やすく", "にくく", "そう"],
        "explanation": "「動詞ます形去ます＋すぎる（て形：すぎて）」表示程度過甚（唱得太過火了）。",
        "targetGrammar": "過度「〜すぎる」"
    },
    {
        "id": "n4-s-114",
        "question": "子供たちが　昼寝をしている（　　）に、晩ご飯の準備を済ませました。",
        "correct": "あいだ",
        "distractors": ["あいだで", "あいだから", "までに"],
        "explanation": "在某段狀態持續期間內完成一次性動作：「〜ている間に」（趁孩子午睡期間）。",
        "targetGrammar": "時間期間「〜あいだに」"
    },
    {
        "id": "n4-s-115",
        "question": "夏休みの宿題は、8月31日（　　）に　必ず提出してください。",
        "correct": "まで",
        "distractors": ["までに", "から", "あいだ"],
        "explanation": "題目後方已附「に」，完成期限句型為「までに」（故填「まで」：8月31日までに）。",
        "targetGrammar": "期限截止「〜までに」"
    },
    {
        "id": "n4-s-116",
        "question": "テレビを　見（　　）ご飯を食べるのは、お行儀が悪いです。",
        "correct": "ながら",
        "distractors": ["つつ", "あいだ", "まま"],
        "explanation": "「動詞ます形去ます＋ながら」表示同一主體同時進行兩項動作（邊看電視邊吃飯）。",
        "targetGrammar": "同時動作「〜ながら」"
    },
    {
        "id": "n4-s-117",
        "question": "電気を　つけた（　　）寝てしまったので、朝起きたら目が痛かったです。",
        "correct": "まま",
        "distractors": ["あいだ", "ながら", "とおり"],
        "explanation": "「動詞た形＋まま」表示維持原有狀態不變（開著電燈就睡著了）。",
        "targetGrammar": "狀態維持「〜まま」"
    },
    {
        "id": "n4-s-118",
        "question": "休日は　外に出かけず、部屋で　寝て（　　）過ごしました。",
        "correct": "ばかり",
        "distractors": ["だけ", "しか", "ほど"],
        "explanation": "「動詞て形＋ばかりいる／ばかり過ごす」表示光是、淨是做某事（光是睡覺度過）。",
        "targetGrammar": "淨是「〜ばかり」"
    },
    {
        "id": "n4-s-119",
        "question": "お腹がすいたのに、冷蔵庫には　卵が　一つ（　　）ありませんでした。",
        "correct": "しか",
        "distractors": ["だけ", "ばかり", "ほど"],
        "explanation": "「數量詞＋しか＋否定」表示限定（只有、僅有一顆雞蛋）。",
        "targetGrammar": "限定否定「〜しか〜ない」"
    },
    {
        "id": "n4-s-120",
        "question": "私は　友達と一緒に　旅行の計画を　立てる（　　）が大好きです。",
        "correct": "の",
        "distractors": ["こと", "もの", "ほう"],
        "explanation": "感情・喜好名詞化（好き・嫌い・上手・下手）前習慣使用形式名詞「の」（立てるのが大好き）。",
        "targetGrammar": "形式名詞「〜のが好き」"
    }
]

def get_sentence_quizzes():
    quizzes = []
    for i, item in enumerate(RAW_SENTENCE_QUIZZES):
        # Determine target position for correct answer (1, 2, 3, 4 balanced)
        target_idx = (i % 4) + 1  # 1-based: 1, 2, 3, 4
        opts = list(item["distractors"])
        opts.insert(target_idx - 1, item["correct"])
        
        quizzes.append({
            "id": item["id"],
            "question": item["question"],
            "options": opts,
            "correctIndex": target_idx,
            "explanation": item["explanation"],
            "targetGrammar": item["targetGrammar"]
        })
    return quizzes

if __name__ == "__main__":
    qs = get_sentence_quizzes()
    print(f"Generated {len(qs)} sentence quizzes.")
    counts = {}
    for q in qs:
        counts[q["correctIndex"]] = counts.get(q["correctIndex"], 0) + 1
    print("Option distribution:", counts)
