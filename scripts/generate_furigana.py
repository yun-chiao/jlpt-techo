#!/usr/bin/env python3
"""為 src/data/vocabulary/*.json 產生逐字振假名（mono-ruby）對位資料。

問題：單純把整串假名標在整串漢字上（熟語ルビ），遇到「彼女／かのじょ」這種
連續漢字時，讀者無法分辨哪幾個假名屬於哪個漢字。

作法：用 pykakasi 內建的 kanwa 辭典取得「每個漢字的所有可能讀音」，再對每個
單字做回溯搜尋，找出一組能「完全重建原本假名」的逐字拆法，並考慮日文複合詞
的兩種音變：

  - 連濁（rendaku）：後接語素首音濁化，例：ひと＋ひと → ひとびと
  - 促音便（gemination）：前語素尾音 く/き/ち/つ → っ，例：がく＋こう → がっこう

若找不到能完全重建的拆法（例如「明日／あした」這類熟字訓），就保留整組標音，
這正是語言學上正確的處理方式。

產出：在每筆單字加上 `furigana` 欄位，格式為 [[文字, 讀音 or null], ...]。

用法（需要 pykakasi）：
    python3 -m venv /tmp/jpenv
    /tmp/jpenv/bin/pip install pykakasi
    /tmp/jpenv/bin/python scripts/generate_furigana.py
"""

import json
import pathlib
import re
import sys

try:
    from pykakasi.kanji import Kanwa
except ImportError:
    sys.exit('請先安裝 pykakasi：/tmp/jpenv/bin/pip install pykakasi')

VOCAB_DIR = pathlib.Path(__file__).resolve().parent.parent / 'src' / 'data' / 'vocabulary'

# 連濁：清音 → 濁音／半濁音
RENDAKU = {
    'か': 'が', 'き': 'ぎ', 'く': 'ぐ', 'け': 'げ', 'こ': 'ご',
    'さ': 'ざ', 'し': 'じ', 'す': 'ず', 'せ': 'ぜ', 'そ': 'ぞ',
    'た': 'だ', 'ち': 'ぢ', 'つ': 'づ', 'て': 'で', 'と': 'ど',
    'は': 'ば', 'ひ': 'び', 'ふ': 'ぶ', 'へ': 'べ', 'ほ': 'ぼ',
}
HANDAKU = {'は': 'ぱ', 'ひ': 'ぴ', 'ふ': 'ぷ', 'へ': 'ぺ', 'ほ': 'ぽ'}
# 促音便：語素尾音 → っ
SOKUON_TAIL = {'く', 'き', 'ち', 'つ'}

_kanwa = Kanwa()
_reading_cache: dict[str, list[str]] = {}


def is_kanji(ch: str) -> bool:
    code = ord(ch)
    return 0x4E00 <= code <= 0x9FFF or ch in '々ヶヵ'


def to_hiragana(text: str) -> str:
    return ''.join(
        chr(ord(c) - 0x60) if '\u30a1' <= c <= '\u30f6' else c for c in text
    )


def readings_for(ch: str) -> list[str]:
    """回傳單一漢字的所有候選讀音（依 kanwa 辭典順序，常用在前）。"""
    if ch in _reading_cache:
        return _reading_cache[ch]
    bucket = _kanwa.load(ch)  # 辭典沒收錄該字時會回傳 None
    entries = (bucket.get(ch) if bucket else None) or []
    seen: list[str] = []
    for yomi, _tail in entries:
        yomi = to_hiragana(yomi)
        # kanwa 的訓讀含送假名尾碼（例：まなぶ），一併保留，交給比對決定
        if yomi and yomi not in seen:
            seen.append(yomi)
    _reading_cache[ch] = seen
    return seen


def variants(reading: str, *, first: bool, last: bool) -> list[tuple[str, int]]:
    """產生含音變的候選讀音，回傳 (讀音, 加權罰分)；罰分越低越優先。"""
    out: list[tuple[str, int]] = [(reading, 0)]
    if not reading:
        return out
    if not first:  # 非首語素才可能連濁
        head = reading[0]
        if head in RENDAKU:
            out.append((RENDAKU[head] + reading[1:], 1))
        if head in HANDAKU:
            out.append((HANDAKU[head] + reading[1:], 2))
    if not last:
        tail = reading[-1]
        if tail in SOKUON_TAIL:  # 促音便：がく＋こう → がっこう
            out.append((reading[:-1] + 'っ', 1))
        if tail == 'う' and len(reading) > 1:  # じゅう＋ふん → じゅっぷん
            out.append((reading[:-1] + 'っ', 2))
        if tail in {'ち', 'つ'} and len(reading) > 1:  # 省略：にち＋ほん → にほん
            out.append((reading[:-1], 2))
    return out



