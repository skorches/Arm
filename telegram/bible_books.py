"""
Bible book name mappings - converts abbreviations to full names
"""

import re

# Mapping of abbreviations to full Bible book names
BIBLE_BOOK_ABBREVIATIONS = {
    # Old Testament
    "Gen.": "Genesis",
    "Ex.": "Exodus",
    "Lev.": "Leviticus",
    "Num.": "Numbers",
    "Dt.": "Deuteronomy",
    "Josh.": "Joshua",
    "Jud.": "Judges",
    "Ruth": "Ruth",
    "1 Sam.": "1 Samuel",
    "2 Sam.": "2 Samuel",
    "1 Ki.": "1 Kings",
    "2 Ki.": "2 Kings",
    "1 Chr.": "1 Chronicles",
    "2 Chr.": "2 Chronicles",
    "Ezra": "Ezra",
    "Neh.": "Nehemiah",
    "Est.": "Esther",
    "Job": "Job",
    "Ps.": "Psalms",
    "Prov.": "Proverbs",
    "Eccl.": "Ecclesiastes",
    "Song": "Song of Songs",
    "Isa.": "Isaiah",
    "Jer.": "Jeremiah",
    "Lam.": "Lamentations",
    "Ezek.": "Ezekiel",
    "Dan.": "Daniel",
    "Hos.": "Hosea",
    "Joel": "Joel",
    "Amos": "Amos",
    "Obadiah": "Obadiah",
    "Jonah": "Jonah",
    "Mic.": "Micah",
    "Nahum": "Nahum",
    "Habakkuk": "Habakkuk",
    "Zephaniah": "Zephaniah",
    "Haggai": "Haggai",
    "Zech.": "Zechariah",
    "Malachi": "Malachi",
    
    # New Testament
    "Mt.": "Matthew",
    "Mk.": "Mark",
    "Lk.": "Luke",
    "Jn.": "John",
    "Acts": "Acts",
    "Rom.": "Romans",
    "1 Cor.": "1 Corinthians",
    "2 Cor.": "2 Corinthians",
    "Gal.": "Galatians",
    "Eph.": "Ephesians",
    "Phil": "Philippians",
    "Phil.": "Philippians",
    "Col.": "Colossians",
    "1 Th.": "1 Thessalonians",
    "2 Th.": "2 Thessalonians",
    "1 Tim.": "1 Timothy",
    "2 Tim.": "2 Timothy",
    "Ti.": "Titus",
    "Philemon": "Philemon",
    "Heb.": "Hebrews",
    "Jas.": "James",
    "1 Pet.": "1 Peter",
    "2 Pet.": "2 Peter",
    "1 Jn.": "1 John",
    "2 John": "2 John",
    "3 John": "3 John",
    "Jude": "Jude",
    "Rev.": "Revelation",
}

def expand_bible_reading(reading_text):
    """
    Convert abbreviated Bible book names to full names.
    
    Example:
        "Gen. 1–3; Mt. 1" -> "Genesis 1–3; Matthew 1"
        "Ps. 119:1-88; 1 Cor. 7:20-40" -> "Psalms 119:1-88; 1 Corinthians 7:20-40"
    """
    if not reading_text:
        return reading_text
    
    result = reading_text
    
    # Sort by length (longest first) to avoid partial matches
    # e.g., "1 Sam." should match before "Sam."
    sorted_abbrevs = sorted(BIBLE_BOOK_ABBREVIATIONS.items(), key=lambda x: len(x[0]), reverse=True)
    
    for abbrev, full_name in sorted_abbrevs:
        # Escape special regex characters and match the abbreviation
        # Use lookbehind/lookahead to ensure we match whole abbreviations
        # This handles cases like "1 Sam." vs "Sam." and periods correctly
        escaped_abbrev = re.escape(abbrev)
        # Match abbreviation at word boundary or start, followed by space, semicolon, or end
        pattern = r'(?<!\w)' + escaped_abbrev + r'(?=\s|;|$)'
        result = re.sub(pattern, full_name, result)
    
    return result

