# -*- coding: utf-8 -*-
"""
50 JLPT N4 Star Scramble Quizzes (n4-star-1 to n4-star-50)
"""

RAW_STAR_QUIZZES = [
    # 1
    {
        "id": "n4-star-1",
        "preText": "来週のスピーチコンテストで　",
        "postText": "　練習しています。",
        "chunks": ["上手に", "ように", "話せる", "毎日"],
        "correctOrder": [4, 1, 3, 2],
        "fullSentence": "来週のスピーチコンテストで毎日上手に話せるように練習しています。",
        "translation": "為了在下週的演講比賽上能講得流利，我每天都在練習。",
        "grammarPoint": "目的「〜ように」"
    },
    # 2
    {
        "id": "n4-star-2",
        "preText": "大切な会議の資料ですから、先生に　",
        "postText": "　準備しました。",
        "chunks": ["とおりに", "言われた", "忘れないように", "きちんと"],
        "correctOrder": [2, 1, 4, 3],
        "fullSentence": "大切な会議の資料ですから、先生に言われたとおりにきちんと忘れないように準備しました。",
        "translation": "因為是很重要的會議資料，所以我按照老師所說的那樣，好好準備以防忘記。",
        "grammarPoint": "遵照指示「〜とおりに」與預防目的「〜ないように」"
    },
    # 3
    {
        "id": "n4-star-3",
        "preText": "妹は　母に　",
        "postText": "　泣いてしまいました。",
        "chunks": ["捨てられて", "大事にしていた漫画を", "思わず", "しまって"],
        "correctOrder": [2, 1, 4, 3],
        "fullSentence": "妹は母に大事にしていた漫画を捨てられてしまって思わず泣いてしまいました。",
        "translation": "妹妹因為珍藏的漫畫被媽媽丟掉了，忍不住哭了出來。",
        "grammarPoint": "所有物受身「〜を…られる」與遺憾「〜てしまう」"
    },
    # 4
    {
        "id": "n4-star-4",
        "preText": "この料理は　",
        "postText": "　簡単に作れます。",
        "chunks": ["電子レンジで", "材料を", "切って", "温めるだけで"],
        "correctOrder": [2, 3, 1, 4],
        "fullSentence": "この料理は材料を切って電子レンジで温めるだけで簡単に作れます。",
        "translation": "這道料理只要把材料切一切，用微波爐加熱就能輕鬆做好。",
        "grammarPoint": "限定「〜だけで」"
    },
    # 5
    {
        "id": "n4-star-5",
        "preText": "風邪をひいて　熱があるなら、無理を　",
        "postText": "　いいですよ。",
        "chunks": ["休んだ", "ほうが", "しないで", "早く"],
        "correctOrder": [3, 4, 1, 2],
        "fullSentence": "風邪をひいて熱があるなら、無理をしないで早く休んだほうがいいですよ。",
        "translation": "要是感冒發燒的話，別勉強自己，早點休息比較好喔。",
        "grammarPoint": "忠告「〜たほうがいい」與「〜ないで」"
    },
    # 6
    {
        "id": "n4-star-6",
        "preText": "電車が　遅れた　",
        "postText": "　遅刻してしまった。",
        "chunks": ["大切な", "せいで", "約束の", "時間に"],
        "correctOrder": [2, 1, 3, 4],
        "fullSentence": "電車が遅れたせいで大切な約束の時間に遅刻してしまった。",
        "translation": "因為電車誤點的緣故，重要約定時間遲到了。",
        "grammarPoint": "負面原因「〜せいで」"
    },
    # 7
    {
        "id": "n4-star-7",
        "preText": "図書館で　借りた本は、期限までに　",
        "postText": "　いけません。",
        "chunks": ["返さなければ", "きちんと", "図書館へ", "直接"],
        "correctOrder": [2, 4, 3, 1],
        "fullSentence": "図書館で借りた本は、期限までにきちんと直接図書館へ返さなければいけません。",
        "translation": "在圖書館借的書，必須在期限前親自好好歸還圖書館。",
        "grammarPoint": "義務「〜なければいけない」"
    },
    # 8
    {
        "id": "n4-star-8",
        "preText": "雨が　やんだら、公園へ　",
        "postText": "　行きましょう。",
        "chunks": ["散歩に", "犬を", "連れて", "いっしょに"],
        "correctOrder": [2, 3, 4, 1],
        "fullSentence": "雨がやんだら、公園へ犬を連れていっしょに散歩に行きましょう。",
        "translation": "雨停了的話，帶著狗狗一起去公園散步吧。",
        "grammarPoint": "伴隨動詞「〜を連れて」與目的「〜に行く」"
    },
    # 9
    {
        "id": "n4-star-9",
        "preText": "日本語を　上手に　話せる　",
        "postText": "　勉強しています。",
        "chunks": ["アニメを", "ように、", "見て", "毎日"],
        "correctOrder": [2, 4, 1, 3],
        "fullSentence": "日本語を上手に話せるように、毎日アニメを見て勉強しています。",
        "translation": "為了把日語說得好，每天都看動畫來學習。",
        "grammarPoint": "目的「〜ように」與手段「〜て勉強する」"
    },
    # 10
    {
        "id": "n4-star-10",
        "preText": "来月　友達の　結婚式が　",
        "postText": "　買いました。",
        "chunks": ["あるので、", "新しい", "スーツを", "きれいな"],
        "correctOrder": [1, 4, 2, 3],
        "fullSentence": "来月友達の結婚式があるので、きれいな新しいスーツを買いました。",
        "translation": "因為下個月有朋友婚禮，所以買了一套嶄新漂亮的新西裝。",
        "grammarPoint": "原因「〜ので」與形容詞名詞修飾"
    },
    # 11
    {
        "id": "n4-star-11",
        "preText": "この新しい靴は　サイズが　",
        "postText": "　足が痛くなりました。",
        "chunks": ["小さくて", "歩きにくくて", "とても", "私の足には"],
        "correctOrder": [4, 1, 3, 2],
        "fullSentence": "この新しい靴はサイズが私の足には小さくてとても歩きにくくて足が痛くなりました。",
        "translation": "這雙新鞋的尺寸對我的腳來說太小，非常難走，以至於腳都痛了。",
        "grammarPoint": "難易「〜にくい」與て形並列"
    },
    # 12
    {
        "id": "n4-star-12",
        "preText": "奨学金を申請するため、先生に　",
        "postText": "　お願いしました。",
        "chunks": ["推薦書を", "書いてほしいと", "丁寧に", "私のために"],
        "correctOrder": [4, 1, 2, 3],
        "fullSentence": "奨学金を申請するため、先生に私のために推薦書を書いてほしいと丁寧にお願いしました。",
        "translation": "為了申請獎學金，我客氣地拜託老師希望能替我寫推薦信。",
        "grammarPoint": "願望請求「〜てほしいと」"
    },
    # 13
    {
        "id": "n4-star-13",
        "preText": "果物屋の店先に並んでいる　",
        "postText": "　思わず買いました。",
        "chunks": ["リンゴが", "美味しそうに", "見えたので", "とても"],
        "correctOrder": [1, 4, 2, 3],
        "fullSentence": "果物屋の店先に並んでいるリンゴがとても美味しそうに見えたので思わず買いました。",
        "translation": "水果店前陳列的蘋果看起來非常美味，我不禁買了下來。",
        "grammarPoint": "樣態「〜そうに見える」"
    },
    # 14
    {
        "id": "n4-star-14",
        "preText": "すみませんが、",
        "postText": "　いただけませんか。",
        "chunks": ["駅への", "教えて", "行き方を", "地図で"],
        "correctOrder": [1, 3, 4, 2],
        "fullSentence": "すみませんが、駅への行き方を地図で教えていただけませんか。",
        "translation": "不好意思，能不能請您用地圖告訴我前往車站的路線呢？",
        "grammarPoint": "客氣請求「〜ていただけませんか」"
    },
    # 15
    {
        "id": "n4-star-15",
        "preText": "山田さんは　来週の懇親会に　",
        "postText": "　言っていました。",
        "chunks": ["出席できない", "と残念そうに", "かもしれない", "急用で"],
        "correctOrder": [4, 1, 3, 2],
        "fullSentence": "山田さんは来週の懇親会に急用で出席できないかもしれないと残念そうに言っていました。",
        "translation": "山田說因為有急事，下週的交流餐會說不定無法出席，顯得很遺憾的樣子。",
        "grammarPoint": "推測「〜かもしれない」與引用「〜と言っていた」"
    },
    # 16
    {
        "id": "n4-star-16",
        "preText": "今学期のレポートは　",
        "postText": "　なりません。",
        "chunks": ["明日の", "先生へ", "夕方までに", "提出しなければ"],
        "correctOrder": [1, 3, 2, 4],
        "fullSentence": "今学期のレポートは明日の夕方までに先生へ提出しなければなりません。",
        "translation": "這學期的報告必須在明天傍晚之前繳交給老師。",
        "grammarPoint": "期限「〜までに」與義務「〜なければならない」"
    },
    # 17
    {
        "id": "n4-star-17",
        "preText": "私が住んでいる町は　",
        "postText": "　とても住みやすいです。",
        "chunks": ["きれいだし", "空気も", "交通も", "便利だし"],
        "correctOrder": [2, 1, 3, 4],
        "fullSentence": "私が住んでいる町は空気もきれいだし交通も便利だしとても住みやすいです。",
        "translation": "我住的小鎮空氣清新，交通也方便，非常宜居。",
        "grammarPoint": "並列理由「〜し〜し」"
    },
    # 18
    {
        "id": "n4-star-18",
        "preText": "今年の夏休みは　",
        "postText": "　思っています。",
        "chunks": ["家族と", "旅行しようと", "北海道へ", "一緒に"],
        "correctOrder": [1, 4, 3, 2],
        "fullSentence": "今年の夏休みは家族と一緒に北海道へ旅行しようと思っています。",
        "translation": "今年的暑假，我打算和家人一起去北海道旅行。",
        "grammarPoint": "意向打算「〜ようと思っている」"
    },
    # 19
    {
        "id": "n4-star-19",
        "preText": "職員室の前の掲示板に　",
        "postText": "　ありますよ。",
        "chunks": ["来月の", "予定が", "試験の", "貼って"],
        "correctOrder": [1, 3, 2, 4],
        "fullSentence": "職員室の前の掲示板に来月の試験の予定が貼ってありますよ。",
        "translation": "教職員辦公室前的佈告欄上貼著下個月考試的時程表喔。",
        "grammarPoint": "存續態「〜てある」"
    },
    # 20
    {
        "id": "n4-star-20",
        "preText": "会社の辞令で、",
        "postText": "　ことになりました。",
        "chunks": ["来月から", "働く", "大阪支社で", "新プロジェクトで"],
        "correctOrder": [1, 4, 3, 2],
        "fullSentence": "会社の辞令で、来月から新プロジェクトで大阪支社で働くことになりました。",
        "translation": "因公司的調令，下個月起將要在大阪分社參與新專案工作。",
        "grammarPoint": "客觀決定「〜ことになる」"
    },
    # 21
    {
        "id": "n4-star-21",
        "preText": "いくら　",
        "postText": "　あきらめてはいけません。",
        "chunks": ["難しくても", "試験の", "問題が", "最後まで"],
        "correctOrder": [2, 3, 1, 4],
        "fullSentence": "いくら試験の問題が難しくても最後まであきらめてはいけません。",
        "translation": "無論考試題目多麼難，都絕不能輕易放棄到最後一刻。",
        "grammarPoint": "讓步「いくら〜ても」"
    },
    # 22
    {
        "id": "n4-star-22",
        "preText": "体調が悪いなら、無理をしないで　",
        "postText": "　構いませんよ。",
        "chunks": ["今日は", "帰っても", "早く", "家に"],
        "correctOrder": [1, 3, 4, 2],
        "fullSentence": "体調が悪いなら、無理をしないで今日は早く家に帰っても構いませんよ。",
        "translation": "身體不舒服的話，別勉強自己，今天提早回家也沒關係喔。",
        "grammarPoint": "許可「〜ても構わない」"
    },
    # 23
    {
        "id": "n4-star-23",
        "preText": "朝の忙しい時に　",
        "postText": "　遅刻してしまいますよ。",
        "chunks": ["見ながら", "テレビを", "食べていると", "ご飯を"],
        "correctOrder": [2, 1, 4, 3],
        "fullSentence": "朝の忙しい時にテレビを見ながらご飯を食べていると遅刻してしまいますよ。",
        "translation": "早晨忙碌時若邊看電視邊吃早餐，可是會遲到的喔。",
        "grammarPoint": "同時動作「〜ながら」與必然「〜と」"
    },
    # 24
    {
        "id": "n4-star-24",
        "preText": "昨晩は　エアコンを　",
        "postText": "　風邪をひいてしまった。",
        "chunks": ["つけた", "寝てしまった", "ので", "まま"],
        "correctOrder": [1, 4, 2, 3],
        "fullSentence": "昨晩はエアコンをつけたまま寝てしまったので風邪をひいてしまった。",
        "translation": "昨晚因為開著冷氣就睡著了，所以感冒了。",
        "grammarPoint": "狀態維持「〜たまま」與遺憾「〜てしまう」"
    },
    # 25
    {
        "id": "n4-star-25",
        "preText": "日本語の勉強を　",
        "postText": "　まだ上手に話せません。",
        "chunks": ["始めた", "なので", "ばかり", "先月"],
        "correctOrder": [4, 1, 3, 2],
        "fullSentence": "日本語の勉強を先月始めたばかりなのでまだ上手に話せません。",
        "translation": "日語學習因為上個月才剛開始，所以還說得不太好。",
        "grammarPoint": "剛完成「〜たばかり」與原因「〜ので」"
    },
    # 26
    {
        "id": "n4-star-26",
        "preText": "飛行機より　",
        "postText": "　景色を楽しめます。",
        "chunks": ["新幹線の", "ゆっくり", "ほうが", "時間をかけて"],
        "correctOrder": [1, 3, 4, 2],
        "fullSentence": "飛行機より新幹線のほうが時間をかけてゆっくり景色を楽しめます。",
        "translation": "比起飛機，搭乘新幹線更能多花點時間從容欣賞沿途風景。",
        "grammarPoint": "比較「〜より〜のほうが」"
    },
    # 27
    {
        "id": "n4-star-27",
        "preText": "一年の季節の中で　",
        "postText": "　一番好きです。",
        "chunks": ["桜が", "春が", "咲く", "美しく"],
        "correctOrder": [1, 4, 3, 2],
        "fullSentence": "一年の季節の中で桜が美しく咲く春が一番好きです。",
        "translation": "在一年四季之中，我最喜歡櫻花美麗綻放的春天。",
        "grammarPoint": "名詞修飾與最高級「〜の中で〜が一番」"
    },
    # 28
    {
        "id": "n4-star-28",
        "preText": "毎日何時間も　",
        "postText": "　とても悔しいです。",
        "chunks": ["一生懸命", "試験に", "落ちてしまって", "勉強したのに"],
        "correctOrder": [1, 4, 2, 3],
        "fullSentence": "毎日何時間も一生懸命勉強したのに試験に落ちてしまってとても悔しいです。",
        "translation": "明明每天都好幾個小時拼命讀書，考試卻還是落榜了，令人非常不甘心。",
        "grammarPoint": "逆接遺憾「〜のに」與「〜てしまう」"
    },
    # 29
    {
        "id": "n4-star-29",
        "preText": "明日のサッカーの試合が　",
        "postText": "　心配しています。",
        "chunks": ["予定通り", "行われる", "天気を", "かどうか"],
        "correctOrder": [1, 2, 4, 3],
        "fullSentence": "明日のサッカーの試合が予定通り行われるかどうか天気を心配しています。",
        "translation": "我很擔心天氣是否會影響明天的足球比賽如期舉行。",
        "grammarPoint": "間接疑問「〜かどうか」"
    },
    # 30
    {
        "id": "n4-star-30",
        "preText": "駅までの行き方が　",
        "postText": "　教えてください。",
        "chunks": ["よく", "交番で", "分からないので", "道を"],
        "correctOrder": [1, 3, 2, 4],
        "fullSentence": "駅までの行き方がよく分からないので交番で道を教えてください。",
        "translation": "因為不太清楚前往車站的走法，請在派出所為我指路。",
        "grammarPoint": "原因「〜ので」與請求「〜てください」"
    },
    # 31
    {
        "id": "n4-star-31",
        "preText": "先生は　掃除をサボった　",
        "postText": "　教室を掃除させました。",
        "chunks": ["放課後に", "生徒に", "厳しく", "一人で"],
        "correctOrder": [2, 1, 4, 3],
        "fullSentence": "先生は掃除をサボった生徒に放課後に一人で厳しく教室を掃除させました。",
        "translation": "老師讓放學後摸魚沒打掃的學生一個人嚴格地把教室打掃乾淨。",
        "grammarPoint": "使役態「〜に…させる」"
    },
    # 32
    {
        "id": "n4-star-32",
        "preText": "部活の厳しい練習で、",
        "postText": "　走らされました。",
        "chunks": ["グラウンドを", "何周も", "休まずに", "夕方まで"],
        "correctOrder": [4, 1, 3, 2],
        "fullSentence": "部活の厳しい練習で、夕方までグラウンドを休まずに何周も走らされました。",
        "translation": "在社團嚴苛的訓練中，我們被迫在球場上不休息地跑到傍晚，跑了好幾圈。",
        "grammarPoint": "使役受身「〜走らされる」"
    },
    # 33
    {
        "id": "n4-star-33",
        "preText": "社長は　大切なお客様を　",
        "postText": "　なられました。",
        "chunks": ["笑顔で", "玄関まで", "お見送りに", "丁寧に"],
        "correctOrder": [4, 1, 2, 3],
        "fullSentence": "社長は大切なお客様を丁寧に笑顔で玄関までお見送りになられました。",
        "translation": "社長禮貌微笑地親自將重要的貴賓送到玄關。",
        "grammarPoint": "尊敬語「お〜になる」"
    },
    # 34
    {
        "id": "n4-star-34",
        "preText": "先生に　私の新しい研究の　",
        "postText": "　思います。",
        "chunks": ["成果を", "お伝えしたいと", "直接会って", "ぜひ"],
        "correctOrder": [1, 4, 3, 2],
        "fullSentence": "先生に私の新しい研究の成果をぜひ直接会ってお伝えしたいと思います。",
        "translation": "我務必希望能當面見到老師，親自向老師報告我的最新研究成果。",
        "grammarPoint": "自謙語「お〜する」與願望「〜たいと思う」"
    },
    # 35
    {
        "id": "n4-star-35",
        "preText": "重い荷物を　階段の上まで　",
        "postText": "　とても助かりました。",
        "chunks": ["持ってくれた", "おかげで", "親切な人の", "本当に"],
        "correctOrder": [1, 3, 2, 4],
        "fullSentence": "重い荷物を階段の上まで持ってくれた親切な人のおかげで本当にとても助かりました。",
        "translation": "多虧好心人幫我把重行李一路提到樓梯上方，真是幫了大忙。",
        "grammarPoint": "授受「〜てくれる」與恩惠「〜おかげで」"
    },
    # 36
    {
        "id": "n4-star-36",
        "preText": "故障したパソコンを　",
        "postText": "　正常に動くようになりました。",
        "chunks": ["友達に", "直してもらったら", "機械に詳しい", "すぐに"],
        "correctOrder": [3, 1, 4, 2],
        "fullSentence": "故障したパソコンを機械に詳しい友達にすぐに直してもらったら正常に動くようになりました。",
        "translation": "故障的電腦請懂機械的朋友立即修好之後，又恢復正常運作了。",
        "grammarPoint": "授受「〜てもらう」與接續「〜たら」"
    },
    # 37
    {
        "id": "n4-star-37",
        "preText": "田中さんは　1時間前に　",
        "postText": "　はずですよ。",
        "chunks": ["家を出た", "もうすぐ", "のだから", "ここに着く"],
        "correctOrder": [1, 3, 2, 4],
        "fullSentence": "田中さんは1時間前に家を出たのだからもうすぐここに着くはずですよ。",
        "translation": "田中既然1小時前就出門了，照理說應該馬上就會抵達這裡了喔。",
        "grammarPoint": "推斷「〜はずだ」與理由「〜のだから」"
    },
    # 38
    {
        "id": "n4-star-38",
        "preText": "いつも正直な山田さんが　",
        "postText": "　ありません。",
        "chunks": ["嘘を", "そんな", "つくはずが", "絶対に"],
        "correctOrder": [4, 2, 1, 3],
        "fullSentence": "いつも正直な山田さんが絶対にそんな嘘をつくはずがありません。",
        "translation": "向來老實正直的山田，絕不可能說那種謊言。",
        "grammarPoint": "確信否定推斷「〜はずがない」"
    },
    # 39
    {
        "id": "n4-star-39",
        "preText": "静かな夜空に浮かぶ　",
        "postText": "　輝いていました。",
        "chunks": ["真珠のように", "満月が", "まるで", "大きな"],
        "correctOrder": [4, 2, 3, 1],
        "fullSentence": "静かな夜空に浮かぶ大きな満月がまるで真珠のように輝いていました。",
        "translation": "懸掛在寂靜夜空中的碩大滿月，宛如珍珠一般閃爍著光芒。",
        "grammarPoint": "比喻「まるで〜のようだ／ように」"
    },
    # 40
    {
        "id": "n4-star-40",
        "preText": "小学生のころ、この　",
        "postText": "　ことがあります。",
        "chunks": ["魚を", "澄んだ川で", "つかまえた", "手で"],
        "correctOrder": [2, 4, 1, 3],
        "fullSentence": "小学生のころ、この澄んだ川で手で魚をつかまえたことがあります。",
        "translation": "小學時期，我曾經在這條清澈的河流裡徒手抓過魚。",
        "grammarPoint": "過去經驗「〜たことがある」"
    },
    # 41
    {
        "id": "n4-star-41",
        "preText": "来週のキャンプに　",
        "postText": "　おきました。",
        "chunks": ["必要な", "道具を", "備えて", "買って"],
        "correctOrder": [3, 1, 2, 4],
        "fullSentence": "来週のキャンプに備えて必要な道具を買っておきました。",
        "translation": "為了下週的露營預作準備，我預先把必要的用具買齊了。",
        "grammarPoint": "事先準備「〜ておく」"
    },
    # 42
    {
        "id": "n4-star-42",
        "preText": "急いでいたので、大切な　",
        "postText": "　しまいました。",
        "chunks": ["書類を", "忘れて", "電車の棚に", "うっかり"],
        "correctOrder": [1, 4, 3, 2],
        "fullSentence": "急いでいたので、大切な書類をうっかり電車の棚に忘れてしまいました。",
        "translation": "因為當時趕時間，不小心把重要文件遺忘在電車的行李架上了。",
        "grammarPoint": "遺憾失誤「〜てしまう」"
    },
    # 43
    {
        "id": "n4-star-43",
        "preText": "夜ぐっすり眠るために、寝る前は　",
        "postText": "　いいですよ。",
        "chunks": ["スマホを", "ほうが", "見ない", "あまり"],
        "correctOrder": [4, 1, 3, 2],
        "fullSentence": "夜ぐっすり眠るために、寝る前はあまりスマホを見ないほうがいいですよ。",
        "translation": "為了夜間熟睡，睡前最好不要太常看手機喔。",
        "grammarPoint": "否定忠告「〜ないほうがいい」"
    },
    # 44
    {
        "id": "n4-star-44",
        "preText": "財布の中を確かめたら、",
        "postText": "　驚きました。",
        "chunks": ["残っていなくて", "小銭しか", "千円札がなくて", "百円玉の"],
        "correctOrder": [3, 4, 2, 1],
        "fullSentence": "財布の中を確かめたら、千円札がなくて百円玉の小銭しか残っていなくて驚きました。",
        "translation": "確認了錢包內部才驚訝地發現，沒有千圓鈔票，只剩下百圓硬幣零錢。",
        "grammarPoint": "限定否定「〜しか〜ない」"
    },
    # 45
    {
        "id": "n4-star-45",
        "preText": "弟は　野菜を食べないで、",
        "postText": "　母に叱られました。",
        "chunks": ["甘い", "食べて", "ばかり", "お菓子"],
        "correctOrder": [1, 4, 3, 2],
        "fullSentence": "弟は野菜を食べないで、甘いお菓子ばかり食べて母に叱られました。",
        "translation": "弟弟不吃蔬菜，光是吃甜食點心，被媽媽責罵了。",
        "grammarPoint": "頻繁限定「〜ばかり」"
    },
    # 46
    {
        "id": "n4-star-46",
        "preText": "外国語は　毎日　",
        "postText": "　上手になります。",
        "chunks": ["練習すれば", "自然に", "するほど", "声を出して"],
        "correctOrder": [4, 1, 3, 2],
        "fullSentence": "外国語は毎日声を出して練習すればするほど自然に上手になります。",
        "translation": "外語每天越是大聲發音練習，就會越自然地變得流利。",
        "grammarPoint": "越...越...「〜ば〜ほど」"
    },
    # 47
    {
        "id": "n4-star-47",
        "preText": "日本の古い歴史を　",
        "postText": "　おすすめです。",
        "chunks": ["京都を", "学びたいなら", "訪れるのが", "一度"],
        "correctOrder": [2, 4, 1, 3],
        "fullSentence": "日本の古い歴史を学びたいなら一度京都を訪れるのがおすすめです。",
        "translation": "如果想要學習日本悠久的歷史，推薦務必造訪一次京都。",
        "grammarPoint": "話題假定「〜なら」與名詞化「〜のが」"
    },
    # 48
    {
        "id": "n4-star-48",
        "preText": "寒い冬が過ぎて　",
        "postText": "　咲き誇ります。",
        "chunks": ["春になると", "公園には", "色鮮やかな", "花々が"],
        "correctOrder": [1, 2, 3, 4],
        "fullSentence": "寒い冬が過ぎて春になると公園には色鮮やかな花々が咲き誇ります。",
        "translation": "寒冬過去到了春天，公園裡色彩鮮艷的繁花盛開。",
        "grammarPoint": "恆常必然「〜と」"
    },
    # 49
    {
        "id": "n4-star-49",
        "preText": "朝は時間がなくて急いでいたので、",
        "postText": "　出かけてしまった。",
        "chunks": ["部屋の", "忘れて", "窓を閉めるのを", "うっかり"],
        "correctOrder": [1, 3, 4, 2],
        "fullSentence": "朝は時間がなくて急いでいたので、部屋の窓を閉めるのをうっかり忘れて出かけてしまった。",
        "translation": "早晨因為沒有時間匆忙出門，不小心忘了關房間窗戶就出門了。",
        "grammarPoint": "形式名詞「〜のを忘れる」"
    },
    # 50
    {
        "id": "n4-star-50",
        "preText": "このスマートフォンアプリは、",
        "postText": "　とても便利です。",
        "chunks": ["電車の", "最短ルートを", "調べるのに", "乗り換えの"],
        "correctOrder": [1, 4, 2, 3],
        "fullSentence": "このスマートフォンアプリは、電車の乗り換えの最短ルートを調べるのにとても便利です。",
        "translation": "這款智慧手機應用程式，用來查詢電車轉乘的最短路線非常方便。",
        "grammarPoint": "用途評價「〜のに便利だ」"
    }
]

