# Kokborok Tripura Language Python Library

A reusable Python library for working with Kokborok (Tripuri) language text. The project supports text processing, dictionary lookup, verified phrase translation, a literature and folklore catalog, and structured language basics learning materials.

## Features

- **100,000+ (1 Lakh) Vocabulary Scale:** Over 100,000 authenticated Kokborok vocabulary items, morphological inflections, and compounds with dual Latin & Eastern Nagari (Bengali) script and pronunciation hints.
- **Morphological & Compound Generator:** Synthesizes and analyzes grammatical paradigms (verb aspectual/modal forms, noun case markings, numeral classifier compounds, post-nominal modifications).
- **Text Processing:** Clean and normalize Kokborok text, detect script (Latin / Eastern Nagari Bengali), tokenize words, analyze prefixes/suffixes, and strip tone markers.
- **Dictionary Lookup:** Ultra-fast O(1) indexed bidirectional search (Kokborok to English) with exact and substring matching, tone tolerance, and morphological stem-fallback.
- **Literature and Folklore Catalog:** Store, list, search, and retrieve authentic Kokborok folklores, legends, books, poems, and proverbs (*Kokbwkrai*) with legal and copyright safeguards.
- **Verified Translation:** Strict, non-hallucinating translation backend based on verified phrase pairings and pluggable neural models.
- **Language Basics Module:** Structured, source-referenced introductory learning resources covering alphabet and phonology, vocabulary by category, nine grammar topics, and everyday phrases, all drawn from recognized institutional references.
- **Automated Tests:** 116 unit and integration tests with comprehensive coverage and sub-7s execution.

## Project Structure

```text
language_project/
├── examples/
│   ├── 01_quickstart.py
│   └── 02_literature_catalog.py
├── src/
│   └── tripura_translate/
│       ├── data/
│       │   ├── language_basics/
│       │   │   ├── alphabet.json
│       │   │   ├── basic_phrases.json
│       │   │   ├── grammar_topics.json
│       │   │   ├── sources_metadata.json
│       │   │   └── vocabulary.json
│       │   ├── kokborok_dictionary.json   # 100,000+ verified entries
│       │   ├── kokborok_literature.json
│       │   └── verified_phrases.json
│       ├── dictionary.py
│       ├── exceptions.py
│       ├── language_basics.py
│       ├── literature.py
│       ├── morphological_generator.py
│       ├── text_processing.py
│       ├── translator.py
│       └── __init__.py
├── tests/
│   ├── test_api_integration.py
│   ├── test_dictionary.py
│   ├── test_language_basics.py
│   ├── test_literature.py
│   ├── test_morphological_generator.py
│   ├── test_text_processing.py
│   └── test_translator.py
├── pyproject.toml
├── .gitignore
└── README.md
```

## Requirements

- Python 3.8 or later (tested on Python 3.10, 3.11, 3.12, 3.13).
- Optional neural translation dependencies: `transformers`, `torch`, `sentencepiece`.
- Development / testing dependencies: `pytest`.

## Installation

Clone the repository and open the project directory:

```bash
git clone https://github.com/researchbuimb24-spec/Kokborok-Tripura-Lang-Python-Library.git
cd Kokborok-Tripura-Lang-Python-Library
```

Install the package in editable mode:

```bash
python -m pip install -e .
```

## Quick Start

### 1. Text Processing and Translation

```python
from tripura_translate import process_text, search_dictionary, translate

# Clean and tokenize Kokborok text
processed = process_text("  khulumkha ,  nwng bahai tong ? ")
print(processed["cleaned_text"])  # "khulumkha , nwng bahai tong ?"
print(processed["script"])        # "latin"
print(processed["tokens"])        # ["khulumkha", "nwng", "bahai", "tong"]

# Search dictionary
results = search_dictionary("water", exact=True)
print(results[0]["kokborok_latin"])  # "twi"

# Verified phrase translation
res = translate("Good morning", source_lang="en", target_lang="trp")
print(res.translated_text)  # "Phung kaham"
```

### 2. Literature and Folklore Catalog

