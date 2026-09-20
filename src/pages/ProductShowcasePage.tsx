import { useState } from 'react';
import { useDocumentTitle } from '../hooks/useDocumentTitle';
import { RetroCard } from '../components/RetroCard';

type LevelKey = 'n5' | 'n4' | 'n3' | 'n2' | 'n1' | 'all';

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
        meaning: '壞掉、故障、破裂（物品自己壞了）',
        exampleJa: '📌 洗濯機が壊れてしまったので、コインランドリーへ行った。',
        exampleZh: '洗衣機壞掉了，所以去了投幣式洗衣店。（⚠️ 他動詞是 壊します）',
      },
      {
        type: 'grammar',
        title: 'N4 文法第6課',
        category: '動作名詞化・人與事區分',
        front: '〜のは…です',
        promptTip: 'きのう来た（　）は田中さんです，為什麼不能選「こと」？',
        ruby: '［動詞普通形］＋ のは ［說明／評價］ です',
        subMeta: '「の」可代指人、物、事；「こと」只能指抽象的事',
        meaning: '把前面的動作變成主題「…的是…」',
        formula: '動詞普通形 ＋ のは [人／物／事] です',
        alert: '代指「人」的時候只能用「の」不能用「こと」！不能說「来たことは田中さんです」。',
        exampleJa: '✅ きのう遅れて来たのは田中さんです。',
        exampleZh: '昨天遲到的人是田中先生。',
      },
    ],
  },
  n5: {
    key: 'n5',
    upper: 'N5',
    color: '#8338ec',
    tint: '#f2e8fd',
    title: '【日檢手帖】JLPT N5 完全備考套組',
    subTitle: '零基礎安心指南・生活招呼、基礎助詞與第一次考日檢的定心丸',
    priceUsd: '$7.99',
    priceTwdApprox: '約 NT$250',
    stats: {
      cards: '712 張智慧字卡',
      grammar: '48 個入門文法',
      vocab: '664 個高頻單字',
      quizzes: '144 題實戰測驗',
    },
    features: [
      '📱 712 張 Anki 智慧字卡：初學者必備逐字振假名標音，完全不用怕看不懂漢字',
      '📑 FUDGE 日雜風 A4 講義手冊：助詞入門、基本句型公式與第一次考場指南',
      '✍️ 支援手機、平板、電腦與列印紙本複習',
    ],
    handbookUrl: '/dist-products/n5/日檢手帖-N5-試閱講義手冊.html',
    samples: [
      {
        type: 'vocab',
        title: 'N5 單字',
        category: '動詞（I類）',
        front: '行きます',
        promptTip: '請回想讀音、ます形變形與常用場所助詞',
        ruby: '<ruby>行<rt>い</rt></ruby>きます',
        subMeta: '/ ikimasu / ｜ 五段動詞',
        meaning: '去、前往（表示朝遠離說話者的方向移動）',
        exampleJa: '📌 毎朝８時に地下鉄で会社へ行きます。',
        exampleZh: '每天早上 8 點搭捷運去公司。',
      },
      {
        type: 'grammar',
        title: 'N5 文法第6課',
        category: '委婉請求與指示',
        front: '〜てください',
        promptTip: '請做…（動詞要用什麼形接續？）',
        ruby: '［動詞て形］＋ ください',
        subMeta: '對上司或長輩可在前面加 すみませんが 緩和語氣',
        meaning: '請…（請對方做某個動作的親切說法）',
        formula: '動詞て形 ＋ ください',
        alert: '不能直接對極高位者使用，職場對客戶要用更高級的「〜ていただけますでしょうか」。',
        exampleJa: '✅ すみませんが、名前をここに書いてください。',
        exampleZh: '不好意思，請在這裡寫下您的名字。',
      },
    ],
  },
  all: {
    key: 'all',
    upper: 'ALL',
    color: '#2b2523',
    tint: '#ffe5a3',
    title: '【日檢手帖】N1～N5 終身全套典藏包',
    subTitle: '全級別大禮包・一次買齊 5 年份自學教材（原價 $52 美金，現省 42%！）',
    priceUsd: '$29.99',
    priceTwdApprox: '約 NT$950',
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
  useDocumentTitle('數位備考套組｜日檢手帖 N1～N5 Anki 牌組＆考場速查手冊');
  const [selectedLevel, setSelectedLevel] = useState<LevelKey>('n3');
  const [activeSampleIdx, setActiveSampleIdx] = useState(0);
  const [isCardFlipped, setIsCardFlipped] = useState(false);
  const [activeHandbookTab, setActiveHandbookTab] = useState<'cover' | 'formula' | 'cards' | 'quizzes' | 'vocab'>('cover');

  const prod = PRODUCTS[selectedLevel];
  const sampleList = selectedLevel === 'all' ? PRODUCTS.n3.samples : prod.samples;
  const currentSample = sampleList[activeSampleIdx % sampleList.length];

  const handleLevelChange = (lvl: LevelKey) => {
    setSelectedLevel(lvl);
    setActiveSampleIdx(0);
    setIsCardFlipped(false);
  };

  return (
    <div className="mx-auto max-w-5xl px-4 py-8 md:py-12">
      {/* 頂部標題 */}
      <div className="text-center">
        <span className="inline-block rounded-lg border-2 border-paper-sumi bg-paper-butter px-3 py-1 font-display text-xs font-black shadow-retro-sm md:text-sm">
          FUDGE / CLUEL 日雜風格・全自學數位教材
        </span>
        <h1 className="mt-4 font-display text-3xl font-black md:text-5xl">
          日檢手帖・獨立分級數位備考套組
        </h1>
        <p className="mx-auto mt-3 max-w-2xl text-sm leading-relaxed text-paper-sumi/75 md:text-base">
          專為喜愛用 <span className="font-bold text-paper-sumi">iPad 平板筆記</span> 與 <span className="font-bold text-paper-sumi">Anki 智慧間隔記憶</span> 的自學者打造。考前不用自己花 40 小時手刻字卡，一次帶走逐字振假名字卡包與 FUDGE 日雜風 A4 考場速查講義！
        </p>
      </div>

      {/* 為什麼數位學習比實體書強大的四大理由 */}
      <div className="mt-8 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4 md:mt-10">
        <RetroCard shadow="sm" className="p-4 text-center">
          <div className="text-3xl">📱</div>
          <h3 className="mt-2 font-display text-base font-bold">iPad / 平板筆記</h3>
          <p className="mt-1 text-xs text-paper-sumi/70">
            向量高解析 PDF，放進 GoodNotes / Notability 放大不失真，隨心畫線做標記。
          </p>
        </RetroCard>
        <RetroCard shadow="sm" className="p-4 text-center">
          <div className="text-3xl">⚡</div>
          <h3 className="mt-2 font-display text-base font-bold">Anki 間隔記憶</h3>
          <p className="mt-1 text-xs text-paper-sumi/70">
            記憶科學演算法，專門在你快忘記時提醒你，每天 15 分鐘勝過死背 2 小時。
          </p>
        </RetroCard>
        <RetroCard shadow="sm" className="p-4 text-center">
          <div className="text-3xl">✈️</div>
          <h3 className="mt-2 font-display text-base font-bold">100% 離線隨身翻</h3>
          <p className="mt-1 text-xs text-paper-sumi/70">
            捷運通勤、飛機上、沒有網路的地方隨時隨地拿出手機刷卡、翻閱講義。
          </p>
        </RetroCard>
        <RetroCard shadow="sm" className="p-4 text-center">
          <div className="text-3xl">🖨️</div>
          <h3 className="mt-2 font-display text-base font-bold">考場紙本隨印隨讀</h3>
          <p className="mt-1 text-xs text-paper-sumi/70">
            進考場手機必須關機！支援一鍵以 A4 格式雙面列印，考前 30 分鐘安心神手冊。
          </p>
        </RetroCard>
      </div>

      {/* 級別切換 Tabs */}
      <div className="mt-10 flex flex-wrap items-center justify-center gap-2.5">
        {(['n5', 'n4', 'n3', 'n2', 'n1', 'all'] as LevelKey[]).map((lvl) => {
          const item = PRODUCTS[lvl];
          const active = selectedLevel === lvl;
          return (
            <button
              key={lvl}
              type="button"
              onClick={() => handleLevelChange(lvl)}
              className={`inline-flex items-center gap-2 rounded-xl border-2 border-paper-sumi px-4 py-2.5 font-display text-sm font-black transition-all ${
                active
                  ? 'bg-paper-sumi text-paper-card shadow-retro'
                  : 'bg-paper-card text-paper-sumi shadow-retro-sm hover:translate-x-[-1px] hover:translate-y-[-1px]'
              }`}
            >
              <span
                className="h-2.5 w-2.5 rounded-full"
                style={{ backgroundColor: item.color }}
              />
              {lvl === 'all' ? '👑 N1～N5 終身典藏包' : `${item.upper} 套組`}
            </button>
          );
        })}
      </div>

      {/* 當前選中產品的展示主卡片 */}
      <div className="mt-6 rounded-2xl border-3 border-paper-sumi bg-paper-card p-6 shadow-retro-lg md:p-8">
        
        {/* 產品頭部與價格 */}
        <div className="flex flex-col gap-4 border-b-2 border-dashed border-paper-sumi pb-6 md:flex-row md:items-center md:justify-between">
          <div>
            <div className="flex items-center gap-3">
              <span
                className="rounded-lg border-2 border-paper-sumi px-3 py-1 font-mono text-sm font-black text-paper-card"
                style={{ backgroundColor: prod.color }}
              >
                {prod.upper}
              </span>
              <h2 className="font-display text-2xl font-black md:text-3xl">{prod.title}</h2>
            </div>
            <p className="mt-2 text-xs font-bold text-paper-sumi/70 md:text-sm">{prod.subTitle}</p>
          </div>

          <div className="flex flex-col items-start gap-1 md:items-end">
            <div className="flex items-baseline gap-2">
              <span className="font-display text-3xl font-black text-paper-sumi md:text-4xl">{prod.priceUsd}</span>
              <span className="font-mono text-xs text-paper-sumi/60">{prod.priceTwdApprox}</span>
            </div>
            <a
              href="https://buymeacoffee.com/chiaoban/shop"
              target="_blank"
              rel="noreferrer"
              className="btn-retro mt-2 inline-flex w-full items-center justify-center gap-2 bg-paper-butter !py-2.5 text-sm font-black md:w-auto"
            >
              🛒 前往商店購買 {prod.upper} 套組 ({prod.priceUsd}) →
            </a>
          </div>
        </div>

        {/* 規格四宮格 */}
        <div className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-4">
          <div className="rounded-xl border border-paper-sumi/30 bg-paper-canvas p-3 text-center">
            <div className="font-display text-base font-black text-paper-sumi">{prod.stats.cards}</div>
            <div className="mt-0.5 text-xs text-paper-sumi/60">Anki 智慧字卡</div>
          </div>
          <div className="rounded-xl border border-paper-sumi/30 bg-paper-canvas p-3 text-center">
            <div className="font-display text-base font-black text-paper-sumi">{prod.stats.grammar}</div>
            <div className="mt-0.5 text-xs text-paper-sumi/60">必考核心句型</div>
          </div>
          <div className="rounded-xl border border-paper-sumi/30 bg-paper-canvas p-3 text-center">
            <div className="font-display text-base font-black text-paper-sumi">{prod.stats.vocab}</div>
            <div className="mt-0.5 text-xs text-paper-sumi/60">逐字振假名單字</div>
          </div>
          <div className="rounded-xl border border-paper-sumi/30 bg-paper-canvas p-3 text-center">
            <div className="font-display text-base font-black text-paper-sumi">{prod.stats.quizzes}</div>
            <div className="mt-0.5 text-xs text-paper-sumi/60">實戰演練測驗</div>
          </div>
        </div>

        {/* 雙欄實體預覽：左邊 Anki 翻牌模擬器，右邊講義手冊預覽 */}
        <div className="mt-8 grid grid-cols-1 gap-6 lg:grid-cols-2">
          
          {/* 左欄：Anki 實體字卡動態翻牌模擬器 */}
          <div className="rounded-xl border-2 border-paper-sumi bg-paper-canvas p-5">
            <div className="flex items-center justify-between">
              <h3 className="font-display text-base font-black">📱 Anki 智慧字卡線上試玩</h3>
              <span className="rounded bg-paper-sumi px-2 py-0.5 font-mono text-xs font-bold text-paper-card">
                範例 {activeSampleIdx + 1} / {sampleList.length}
              </span>
            </div>
            <p className="mt-1 text-xs text-paper-sumi/60">點擊卡片任何地方即可翻面查看背面讀音與詳解：</p>

            {/* 卡片本體（點擊翻面） */}
            <div
              role="button"
              tabIndex={0}
              onClick={() => setIsCardFlipped((v) => !v)}
              onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') setIsCardFlipped((v) => !v); }}
              className="mt-4 flex min-h-[300px] cursor-pointer flex-col justify-between rounded-xl border-2 border-paper-sumi bg-paper-card p-5 shadow-retro transition-transform hover:translate-y-[-2px]"
            >
              {/* 卡片標籤列 */}
              <div className="flex items-center gap-2">
                <span
                  className="rounded px-2 py-0.5 text-[11px] font-black text-paper-card"
                  style={{ backgroundColor: prod.color }}
                >
                  {currentSample.title}
                </span>
                <span className="rounded border border-paper-sumi/30 bg-paper-canvas px-2 py-0.5 text-[11px] font-bold">
                  {currentSample.category}
                </span>
                <span className="ml-auto font-mono text-[10px] text-paper-sumi/40">日檢手帖 NIKKEN TECHO</span>
              </div>

              {/* 正面內容 */}
              {!isCardFlipped ? (
                <div className="my-6 text-center">
                  <div className="font-serif text-3xl font-black text-paper-sumi md:text-4xl">
                    {currentSample.front}
                  </div>
                  <div className="mt-3 font-mono text-xs text-paper-sumi/50">
                    {currentSample.promptTip}
                  </div>
                </div>
              ) : (
                /* 背面內容 */
                <div className="my-3 text-left">
                  <div
                    className="text-center font-serif text-2xl font-black md:text-3xl"
                    dangerouslySetInnerHTML={{ __html: currentSample.ruby }}
                  />
                  <div className="mt-1 text-center font-mono text-xs text-paper-sumi/60">
                    {currentSample.subMeta}
                  </div>

                  <div
                    className="mt-3 rounded-r-lg border-l-4 p-2.5 text-xs font-bold md:text-sm"
                    style={{ borderLeftColor: prod.color, backgroundColor: prod.tint }}
                  >
                    💡 {currentSample.meaning}
                  </div>

                  {currentSample.alert && (
                    <div className="mt-2 rounded border border-amber-400 bg-amber-50 p-2 text-[11.5px] text-amber-900">
                      ⚠️ <strong>考場陷阱提示：</strong>{currentSample.alert}
                    </div>
                  )}

                  <div className="mt-3 rounded border border-paper-sumi/20 bg-paper-canvas p-2.5 text-xs">
                    <div className="font-bold">{currentSample.exampleJa}</div>
                    <div className="mt-0.5 text-paper-sumi/70">{currentSample.exampleZh}</div>
                  </div>
                </div>
              )}

              {/* 翻牌提示列 */}
              <div className="rounded border border-dashed border-paper-sumi/30 bg-paper-canvas py-1 text-center font-mono text-xs font-bold text-paper-sumi/50">
                {isCardFlipped ? '🔄 點擊翻回正面' : '👆 點擊卡片查看背面讀音與解說'}
              </div>
            </div>

            {/* 切換下一張範例按鈕 */}
            <div className="mt-3 flex items-center justify-between text-xs">
              <span className="text-paper-sumi/60">支援手機 AnkiMobile、AnkiDroid 與電腦一鍵匯入</span>
              <button
                type="button"
                onClick={() => {
                  setActiveSampleIdx((i) => (i + 1) % sampleList.length);
                  setIsCardFlipped(false);
                }}
                className="rounded-lg border border-paper-sumi bg-paper-card px-2.5 py-1 font-display font-bold hover:bg-paper-butter"
              >
                換下一張範例卡 ›
              </button>
            </div>
          </div>

          {/* 右欄：A4 講義手冊各章節線上翻閱預覽 */}
          <div className="rounded-xl border-2 border-paper-sumi bg-paper-canvas p-5">
            <div className="flex items-center justify-between">
              <h3 className="font-display text-base font-black">📑 A4 考場速查講義手冊預覽</h3>
              <span className="rounded bg-paper-butter px-2 py-0.5 font-mono text-xs font-bold">
                日雜 FUDGE 排版
              </span>
            </div>
            <p className="mt-1 text-xs text-paper-sumi/60">支援 iPad GoodNotes 手寫做筆記，或以 A4 列印成實體講義：</p>

            {/* 章節切換 Tab */}
            <div className="mt-3 flex flex-wrap gap-1.5">
              {[
                { id: 'cover', label: '📖 雜誌封面' },
                { id: 'formula', label: '📊 公式速查表' },
                { id: 'cards', label: '🔍 深度解構卡' },
                { id: 'quizzes', label: '📝 實戰演練題' },
                { id: 'vocab', label: '🔤 逐字標音單字' },
              ].map((tab) => (
                <button
                  key={tab.id}
                  type="button"
                  onClick={() => setActiveHandbookTab(tab.id as typeof activeHandbookTab)}
                  className={`rounded-md border border-paper-sumi px-2 py-1 text-xs font-bold transition-colors ${
                    activeHandbookTab === tab.id
                      ? 'bg-paper-sumi text-paper-card'
                      : 'bg-paper-card text-paper-sumi hover:bg-paper-butter'
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </div>

            {/* 靜態視覺模擬預覽窗 */}
            <div className="mt-3 overflow-hidden rounded-xl border-2 border-paper-sumi bg-paper-card p-4 shadow-retro-sm">
              {activeHandbookTab === 'cover' && (
                <div className="flex min-h-[220px] flex-col items-center justify-center border-2 border-paper-sumi p-6 text-center">
                  <span className="font-serif text-xs font-bold tracking-widest text-paper-sumi/60">NIKKEN TECHO ・ JLPT {prod.upper}</span>
                  <div
                    className="mt-3 inline-block rounded-lg border-2 border-paper-sumi px-6 py-2 font-mono text-4xl font-black text-paper-card shadow-retro-sm"
                    style={{ backgroundColor: prod.color }}
                  >
                    {prod.upper}
                  </div>
                  <h4 className="mt-3 font-serif text-lg font-black">考場最後 30 分鐘文法公式＆單字速查手冊</h4>
                  <p className="mt-1 text-xs text-paper-sumi/70">{prod.subTitle}</p>
                </div>
              )}

              {activeHandbookTab === 'formula' && (
                <div className="space-y-2 text-xs">
                  <div className="border-b pb-1 font-bold text-paper-sumi/50">第一章：文法公式速查清單（摘錄）</div>
                  <div className="flex items-center justify-between rounded bg-paper-canvas p-1.5 font-mono">
                    <span className="font-bold">第 1 課・〜はおろか</span>
                    <code>[名詞] はおろか、〜も／さえ</code>
                  </div>
                  <div className="flex items-center justify-between rounded bg-paper-canvas p-1.5 font-mono">
                    <span className="font-bold">第 9 課・〜をめぐって</span>
                    <code>[名詞] をめぐって＋爭議動詞</code>
                  </div>
                  <div className="flex items-center justify-between rounded bg-paper-canvas p-1.5 font-mono">
                    <span className="font-bold">第 15 課・〜というと</span>
                    <code>[名詞] というと＋直覺聯想</code>
                  </div>
                  <div className="flex items-center justify-between rounded bg-paper-canvas p-1.5 font-mono">
                    <span className="font-bold">第 28 課・〜わけがない</span>
                    <code>[普通形] わけがない（情理反駁）</code>
                  </div>
                </div>
              )}

              {activeHandbookTab === 'cards' && (
                <div className="space-y-2 text-xs">
                  <div className="border-b pb-1 font-bold text-paper-sumi/50">第二章：文法點完全解析卡片（公式・真例句・陷阱）</div>
                  <div className="rounded-lg border border-paper-sumi/30 p-2.5">
                    <span className="rounded bg-paper-canvas px-1.5 py-0.5 text-[10px] font-bold">第 28 課</span>
                    <strong className="ml-2 font-display text-sm">〜わけがない</strong>
                    <div className="mt-1 font-mono text-[11px] text-paper-sumi/70">🔹 公式：普通形＋わけがない</div>
                    <div className="mt-1.5 rounded bg-amber-50 p-1.5 text-[11px] text-amber-900">
                      ⚠️ 考場陷阱提示：わけがない 強調主觀反駁，はずがない 是客觀推算。
                    </div>
                  </div>
                </div>
              )}

              {activeHandbookTab === 'quizzes' && (
                <div className="space-y-2 text-xs">
                  <div className="border-b pb-1 font-bold text-paper-sumi/50">第三章：實戰測驗題（附選項即答詳解）</div>
                  <div className="rounded border p-2">
                    <p className="font-bold">第 1 題：たまに朝ご飯を（ ___ ）ことがあるので、注意された。</p>
                    <p className="text-paper-sumi/70">(A) 食べて / (B) 食べよう / (C) 食べなかった / (D) 食べない</p>
                    <p className="mt-1 rounded bg-paper-canvas p-1 text-[11px]">
                      正解：<strong>D（食べない）</strong> ｜ 偶爾發生的習慣用ない形＋ことがある。
                    </p>
                  </div>
                </div>
              )}

              {activeHandbookTab === 'vocab' && (
                <div className="space-y-1.5 text-xs">
                  <div className="border-b pb-1 font-bold text-paper-sumi/50">第四章：逐字標音單字手帖（連續漢字等寬底線）</div>
                  <div className="flex items-center justify-between border-b py-1">
                    <span><ruby>受<rt>う</rt></ruby>け<ruby>付<rt>つ</rt></ruby>けます</span>
                    <span className="text-paper-sumi/60">他動詞</span>
                    <strong>受理、接待</strong>
                  </div>
                  <div className="flex items-center justify-between border-b py-1">
                    <span><ruby>壊<rt>こわ</rt></ruby>れます</span>
                    <span className="text-paper-sumi/60">自動詞</span>
                    <strong>壞掉、故障</strong>
                  </div>
                  <div className="flex items-center justify-between py-1">
                    <span><ruby>約<rt>やく</rt></ruby><ruby>束<rt>そく</rt></ruby></span>
                    <span className="text-paper-sumi/60">名詞</span>
                    <strong>約定、諾言</strong>
                  </div>
                </div>
              )}
            </div>

            {/* 前往全螢幕閱讀或列印按鈕 */}
            <div className="mt-4 text-center">
              <a
                href={prod.handbookUrl}
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center gap-1 font-display text-xs font-bold underline decoration-2 underline-offset-4 hover:text-level"
              >
                🔍 開啟全頁高解析 A4 講義【精華試閱版】/ 試閱體驗 ↗
              </a>
            </div>
          </div>

        </div>

        {/* 底部行動呼籲 CTA */}
        <div className="mt-8 rounded-xl border-2 border-paper-sumi bg-paper-butter p-6 text-center">
          <h3 className="font-display text-xl font-black md:text-2xl">
            準備好一次通過 {prod.upper} 了嗎？
          </h3>
          <p className="mx-auto mt-2 max-w-lg text-xs leading-relaxed text-paper-sumi/80 md:text-sm">
            贊助日檢手帖，立即獲取完整 <strong>{prod.title}</strong>（含 Anki 逐字振假名字卡包 ＋ FUDGE 日雜風 A4 講義手冊）。付款後系統自動寄送下載連結，永久離線複習！
          </p>
          <div className="mt-4 flex flex-wrap items-center justify-center gap-3">
            <a
              href="https://buymeacoffee.com/chiaoban/shop"
              target="_blank"
              rel="noreferrer"
              className="btn-retro bg-paper-card text-sm font-black md:text-base"
            >
              🛒 前往商店購買 {prod.upper} 套組 ({prod.priceUsd}) →
            </a>
            <button
              type="button"
              onClick={() => handleLevelChange('all')}
              className="btn-retro text-xs md:text-sm"
            >
              👑 看看 N1～N5 終身全套包 ($29.99)
            </button>
          </div>
        </div>

      </div>
    </div>
  );
}
