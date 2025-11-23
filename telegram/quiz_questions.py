"""
Bible Quiz Questions Database
Multiple choice questions with answers, difficulty levels, and categories
"""

QUIZ_QUESTIONS = [
    # EASY - Old Testament
    {
        "question": "Who built the ark?",
        "options": ["Noah", "Moses", "Abraham", "David"],
        "correct": 0,
        "reference": "Genesis 6:14-22",
        "difficulty": "easy",
        "category": "old_testament"
    },
    {
        "question": "Who was the first man created by God?",
        "options": ["Noah", "Adam", "Abraham", "Moses"],
        "correct": 1,
        "reference": "Genesis 2:7",
        "difficulty": "easy",
        "category": "old_testament"
    },
    {
        "question": "What was the name of the garden where Adam and Eve lived?",
        "options": ["Garden of Gethsemane", "Garden of Eden", "Garden of Babylon", "Garden of Paradise"],
        "correct": 1,
        "reference": "Genesis 2:8",
        "difficulty": "easy",
        "category": "old_testament"
    },
    {
        "question": "Who was thrown into a lions' den?",
        "options": ["Daniel", "David", "Joseph", "Moses"],
        "correct": 0,
        "reference": "Daniel 6:16",
        "difficulty": "easy",
        "category": "old_testament"
    },
    {
        "question": "What was the name of the sea that Moses parted?",
        "options": ["Red Sea", "Dead Sea", "Mediterranean Sea", "Sea of Galilee"],
        "correct": 0,
        "reference": "Exodus 14:21",
        "difficulty": "easy",
        "category": "old_testament"
    },
    {
        "question": "Who was sold into slavery by his brothers?",
        "options": ["Moses", "Joseph", "David", "Daniel"],
        "correct": 1,
        "reference": "Genesis 37:28",
        "difficulty": "easy",
        "category": "old_testament"
    },
    {
        "question": "Who was swallowed by a great fish?",
        "options": ["Moses", "Jonah", "Daniel", "Noah"],
        "correct": 1,
        "reference": "Jonah 1:17",
        "difficulty": "easy",
        "category": "old_testament"
    },
    {
        "question": "What is the first book of the Bible?",
        "options": ["Exodus", "Genesis", "John", "Matthew"],
        "correct": 1,
        "reference": "Genesis",
        "difficulty": "easy",
        "category": "bible_facts"
    },
    {
        "question": "Who was the first king of Israel?",
        "options": ["David", "Saul", "Solomon", "Rehoboam"],
        "correct": 1,
        "reference": "1 Samuel 10:1",
        "difficulty": "easy",
        "category": "old_testament"
    },
    {
        "question": "How many days and nights did it rain during the flood?",
        "options": ["7 days", "40 days", "100 days", "1 year"],
        "correct": 1,
        "reference": "Genesis 7:12",
        "difficulty": "easy",
        "category": "old_testament"
    },
    
    # EASY - New Testament
    {
        "question": "What was the first miracle Jesus performed?",
        "options": ["Healing a blind man", "Turning water into wine", "Walking on water", "Raising Lazarus"],
        "correct": 1,
        "reference": "John 2:1-11",
        "difficulty": "easy",
        "category": "new_testament"
    },
    {
        "question": "What is the shortest verse in the Bible?",
        "options": ["God is love", "Jesus wept", "In the beginning", "The Lord is my shepherd"],
        "correct": 1,
        "reference": "John 11:35",
        "difficulty": "easy",
        "category": "bible_facts"
    },
    {
        "question": "How many disciples did Jesus have?",
        "options": ["10", "12", "15", "20"],
        "correct": 1,
        "reference": "Matthew 10:1-4",
        "difficulty": "easy",
        "category": "new_testament"
    },
    {
        "question": "Who was the mother of Jesus?",
        "options": ["Mary", "Elizabeth", "Sarah", "Ruth"],
        "correct": 0,
        "reference": "Matthew 1:18",
        "difficulty": "easy",
        "category": "new_testament"
    },
    {
        "question": "How many days was Jesus in the tomb before rising?",
        "options": ["1 day", "2 days", "3 days", "7 days"],
        "correct": 2,
        "reference": "Matthew 12:40",
        "difficulty": "easy",
        "category": "new_testament"
    },
    {
        "question": "Who denied Jesus three times?",
        "options": ["Judas", "Peter", "Thomas", "John"],
        "correct": 1,
        "reference": "Matthew 26:69-75",
        "difficulty": "easy",
        "category": "new_testament"
    },
    {
        "question": "What did Jesus feed to 5000 people with just 5 loaves and 2 fish?",
        "options": ["Bread and wine", "Bread and fish", "Manna", "Fish and wine"],
        "correct": 1,
        "reference": "Matthew 14:17-21",
        "difficulty": "easy",
        "category": "new_testament"
    },
    {
        "question": "What is the last book of the Bible?",
        "options": ["Jude", "Revelation", "3 John", "Hebrews"],
        "correct": 1,
        "reference": "Revelation",
        "difficulty": "easy",
        "category": "bible_facts"
    },
    {
        "question": "How many books are in the New Testament?",
        "options": ["27", "39", "66", "73"],
        "correct": 0,
        "reference": "Standard Bible",
        "difficulty": "easy",
        "category": "bible_facts"
    },
    {
        "question": "What was the name of the place where Jesus was crucified?",
        "options": ["Gethsemane", "Golgotha", "Bethlehem", "Nazareth"],
        "correct": 1,
        "reference": "John 19:17",
        "difficulty": "easy",
        "category": "new_testament"
    },
    
    # MEDIUM - Old Testament
    {
        "question": "Who was known as the 'friend of God'?",
        "options": ["Moses", "David", "Abraham", "Noah"],
        "correct": 2,
        "reference": "James 2:23",
        "difficulty": "medium",
        "category": "old_testament"
    },
    {
        "question": "Who was the wisest king of Israel?",
        "options": ["David", "Saul", "Solomon", "Rehoboam"],
        "correct": 2,
        "reference": "1 Kings 3:12",
        "difficulty": "medium",
        "category": "old_testament"
    },
    {
        "question": "What did God create on the first day?",
        "options": ["Light", "Animals", "Man", "Plants"],
        "correct": 0,
        "reference": "Genesis 1:3-5",
        "difficulty": "medium",
        "category": "old_testament"
    },
    {
        "question": "Who wrote most of the Psalms?",
        "options": ["Solomon", "David", "Moses", "Asaph"],
        "correct": 1,
        "reference": "Various Psalms",
        "difficulty": "medium",
        "category": "old_testament"
    },
    {
        "question": "What was the name of the giant that David defeated?",
        "options": ["Goliath", "Og", "Nimrod", "Sihon"],
        "correct": 0,
        "reference": "1 Samuel 17:50",
        "difficulty": "medium",
        "category": "old_testament"
    },
    {
        "question": "Who was the prophet that anointed David as king?",
        "options": ["Elijah", "Elisha", "Samuel", "Nathan"],
        "correct": 2,
        "reference": "1 Samuel 16:13",
        "difficulty": "medium",
        "category": "old_testament"
    },
    {
        "question": "What was the name of Abraham's wife?",
        "options": ["Rebekah", "Sarah", "Rachel", "Leah"],
        "correct": 1,
        "reference": "Genesis 17:15",
        "difficulty": "medium",
        "category": "old_testament"
    },
    {
        "question": "How many plagues did God send to Egypt?",
        "options": ["7", "10", "12", "40"],
        "correct": 1,
        "reference": "Exodus 7-12",
        "difficulty": "medium",
        "category": "old_testament"
    },
    {
        "question": "What was the name of Moses' brother?",
        "options": ["Aaron", "Joshua", "Caleb", "Miriam"],
        "correct": 0,
        "reference": "Exodus 4:14",
        "difficulty": "medium",
        "category": "old_testament"
    },
    {
        "question": "Who was the first high priest of Israel?",
        "options": ["Moses", "Aaron", "Joshua", "Eleazar"],
        "correct": 1,
        "reference": "Exodus 28:1",
        "difficulty": "medium",
        "category": "old_testament"
    },
    {
        "question": "What was the name of the promised land?",
        "options": ["Canaan", "Egypt", "Babylon", "Assyria"],
        "correct": 0,
        "reference": "Genesis 12:5",
        "difficulty": "medium",
        "category": "old_testament"
    },
    {
        "question": "Who interpreted dreams for Pharaoh?",
        "options": ["Moses", "Joseph", "Daniel", "Samuel"],
        "correct": 1,
        "reference": "Genesis 41:25-36",
        "difficulty": "medium",
        "category": "old_testament"
    },
    {
        "question": "What was the name of the river that flowed through the Garden of Eden?",
        "options": ["Jordan", "Nile", "Euphrates", "Tigris"],
        "correct": 2,
        "reference": "Genesis 2:14",
        "difficulty": "medium",
        "category": "old_testament"
    },
    {
        "question": "Who was the father of the 12 tribes of Israel?",
        "options": ["Abraham", "Isaac", "Jacob", "Joseph"],
        "correct": 2,
        "reference": "Genesis 35:22-26",
        "difficulty": "medium",
        "category": "old_testament"
    },
    {
        "question": "What was the name of the mountain where Moses received the Ten Commandments?",
        "options": ["Mount Zion", "Mount Sinai", "Mount Moriah", "Mount Carmel"],
        "correct": 1,
        "reference": "Exodus 19:20",
        "difficulty": "medium",
        "category": "old_testament"
    },
    
    # MEDIUM - New Testament
    {
        "question": "Who wrote most of the New Testament letters?",
        "options": ["Peter", "John", "Paul", "James"],
        "correct": 2,
        "reference": "Various New Testament books",
        "difficulty": "medium",
        "category": "new_testament"
    },
    {
        "question": "Who was the tax collector that became a disciple?",
        "options": ["Matthew", "Mark", "Luke", "John"],
        "correct": 0,
        "reference": "Matthew 9:9",
        "difficulty": "medium",
        "category": "new_testament"
    },
    {
        "question": "What is the 'Golden Rule'?",
        "options": [
            "Love your neighbor as yourself",
            "Do to others as you would have them do to you",
            "Honor your father and mother",
            "You shall not steal"
        ],
        "correct": 1,
        "reference": "Matthew 7:12",
        "difficulty": "medium",
        "category": "new_testament"
    },
    {
        "question": "Who wrote the book of Revelation?",
        "options": ["Paul", "Peter", "John", "James"],
        "correct": 2,
        "reference": "Revelation 1:1",
        "difficulty": "medium",
        "category": "new_testament"
    },
    {
        "question": "Who was the first martyr of the Christian church?",
        "options": ["Paul", "Peter", "Stephen", "James"],
        "correct": 2,
        "reference": "Acts 7:59-60",
        "difficulty": "medium",
        "category": "new_testament"
    },
    {
        "question": "What is the fruit of the Spirit?",
        "options": [
            "Love, joy, peace, patience, kindness, goodness, faithfulness, gentleness, self-control",
            "Faith, hope, love",
            "Wisdom, understanding, knowledge",
            "Righteousness, holiness, purity"
        ],
        "correct": 0,
        "reference": "Galatians 5:22-23",
        "difficulty": "medium",
        "category": "new_testament"
    },
    {
        "question": "Which disciple was known as 'the doubter'?",
        "options": ["Peter", "Thomas", "Judas", "Philip"],
        "correct": 1,
        "reference": "John 20:24-29",
        "difficulty": "medium",
        "category": "new_testament"
    },
    {
        "question": "What was the name of the garden where Jesus prayed before his arrest?",
        "options": ["Garden of Eden", "Garden of Gethsemane", "Garden of Olives", "Garden of Paradise"],
        "correct": 1,
        "reference": "Matthew 26:36",
        "difficulty": "medium",
        "category": "new_testament"
    },
    {
        "question": "How many times did Peter deny Jesus?",
        "options": ["Once", "Twice", "Three times", "Four times"],
        "correct": 2,
        "reference": "Matthew 26:69-75",
        "difficulty": "medium",
        "category": "new_testament"
    },
    {
        "question": "Who was the disciple that Jesus loved?",
        "options": ["Peter", "John", "James", "Andrew"],
        "correct": 1,
        "reference": "John 13:23",
        "difficulty": "medium",
        "category": "new_testament"
    },
    {
        "question": "What was the name of the city where Jesus was born?",
        "options": ["Nazareth", "Bethlehem", "Jerusalem", "Capernaum"],
        "correct": 1,
        "reference": "Matthew 2:1",
        "difficulty": "medium",
        "category": "new_testament"
    },
    {
        "question": "Who baptized Jesus?",
        "options": ["Peter", "John the Baptist", "Philip", "Ananias"],
        "correct": 1,
        "reference": "Matthew 3:13-17",
        "difficulty": "medium",
        "category": "new_testament"
    },
    {
        "question": "What was the name of the man who helped Jesus carry the cross?",
        "options": ["Simon of Cyrene", "Joseph of Arimathea", "Nicodemus", "Lazarus"],
        "correct": 0,
        "reference": "Matthew 27:32",
        "difficulty": "medium",
        "category": "new_testament"
    },
    {
        "question": "How many books did the apostle Paul write?",
        "options": ["10", "13", "15", "21"],
        "correct": 1,
        "reference": "Various New Testament books",
        "difficulty": "medium",
        "category": "bible_facts"
    },
    {
        "question": "What was the name of the woman at the well that Jesus spoke to?",
        "options": ["Mary", "Martha", "Samaritan woman", "Mary Magdalene"],
        "correct": 2,
        "reference": "John 4:7-26",
        "difficulty": "medium",
        "category": "new_testament"
    },
    
    # MEDIUM - Bible Facts
    {
        "question": "What is the longest book in the Bible?",
        "options": ["Genesis", "Psalms", "Isaiah", "Revelation"],
        "correct": 1,
        "reference": "Psalms (150 chapters)",
        "difficulty": "medium",
        "category": "bible_facts"
    },
    {
        "question": "How many books are in the Old Testament?",
        "options": ["27", "39", "66", "73"],
        "correct": 1,
        "reference": "Standard Bible",
        "difficulty": "medium",
        "category": "bible_facts"
    },
    {
        "question": "What are the first three words of the Bible?",
        "options": ["In the beginning", "God created heaven", "Let there be light", "The Lord said"],
        "correct": 0,
        "reference": "Genesis 1:1",
        "difficulty": "medium",
        "category": "bible_facts"
    },
    
    # HARD - Old Testament
    {
        "question": "How many years did the Israelites wander in the wilderness?",
        "options": ["20 years", "30 years", "40 years", "50 years"],
        "correct": 2,
        "reference": "Numbers 14:33",
        "difficulty": "hard",
        "category": "old_testament"
    },
    {
        "question": "What was the name of the prophet who was taken to heaven in a chariot of fire?",
        "options": ["Elisha", "Elijah", "Isaiah", "Jeremiah"],
        "correct": 1,
        "reference": "2 Kings 2:11",
        "difficulty": "hard",
        "category": "old_testament"
    },
    {
        "question": "Who was the king that built the first temple in Jerusalem?",
        "options": ["David", "Saul", "Solomon", "Rehoboam"],
        "correct": 2,
        "reference": "1 Kings 6:1",
        "difficulty": "hard",
        "category": "old_testament"
    },
    {
        "question": "What was the name of the river where Naaman was told to wash?",
        "options": ["Jordan", "Nile", "Euphrates", "Tigris"],
        "correct": 0,
        "reference": "2 Kings 5:10",
        "difficulty": "hard",
        "category": "old_testament"
    },
    {
        "question": "How many years did Methuselah live?",
        "options": ["777 years", "888 years", "969 years", "1000 years"],
        "correct": 2,
        "reference": "Genesis 5:27",
        "difficulty": "hard",
        "category": "old_testament"
    },
    {
        "question": "What was the name of the prophet who married a prostitute?",
        "options": ["Hosea", "Amos", "Micah", "Nahum"],
        "correct": 0,
        "reference": "Hosea 1:2",
        "difficulty": "hard",
        "category": "old_testament"
    },
    {
        "question": "Who was the judge that defeated the Midianites with only 300 men?",
        "options": ["Samson", "Gideon", "Deborah", "Jephthah"],
        "correct": 1,
        "reference": "Judges 7:7",
        "difficulty": "hard",
        "category": "old_testament"
    },
    {
        "question": "What was the name of the valley where David fought Goliath?",
        "options": ["Valley of Elah", "Valley of Jezreel", "Valley of Aijalon", "Kidron Valley"],
        "correct": 0,
        "reference": "1 Samuel 17:2",
        "difficulty": "hard",
        "category": "old_testament"
    },
    {
        "question": "How many years did Solomon reign?",
        "options": ["20 years", "30 years", "40 years", "50 years"],
        "correct": 2,
        "reference": "1 Kings 11:42",
        "difficulty": "hard",
        "category": "old_testament"
    },
    {
        "question": "What was the name of the king who had the handwriting on the wall?",
        "options": ["Nebuchadnezzar", "Belshazzar", "Darius", "Cyrus"],
        "correct": 1,
        "reference": "Daniel 5:5",
        "difficulty": "hard",
        "category": "old_testament"
    },
    {
        "question": "Who was the prophet that was thrown into a cistern?",
        "options": ["Isaiah", "Jeremiah", "Ezekiel", "Daniel"],
        "correct": 1,
        "reference": "Jeremiah 38:6",
        "difficulty": "hard",
        "category": "old_testament"
    },
    {
        "question": "What was the name of the mountain where Elijah challenged the prophets of Baal?",
        "options": ["Mount Sinai", "Mount Zion", "Mount Carmel", "Mount Moriah"],
        "correct": 2,
        "reference": "1 Kings 18:19",
        "difficulty": "hard",
        "category": "old_testament"
    },
    {
        "question": "How many chapters are in the book of Psalms?",
        "options": ["100", "120", "150", "200"],
        "correct": 2,
        "reference": "Psalms",
        "difficulty": "hard",
        "category": "bible_facts"
    },
    {
        "question": "What was the name of the judge who was betrayed by Delilah?",
        "options": ["Gideon", "Samson", "Jephthah", "Barak"],
        "correct": 1,
        "reference": "Judges 16:4-21",
        "difficulty": "hard",
        "category": "old_testament"
    },
    {
        "question": "Who was the king that had a dream about a statue?",
        "options": ["Nebuchadnezzar", "Belshazzar", "Darius", "Cyrus"],
        "correct": 0,
        "reference": "Daniel 2:1",
        "difficulty": "hard",
        "category": "old_testament"
    },
    
    # HARD - New Testament
    {
        "question": "What was the name of the high priest who questioned Jesus?",
        "options": ["Annas", "Caiaphas", "Ananias", "Gamaliel"],
        "correct": 1,
        "reference": "Matthew 26:57",
        "difficulty": "hard",
        "category": "new_testament"
    },
    {
        "question": "How many times did Jesus appear to his disciples after his resurrection?",
        "options": ["3 times", "5 times", "10 times", "Many times"],
        "correct": 3,
        "reference": "Various Gospels and Acts",
        "difficulty": "hard",
        "category": "new_testament"
    },
    {
        "question": "What was the name of the man who was struck blind on the road to Damascus?",
        "options": ["Peter", "Paul", "Barnabas", "Silas"],
        "correct": 1,
        "reference": "Acts 9:3-9",
        "difficulty": "hard",
        "category": "new_testament"
    },
    {
        "question": "Who was the first Gentile convert mentioned in Acts?",
        "options": ["Cornelius", "Lydia", "The Ethiopian eunuch", "Timothy"],
        "correct": 0,
        "reference": "Acts 10:1-48",
        "difficulty": "hard",
        "category": "new_testament"
    },
    {
        "question": "What was the name of the island where Paul was shipwrecked?",
        "options": ["Cyprus", "Crete", "Malta", "Rhodes"],
        "correct": 2,
        "reference": "Acts 28:1",
        "difficulty": "hard",
        "category": "new_testament"
    },
    {
        "question": "How many people were baptized on the Day of Pentecost?",
        "options": ["About 3,000", "About 5,000", "About 10,000", "About 1,000"],
        "correct": 0,
        "reference": "Acts 2:41",
        "difficulty": "hard",
        "category": "new_testament"
    },
    {
        "question": "What was the name of the disciple who replaced Judas?",
        "options": ["Matthias", "Barnabas", "Silas", "Timothy"],
        "correct": 0,
        "reference": "Acts 1:26",
        "difficulty": "hard",
        "category": "new_testament"
    },
    {
        "question": "Who wrote the book of Hebrews?",
        "options": ["Paul", "Unknown", "Peter", "Luke"],
        "correct": 1,
        "reference": "Hebrews (author unknown)",
        "difficulty": "hard",
        "category": "new_testament"
    },
    {
        "question": "What was the name of the prison where Paul and Silas were imprisoned?",
        "options": ["Philippi", "Corinth", "Ephesus", "Thessalonica"],
        "correct": 0,
        "reference": "Acts 16:23",
        "difficulty": "hard",
        "category": "new_testament"
    },
    {
        "question": "How many times is the word 'love' mentioned in 1 Corinthians 13?",
        "options": ["7 times", "9 times", "13 times", "15 times"],
        "correct": 1,
        "reference": "1 Corinthians 13",
        "difficulty": "hard",
        "category": "new_testament"
    },
    {
        "question": "What was the name of the man who was raised from the dead by Peter?",
        "options": ["Lazarus", "Tabitha", "Eutychus", "Dorcas"],
        "correct": 1,
        "reference": "Acts 9:36-41",
        "difficulty": "hard",
        "category": "new_testament"
    },
    {
        "question": "Which Gospel was written by a doctor?",
        "options": ["Matthew", "Mark", "Luke", "John"],
        "correct": 2,
        "reference": "Colossians 4:14",
        "difficulty": "hard",
        "category": "bible_facts"
    },
    {
        "question": "What was the name of the place where Jesus was tempted by Satan?",
        "options": ["Garden of Gethsemane", "Mount of Olives", "Wilderness", "Mount Tabor"],
        "correct": 2,
        "reference": "Matthew 4:1",
        "difficulty": "hard",
        "category": "new_testament"
    },
    {
        "question": "How many times did Jesus predict his death and resurrection?",
        "options": ["Once", "Twice", "Three times", "Four times"],
        "correct": 2,
        "reference": "Matthew 16:21, 17:22-23, 20:17-19",
        "difficulty": "hard",
        "category": "new_testament"
    },
    {
        "question": "What was the name of the man who helped bury Jesus?",
        "options": ["Simon of Cyrene", "Joseph of Arimathea", "Nicodemus", "Lazarus"],
        "correct": 1,
        "reference": "Matthew 27:57-60",
        "difficulty": "hard",
        "category": "new_testament"
    },
]

