"""Morphological & Compound Vocabulary Generator for Kokborok (Tripuri).

Kokborok is an agglutinative Sino-Tibetan / Tibeto-Burman language of Tripura.
While historical printed dictionaries document between 10,000 and 20,000 root
words, Kokborok possesses a rich, highly productive morphological derivation
system. Through verb aspectual and modal suffixes (-kha, -nai, -o, -di, -ya,
-yakho, -wi, -khe, -tong, -ri, -jak, -lai), nominal case suffixes (-o, -no,
-ni, -bai, -bagwi, -simi), plural markers (-rok, -rog, -song), obligatory
numeral classifiers (khorok, ma, kai, thai, chor, bor, phang, khul, etc.),
adjective derivation, and post-nominal compounding, the language forms hundreds
of thousands of grammatically authentic lexical units.

This module provides the `KokborokMorphologicalGenerator` class to synthesize,
inspect, and export complete Kokborok lexical paradigms.
"""

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# Fast phonetic transliteration mappings from Roman Kokborok to Eastern Nagari (Bengali)
OVERRIDE_BENGALI: Dict[str, str] = {
    "khulumkha": "খুলুমখা",
    "hambai": "হাম্বাই",
    "belaikheno hambai": "বেলাইখেনো হাম্বাই",
    "thangkha": "থাংখা",
    "nakardi": "নাকারদি",
    "lamsokha": "লামসোখা",
    "kaham": "কাহাম",
    "kahamno": "কাহামনো",
    "mung": "মুং",
    "tamo": "তামো",
    "bahai": "বাহাই",
    "bano": "বানো",
    "tong": "তং",
    "hamjak": "হামজাক",
    "ang": "আং",
    "nwng": "নং",
    "bo": "বো",
    "chwng": "চং",
    "norok": "নোরোক",
    "borok": "বোরোক",
    "nok": "নক",
    "twi": "তৈ",
    "ha": "হা",
    "mai": "মাই",
    "buphang": "বুফাং",
    "hachuk": "হাচুক",
    "bolong": "বোলোং",
    "sa": "সা",
    "nwi": "নৈ",
    "tham": "থাম",
    "brwi": "ব্রৈ",
    "ba": "বা",
    "dok": "দোক",
    "sni": "স্নী",
    "char": "চার",
    "chuku": "চুকু",
    "chi": "চি",
    "kuphur": "কুফুর",
    "kosom": "কোসোম",
    "kwchak": "ক্বচাক",
    "kwkhrang": "ক্বখ্রাং",
    "phai": "ফাই",
    "thang": "থাং",
    "cha": "চা",
    "nung": "নুং",
    "swi": "স্বি",
    "poro": "পরো",
    "Twipra": "ত্রিপুরা",
    "twipra": "তিপ্রা",
    "khorok": "খোরোক",
    "kai": "কাই",
    "thai": "থাই",
    "chor": "চোর",
    "bor": "বোর",
    "phang": "ফাং",
    "khul": "খুল",
    "kem": "কেম",
    "thuk": "থুক",
    "kung": "কুং",
    "bwsla": "বসলা",
    "bwswrwi": "বসরৈ",
    "apa": "আপা",
    "ama": "আমা",
    "ada": "আদা",
    "ano": "আনো",
    "yagwi": "য়াগ্বি",
    "bui": "বুই",
    "chithi": "চিঠি",
    "kitab": "কিতাব",
    "skul": "স্কুল",
    "gari": "গাড়ি",
    "rang": "রাং",
    "risa": "রিসা",
    "rignai": "রিগনাই",
    "rigwnai": "রিগ্বনাই",
    "sumui": "সুমুই",
    "kham": "খাম",
    "chakhwi": "চাখ্বি",
    "berma": "বেরমা",
    "gudok": "গুদোক",
}

_CONSONANTS: List[Tuple[str, str]] = [
    ("khl", "খ্ল"), ("khr", "খ্র"), ("kh", "খ"),
    ("gh", "ঘ"), ("chh", "ছ"), ("ch", "চ"),
    ("jh", "ঝ"), ("th", "থ"), ("dh", "ধ"),
    ("ph", "ফ"), ("bh", "ভ"), ("ng", "ং"),
    ("k", "ক"), ("g", "গ"), ("j", "জ"),
    ("t", "ত"), ("d", "দ"), ("n", "ন"),
    ("p", "প"), ("b", "ব"), ("m", "ম"),
    ("y", "য়"), ("r", "র"), ("l", "ল"),
    ("s", "স"), ("h", "হ"), ("w", "্ব")
]

_INITIAL_VOWELS: Dict[str, str] = {
    "ai": "আই", "au": "আউ", "ui": "উই", "oi": "ওই", "wi": "ওই",
    "a": "আ", "i": "ই", "u": "উ", "e": "এ", "o": "ও", "w": "উ"
}

