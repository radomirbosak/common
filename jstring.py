import unicodedata

hiragana = (
    "ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴ ふぶぷへべぺほぼぽ"
    "まみむめもゃやゅゆょよらりるれろゎわゐゑをんゔゕゖ゙゚゛゜ゝゞゟ"
)

katakana = (
    "゠ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモ"
    "ャヤュユョヨラリルレロヮワヰヱヲンヴヵヶヷヸヹヺ・ーヽヾヿ"
)


_kanji_ranges = ["㐀䶵", "一鿋", "豈頻"]


def _kanji_generator():
    for startchar, stopchar in _kanji_ranges:
        coderange = range(ord(startchar), ord(stopchar) + 1)
        yield from (chr(charcode) for charcode in coderange)


kanji = "".join(_kanji_generator())


hira_start = int("3041", 16)
hira_end = int("3096", 16)
kata_start = int("30a1", 16)

hira_to_kata = dict()
kata_to_hira = dict()
for i in range(hira_start, hira_end + 1):
    hira_to_kata[chr(i)] = chr(i - hira_start + kata_start)
    kata_to_hira[chr(i - hira_start + kata_start)] = chr(i)


def katakana_to_hiragana(text):
    return "".join(kata_to_hira.get(char, char) for char in text)


def visual_len(text):
    WIDTH_MAP = {"W": 2, "Na": 1, "F": 2}
    return sum(WIDTH_MAP[unicodedata.east_asian_width(char)] for char in text)


def fw_ljust(text, width):
    vlen = visual_len(text)
    if vlen >= width:
        return text
    return text + " " * (width - vlen)