def align_run(chars: str, kana: str, *, okurigana: bool) -> list[tuple[str, str]] | None:
    """把一串連續漢字 chars 與其讀音 kana 做逐字對位，失敗回傳 None。

    okurigana=True 代表這串漢字後面還接著送假名，此時最後一個漢字的讀音
    允許被送假名吃掉尾音（例：気持ち → 持 的辭典讀音「もち」實際只唸「も」）。
    """
    n = len(chars)
    best: list[tuple[list[tuple[str, str]], int]] = []

    def candidates(idx: int, prev_reading: str | None) -> list[tuple[str, int]]:
        ch = chars[idx]
        is_first, is_last = idx == 0, idx == n - 1
        # 疊字符號「々」：沿用前一個漢字的讀音（可連濁），例：時々 → ときどき
        bases = (
            [prev_reading] if ch == '々' and prev_reading else readings_for(ch)
        )
        out: list[tuple[str, int]] = []
        for base in bases:
            for variant, extra in variants(base, first=is_first, last=is_last):
                out.append((variant, extra))
                # 末字後接送假名時，辭典讀音可能含送假名，允許截掉 1～2 個尾音
                if is_last and okurigana:
                    for cut in (1, 2):
                        if len(variant) > cut:
                            out.append((variant[:-cut], 3 + cut))
        return out

    def search(idx: int, pos: int, acc: list[tuple[str, str]], penalty: int) -> None:
        if len(best) > 400:  # 安全上限，避免病態回溯
            return
        if idx == n:
            if pos == len(kana):
                best.append((list(acc), penalty))
            return
        remaining_chars = n - idx - 1
        prev_reading = acc[-1][1] if acc else None
        for variant, extra in candidates(idx, prev_reading):
            end = pos + len(variant)
            # 後面每個漢字至少要留 1 個假名
            if not variant or end + remaining_chars > len(kana):
                continue
            if kana[pos:end] != variant:
                continue
            acc.append((chars[idx], variant))
            search(idx + 1, end, acc, penalty + extra)
            acc.pop()

    search(0, 0, [], 0)
    if not best:
        return None
    # 罰分最低者優先；同分時取假名長度分布最平均的（避免 1 字吃掉大半讀音）
    def spread(seg: list[tuple[str, str]]) -> float:
        lens = [len(r) for _, r in seg]
        avg = sum(lens) / len(lens)
        return sum((x - avg) ** 2 for x in lens)

    best.sort(key=lambda item: (item[1], spread(item[0])))
    return best[0][0]


def build_furigana(kanji: str, kana: str) -> list[list[str | None]] | None:
    """回傳 [[文字, 讀音 or None], ...]；沒有漢字時回傳 None。"""
    if not any(is_kanji(c) for c in kanji):
        return None

    # 先切成「漢字段 / 非漢字段」
    segments: list[tuple[str, bool]] = []
    for ch in kanji:
        flag = is_kanji(ch)
        if segments and segments[-1][1] == flag:
            segments[-1] = (segments[-1][0] + ch, flag)
        else:
            segments.append((ch, flag))

    pattern = '^' + ''.join(
        '(.+)' if flag else f'({re.escape(to_hiragana(text))})'
        for text, flag in segments
    ) + '$'
    match = re.match(pattern, to_hiragana(kana))
    if not match:
        return [[kanji, kana]]  # 整組標音（保底）

    result: list[list[str | None]] = []
    for idx, (text, flag) in enumerate(segments):
        part = match.group(idx + 1)
        if not flag:
            result.append([text, None])
            continue
        if len(text) == 1:
            result.append([text, part])
            continue
        # 這串漢字後面是否緊接著送假名
        has_okurigana = idx + 1 < len(segments)
        aligned = align_run(text, part, okurigana=has_okurigana)
        if aligned:
            result.extend([[c, r] for c, r in aligned])
        else:
            result.append([text, part])  # 熟字訓等：保留整組標音
    return result


def dumps_preserving_style(data: list[dict], original: str) -> str:
    """沿用原檔的排版風格輸出，讓 diff 只顯示真正新增的內容。

    本專案的單字檔有兩種既有風格：
      - n1～n3：每筆單字壓成一行
      - n4／n5：標準 indent=2 展開
    另外不論哪種風格，furigana 陣列一律壓成一行，避免每筆多出十幾行 diff。
    """
    lines = original.splitlines()
    one_line_style = len(lines) > 1 and lines[1].rstrip().endswith('},')

    if one_line_style:
        body = ',\n'.join(
            '  ' + json.dumps(item, ensure_ascii=False, separators=(', ', ': '))
            for item in data
        )
        return f'[\n{body}\n]\n'

    placeholders: dict[str, str] = {}
    for idx, item in enumerate(data):
        if 'furigana' not in item:
            continue
        token = f'@@FURIGANA_{idx}@@'
        placeholders[token] = json.dumps(
            item['furigana'], ensure_ascii=False, separators=(', ', ': ')
        )
        item['furigana'] = token

    text = json.dumps(data, ensure_ascii=False, indent=2)
    for token, compact in placeholders.items():
        text = text.replace(f'"{token}"', compact)
    return text + '\n'


def main() -> None:
    grand_total = grand_mono = grand_group = 0
    for path in sorted(VOCAB_DIR.glob('*.json')):
        original = path.read_text(encoding='utf-8')
        data = json.loads(original)
        mono = group = 0
        for item in data:
            furigana = build_furigana(item['kanji'], item['kana'])
            item.pop('furigana', None)
            if furigana is None:
                continue
            item['furigana'] = furigana
            multi = [seg for seg in furigana if seg[1] and len(seg[0]) > 1]
            if multi:
                group += 1
            else:
                mono += 1
        path.write_text(dumps_preserving_style(data, original), encoding='utf-8')
        total = mono + group
        grand_total += total
        grand_mono += mono
        grand_group += group
        rate = mono / total * 100 if total else 0
        print(f'{path.name}: 含漢字 {total} 筆・逐字對位 {mono}・整組標音 {group} '
              f'（逐字率 {rate:.1f}%）')

    rate = grand_mono / grand_total * 100 if grand_total else 0
    print(f'\n合計：含漢字 {grand_total} 筆・逐字對位 {grand_mono}・'
          f'整組標音 {grand_group}（逐字率 {rate:.1f}%）')


if __name__ == '__main__':
    main()
