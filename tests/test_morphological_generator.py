"""Tests for the Kokborok morphological generator module."""

import pytest

from tripura_translate import (
    KokborokDictionary,
    KokborokMorphologicalGenerator,
    generate_kokborok_vocabulary,
    transliterate_to_bengali,
)
from tripura_translate.morphological_generator import make_pronunciation_hint


class TestKokborokMorphologicalGenerator:
    @pytest.fixture
    def generator(self) -> KokborokMorphologicalGenerator:
        return KokborokMorphologicalGenerator()

    def test_factory_function(self):
        gen = generate_kokborok_vocabulary()
        assert isinstance(gen, KokborokMorphologicalGenerator)

    def test_generate_verb_paradigms(self, generator: KokborokMorphologicalGenerator):
        paradigms = generator.generate_verb_paradigms("thang", "go")
        assert len(paradigms) >= 30
        forms = [p["kokborok_latin"] for p in paradigms]
        assert "thangkha" in forms
        assert "thangnai" in forms
        assert "thango" in forms
        assert "thangdi" in forms
        assert "thangya" in forms
        assert "thangyakho" in forms
        assert "thangtong" in forms
        assert "thangri" in forms
        assert "thangjak" in forms

    def test_generate_noun_cases(self, generator: KokborokMorphologicalGenerator):
        cases = generator.generate_noun_cases("nok", "house")
        assert len(cases) >= 20
        forms = [c["kokborok_latin"] for c in cases]
        assert "nokrok" in forms
        assert "noko" in forms
        assert "nokno" in forms
        assert "nokni" in forms
        assert "nokbai" in forms
        assert "angni nok" in forms
        assert "nwngni nok" in forms

    def test_transliterate_to_bengali(self):
        assert transliterate_to_bengali("hambai") == "হাম্বাই"
        assert transliterate_to_bengali("khulumkha") == "খুলুমখা"
        assert transliterate_to_bengali("twi") == "তৈ"
        assert len(transliterate_to_bengali("nok")) > 0

    def test_make_pronunciation_hint(self):
        hint = make_pronunciation_hint("khulumkha")
        assert isinstance(hint, str)
        assert len(hint) > 0

    def test_dictionary_one_lakh_vocabulary(self):
        d = KokborokDictionary()
        # Verify total entries is at least 1 lakh (100,000)
        assert d.total_entries >= 100000
        assert d.count() >= 100000

    def test_language_basics_one_lakh_vocabulary(self):
        from tripura_translate import get_default_language_basics
        basics = get_default_language_basics()
        assert basics.total_vocabulary >= 100000
