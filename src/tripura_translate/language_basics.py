"""Kokborok (Tripuri) Language Basics module.

This module provides structured, authentic learning resources for the Kokborok
language, covering:
1. Alphabet, phonology, and pronunciation guidance (vowels, consonants, tones, scripts).
2. Basic vocabulary categorized into essential daily life domains.
3. Grammatical topics (pronouns, nouns/plurals, verbs, tense/aspect, negation,
   questions, sentence structure, postpositions, sentence construction).
4. Verified conversational and classroom phrases.
5. Reference source bibliography with accessibility status and copyright details.

All content is verified against recognized institutional references:
- Pushpa Pai / Karapurkar (1976), 'Kokborok Grammar', CIIL Mysore.
- Pushpa Karapurkar et al. (1972), 'Tripuri Phonetic Reader', CIIL Mysore.
- Nand Kishore Pandey (2018), 'Hindi-Kokborok Learner's Dictionary', Kendriya Hindi Sansthan / Bharatavani.
- Official Tripura Language Primers (Classes I-VIII), Directorate of Kokborok & OML / Adivaani.
- CBSE Kokborok Secondary Curriculum (2024-25), Subject Code 091.
- Faijul Hoque (2014), 'Kokborok: A Major Tribal Language of Tripura', IOSR-JHSS.
"""

from copy import deepcopy
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from tripura_translate.exceptions import (
    EmptyInputError,
    GrammarTopicNotFoundError,
)
from tripura_translate.text_processing import clean_text, validate_text

_DEFAULT_DATA_DIR = Path(__file__).parent / "data" / "language_basics"
_DEFAULT_BASICS_CACHE: Optional[Dict[str, Any]] = None