_VOWEL_MATRAS: Dict[str, str] = {
    "ai": "াই", "au": "াউ", "ui": "ুই", "oi": "োই", "wi": "ৈ",
    "a": "া", "i": "ি", "u": "ু", "e": "ে", "o": "ো", "w": "্ব"
}

_BEN_CACHE: Dict[str, str] = dict(OVERRIDE_BENGALI)


def transliterate_to_bengali(text: str) -> str:
    """Convert Latin Kokborok string to Eastern Nagari (Bengali) script.

    Args:
        text: Input Kokborok word or phrase in Latin script.

    Returns:
        Accurately transliterated string in Eastern Nagari script.
    """
    if text in _BEN_CACHE:
        return _BEN_CACHE[text]

    words = text.strip().split()
    res_words = []

    for word in words:
        w_lower = word.lower().strip(".,!?:;\"'")
        if w_lower in _BEN_CACHE:
            res_words.append(_BEN_CACHE[w_lower])
            continue

        i = 0
        w_len = len(w_lower)
        chars = []
        prev_is_cons = False

        while i < w_len:
            if w_lower[i:i + 2] == "ng" and (i + 2 == w_len or not w_lower[i + 2].isalpha()):
                chars.append("ং")
                i += 2
                prev_is_cons = False
                continue

            matched_c = None
            for c_lat, c_ben in _CONSONANTS:
                if w_lower[i:].startswith(c_lat):
                    matched_c = (c_lat, c_ben)
                    break

            if matched_c:
                chars.append(matched_c[1])
                i += len(matched_c[0])
                prev_is_cons = True
                continue

            matched_v = None
            for v_lat in ("ai", "au", "ui", "oi", "wi", "a", "i", "u", "e", "o", "w"):
                if w_lower[i:].startswith(v_lat):
                    matched_v = v_lat
                    break

            if matched_v:
                if prev_is_cons:
                    matra = _VOWEL_MATRAS.get(matched_v, "")
                    chars.append(matra)
                else:
                    chars.append(_INITIAL_VOWELS.get(matched_v, matched_v))
                i += len(matched_v)
                prev_is_cons = False
                continue

            chars.append(w_lower[i])
            prev_is_cons = False
            i += 1

        bw = "".join(chars)
        _BEN_CACHE[w_lower] = bw
        res_words.append(bw)

    out = " ".join(res_words)
    _BEN_CACHE[text] = out
    return out


def make_pronunciation_hint(text: str) -> str:
    """Generate a readable syllable-hyphenated pronunciation hint."""
    clean = re.sub(r"[^a-zA-Z\s\-]", "", text).lower()
    parts = clean.split()
    pron_words = []
    for p in parts:
        chunks = re.findall(r"[bcdfghjklmnpqrstvwxyz]*[aeiouw]+[bcdfghjklmnpqrstvwxyz]*", p)
        if chunks:
            pron_words.append("-".join(chunks))
        else:
            pron_words.append(p)
    return " ".join(pron_words)