def get_star_quizzes():
    quizzes = []
    for item in RAW_STAR_QUIZZES:
        order = item["correctOrder"]
        chunks = item["chunks"]
        star_idx = 2  # 0-based: 3rd slot
        star_answer = order[star_idx]
        
        # Verify reconstruction
        pre = item["preText"].replace("　", "").replace(" ", "")
        post = item["postText"].replace("　", "").replace(" ", "")
        ordered_chunks = "".join(chunks[i - 1] for i in order)
        assembled = pre + ordered_chunks + post
        expected = item["fullSentence"].replace("　", "").replace(" ", "")
        
        if assembled != expected:
            raise ValueError(f"Mismatch in {item['id']}: assembled '{assembled}' != expected '{expected}'")
        
        # Build explanation
        steps = " ➔ ".join(f"{chunks[i - 1]} ({i})" for i in order)
        exp = f"{steps}。★ 為 {star_answer} 號。【考點：{item['grammarPoint']}】"
        
        quizzes.append({
            "id": item["id"],
            "preText": item["preText"],
            "postText": item["postText"],
            "starIndex": 2,
            "chunks": chunks,
            "correctOrder": order,
            "explanation": exp,
            "fullSentence": item["fullSentence"],
            "translation": item["translation"]
        })
    return quizzes