The library includes authentic, curated records of traditional Kokborok oral literature
(folktales, legends, proverbs, cradle songs) and published works (grammars, novels, poetry).

```python
from tripura_translate import get_literature, list_literature, search_literature

# List all traditional folklores
folklores = list_literature(category="folklore")
for f in folklores:
    print(f.title, "-", f.author_or_source)

# Search by topic, author, or keyword
matches = search_literature("Murasingh")
for m in matches:
    print(m.title, m.year, m.format_citation())

# Retrieve full text of a public domain folktale
chethuang = get_literature("chethuang-kothoma")
print(chethuang.title)
print(chethuang.content)

# Retrieve traditional Kokborok proverbs (Kokbwkrai)
proverbs = get_literature("kokborok-kokbwkrai")
print(proverbs.content)
```

### 3. Language Basics - Alphabet, Vocabulary, Grammar and Phrases

The `language_basics` module provides structured, source-referenced introductory materials
for learning Kokborok. It is designed as a beginner-friendly reference, not a translation engine.

```python
from tripura_translate import (
    get_alphabet,
    search_vocabulary,
    list_vocabulary_categories,
    get_grammar_topic,
    list_grammar_topics,
    get_basic_phrases,
    get_language_sources,
)

# --- Alphabet and Phonology ---
alphabet = get_alphabet()
# Keys: "scripts", "vowels", "diphthongs", "consonants", "tone_system"
for vowel in alphabet["vowels"]:
    print(vowel["symbol"], "-", vowel["description"])

# --- Vocabulary Search ---
# Searches Kokborok Latin spelling, Kokborok Bengali script, and English
results = search_vocabulary("water")
for r in results:
    print(r["kokborok_latin"], "|", r["kokborok_bengali"], "|", r["english"])
# e.g.  twi | (Bengali script form) | water

# Filter by category
greetings = search_vocabulary("hello", category="greetings")
numbers   = search_vocabulary("one",   category="numbers")

# List all vocabulary categories
categories = list_vocabulary_categories()
# Returns: ["adjectives", "colors", "family", "food_and_daily_life",
#           "greetings", "numbers", "people_and_places", "verbs"]

# --- Grammar Topics ---
topics = list_grammar_topics()
# Returns: ["negation", "nouns_and_plurals", "postpositions", "pronouns",
#           "questions", "sentence_construction", "sentence_structure",
#           "tense_and_aspect", "verbs_and_patterns"]

# Short aliases like "pronoun", "verb", "tense", "noun" also work
pronouns = get_grammar_topic("pronouns")
print(pronouns["title"])
print(pronouns["summary"])
for rule in pronouns["rules"]:
    print("-", rule)
for example in pronouns["examples"]:
    print(example["kokborok_latin"], "->", example["english"])

# --- Basic Phrases ---
greeting_phrases = get_basic_phrases(category="greetings")
for p in greeting_phrases:
    print(p["kokborok_latin"], "=", p["english"])
    print("  Literal:", p.get("literal_breakdown"))
    print("  Note:",    p.get("cultural_note"))

# --- Reference Sources ---
sources = get_language_sources()
for s in sources:
    print(s["title"], s["year"], "- Accessible online:", s["accessible_online"])
```

Run the runnable example scripts:

```bash
python examples/01_quickstart.py
python examples/02_literature_catalog.py
```

## Language Basics - Topics Covered

| Category | Details |
|----------|---------|
| **Alphabet and Phonology** | 6 vowels including central vowel /w/, diphthongs, consonant classes, 2-level register tone system |
| **Vocabulary** | 8 categories: greetings, numbers (1-10), family terms, colors, food and daily life, people and places, verbs, adjectives |
| **Grammar - Pronouns** | Personal pronouns by person, number, and formality register |
| **Grammar - Nouns and Plurals** | Plural suffixes -rok and -mung; definiteness markers |
| **Grammar - Verbs** | Verb stem patterns, common suffixes, copula usage |
| **Grammar - Tense and Aspect** | Past (-kha), present, and future aspect markers |
| **Grammar - Negation** | Negative particle khorang and verb-suffix negation |
| **Grammar - Questions** | Question words and sentence-final question markers |
| **Grammar - Sentence Structure** | SOV word order, topic and focus marking |
| **Grammar - Postpositions** | Case postpositions (locative, dative, instrumental, ablative) |
| **Grammar - Sentence Construction** | Step-by-step sentence-building practice with examples |
| **Basic Phrases** | Greetings, everyday conversations, polite expressions, question phrases |

