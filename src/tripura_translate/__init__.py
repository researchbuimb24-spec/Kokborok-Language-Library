"""tripura-translate: A Python library for Kokborok (Tripuri) language processing,
dictionary search, and translation interfaces.
"""

from tripura_translate.dictionary import (
    KokborokDictionary,
    get_default_dictionary,
    search_dictionary,
)
from tripura_translate.exceptions import (
    DependencyMissingError,
    DictionaryEntryNotFoundError,
    EmptyInputError,
    GrammarTopicNotFoundError,
    InvalidLanguageError,
    LanguageBasicsError,
    LiteratureNotFoundError,
    ModelNotFoundError,
    TranslationModelError,
    TranslationNotAvailableError,
    TripuraTranslateError,
    UnsupportedDirectionError,
)
from tripura_translate.language_basics import (
    KokborokLanguageBasics,
    get_alphabet,
    get_basic_phrases,
    get_default_language_basics,
    get_grammar_topic,
    get_language_sources,
    list_grammar_topics,
    list_vocabulary_categories,
    search_vocabulary,
)
from tripura_translate.literature import (
    KokborokLiterature,
    LiteratureItem,
    get_default_literature,
    get_literature,
    list_literature,
    search_literature,
)
from tripura_translate.morphological_generator import (
    KokborokMorphologicalGenerator,
    generate_kokborok_vocabulary,
    transliterate_to_bengali,
)
from tripura_translate.text_processing import (
    analyze_word_structure,
    clean_text,
    detect_script,
    format_kokborok_text,
    process_text,
    remove_tone_markers,
    tokenize_kokborok,
    validate_text,
)
from tripura_translate.translator import (
    BaseTranslator,
    HuggingFaceTranslator,
    TranslationResult,
    Translator,
    VerifiedPhraseTranslator,
    get_default_translator,
    normalize_lang_code,
    translate,
)

__version__ = "0.1.0"
__author__ = "Tripura Translate Contributors"
__license__ = "MIT"

__all__ = [
    # Top-level functions
    "process_text",
    "clean_text",
    "detect_script",
    "validate_text",
    "tokenize_kokborok",
    "analyze_word_structure",
    "remove_tone_markers",
    "format_kokborok_text",
    "search_dictionary",
    "translate",
    "normalize_lang_code",
    "search_literature",
    "list_literature",
    "get_literature",
    "get_alphabet",
    "search_vocabulary",
    "get_grammar_topic",
    "list_grammar_topics",
    "get_basic_phrases",
    "get_language_sources",
    "list_vocabulary_categories",
    # Classes
    "KokborokDictionary",
    "KokborokLiterature",
    "LiteratureItem",
    "KokborokLanguageBasics",
    "KokborokMorphologicalGenerator",
    "Translator",
    "VerifiedPhraseTranslator",
    "HuggingFaceTranslator",
    "BaseTranslator",
    "TranslationResult",
    "generate_kokborok_vocabulary",
    "transliterate_to_bengali",
    "get_default_dictionary",
    "get_default_literature",
    "get_default_language_basics",
    "get_default_translator",
    # Exceptions
    "TripuraTranslateError",
    "EmptyInputError",
    "InvalidLanguageError",
    "UnsupportedDirectionError",
    "DictionaryEntryNotFoundError",
    "LiteratureNotFoundError",
    "LanguageBasicsError",
    "GrammarTopicNotFoundError",
    "TranslationModelError",
    "ModelNotFoundError",
    "DependencyMissingError",
    "TranslationNotAvailableError",
    # Metadata
    "__version__",
]

