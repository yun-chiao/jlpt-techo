import { useState, useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { useDocumentTitle } from '../hooks/useDocumentTitle';
import { RetroCard } from '../components/RetroCard';

type LevelKey = 'n5' | 'n4' | 'n3' | 'n2' | 'n1' | 'all';
type ProductLine = 'quiz' | 'textbook';

interface CardSample {
  type: 'vocab' | 'grammar';
  title: string;
  category: string;
  front: string;
  promptTip: string;
  ruby: string;
  subMeta: string;
  meaning: string;
  formula?: string;
  alert?: string;
  exampleJa: string;
  exampleZh: string;
}

interface ProductInfo {
  key: LevelKey;
  upper: string;
  color: string;
  tint: string;
  title: string;
  subTitle: string;
  priceUsd: string;
  priceTwdApprox: string;
  stats: {
    cards: string;
    grammar: string;
    vocab: string;
    quizzes: string;
  };
  features: string[];
  handbookUrl: string;
  samples: CardSample[];
}

interface QuizProductInfo {
  key: LevelKey;
  upper: string;
  color: string;
  tint: string;
  title: string;
  subTitle: string;
  priceUsd: string;
  priceTwdApprox: string;
  stats: {
    cloze: string;
    star: string;
    passage: string;
    solutions: string;
  };
  features: string[];
  blankWorkbookUrl: string;
  solutionWorkbookUrl: string;
}

const QUIZ_PRODUCTS: Record<LevelKey, QuizProductInfo> = {
  n2: {
    key: 'n2',
    upper: 'N2',
    color: '#ff6b35',
    tint: '#fff0e8',
    title: '【日檢手帖】JLPT N2 500 題厚切全真手帳題本',
    subTitle: '日本留學與赴日求職黃金門檻・商務時事與長文理解實戰雙版本',
    priceUsd: '$12.99',
    priceTwdApprox: '約 NT$400',
    stats: {
      cloze: '300 題',
      star: '125 題',
      passage: '25 篇 (75題)',
      solutions: '500 題',
    },
    features: [
      '🔥 【獨家 350 題進階題庫】：收錄網頁未公開之 350 題高頻文法與長文，全面衝刺 500 題題海',
      '✍️ 【實戰純題目空白本】：完整 500 題純淨排版，留有手寫做題空間，無干擾模擬真實考場',
      '📑 【逐題詳解訂正神手帳】：500 題完整日文句、中日對照、💡 考點解析與專屬錯題筆記欄',
      '📊 【答案速查矩陣卡】：卷末附標準正解快速對照表，做完即時對分驗算',
      '📱 【iPad GoodNotes / A4 列印雙支援】：向量高清排版，隨心用 Apple Pencil 劃重點',
    ],
    blankWorkbookUrl: '/dist-products/quiz/日檢手帖-N2-500題全真手帳題本-試閱版.html',
    solutionWorkbookUrl: '/dist-products/quiz/日檢手帖-N2-500題全真手帳題本-詳解試閱版.html',
  },
  n1: {
    key: 'n1',
    upper: 'N1',
    color: '#e63956',
    tint: '#ffeaef',
    title: '【日檢手帖】JLPT N1 500 題厚切全真手帳題本',
    subTitle: '最高殿堂抽象文語、深層邏輯與學術長文・雙版本實戰套組',
    priceUsd: '$14.99',
    priceTwdApprox: '約 NT$460',
    stats: {
      cloze: '300 題',
      star: '125 題',
      passage: '25 篇 (75題)',
      solutions: '500 題',
    },
    features: [
      '🔥 【獨家 350 題進階題庫】：收錄網頁未公開之 350 題高頻文法與長文，全面衝刺 500 題題海',
      '✍️ 【實戰純題目空白本】：完整 500 題純淨排版，留有手寫做題空間，無干擾模擬真實考場',
      '📑 【逐題詳解訂正神手帳】：500 題完整日文句、中日對照、💡 考點解析與專屬錯題筆記欄',
      '📊 【答案速查矩陣卡】：卷末附標準正解快速對照表，做完即時對分驗算',
      '📱 【iPad GoodNotes / A4 列印雙支援】：向量高清排版，隨心用 Apple Pencil 劃重點',
    ],
    blankWorkbookUrl: '/dist-products/quiz/日檢手帖-N1-500題全真手帳題本-試閱版.html',
    solutionWorkbookUrl: '/dist-products/quiz/日檢手帖-N1-500題全真手帳題本-詳解試閱版.html',
  },
  n3: {
    key: 'n3',
    upper: 'N3',
    color: '#7cb518',
    tint: '#f2f8e6',
    title: '【日檢手帖】JLPT N3 500 題厚切全真手帳題本',
    subTitle: '跨越日檢分水嶺・日常複雜情境與職場銜接 500 題實戰雙版本',
    priceUsd: '$9.99',
    priceTwdApprox: '約 NT$310',
    stats: {
      cloze: '300 題',
      star: '125 題',
      passage: '25 篇 (75題)',
      solutions: '500 題',
    },
    features: [
      '🔥 【獨家 350 題進階題庫】：收錄網頁未公開之 350 題高頻文法與長文，全面衝刺 500 題題海',
      '✍️ 【實戰純題目空白本】：完整 500 題純淨排版，留有手寫做題空間，無干擾模擬真實考場',
      '📑 【逐題詳解訂正神手帳】：500 題完整日文句、中日對照、💡 考點解析與專屬錯題筆記欄',
      '📊 【答案速查矩陣卡】：卷末附標準正解快速對照表，做完即時對分驗算',
      '📱 【iPad GoodNotes / A4 列印雙支援】：向量高清排版，隨心用 Apple Pencil 劃重點',
    ],
    blankWorkbookUrl: '/dist-products/quiz/日檢手帖-N3-500題全真手帳題本-試閱版.html',
    solutionWorkbookUrl: '/dist-products/quiz/日檢手帖-N3-500題全真手帳題本-詳解試閱版.html',
  },
  n4: {
    key: 'n4',
    upper: 'N4',
    color: '#0096c7',
    tint: '#e2f4fa',
    title: '【日檢手帖】JLPT N4 500 題厚切全真手帳題本',
    subTitle: '進階基礎・日常動詞活用、敬語使役被動與生活指南 500 題',
    priceUsd: '$8.99',
    priceTwdApprox: '約 NT$280',
    stats: {
      cloze: '300 題',
      star: '125 題',
      passage: '25 篇 (75題)',
      solutions: '500 題',
    },
    features: [
      '🔥 【獨家 350 題進階題庫】：收錄網頁未公開之 350 題高頻文法與長文，全面衝刺 500 題題海',
      '✍️ 【實戰純題目空白本】：完整 500 題純淨排版，留有手寫做題空間，無干擾模擬真實考場',
      '📑 【逐題詳解訂正神手帳】：500 題完整日文句、中日對照、💡 考點解析與專屬錯題筆記欄',
      '📊 【答案速查矩陣卡】：卷末附標準正解快速對照表，做完即時對分驗算',
      '📱 【iPad GoodNotes / A4 列印雙支援】：向量高清排版，隨心用 Apple Pencil 劃重點',
    ],
    blankWorkbookUrl: '/dist-products/quiz/日檢手帖-N4-500題全真手帳題本-試閱版.html',
    solutionWorkbookUrl: '/dist-products/quiz/日檢手帖-N4-500題全真手帳題本-詳解試閱版.html',
  },
  n5: {
    key: 'n5',
    upper: 'N5',
    color: '#8338ec',
    tint: '#f2f8e6',
    title: '【日檢手帖】JLPT N5 500 題厚切全真手帳題本',
    subTitle: '零基礎入門首選・基礎格助詞、日常對話與生活記事 500 題實戰',
    priceUsd: '$6.99',
    priceTwdApprox: '約 NT$220',
    stats: {
      cloze: '300 題',
      star: '125 題',
      passage: '25 篇 (75題)',
      solutions: '500 題',
    },
    features: [
      '🔥 【獨家 350 題進階題庫】：收錄網頁未公開之 350 題高頻文法與長文，全面衝刺 500 題題海',
      '✍️ 【實戰純題目空白本】：完整 500 題純淨排版，留有手寫做題空間，無干擾模擬真實考場',
      '📑 【逐題詳解訂正神手帳】：500 題完整日文句、中日對照、💡 考點解析與專屬錯題筆記欄',
      '📊 【答案速查矩陣卡】：卷末附標準正解快速對照表，做完即時對分驗算',
      '📱 【iPad GoodNotes / A4 列印雙支援】：向量高清排版，隨心用 Apple Pencil 劃重點',
    ],
    blankWorkbookUrl: '/dist-products/quiz/日檢手帖-N5-500題全真手帳題本-試閱版.html',
    solutionWorkbookUrl: '/dist-products/quiz/日檢手帖-N5-500題全真手帳題本-詳解試閱版.html',
  },
  all: {
    key: 'all',
    upper: 'N1～N5',
    color: '#2b2523',
    tint: '#faf7f2',
    title: '【日檢手帖】JLPT N1～N5 全真 2,500 題終身典藏題本包',
    subTitle: '一次買齊五大級別共 10 冊手帳題本（5冊實戰空白本＋5冊逐題手寫風詳解訂正手帳）',
    priceUsd: '$24.99',
    priceTwdApprox: '約 NT$780',
    stats: {
      cloze: '1,500 題',
      star: '625 題',
      passage: '125 篇 (375題)',
      solutions: '2,500 題',
    },
    features: [
      '👑 包含 N5、N4、N3、N2、N1 全部 5 個獨立級別的 500 題全真題本套組（共 2,500 題）',
      '🔥 包含高達 1,750 題網頁未公開之獨家進階真題，終身題海直通最高殿堂',
      '✍️ 5 冊【考場實戰純題空白手寫本】：完整收錄全 2,500 題，隨心在 iPad 或紙本計時刷題',
      '📑 5 冊【逐題詳解訂正神手帳】：2,500 題逐題日文原句、中日對照、考點拆解與錯題筆記欄',
      '📊 5 份【標準正解 Answer Key 矩陣卡】：考前 30 分鐘快速對分核對',
      '💡 現省 54% 終身大特惠：一次付費，永久獲取 N1～N5 題本檔案！',
    ],
    blankWorkbookUrl: '/dist-products/quiz/日檢手帖-N2-500題全真手帳題本-試閱版.html',
    solutionWorkbookUrl: '/dist-products/quiz/日檢手帖-N2-500題全真手帳題本-詳解試閱版.html',
  },
};

const PRODUCTS: Record<LevelKey, ProductInfo> = {
  n3: {
    key: 'n3',
    upper: 'N3',
    color: '#7cb518',
    tint: '#f2f8e6',
    title: '【日檢手帖】JLPT N3 完全備考套組',
    subTitle: '跨越日檢分水嶺・日常複雜情境與職場銜接全攻略',
    priceUsd: '$9.99',
    priceTwdApprox: '約 NT$310',
    stats: {
      cards: '720 張智慧字卡',
      grammar: '120 個文法點',
      vocab: '600 個高頻單字',
      quizzes: '360 題實戰測驗',
    },
    features: [
      '📱 720 張 Anki 智慧字卡：逐字振假名對位＋羅馬拼音＋生活例句＋考場陷阱提示',
      '📑 FUDGE 日雜風 A4 講義手冊：收錄 120 文法公式清單、深度解析與 600 單字表',
      '✍️ GoodNotes / Notability 完美支援：向量高清排版，隨心手寫註記與畫線重點',
      '🖨️ A4 高解析列印支援：考場進場手機關機後的考前最後 30 分鐘複習神手冊',
    ],
    handbookUrl: '/dist-products/n3/日檢手帖-N3-試閱講義手冊.html',
    samples: [
      {
        type: 'vocab',
        title: 'N3 單字',
        category: '動詞（II類）',
        front: '受け付けます',
        promptTip: '請回想讀音、詞性與中文意思',
        ruby: '<ruby>受<rt>う</rt></ruby>け<ruby>付<rt>つ</rt></ruby>けます',
        subMeta: '/ uketsukemasu / ｜ 他動詞',
        meaning: '受理、接受（申請）；接待、受理報名',
        exampleJa: '📌 ホテルのフロントでチェックインを受け付けます。',
        exampleZh: '在飯店櫃檯受理入住手續。',
      },
      {
        type: 'grammar',
        title: 'N3 文法第28課',
        category: '情理推斷否定',
        front: '〜わけがない',
        promptTip: '請回想接續公式、核心意思與易混陷阱',
        ruby: '［普通形］＋ わけがない',
        subMeta: '名詞＋な／である ｜ な形＋な／である',
        meaning: '絕不可能…、哪有可能是…（帶強烈反駁情緒）',
        formula: '名詞／な形／い形／動詞普通形 ＋ わけがない',
        alert: '與「〜はずがない」區分：はずがない 是冷靜客觀推算；わけがない 帶有講話者的主觀情緒與反駁。',
        exampleJa: '✅ そんな馬鹿な話があるわけがない！',
        exampleZh: '哪可能有這種鬼話！（在反駁對方）',
      },
      {
        type: 'vocab',
        title: 'N3 單字',
        category: '名詞・抽象',
        front: 'きっかけ',
        promptTip: '請回想讀音與常用搭配助詞',
        ruby: 'きっかけ',
        subMeta: '/ kikkake / ｜ 促音詞彙',
        meaning: '契機、起因、藉口、轉折點',
        exampleJa: '📌 日本のアニメを見たのが、日本語を勉強するきっかけです。',
        exampleZh: '看了日本動漫，是我開始學日文的契機。',
      },
      {
        type: 'grammar',
        title: 'N3 文法第15課',
        category: '話題定義與轉換',
        front: '〜というと・〜といえば',
        promptTip: '說到…、提到…（三者功能怎麼分？）',
        ruby: '［名詞］＋ というと／といえば',
        subMeta: '口訣：下定義用 というのは、腦袋直覺聯想用 というと、順勢岔開話題用 といえば',
        meaning: '一說到…（就想到）；提到…（順便帶出另一件事）',
        formula: '名詞 ＋ というと／といえば',
        alert: '「というと」常用於向對方反問確認；「といえば」擅長自然延伸話題。',
        exampleJa: '✅ 春というと桜を思い出す。旅行といえば来週京都に行くよ。',
        exampleZh: '說到春天就想到櫻花。提到旅行，我下週要去京都喔。',
      },
    ],
  },
  n2: {
    key: 'n2',
    upper: 'N2',
    color: '#ff6b35',
    tint: '#fff0e8',
    title: '【日檢手帖】JLPT N2 完全備考套組',
    subTitle: '日本留學與赴日求職黃金門檻・商務時事與長文理解',
    priceUsd: '$12.99',
    priceTwdApprox: '約 NT$400',
    stats: {
      cards: '720 張智慧字卡',
      grammar: '120 個文法點',
      vocab: '600 個高頻單字',
      quizzes: '360 題實戰測驗',
    },
    features: [
      '📱 720 張 Anki 智慧字卡：N2 高階抽象名詞、複合動詞與商務情境例句全面精修',
      '📑 FUDGE 日雜風 A4 講義手冊：120 個 N2 複雜句型公式表格化、考場陷阱標記',
      '✍️ GoodNotes / Notability 完美支援：平板無縫雙開做筆記，字體極致清晰',
      '🖨️ A4 格式高解析列印支援：考前 30 分鐘文法秒殺清單隨身帶',
    ],
    handbookUrl: '/dist-products/n2/日檢手帖-N2-試閱講義手冊.html',
    samples: [
      {
        type: 'vocab',
        title: 'N2 單字',
        category: '慣用語・表現',
        front: '身をもって',
        promptTip: '請回想讀音與常用搭配動詞',
        ruby: '<ruby>身<rt>み</rt></ruby>をもって',
        subMeta: '/ mi o motte / ｜ 副詞片語',
        meaning: '親身、以身作則地、用自身體驗深刻感受',
        exampleJa: '📌 健康の大切さを、病気になって身をもって知った。',
        exampleZh: '生了病之後，才親身體會到健康的重要。',
      },
      {
        type: 'grammar',
        title: 'N2 文法第9課',
        category: '話題與焦點爭議',
        front: '〜をめぐって',
        promptTip: '圍繞著…（後面只能接什麼樣的動詞？）',
        ruby: '［名詞］＋ をめぐって',
        subMeta: '名詞修飾：〜をめぐる＋名詞',
        meaning: '圍繞著…（爭端、焦點議題產生討論或對立）',
        formula: '名詞 ＋ をめぐって（／をめぐる＋名詞）',
        alert: '後項必接「争う、議論する、対立する」等表示爭議對立的動詞，不能接一般日常動作。',
        exampleJa: '✅ 新空港の建設をめぐって、住民の間で激しい議論が続いている。',
        exampleZh: '圍繞著新機場興建問題，居民之間持續進行著激烈爭論。',
      },
    ],
  },
  n1: {
    key: 'n1',
    upper: 'N1',
    color: '#e63956',
    tint: '#ffeaef',
    title: '【日檢手帖】JLPT N1 完全備考套組',
    subTitle: '最高殿堂・抽象邏輯、書面政經與古典文語完全制霸',
    priceUsd: '$12.99',
    priceTwdApprox: '約 NT$400',
    stats: {
      cards: '720 張智慧字卡',
      grammar: '120 個文法點',
      vocab: '600 個高頻單字',
      quizzes: '360 題實戰測驗',
    },
    features: [
      '📱 720 張 Anki 智慧字卡：N1 生僻漢字、書面文語、四字熟語與時事深度解析',
      '📑 FUDGE 日雜風 A4 講義手冊：120 個 N1 最高難度文法公式與前後呼應否定詞速查',
      '✍️ iPad 電子手帳與列印雙模式：向量清晰排版，考前最後衝刺專用',
    ],
    handbookUrl: '/dist-products/n1/日檢手帖-N1-試閱講義手冊.html',
    samples: [
      {
        type: 'vocab',
        title: 'N1 單字',
        category: '社會・時事',
        front: '待機児童',
        promptTip: '請回想四個漢字各自的讀音與含義',
        ruby: '<ruby>待<rt>たい</rt></ruby><ruby>機<rt>き</rt></ruby><ruby>児<rt>じ</rt></ruby><ruby>童<rt>どう</rt></ruby>',
        subMeta: '/ taikijidou / ｜ 熟字音讀組合',
        meaning: '候補入托兒童（符合公立托育條件卻因額滿而排隊等待的幼兒）',
        exampleJa: '📌 自治体は待機児童のゼロを目指して保育施設を増設した。',
        exampleZh: '地方政府以托育候補兒童歸零為目標，增設了保育設施。',
      },
      {
        type: 'grammar',
        title: 'N1 文法第1課',
        category: '輕重對比強烈否定',
        front: '〜はおろか',
        promptTip: '不用說…就連…也（前後項輕重順序是？）',
        ruby: '［名詞］＋ はおろか、〜も／さえ',
        subMeta: '句尾常呼應否定形，強調「連基本的都辦不到」',
        meaning: '不用說…了，連…都…（別說程度輕的前者，連更重的後者都做不到）',
        formula: '名詞 ＋ はおろか、〜も／さえ＋否定',
        alert: '輕重順序不能顛倒！前面放程度較輕（更容易做到）的事，後面放更難的事。',
        exampleJa: '✅ 骨折で走ることはおろか、立つことさえ難しい。',
        exampleZh: '骨折別說跑步了，連站立都很困難。',
      },
    ],
  },
  n4: {
    key: 'n4',
    upper: 'N4',
    color: '#0096c7',
    tint: '#e2f4fa',
    title: '【日檢手帖】JLPT N4 完全備考套組',
    subTitle: '進階基礎・動詞變化（可能/意向/受身/使役）與條件句精修',
    priceUsd: '$8.99',
    priceTwdApprox: '約 NT$280',
    stats: {
      cards: '721 張智慧字卡',
      grammar: '120 個文法點',
      vocab: '601 個核心單字',
      quizzes: '360 題實戰測驗',
    },
    features: [
      '📱 721 張 Anki 智慧字卡：自他動詞成對比較、動詞變化接續、授受動詞深度解析',
      '📑 FUDGE 日雜風 A4 講義手冊：條件句（と/ば/たら/なら）與形式名詞完全手冊',
      '✍️ 平板 GoodNotes 做筆記最舒服的間距與字體大小設計',
    ],
    handbookUrl: '/dist-products/n4/日檢手帖-N4-試閱講義手冊.html',
    samples: [
      {
        type: 'vocab',
        title: 'N4 單字',
        category: '自動詞・故障',
        front: '壊れます',
        promptTip: '壊れます 是自動詞還是他動詞？他動詞怎麼說？',
        ruby: '<ruby>壊<rt>こわ</rt></ruby>れます',
        subMeta: '/ kowaremasu / ｜ 動詞（II類・自動詞）',
        meaning: '壞掉、破碎、倒塌、破滅',
        exampleJa: '📌 パソコンが突然壊れて、仕事が進まない。',
        exampleZh: '電腦突然壞掉了，工作無法進行。',
      },
      {
        type: 'grammar',
        title: 'N4 文法第8課',
        category: '義務與必須',
        front: '〜なければならない',
        promptTip: '必須、不得不（ない形去掉い接續）',
        ruby: '［動詞ない形（去掉い）］＋ なければならない',
        subMeta: '口語常縮約為：〜なきゃ、〜なくちゃ',
        meaning: '必須…、不得不…（客觀規則或生理必然）',
        formula: '動詞ない形（去 い） ＋ なければならない',
        alert: '常與「〜てはいけない（禁止）」做對比測驗；口語化縮約在聽力極常出現！',
        exampleJa: '✅ 明日は試験だから、早く寝なければならない。',
        exampleZh: '明天有考試，所以必須早點睡。',
      },
    ],
  },
  n5: {
    key: 'n5',
    upper: 'N5',
    color: '#8338ec',
    tint: '#f2e8fd',
    title: '【日檢手帖】JLPT N5 完全備考套組',
    subTitle: '入門基石・五十音後第一哩路，生活招呼與基礎句型大通關',
    priceUsd: '$5.99',
    priceTwdApprox: '約 NT$190',
    stats: {
      cards: '716 張智慧字卡',
      grammar: '48 個文法點',
      vocab: '664 個基礎單字',
      quizzes: '144 題實戰測驗',
    },
    features: [
      '📱 716 張 Anki 智慧字卡：初學者必備動詞三類分類、形容詞肯定否定、格助詞用法',
      '📑 FUDGE 日雜風 A4 講義手冊：全彩平假名片假名對位、初級 48 核心文法整理',
      '✍️ iPad 電子手帳與列印雙模式：適合第一次考日檢的安心夥伴',
    ],
    handbookUrl: '/dist-products/n5/日檢手帖-N5-試閱講義手冊.html',
    samples: [
      {
        type: 'vocab',
        title: 'N5 單字',
        category: '名詞・親屬稱謂',
        front: '両親',
        promptTip: '對別人稱呼自己的父母，該怎麼說？',
        ruby: '<ruby>両<rt>りょう</rt></ruby><ruby>親<rt>しん</rt></ruby>',
        subMeta: '/ ryoushin / ｜ 音讀名詞',
        meaning: '父母親、雙親（稱呼自己的父母）',
        exampleJa: '📌 両親は台湾に住んでいます。',
        exampleZh: '父母親住在台灣。',
      },
      {
        type: 'grammar',
        title: 'N5 文法第3課',
        category: '欲望與願望表達',
        front: '〜たい・〜たくない',
        promptTip: '我想…、我不想…（助詞要用 が 還是 を？）',
        ruby: '［動詞ます形（去掉ます）］＋ たい',
        subMeta: '只用於自己（第一人稱）的願望，不能直接詢問長輩',
        meaning: '想要（做某動作）',
        formula: '名詞 を／が ＋ 動詞ます形（去 ます） ＋ たい',
        alert: '願望對象名詞助詞用「が」或「を」皆可（が 偏重欲望對象，を 偏重動作）。',
        exampleJa: '✅ 日本へ旅行に行きたいです。',
        exampleZh: '我很想去日本旅行。',
      },
    ],
  },
  all: {
    key: 'all',
    upper: 'N1～N5',
    color: '#2b2523',
    tint: '#faf7f2',
    title: '【日檢手帖】JLPT N1～N5 終身全套典藏包',
    subTitle: '一次帶走 N1～N5 全部 5 個獨立級別，陪伴你從入門直到最高殿堂',
    priceUsd: '$29.99',
    priceTwdApprox: '約 NT$930',
    stats: {
      cards: '3,593 張全級別字卡',
      grammar: '528 個文法點',
      vocab: '3,065 個高頻單字',
      quizzes: '1,584 題實戰測驗',
    },
    features: [
      '👑 包含 N5、N4、N3、N2、N1 全部 5 個獨立級別的完整教材包',
      '📱 3,593 張日雜風 Anki 智慧字卡：全數逐字振假名＋生活例句＋考場陷阱提示',
      '📑 5 冊 FUDGE 日雜風 A4 講義手冊（支援存為 PDF 或放入 GoodNotes）',
      '💡 一次投資，陪伴你從五十音初學直通 N1 最高殿堂！',
    ],
    handbookUrl: '/dist-products/n3/日檢手帖-N3-試閱講義手冊.html',
    samples: [],
  },
};

export function ProductShowcasePage() {
  const [searchParams] = useSearchParams();
  const tabParam = searchParams.get('tab');
  const levelParam = searchParams.get('level') as LevelKey;

  const [activeLine, setActiveLine] = useState<ProductLine>(tabParam === 'quiz' ? 'quiz' : 'quiz');
  const [selectedLevel, setSelectedLevel] = useState<LevelKey>(
    levelParam && ['n1', 'n2', 'n3', 'n4', 'n5', 'all'].includes(levelParam) ? levelParam : 'n2'
  );
  
  // 題本試閱切換：'blank'（實戰空白做題本）| 'solution'（逐題詳解訂正本）
  const [previewWorkbookType, setPreviewWorkbookType] = useState<'blank' | 'solution'>('blank');

  // 教材樣張翻牌
  const [activeTextbookSampleIdx, setActiveTextbookSampleIdx] = useState(0);
  const [isCardFlipped, setIsCardFlipped] = useState(false);

  useEffect(() => {
    if (tabParam === 'textbook') setActiveLine('textbook');
    else if (tabParam === 'quiz') setActiveLine('quiz');
    if (levelParam && ['n1', 'n2', 'n3', 'n4', 'n5', 'all'].includes(levelParam)) {
      setSelectedLevel(levelParam);
    }
  }, [tabParam, levelParam]);

  useDocumentTitle(
    activeLine === 'quiz'
      ? '500 題全真手帳題本｜日檢手帖 N1～N5 GoodNotes / A4 列印雙版本套組'
      : '數位備考套組｜日檢手帖 N1～N5 Anki 牌組＆考場速查手冊'
  );

  const currentQuizProd = QUIZ_PRODUCTS[selectedLevel];

  const currentTextbookProd = PRODUCTS[selectedLevel];
  const tbSamples = selectedLevel === 'all' ? PRODUCTS.n3.samples : currentTextbookProd.samples;
  const curTbSample = tbSamples[activeTextbookSampleIdx % tbSamples.length];

  const handleLevelChange = (lvl: LevelKey) => {
    setSelectedLevel(lvl);
    setActiveTextbookSampleIdx(0);
    setIsCardFlipped(false);
  };

  return (
    <div className="mx-auto max-w-5xl px-3 py-5 sm:px-4 sm:py-8 md:py-12">
      {/* 頂部雙商品線切換（日雜文青質感） */}
      <div className="mx-auto max-w-xl">
        <div className="grid grid-cols-2 gap-1.5 rounded-2xl border-2 border-paper-sumi bg-paper-canvas p-1 sm:gap-2 sm:p-1.5 shadow-retro">
          <button
            type="button"
            onClick={() => setActiveLine('quiz')}
            className={`flex items-center justify-center gap-1 rounded-xl px-2 py-2 font-display text-xs font-black transition-all sm:gap-1.5 sm:px-3 sm:py-2.5 sm:text-sm ${
              activeLine === 'quiz'
                ? 'bg-paper-sumi text-white shadow-retro-sm'
                : 'text-paper-sumi hover:bg-paper-butter'
            }`}
          >
            <span>✍️</span>
            <span className="whitespace-nowrap">500 題手帳題本</span>
            <span className="rounded bg-[#ff6b35] px-1 py-0.2 font-mono text-[9px] font-black text-white sm:px-1.5 sm:py-0.5 sm:text-[10px]">HOT</span>
          </button>
          <button
            type="button"
            onClick={() => setActiveLine('textbook')}
            className={`flex items-center justify-center gap-1 rounded-xl px-2 py-2 font-display text-xs font-black transition-all sm:gap-1.5 sm:px-3 sm:py-2.5 sm:text-sm ${
              activeLine === 'textbook'
                ? 'bg-paper-sumi text-white shadow-retro-sm'
                : 'text-paper-sumi hover:bg-paper-butter'
            }`}
          >
            <span>📱</span>
            <span className="whitespace-nowrap">Anki 備考套組</span>
          </button>
        </div>
      </div>

      {/* 頂部標題說明 */}
      <div className="mt-6 text-center sm:mt-8">
        <span className="inline-block rounded-lg border-2 border-paper-sumi bg-paper-butter px-2.5 py-0.5 font-display text-[10.5px] font-black shadow-retro-sm sm:text-xs md:text-sm">
          {activeLine === 'quiz' ? 'GoodNotes / Notability / A4 實體列印雙版本手帳' : 'FUDGE / CLUEL 日雜風格・全自學數位教材'}
        </span>
        <h1 className="mt-2.5 font-display text-xl font-black sm:mt-3 sm:text-3xl md:text-4xl">
          {activeLine === 'quiz' ? '日檢手帖・500 題厚切全真手帳題本' : '日檢手帖・獨立分級數位備考套組'}
        </h1>
        <p className="mx-auto mt-2 max-w-2xl text-xs leading-relaxed text-paper-sumi/75 sm:mt-2.5 sm:text-sm md:text-base">
          {activeLine === 'quiz' ? (
            <>
              專為喜愛在 <span className="font-bold text-paper-sumi">iPad 筆記軟體（GoodNotes / Notability）手寫刷題</span> 與 <span className="font-bold text-paper-sumi">A4 實體紙本模擬考場</span> 的考生打造。包含【實戰空白做題本】＋【逐題手寫風詳解訂正神手帳】雙版本！
            </>
          ) : (
            <>
              專為喜愛用 <span className="font-bold text-paper-sumi">iPad 平板筆記</span> 與 <span className="font-bold text-paper-sumi">Anki 智慧間隔記憶</span> 的自學者打造。逐字振假名記憶字卡包與 FUDGE 日雜風 A4 考場速查講義！
            </>
          )}
        </p>
      </div>

      {/* 級別切換按鈕列 */}
      <div className="mt-5 sm:mt-7">
        <div className="grid grid-cols-5 gap-1.5 sm:gap-2.5">
          {(['n5', 'n4', 'n3', 'n2', 'n1'] as LevelKey[]).map((lvl) => {
            const item = activeLine === 'quiz' ? QUIZ_PRODUCTS[lvl] : PRODUCTS[lvl];
            const active = selectedLevel === lvl;
            return (
              <button
                key={lvl}
                type="button"
                onClick={() => handleLevelChange(lvl)}
                className={`flex flex-col items-center justify-center rounded-xl border-2 border-paper-sumi py-1.5 transition-all sm:py-2.5 ${
                  active
                    ? 'bg-paper-sumi text-paper-card shadow-retro'
                    : 'bg-paper-card text-paper-sumi shadow-retro-sm hover:translate-y-[-1px]'
                }`}
              >
                <span
                  className="h-2 w-2 rounded-full sm:h-2.5 sm:w-2.5"
                  style={{ backgroundColor: item.color }}
                />
                <span className="mt-0.5 font-display text-xs font-black sm:mt-1 sm:text-sm">{item.upper}</span>
              </button>
            );
          })}
        </div>

        <div className="mt-2 sm:mt-2.5">
          <button
            type="button"
            onClick={() => handleLevelChange('all')}
            className={`flex w-full items-center justify-center gap-1.5 rounded-xl border-2 border-paper-sumi py-2 px-3 font-display text-xs font-black transition-all sm:py-2.5 sm:text-sm ${
              selectedLevel === 'all'
                ? 'bg-paper-sumi text-paper-card shadow-retro'
                : 'bg-paper-butter text-paper-sumi shadow-retro-sm hover:translate-y-[-1px]'
            }`}
          >
            <span>👑</span>
            <span>
              {activeLine === 'quiz'
                ? 'N1～N5 全真 2,500 題終身典藏題本包（共 10 冊・現省 54%）'
                : 'N1～N5 終身全套典藏包（一次買齊 5 級教材・現省 42%）'}
            </span>
          </button>
        </div>
      </div>

      {/* ─────────────────────────────────────────────────────────────
       * 情況 A：【題庫系列】展示主卡片
       * ──────────────────────────────────────────────────────────── */}
      {activeLine === 'quiz' && (
        <div className="mt-4 rounded-2xl border-2 border-paper-sumi bg-paper-card p-3.5 shadow-retro sm:mt-6 sm:border-3 sm:p-6 sm:shadow-retro-lg md:p-8">
          {/* 題本標頭與價格 */}
          <div className="flex flex-col gap-3 border-b-2 border-dashed border-paper-sumi pb-4 sm:pb-5 md:flex-row md:items-center md:justify-between">
            <div>
              <div className="flex items-center gap-2 sm:gap-3">
                <span
                  className="rounded-lg border-2 border-paper-sumi px-2 py-0.5 font-mono text-xs font-black text-paper-card sm:px-3 sm:py-1 sm:text-sm"
                  style={{ backgroundColor: currentQuizProd.color }}
                >
                  {currentQuizProd.upper}
                </span>
                <h2 className="font-display text-lg font-black sm:text-2xl md:text-3xl">{currentQuizProd.title}</h2>
              </div>
              <p className="mt-1 text-xs font-bold text-paper-sumi/70 sm:mt-1.5 sm:text-sm">{currentQuizProd.subTitle}</p>
            </div>

            <div className="flex flex-row items-center justify-between gap-3 pt-2 sm:pt-0 md:flex-col md:items-end md:justify-center md:gap-2 md:pt-0 shrink-0">
              <div className="flex items-baseline gap-1.5 sm:gap-2">
                <span className="font-display text-2xl font-black text-paper-sumi sm:text-3xl md:text-4xl">{currentQuizProd.priceUsd}</span>
                <span className="font-mono text-xs font-bold text-paper-sumi/60">{currentQuizProd.priceTwdApprox}</span>
              </div>
              <a
                href="https://buymeacoffee.com/chiaoban/extras"
                target="_blank"
                rel="noreferrer"
                className="btn-retro !bg-paper-butter !px-4 !py-2 sm:!px-5 sm:!py-2.5 text-xs sm:text-sm font-black text-paper-sumi shadow-retro hover:scale-[1.02] active:scale-95 transition-all whitespace-nowrap"
              >
                <span>🛒 立即購買套組</span>
                <span className="font-mono">→</span>
              </a>
            </div>
          </div>

          {/* 4 大規格指標 */}
          <div className="mt-4 grid grid-cols-2 gap-2 sm:mt-5 sm:grid-cols-4 sm:gap-3">
            <div className="rounded-xl border border-paper-sumi/25 bg-paper-canvas p-2.5 text-center sm:p-3">
              <div className="font-mono text-lg font-black text-paper-sumi sm:text-2xl">{currentQuizProd.stats.cloze}</div>
              <div className="mt-0.5 text-[11px] font-bold text-paper-sumi/65">Part 1 文法挖空</div>
            </div>
            <div className="rounded-xl border border-paper-sumi/25 bg-paper-canvas p-2.5 text-center sm:p-3">
              <div className="font-mono text-lg font-black text-paper-sumi sm:text-2xl">{currentQuizProd.stats.star}</div>
              <div className="mt-0.5 text-[11px] font-bold text-paper-sumi/65">Part 2 ★ 語序重組</div>
            </div>
            <div className="rounded-xl border border-paper-sumi/25 bg-paper-canvas p-2.5 text-center sm:p-3">
              <div className="font-mono text-lg font-black text-paper-sumi sm:text-2xl">{currentQuizProd.stats.passage}</div>
              <div className="mt-0.5 text-[11px] font-bold text-paper-sumi/65">Part 3 篇章長文</div>
            </div>
            <div className="rounded-xl border border-paper-sumi/25 bg-paper-canvas p-2.5 text-center sm:p-3">
              <div className="font-mono text-lg font-black text-paper-sumi sm:text-2xl">{currentQuizProd.stats.solutions}</div>
              <div className="mt-0.5 text-[11px] font-bold text-paper-sumi/65">逐題詳解與錯題欄</div>
            </div>
          </div>

          {/* A4 手帳題本真實試閱專區（全寬大器翻閱，支援實戰空白 vs 逐題詳解雙模式切換） */}
          <div className="mt-5 rounded-xl border-2 border-paper-sumi bg-paper-canvas p-3.5 sm:p-5">
            <div className="flex flex-col gap-2.5 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <h3 className="font-display text-sm font-black text-paper-sumi sm:text-base">
                  📖 A4 / GoodNotes 手帳題本真實內頁試閱（30 題精華版）
                </h3>
                <p className="mt-0.5 text-xs text-paper-sumi/65">
                  可在下方視窗內直接滑動翻閱真實 A4 排版、做題留白與考場格式：
                </p>
              </div>

              {/* 雙版本試閱切換鈕 */}
              <div className="grid grid-cols-2 gap-1 w-full sm:w-auto sm:inline-flex rounded-xl border-2 border-paper-sumi bg-white p-1 font-display text-xs font-bold shadow-retro-sm shrink-0">
                <button
                  type="button"
                  onClick={() => setPreviewWorkbookType('blank')}
                  className={`rounded-lg px-2 py-1.5 text-center transition-all whitespace-nowrap ${
                    previewWorkbookType === 'blank'
                      ? 'bg-paper-sumi text-white font-black shadow-retro-sm'
                      : 'text-paper-sumi hover:bg-paper-butter'
                  }`}
                >
                  📄 實戰空白本
                </button>
                <button
                  type="button"
                  onClick={() => setPreviewWorkbookType('solution')}
                  className={`rounded-lg px-2 py-1.5 text-center transition-all whitespace-nowrap ${
                    previewWorkbookType === 'solution'
                      ? 'bg-paper-butter text-paper-sumi font-black border border-paper-sumi'
                      : 'text-paper-sumi hover:bg-paper-butter'
                  }`}
                >
                  ✍️ 逐題詳解本
                </button>
              </div>
            </div>

            {/* A4 題本內嵌視窗 */}
            <div className="relative mt-3.5 h-[440px] w-full overflow-hidden rounded-xl border-2 border-paper-sumi bg-white shadow-retro-sm sm:h-[560px] md:h-[640px]">
              <iframe
                key={previewWorkbookType}
                src={previewWorkbookType === 'blank' ? currentQuizProd.blankWorkbookUrl : currentQuizProd.solutionWorkbookUrl}
                title={`${currentQuizProd.upper} 500題手帳題本試閱`}
                className="h-full w-full border-0 bg-[#faf7f2]"
                style={{ width: '100%', minWidth: '100%', maxWidth: '100%' }}
                loading="lazy"
              />
            </div>

            {/* 視窗下方全頁超連結 */}
            <div className="mt-3 flex flex-col gap-1.5 text-xs sm:flex-row sm:items-center sm:justify-between">
              <span className="font-mono text-paper-sumi/70">
                💡 支援 iPad GoodNotes / Notability 向量手寫註記 ＆ A4 高解析列印
              </span>
              <a
                href={previewWorkbookType === 'blank' ? currentQuizProd.blankWorkbookUrl : currentQuizProd.solutionWorkbookUrl}
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center gap-1 font-display font-bold text-[#ff6b35] underline decoration-2 underline-offset-4 hover:text-paper-sumi"
              >
                🔍 開啟全頁高解析 A4 題本【{previewWorkbookType === 'blank' ? '實戰空白試閱版' : '逐題詳解試閱版'}】↗
              </a>
            </div>
          </div>

          {/* 包含內容清單 */}
          <div className="mt-5 rounded-xl border-2 border-paper-sumi bg-paper-canvas p-3 sm:p-4">
            <h3 className="font-display text-xs font-black sm:text-sm">
              📦 {currentQuizProd.title} 包含完整內容：
            </h3>
            <ul className="mt-2 space-y-1 text-xs text-paper-sumi/85 sm:text-sm">
              {currentQuizProd.features.map((feat, idx) => (
                <li key={idx} className="flex items-start gap-1.5">
                  <span className="font-bold text-[#ff6b35]">✔</span>
                  <span>{feat}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* 為什麼手寫刷題是通過日檢關鍵 */}
          <div className="mt-5 border-t-2 border-dashed border-paper-sumi/40 pt-5">
            <div className="text-center">
              <h3 className="font-display text-sm font-black sm:text-base">
                為什麼考前最後衝刺，手寫題本是「提分關鍵」？
              </h3>
            </div>
            <div className="mt-3 grid grid-cols-2 gap-2 sm:grid-cols-2 sm:gap-3 lg:grid-cols-4">
              <RetroCard shadow="sm" className="p-2.5 text-center sm:p-3">
                <div className="text-xl sm:text-2xl">✍️</div>
                <h4 className="mt-1 font-display text-xs font-bold sm:text-sm">圈詞劃重點記憶</h4>
                <p className="mt-0.5 text-[10.5px] leading-relaxed text-paper-sumi/70 sm:text-xs">
                  手寫圈出接續詞與助詞，建立大腦對文法骨架的肌肉記憶。
                </p>
              </RetroCard>
              <RetroCard shadow="sm" className="p-2.5 text-center sm:p-3">
                <div className="text-xl sm:text-2xl">⏱️</div>
                <h4 className="mt-1 font-display text-xs font-bold sm:text-sm">考場真實限時感</h4>
                <p className="mt-0.5 text-[10.5px] leading-relaxed text-paper-sumi/70 sm:text-xs">
                  用空白本計時刷題，克服考場上的閱讀速度與畫卡焦慮。
                </p>
              </RetroCard>
              <RetroCard shadow="sm" className="p-2.5 text-center sm:p-3">
                <div className="text-xl sm:text-2xl">📖</div>
                <h4 className="mt-1 font-display text-xs font-bold sm:text-sm">一本隨身錯題本</h4>
                <p className="mt-0.5 text-[10.5px] leading-relaxed text-paper-sumi/70 sm:text-xs">
                  訂正本自帶手寫錯題欄，考前 30 分鐘只需看這本自己的盲點筆記。
                </p>
              </RetroCard>
              <RetroCard shadow="sm" className="p-2.5 text-center sm:p-3">
                <div className="text-xl sm:text-2xl">📱</div>
                <h4 className="mt-1 font-display text-xs font-bold sm:text-sm">iPad / 紙本雙通</h4>
                <p className="mt-0.5 text-[10.5px] leading-relaxed text-paper-sumi/70 sm:text-xs">
                  向量高清無損，GoodNotes 翻頁無卡頓，也能列印帶入考場。
                </p>
              </RetroCard>
            </div>
          </div>

          {/* 底部行動呼籲 CTA */}
          <div className="mt-5 rounded-xl border-2 border-paper-sumi bg-paper-butter p-4 text-center sm:mt-6 sm:p-6">
            <h3 className="font-display text-base font-black sm:text-xl md:text-2xl">
              準備好用 500 題手帳題本征服 {currentQuizProd.upper} 了嗎？
            </h3>
            <p className="mx-auto mt-1.5 max-w-lg text-xs leading-relaxed text-paper-sumi/80 sm:text-sm">
              贊助日檢手帖，立即獲取 <strong>{currentQuizProd.title}</strong>（含實戰空白題本 ＋ 逐題手寫風詳解訂正手帳雙 PDF 檔案）。付款後系統自動寄送下載連結，永久離線複習！
            </p>
            <div className="mt-4 flex flex-col items-center justify-center gap-2.5 sm:flex-row sm:gap-3">
              <a
                href="https://buymeacoffee.com/chiaoban/extras"
                target="_blank"
                rel="noreferrer"
                className="btn-retro w-full sm:w-auto !bg-paper-sumi !text-white !border-paper-sumi px-5 py-2.5 text-xs sm:text-sm md:text-base font-black shadow-retro-md hover:!bg-paper-card hover:!text-paper-sumi transition-all"
              >
                <span>🛒 立即購買 {currentQuizProd.upper} 題本套組（{currentQuizProd.priceUsd}）</span>
                <span className="font-mono">→</span>
              </a>
              <button
                type="button"
                onClick={() => handleLevelChange('all')}
                className="btn-retro w-full sm:w-auto !bg-white px-4 py-2.5 text-xs sm:text-sm font-bold text-paper-sumi shadow-retro-sm"
              >
                👑 看看 N1～N5 全真 2,500 題終身典藏包 ($24.99)
              </button>
            </div>
            <div className="mt-3 text-center">
              <Link
                to={selectedLevel === 'all' ? '/quiz/n2' : `/quiz/${selectedLevel}`}
                className="font-mono text-xs font-bold text-paper-sumi/80 hover:text-[#ff6b35] underline underline-offset-4"
              >
                👉 想要直接在線上免費刷題？前往 {currentQuizProd.upper} 線上精華題庫（150 題）→
              </Link>
            </div>
          </div>

        </div>
      )}

      {/* ─────────────────────────────────────────────────────────────
       * 情況 B：【教材系列】展示主卡片（Anki + 講義）
       * ──────────────────────────────────────────────────────────── */}
      {activeLine === 'textbook' && (
        <div className="mt-4 rounded-2xl border-2 border-paper-sumi bg-paper-card p-3.5 shadow-retro sm:mt-6 sm:border-3 sm:p-6 sm:shadow-retro-lg md:p-8">
          
          {/* 產品頭部與價格 */}
          <div className="flex flex-col gap-3 border-b-2 border-dashed border-paper-sumi pb-4 sm:pb-5 md:flex-row md:items-center md:justify-between">
            <div>
              <div className="flex items-center gap-2 sm:gap-3">
                <span
                  className="rounded-lg border-2 border-paper-sumi px-2 py-0.5 font-mono text-xs font-black text-paper-card sm:px-3 sm:py-1 sm:text-sm"
                  style={{ backgroundColor: currentTextbookProd.color }}
                >
                  {currentTextbookProd.upper}
                </span>
                <h2 className="font-display text-lg font-black sm:text-2xl md:text-3xl">{currentTextbookProd.title}</h2>
              </div>
              <p className="mt-1 text-xs font-bold text-paper-sumi/70 sm:mt-1.5 sm:text-sm">{currentTextbookProd.subTitle}</p>
            </div>

            <div className="flex flex-row items-center justify-between gap-3 pt-2 sm:pt-0 md:flex-col md:items-end md:justify-center md:gap-2 md:pt-0 shrink-0">
              <div className="flex items-baseline gap-1.5 sm:gap-2">
                <span className="font-display text-2xl font-black text-paper-sumi sm:text-3xl md:text-4xl">{currentTextbookProd.priceUsd}</span>
                <span className="font-mono text-xs font-bold text-paper-sumi/60">{currentTextbookProd.priceTwdApprox}</span>
              </div>
              <a
                href="https://buymeacoffee.com/chiaoban/extras"
                target="_blank"
                rel="noreferrer"
                className="btn-retro !bg-paper-butter !px-4 !py-2 sm:!px-5 sm:!py-2.5 text-xs sm:text-sm font-black text-paper-sumi shadow-retro hover:scale-[1.02] active:scale-95 transition-all whitespace-nowrap"
              >
                <span>🛒 立即購買套組</span>
                <span className="font-mono">→</span>
              </a>
            </div>
          </div>

          {/* 4 大指標 */}
          <div className="mt-4 grid grid-cols-2 gap-2 sm:mt-5 sm:grid-cols-4 sm:gap-3">
            <div className="rounded-xl border border-paper-sumi/25 bg-paper-canvas p-2.5 text-center sm:p-3">
              <div className="font-mono text-base font-black text-paper-sumi sm:text-xl">{currentTextbookProd.stats.cards}</div>
              <div className="text-[11px] font-bold text-paper-sumi/60">Anki 智慧字卡</div>
            </div>
            <div className="rounded-xl border border-paper-sumi/25 bg-paper-canvas p-2.5 text-center sm:p-3">
              <div className="font-mono text-base font-black text-paper-sumi sm:text-xl">{currentTextbookProd.stats.grammar}</div>
              <div className="text-[11px] font-bold text-paper-sumi/60">文法公式清單</div>
            </div>
            <div className="rounded-xl border border-paper-sumi/25 bg-paper-canvas p-2.5 text-center sm:p-3">
              <div className="font-mono text-base font-black text-paper-sumi sm:text-xl">{currentTextbookProd.stats.vocab}</div>
              <div className="text-[11px] font-bold text-paper-sumi/60">必背高頻單字</div>
            </div>
            <div className="rounded-xl border border-paper-sumi/25 bg-paper-canvas p-2.5 text-center sm:p-3">
              <div className="font-mono text-base font-black text-paper-sumi sm:text-xl">{currentTextbookProd.stats.quizzes}</div>
              <div className="text-[11px] font-bold text-paper-sumi/60">隨堂測驗題</div>
            </div>
          </div>

          {/* 左右分欄展示：左欄 Anki 卡片翻牌，右欄 A4 手冊預覽 */}
          <div className="mt-5 grid grid-cols-1 gap-4 lg:grid-cols-2 lg:gap-6">
            <div className="flex flex-col justify-between rounded-xl border-2 border-paper-sumi bg-paper-canvas p-3 sm:p-4">
              <div>
                <div className="flex items-center justify-between">
                  <h3 className="font-display text-xs font-black sm:text-sm">📱 Anki 智慧字卡真實樣式</h3>
                  <span className="font-mono text-[10.5px] text-paper-sumi/60">點擊卡片翻面看解析</span>
                </div>

                {curTbSample && (
                  <div
                    onClick={() => setIsCardFlipped((v) => !v)}
                    className="mt-3 cursor-pointer rounded-xl border-2 border-paper-sumi bg-white p-4 shadow-retro-sm transition-all hover:scale-[1.01] sm:p-5"
                  >
                    <div className="flex items-center justify-between border-b border-paper-sumi/15 pb-2">
                      <span className="rounded bg-paper-butter px-2 py-0.5 font-mono text-[10px] font-black text-paper-sumi">
                        {curTbSample.title} ｜ {curTbSample.category}
                      </span>
                      <span className="font-mono text-[11px] font-bold text-paper-sumi/60">
                        {isCardFlipped ? '【背面：公式詳解】' : '【正面：考點回想】'}
                      </span>
                    </div>

                    {!isCardFlipped ? (
                      <div className="my-6 text-center">
                        <div className="font-serif text-2xl font-black text-paper-sumi sm:text-3xl">
                          {curTbSample.front}
                        </div>
                        <div className="mt-2 text-xs font-bold text-[#ff6b35]">
                          💡 {curTbSample.promptTip}
                        </div>
                      </div>
                    ) : (
                      <div className="my-3 space-y-2 text-xs leading-relaxed text-paper-sumi">
                        <div
                          className="font-serif text-lg font-black"
                          dangerouslySetInnerHTML={{ __html: curTbSample.ruby }}
                        />
                        <div className="font-mono text-[11px] text-paper-sumi/60">{curTbSample.subMeta}</div>
                        <div className="border-t border-paper-sumi/15 pt-2">
                          <strong>中文含義：</strong>{curTbSample.meaning}
                        </div>
                        {curTbSample.formula && (
                          <div className="rounded bg-paper-canvas p-1.5 font-mono">
                            <strong>公式：</strong>{curTbSample.formula}
                          </div>
                        )}
                        <div>
                          <strong>例句：</strong>{curTbSample.exampleJa}
                          <div className="text-paper-sumi/65">{curTbSample.exampleZh}</div>
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>

              <div className="mt-3 flex items-center justify-between border-t border-paper-sumi/15 pt-2">
                <span className="font-mono text-xs text-paper-sumi/60">
                  樣張 { (activeTextbookSampleIdx % tbSamples.length) + 1 } / { tbSamples.length }
                </span>
                <button
                  type="button"
                  onClick={() => {
                    setActiveTextbookSampleIdx((i) => (i + 1) % tbSamples.length);
                    setIsCardFlipped(false);
                  }}
                  className="rounded-lg border border-paper-sumi bg-paper-card px-2.5 py-1 font-display text-xs font-bold hover:bg-paper-butter"
                >
                  換下一張 ›
                </button>
              </div>
            </div>

            {/* 右欄：A4 講義預覽 */}
            <div className="flex flex-col justify-between rounded-xl border-2 border-paper-sumi bg-paper-canvas p-3 sm:p-4">
              <div>
                <div className="flex items-center justify-between">
                  <h3 className="font-display text-xs font-black sm:text-sm">📑 A4 考場速查手冊線上試閱</h3>
                  <span className="rounded bg-paper-butter px-2 py-0.5 font-mono text-[10px] font-bold sm:text-[11px]">
                    日雜 FUDGE 排版
                  </span>
                </div>
                <p className="mt-0.5 text-[11px] text-paper-sumi/60">
                  可在框內直接滑動翻閱各章節公式與排版：
                </p>

                <div className="relative mt-2.5 h-[320px] w-full max-w-full overflow-hidden rounded-xl border-2 border-paper-sumi bg-white shadow-retro-sm sm:h-[380px] md:h-[420px]">
                  <iframe
                    src={currentTextbookProd.handbookUrl}
                    title={`${currentTextbookProd.upper} A4 講義手冊試閱`}
                    className="h-full w-full border-0 bg-[#faf7f2]"
                    style={{ width: '100%', minWidth: '100%', maxWidth: '100%' }}
                    loading="lazy"
                  />
                </div>
              </div>

              <div className="mt-2.5 flex flex-col gap-1 text-[11px] sm:flex-row sm:items-center sm:justify-between sm:text-xs">
                <span className="text-paper-sumi/60">💡 支援 iPad GoodNotes 筆記或 A4 列印</span>
                <a
                  href={currentTextbookProd.handbookUrl}
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center gap-1 font-display font-bold underline decoration-2 underline-offset-4 hover:text-level"
                >
                  🔍 開啟全頁高解析 A4 講義【精華試閱版】↗
                </a>
              </div>
            </div>
          </div>

          {/* 包含內容清單 */}
          <div className="mt-5 rounded-xl border-2 border-paper-sumi bg-paper-canvas p-3 sm:p-4">
            <h3 className="font-display text-xs font-black sm:text-sm">
              📦 {currentTextbookProd.title} 包含完整內容：
            </h3>
            <ul className="mt-2 space-y-1 text-xs text-paper-sumi/85 sm:text-sm">
              {currentTextbookProd.features.map((feat, idx) => (
                <li key={idx} className="flex items-start gap-1.5">
                  <span className="font-bold text-level">✔</span>
                  <span>{feat}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* 底部行動呼籲 CTA */}
          <div className="mt-5 rounded-xl border-2 border-paper-sumi bg-paper-butter p-4 text-center sm:mt-6 sm:p-6">
            <h3 className="font-display text-base font-black sm:text-xl md:text-2xl">
              準備好一次通過 {currentTextbookProd.upper} 了嗎？
            </h3>
            <p className="mx-auto mt-1.5 max-w-lg text-xs leading-relaxed text-paper-sumi/80 sm:text-sm">
              贊助日檢手帖，立即獲取完整 <strong>{currentTextbookProd.title}</strong>（含 Anki 逐字振假名字卡包 ＋ FUDGE 日雜風 A4 講義手冊）。付款後系統自動寄送下載連結，永久離線複習！
            </p>
            <div className="mt-4 flex flex-col items-center justify-center gap-2.5 sm:flex-row sm:gap-3">
              <a
                href="https://buymeacoffee.com/chiaoban/extras"
                target="_blank"
                rel="noreferrer"
                className="btn-retro w-full sm:w-auto !bg-paper-sumi !text-white !border-paper-sumi px-5 py-2.5 text-xs sm:text-sm md:text-base font-black shadow-retro-md hover:!bg-paper-card hover:!text-paper-sumi transition-all"
              >
                <span>🛒 立即購買 {currentTextbookProd.upper} 備考套組（{currentTextbookProd.priceUsd}）</span>
                <span className="font-mono">→</span>
              </a>
              <button
                type="button"
                onClick={() => handleLevelChange('all')}
                className="btn-retro w-full sm:w-auto !bg-white px-4 py-2.5 text-xs sm:text-sm font-bold text-paper-sumi shadow-retro-sm"
              >
                👑 看看 N1～N5 終身全套包 ($29.99)
              </button>
            </div>
            <div className="mt-3 text-center">
              <Link
                to={selectedLevel === 'all' ? '/grammar/n3' : `/grammar/${selectedLevel}`}
                className="font-mono text-xs font-bold text-paper-sumi/80 hover:text-level underline underline-offset-4"
              >
                👉 先在線上自學？前往 {currentTextbookProd.upper} 免費線上文法講義 →
              </Link>
            </div>
          </div>

        </div>
      )}
    </div>
  );
}