# Categories
CATEGORIES = {
    "old_testament": "Old Testament",
    "new_testament": "New Testament",
    "bible_facts": "Bible Facts"
}

# Difficulty levels
DIFFICULTIES = ["easy", "medium", "hard"]

def get_random_question(difficulty=None, category=None):
    """Get a random question from the quiz database, optionally filtered by difficulty and/or category"""
    import random
    filtered_questions = QUIZ_QUESTIONS
    
    if difficulty:
        filtered_questions = [q for q in filtered_questions if q.get('difficulty') == difficulty]
    
    if category:
        filtered_questions = [q for q in filtered_questions if q.get('category') == category]
    
    if not filtered_questions:
        # If no questions match filters, return any random question
        return random.choice(QUIZ_QUESTIONS)
    
    return random.choice(filtered_questions)

def get_question_by_index(index):
    """Get a question by its index"""
    if 0 <= index < len(QUIZ_QUESTIONS):
        return QUIZ_QUESTIONS[index]
    return None

def get_total_questions():
    """Get total number of questions"""
    return len(QUIZ_QUESTIONS)

def get_questions_by_difficulty(difficulty):
    """Get all questions of a specific difficulty"""
    return [q for q in QUIZ_QUESTIONS if q.get('difficulty') == difficulty]

def get_questions_by_category(category):
    """Get all questions of a specific category"""
    return [q for q in QUIZ_QUESTIONS if q.get('category') == category]

def get_stats():
    """Get statistics about the question database"""
    stats = {
        'total': len(QUIZ_QUESTIONS),
        'by_difficulty': {},
        'by_category': {}
    }
    
    for difficulty in DIFFICULTIES:
        stats['by_difficulty'][difficulty] = len(get_questions_by_difficulty(difficulty))
    
    for category in CATEGORIES.keys():
        stats['by_category'][category] = len(get_questions_by_category(category))
    
    return stats