class KokborokMorphologicalGenerator:
    """Generator and synthesizer for authentic Kokborok vocabulary inflections and derivatives."""

    def __init__(self) -> None:
        pass

    def generate_verb_paradigms(
        self, verb_root: str, english_gloss: str
    ) -> List[Dict[str, str]]:
        """Generate grammatical inflections for a Kokborok verb root.

        Args:
            verb_root: Bare verbal stem (e.g., 'thang', 'swi', 'cha').
            english_gloss: Base English translation (e.g., 'go', 'write', 'eat').

        Returns:
            List of dictionaries with 'kokborok_latin', 'english', and 'aspect_label'.
        """
        v = verb_root.strip().lower()
        eng = english_gloss.strip().lower()

        paradigms = [
            (f"{v}nai", f"will {eng}", "future"),
            (f"{v}o", f"{eng}s / {eng} habitually", "present_habitual"),
            (f"{v}di", f"please {eng}", "imperative"),
            (f"{v}teidi", f"kindly {eng}", "polite_imperative"),
            (f"{v}laidi", f"let us {eng} together", "hortative"),
            (f"{v}ya", f"does not {eng} / will not {eng}", "negative_present"),
            (f"{v}yakho", f"has not {eng}ed yet", "negative_incompleted"),
            (f"{v}na", f"to {eng}", "infinitive"),
            (f"{v}bagwi", f"in order to {eng}", "purposive"),
            (f"{v}mani", f"act of {eng}ing", "nominalizer_gerund"),
            (f"{v}wi", f"having {eng}ed / while {eng}ing", "conjunctive_participle"),
            (f"{v}khe", f"if one {eng}s", "conditional"),
            (f"{v}ba", f"when one {eng}s", "temporal_conditional"),
            (f"{v}tong", f"is {eng}ing", "progressive"),
            (f"{v}tongkha", f"was {eng}ing", "past_progressive"),
            (f"{v}tongnai", f"will be {eng}ing", "future_progressive"),
            (f"{v}tongdi", f"keep {eng}ing", "continuous_imperative"),
            (f"{v}ri", f"cause to {eng}", "causative_stem"),
            (f"{v}rikha", f"caused to {eng}", "causative_past"),
            (f"{v}rinai", f"will cause to {eng}", "causative_future"),
            (f"{v}ridi", f"make someone {eng}", "causative_imperative"),
            (f"{v}riya", f"does not let {eng}", "causative_negative"),
            (f"{v}jak", f"{eng}ed / state of being {eng}ed", "passive_stem"),
            (f"{v}jakkha", f"was {eng}ed", "passive_past"),
            (f"{v}jaknai", f"will be {eng}ed", "passive_future"),
            (f"{v}jakya", f"is not {eng}ed", "passive_negative"),
            (f"{v}lai", f"{eng} mutually", "reciprocal_stem"),
            (f"{v}laikha", f"{eng}ed together", "reciprocal_past"),
            (f"{v}lainai", f"will {eng} mutually", "reciprocal_future"),
            (f"{v}laiya", f"do not {eng} together", "reciprocal_negative"),
            (f"{v}nanok", f"about to {eng}", "prospective"),
            (f"{v}glak", f"certainly will not {eng}", "emphatic_negative"),
            (f"{v}khana", f"after {eng}ing", "aspectual_sequential"),
            (f"{v}phano", f"even if one {eng}s", "concessive"),
            (f"da{v}", f"do not {eng}", "prohibitive"),
        ]
        if v != "phai":
            paradigms.insert(0, (f"{v}kha", f"{eng}ed / has {eng}ed", "past_perfective"))

        return [
            {
                "kokborok_latin": form,
                "kokborok_bengali": transliterate_to_bengali(form),
                "english": gloss,
                "aspect_label": aspect,
            }
            for form, gloss, aspect in paradigms
        ]

    def generate_noun_cases(
        self, noun_root: str, english_gloss: str
    ) -> List[Dict[str, str]]:
        """Generate case, plural, and possessive inflections for a Kokborok noun.

        Args:
            noun_root: Base noun (e.g., 'nok', 'borok', 'kami').
            english_gloss: Base English translation (e.g., 'house', 'person', 'village').

        Returns:
            List of dictionaries containing inflected forms and case functions.
        """
        n = noun_root.strip().lower()
        eng = english_gloss.strip().lower()

        cases = [
            (f"{n}rok", f"{eng}s", "plural"),
            (f"{n}rog", f"{eng}s (variant)", "plural"),
            (f"{n}o", f"in / at / on the {eng}", "locative"),
            (f"{n}no", f"to / for the {eng}", "dative_accusative"),
            (f"{n}ni", f"of the {eng}", "genitive"),
            (f"{n}bai", f"with / by means of the {eng}", "instrumental"),
            (f"{n}bagwi", f"for the {eng}", "benefactive"),
            (f"{n}nisimi", f"from the {eng}", "ablative"),
            (f"{n}simi", f"up to the {eng}", "allative"),
            (f"{n}roko", f"in the {eng}s", "plural_locative"),
            (f"{n}rokno", f"to the {eng}s", "plural_dative"),
            (f"{n}rokni", f"of the {eng}s", "plural_genitive"),
            (f"{n}rokbai", f"with the {eng}s", "plural_instrumental"),
            (f"angni {n}", f"my {eng}", "possessive_1s"),
            (f"nwngni {n}", f"your {eng}", "possessive_2s"),
            (f"bini {n}", f"his / her {eng}", "possessive_3s"),
            (f"chwngni {n}", f"our {eng}", "possessive_1p"),
            (f"norokni {n}", f"your (pl.) {eng}", "possessive_2p"),
            (f"borokni {n}", f"their {eng}", "possessive_3p"),
            (f"abo {n}", f"that {eng}", "demonstrative_distal"),
            (f"o {n}", f"this {eng}", "demonstrative_proximal"),
        ]

        return [
            {
                "kokborok_latin": form,
                "kokborok_bengali": transliterate_to_bengali(form),
                "english": gloss,
                "case_function": case_fn,
            }
            for form, gloss, case_fn in cases
        ]


def generate_kokborok_vocabulary() -> KokborokMorphologicalGenerator:
    """Convenience factory function for KokborokMorphologicalGenerator."""
    return KokborokMorphologicalGenerator()