class KokborokLanguageBasics:
    """Manages verified learning materials, vocabulary, grammar topics, and alphabet

    guidance for the Kokborok language.
    """

    # Aliases mapping informal or alternate search keys to canonical topic IDs
    _TOPIC_ALIASES: Dict[str, str] = {
        "pronoun": "pronouns",
        "pronouns": "pronouns",
        "borokthai": "pronouns",
        "noun": "nouns_and_plurals",
        "nouns": "nouns_and_plurals",
        "plural": "nouns_and_plurals",
        "plurals": "nouns_and_plurals",
        "nouns_and_plurals": "nouns_and_plurals",
        "nouns_and_plural_forms": "nouns_and_plurals",
        "mungthai": "nouns_and_plurals",
        "verb": "verbs_and_patterns",
        "verbs": "verbs_and_patterns",
        "verbs_and_patterns": "verbs_and_patterns",
        "verb_patterns": "verbs_and_patterns",
        "tangthai": "verbs_and_patterns",
        "tense": "tense_and_aspect",
        "aspect": "tense_and_aspect",
        "tenses": "tense_and_aspect",
        "tense_and_aspect": "tense_and_aspect",
        "sal_halok": "tense_and_aspect",
        "negative": "negation",
        "negation": "negation",
        "khorang_kaphang": "negation",
        "question": "questions",
        "questions": "questions",
        "songmung": "questions",
        "songmung_kok": "questions",
        "sentence": "sentence_structure",
        "sentence_structure": "sentence_structure",
        "word_order": "sentence_structure",
        "sov": "sentence_structure",
        "kok_bwtang": "sentence_structure",
        "postposition": "postpositions",
        "postpositions": "postpositions",
        "case": "postpositions",
        "cases": "postpositions",
        "postpositions_and_cases": "postpositions",
        "kok_baphang": "postpositions",
        "sentence_construction": "sentence_construction",
        "basic_sentence_construction": "sentence_construction",
        "construction": "sentence_construction",
    }

    def __init__(self, data_dir: Optional[Path] = None) -> None:
        """Initialize Kokborok language basics with dataset directory.

        Args:
            data_dir: Optional custom path to language_basics data directory.
        """
        self._data_dir = Path(data_dir) if data_dir else _DEFAULT_DATA_DIR
        self._alphabet: Dict[str, Any] = {}
        self._vocabulary: List[Dict[str, Any]] = []
        self._grammar_topics: Dict[str, Dict[str, Any]] = {}
        self._phrases: List[Dict[str, Any]] = []
        self._sources: List[Dict[str, Any]] = []
        self._categories: Set[str] = set()
        self._load_datasets()

    def _load_datasets(self) -> None:
        """Load and validate all JSON datasets from the data directory."""
        global _DEFAULT_BASICS_CACHE

        if not self._data_dir.exists():
            raise FileNotFoundError(
                f"Kokborok language basics data directory not found at: {self._data_dir}"
            )

        # Fast path: use cached datasets when loading from the default data directory
        if self._data_dir == _DEFAULT_DATA_DIR and _DEFAULT_BASICS_CACHE is not None:
            self._alphabet = _DEFAULT_BASICS_CACHE["alphabet"]
            self._vocabulary = _DEFAULT_BASICS_CACHE["vocabulary"]
            self._grammar_topics = _DEFAULT_BASICS_CACHE["grammar_topics"]
            self._phrases = _DEFAULT_BASICS_CACHE["phrases"]
            self._sources = _DEFAULT_BASICS_CACHE["sources"]
            self._categories = _DEFAULT_BASICS_CACHE["categories"]
            return

        # 1. Alphabet dataset
        alphabet_file = self._data_dir / "alphabet.json"
        if not alphabet_file.exists():
            raise FileNotFoundError(
                f"Missing alphabet dataset file: {alphabet_file}"
            )
        with open(alphabet_file, "r", encoding="utf-8") as f:
            raw_alphabet = json.load(f)
        if not isinstance(raw_alphabet, dict):
            raise ValueError(f"Invalid format in {alphabet_file}: expected JSON object.")
        self._alphabet = raw_alphabet

        # 2. Vocabulary dataset
        vocab_file = self._data_dir / "vocabulary.json"
        if not vocab_file.exists():
            raise FileNotFoundError(
                f"Missing vocabulary dataset file: {vocab_file}"
            )
        with open(vocab_file, "r", encoding="utf-8") as f:
            raw_vocab = json.load(f)
        if not isinstance(raw_vocab, list):
            raise ValueError(f"Invalid format in {vocab_file}: expected JSON list.")
        self._vocabulary = raw_vocab
        self._categories = {
            entry.get("category", "").lower().strip()
            for entry in self._vocabulary
            if entry.get("category")
        }

        # 3. Grammar topics dataset
        grammar_file = self._data_dir / "grammar_topics.json"
        if not grammar_file.exists():
            raise FileNotFoundError(
                f"Missing grammar topics dataset file: {grammar_file}"
            )
        with open(grammar_file, "r", encoding="utf-8") as f:
            raw_grammar = json.load(f)
        if not isinstance(raw_grammar, dict):
            raise ValueError(f"Invalid format in {grammar_file}: expected JSON object.")
        self._grammar_topics = raw_grammar

        # 4. Basic phrases dataset
        phrases_file = self._data_dir / "basic_phrases.json"
        if not phrases_file.exists():
            raise FileNotFoundError(
                f"Missing basic phrases dataset file: {phrases_file}"
            )
        with open(phrases_file, "r", encoding="utf-8") as f:
            raw_phrases = json.load(f)
        if not isinstance(raw_phrases, list):
            raise ValueError(f"Invalid format in {phrases_file}: expected JSON list.")
        self._phrases = raw_phrases

        # 5. Sources metadata dataset
        sources_file = self._data_dir / "sources_metadata.json"
        if not sources_file.exists():
            raise FileNotFoundError(
                f"Missing sources metadata file: {sources_file}"
            )
        with open(sources_file, "r", encoding="utf-8") as f:
            raw_sources = json.load(f)
        if not isinstance(raw_sources, list):
            raise ValueError(f"Invalid format in {sources_file}: expected JSON list.")
        self._sources = raw_sources

        if self._data_dir == _DEFAULT_DATA_DIR:
            _DEFAULT_BASICS_CACHE = {
                "alphabet": self._alphabet,
                "vocabulary": self._vocabulary,
                "grammar_topics": self._grammar_topics,
                "phrases": self._phrases,
                "sources": self._sources,
                "categories": self._categories,
            }

    @property
    def total_vocabulary(self) -> int:
        """Return the total number of verified vocabulary entries."""
        return len(self._vocabulary)

    @property
    def total_phrases(self) -> int:
        """Return the total number of basic phrases."""
        return len(self._phrases)

    @property
    def total_grammar_topics(self) -> int:
        """Return the total number of grammar topics."""
        return len(self._grammar_topics)

    def get_alphabet(self) -> Dict[str, Any]:
        """Return documented alphabet and sound information for Kokborok.

        Returns:
            A deep copy of the alphabet dictionary, containing:
            - 'scripts': writing conventions (Latin, Eastern Nagari / Bengali).
            - 'vowels': the 6 phonemic vowels (/a/, /e/, /i/, /o/, /u/, and 'w' for /ɨ/)
              with articulatory descriptions, pronunciation guidance, and examples.
            - 'diphthongs': recognized diphthongs and vowel glides.
            - 'consonants': consonant classification (stops, affricates, fricatives, nasals, etc.).
            - 'tone_system': 2-tone register structure with minimal pairs.
        """
        return deepcopy(self._alphabet)

    def search_vocabulary(
        self,
        query: str,
        category: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Search verified Kokborok vocabulary across categories.

        Matches case-insensitively against the Kokborok Latin spelling,
        Kokborok Bengali script spelling, and English meaning.

        Args:
            query: The search term (e.g. 'water', 'twi', 'mother', 'ama').
            category: Optional category filter (e.g. 'greetings', 'numbers',
                'family', 'colors', 'food_and_daily_life', 'people_and_places',
                'verbs', 'adjectives').

        Returns:
            A list of matching vocabulary dictionaries.

        Raises:
            EmptyInputError: If query is empty or whitespace only.
        """
        valid_query = validate_text(query, field_name="query").strip().lower()

        normalized_cat = category.strip().lower() if category else None

        exact_matches: List[Dict[str, Any]] = []
        substring_matches: List[Dict[str, Any]] = []

        for entry in self._vocabulary:
            entry_cat = entry.get("category", "").lower().strip()
            if normalized_cat and entry_cat != normalized_cat:
                continue

            kb_latin = entry.get("kokborok_latin", "").lower()
            kb_bengali = entry.get("kokborok_bengali", "").lower()
            eng = entry.get("english", "").lower()

            # Exact match
            if valid_query in (kb_latin, kb_bengali, eng):
                exact_matches.append(dict(entry))
            # Substring match
            elif (
                valid_query in kb_latin
                or valid_query in kb_bengali
                or valid_query in eng
            ):
                substring_matches.append(dict(entry))

        return exact_matches + substring_matches

    def get_grammar_topic(self, topic: str) -> Dict[str, Any]:
        """Retrieve a specific, documented grammar topic.

        Args:
            topic: The topic identifier or name (e.g. 'pronouns', 'nouns_and_plurals',
                'verbs_and_patterns', 'tense_and_aspect', 'negation', 'questions',
                'sentence_structure', 'postpositions', 'sentence_construction').

        Returns:
            A dictionary containing topic title, Kokborok grammatical term,
            summary, rules, authentic examples with grammatical breakdown, and citations.

        Raises:
            EmptyInputError: If topic is empty or whitespace only.
            GrammarTopicNotFoundError: If the requested topic is unrecognized.
        """
        valid_topic = validate_text(topic, field_name="topic").strip().lower()
        cleaned = clean_text(valid_topic).lower()

        canonical_id = self._TOPIC_ALIASES.get(cleaned, cleaned)

        if canonical_id not in self._grammar_topics:
            available = self.list_grammar_topics()
            raise GrammarTopicNotFoundError(topic=topic, available_topics=available)

        return deepcopy(self._grammar_topics[canonical_id])

    def list_grammar_topics(self) -> List[str]:
        """Return a sorted list of all available grammar topic keys."""
        return sorted(list(self._grammar_topics.keys()))

    def get_basic_phrases(
        self,
        category: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Retrieve authentic basic phrases and everyday expressions.

        Args:
            category: Optional filter by category (e.g. 'greetings',
                'everyday_conversations', 'polite_expressions', 'questions').

        Returns:
            A list of phrase dictionaries with Kokborok text, English meaning,
            literal breakdown, cultural notes, and source reference.
        """
        if not category:
            return deepcopy(self._phrases)

        norm_cat = category.strip().lower()
        filtered = [
            deepcopy(p)
            for p in self._phrases
            if p.get("category", "").lower().strip() == norm_cat
        ]
        return filtered

    def get_language_sources(self) -> List[Dict[str, Any]]:
        """Return metadata for all consulted reference books and sources.

        Includes publication information, accessibility status (e.g. whether
        full text is freely online or cataloged metadata only), URLs, verified
        topics, and copyright status.

        Returns:
            A list of source metadata dictionaries.
        """
        return deepcopy(self._sources)

    def list_vocabulary_categories(self) -> List[str]:
        """Return a sorted list of all distinct vocabulary categories."""
        return sorted(list(self._categories))


# Module-level singleton instance for zero-configuration convenience
_DEFAULT_BASICS_INSTANCE: Optional[KokborokLanguageBasics] = None


def get_default_language_basics() -> KokborokLanguageBasics:
    """Return the shared singleton instance of `KokborokLanguageBasics`."""
    global _DEFAULT_BASICS_INSTANCE
    if _DEFAULT_BASICS_INSTANCE is None:
        _DEFAULT_BASICS_INSTANCE = KokborokLanguageBasics()
    return _DEFAULT_BASICS_INSTANCE


def get_alphabet() -> Dict[str, Any]:
    """Retrieve documented Kokborok alphabet, vowels, consonants, and tone info.

    Returns:
        Dictionary with 'scripts', 'vowels', 'diphthongs', 'consonants', and 'tone_system'.
    """
    return get_default_language_basics().get_alphabet()


def search_vocabulary(
    query: str,
    category: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Search verified Kokborok vocabulary across categories.

    Args:
        query: Search keyword in Kokborok or English (e.g. 'water', 'twi', 'hello').
        category: Optional domain filter ('greetings', 'numbers', 'family',
            'colors', 'food_and_daily_life', 'people_and_places', 'verbs', 'adjectives').

    Returns:
        List of matching vocabulary dictionaries.

    Raises:
        EmptyInputError: If query is empty or whitespace only.
    """
    return get_default_language_basics().search_vocabulary(query=query, category=category)


def get_grammar_topic(topic: str) -> Dict[str, Any]:
    """Retrieve documented learning material for a specific Kokborok grammar topic.

    Supported topics include:
    - 'pronouns'
    - 'nouns_and_plurals'
    - 'verbs_and_patterns'
    - 'tense_and_aspect'
    - 'negation'
    - 'questions'
    - 'sentence_structure'
    - 'postpositions'
    - 'sentence_construction'

    Args:
        topic: The topic name or key.

    Returns:
        Dictionary containing topic title, summary, rules, authentic examples, and citations.

    Raises:
        EmptyInputError: If topic is empty or whitespace.
        GrammarTopicNotFoundError: If topic is not recognized.
    """
    return get_default_language_basics().get_grammar_topic(topic=topic)


def list_grammar_topics() -> List[str]:
    """List all available Kokborok grammar topics."""
    return get_default_language_basics().list_grammar_topics()


def get_basic_phrases(category: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieve verified Kokborok basic phrases and everyday expressions.

    Args:
        category: Optional category filter ('greetings', 'everyday_conversations',
            'polite_expressions', 'questions').

    Returns:
        List of phrase dictionaries.
    """
    return get_default_language_basics().get_basic_phrases(category=category)


def get_language_sources() -> List[Dict[str, Any]]:
    """Retrieve the bibliographic catalog and accessibility records of all consulted sources.

    Returns:
        List of source metadata dictionaries with URLs, accessibility status, and verified topics.
    """
    return get_default_language_basics().get_language_sources()


def list_vocabulary_categories() -> List[str]:
    """List all distinct vocabulary categories in the Kokborok basics module."""
    return get_default_language_basics().list_vocabulary_categories()