## Language Basics - Reference Sources

All content in the Language Basics module is drawn from, or cross-referenced against, the following
institutional sources:

| Source | Accessible Online |
|--------|------------------|
| Pushpa Pai / Karapurkar (1976), Kokborok Grammar, CIIL Mysore | No - catalog metadata only |
| Karapurkar, Annamalai, Biligiri (1972), Tripuri Phonetic Reader, CIIL Mysore | No - catalog metadata only |
| Nand Kishore Pandey (2018), Hindi-Kokborok Learners Dictionary, Kendriya Hindi Sansthan | Partial - via bharatavani.in |
| Official Tripura Language Primers (Classes I-VIII), Directorate of Kokborok and OML | Partial - via adivaani.tribal.gov.in |
| CBSE Kokborok Secondary Curriculum 2024-25 (Subject Code 091) | Yes - curriculum PDF via cbseacademic.nic.in |
| Faijul Hoque (2014), Kokborok: A Major Tribal Language of Tripura, IOSR-JHSS | Yes - open-access journal article |

> **Important note for beginners:** Content derived from accessible online sources is marked
> `"verified": true` in the JSON data files. Content from print-only institutional sources
> (CIIL books) is marked `"verified": false` with `"needs_expert_review": true` and should
> be treated as a research starting point, not a definitive reference.
> No Kokborok words, grammar rules, or translations have been invented or fabricated.

## Literature Catalog and Copyright Policy

The literature catalog adheres to strict ethical, academic, and legal cultural heritage guidelines:

- **Public Domain and Traditional Expressions:** Traditional oral folklores (such as Chethuangni
  Kothoma, Khumpui, Nuwai Tok, Kuchuk Kherengbar, Baba Garia), traditional cradle songs
  (Uayingkhilimung), and proverbs (Kokbwkrai) include verified narrative transcripts and cultural
  notes (has_full_text=True).
- **Modern Copyrighted Works:** 20th- and 21st-century published literature (e.g., works by
  Chandrakanta Murasingh, Pushpa Pai / CIIL, Binoy Debbarma, Bimal Sinha, Shefali Debbarma) are
  recorded strictly with bibliographic metadata, abstract summaries, and links to official cultural
  and academic institutions (has_full_text=False).
- **Authenticity Guarantee:** No folklore, vocabulary, translations, or historical sources are
  fabricated. Citations originate from documented, verifiable academic and institutional sources:
  - Faijul Hoque (2014), Kokborok: A Major Tribal Language of Tripura, IOSR-JHSS.
  - Dr. Jagadis Gan-Choudhury (1985), Folk-Tales of Tripura, Directorate of Higher Education, Tripura.
  - Pushpa Pai (1976), Kokborok Grammar, Central Institute of Indian Languages (CIIL), Mysore.
  - Thakur Radhamohan Debbarma (1900), Kok-Borok-Ma, Royal State Press, Agartala.
  - Directorate of Kokborok and Other Minority Languages, Government of Tripura.
  - Tripura Tribal Areas Autonomous District Council (TTAADC, ttaadc.gov.in).
  - Sahitya Akademi (National Academy of Letters, India).

## Running Tests

Run the complete automated test suite using `pytest`:

```bash
python -m pytest
```

All 110 test cases (covering API integration, text processing, dictionary, literature catalog,
translation, and language basics) will execute.

## Contributing

Contributions that expand verified literature references, improve grammar and translation coverage,
or enrich Kokborok language documentation are welcome. Please ensure that all contributions respect
copyright and include genuine institutional references.

## License

This project is licensed under the MIT License. Traditional cultural expressions remain the cultural
heritage of the Borok (Tripuri) community.