if __name__ == "__main__":
    qs = get_star_quizzes()
    print(f"Generated {len(qs)} star quizzes successfully.")
    counts = {}
    for q in qs:
        ans = q["correctOrder"][q["starIndex"]]
        counts[ans] = counts.get(ans, 0) + 1
    print("Star answer distribution:", counts)

def get_balanced_star_quizzes():
    quizzes = []
    for k, item in enumerate(RAW_STAR_QUIZZES):
        desired_star = (k % 4) + 1
        chunks = list(item["chunks"])
        order = list(item["correctOrder"])
        current_star = order[2]
        if current_star != desired_star:
            idx1 = current_star - 1
            idx2 = desired_star - 1
            chunks[idx1], chunks[idx2] = chunks[idx2], chunks[idx1]
            new_order = []
            for val in order:
                if val == current_star:
                    new_order.append(desired_star)
                elif val == desired_star:
                    new_order.append(current_star)
                else:
                    new_order.append(val)
            order = new_order
        
        pre = item["preText"].replace("　", "").replace(" ", "")
        post = item["postText"].replace("　", "").replace(" ", "")
        ordered_chunks = "".join(chunks[i - 1] for i in order)
        assembled = pre + ordered_chunks + post
        expected = item["fullSentence"].replace("　", "").replace(" ", "")
        if assembled != expected:
            raise ValueError(f"Failed on {item['id']}: assembled '{assembled}' != expected '{expected}'")
        
        steps = " ➔ ".join(f"{chunks[i - 1]} ({i})" for i in order)
        exp = f"{steps}。★ 為 {desired_star} 號。【文法重點：{item['grammarPoint']}】"
        
        quizzes.append({
            "id": item["id"],
            "preText": item["preText"],
            "postText": item["postText"],
            "starIndex": 2,
            "chunks": chunks,
            "correctOrder": order,
            "explanation": exp,
            "fullSentence": item["fullSentence"],
            "translation": item["translation"]
        })
    return quizzes

