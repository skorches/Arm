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
    
    # MORE EASY - Old Testament
    {
        "question": "What did God create on the fourth day?",
        "options": ["Animals", "Sun, moon, and stars", "Plants", "Man"],
        "correct": 1,
        "reference": "Genesis 1:14-19",
        "difficulty": "easy",
        "category": "old_testament"
    },
    {
        "question": "Who was the father of Isaac?",
        "options": ["Noah", "Abraham", "Jacob", "Moses"],
        "correct": 1,
        "reference": "Genesis 21:3",
        "difficulty": "easy",
        "category": "old_testament"
    },
    {
        "question": "What did God provide to the Israelites in the wilderness?",
        "options": ["Bread", "Manna", "Fish", "Fruit"],
        "correct": 1,
        "reference": "Exodus 16:15",
        "difficulty": "easy",
        "category": "old_testament"
    },
    {
        "question": "Who was the strongest man in the Bible?",
        "options": ["Goliath", "Samson", "David", "Gideon"],
        "correct": 1,
        "reference": "Judges 16:17",
        "difficulty": "easy",
        "category": "old_testament"
    },
    {
        "question": "What did David use to defeat Goliath?",
        "options": ["Sword", "Spear", "Sling and stone", "Bow and arrow"],
        "correct": 2,
        "reference": "1 Samuel 17:50",
        "difficulty": "easy",
        "category": "old_testament"
    },
    {
        "question": "Who was the wisest man who ever lived?",
        "options": ["David", "Solomon", "Moses", "Abraham"],
        "correct": 1,
        "reference": "1 Kings 3:12",
        "difficulty": "easy",
        "category": "old_testament"
    },
    {
        "question": "What is the longest book in the Old Testament?",
        "options": ["Genesis", "Psalms", "Isaiah", "Jeremiah"],
        "correct": 1,
        "reference": "Psalms (150 chapters)",
        "difficulty": "easy",
        "category": "bible_facts"
    },
    {
        "question": "How many books are in the Bible?",
        "options": ["60", "66", "70", "73"],
        "correct": 1,
        "reference": "Standard Bible",
        "difficulty": "easy",
        "category": "bible_facts"
    },
    
    # MORE EASY - New Testament
    {
        "question": "What was Jesus' occupation before he started preaching?",
        "options": ["Fisherman", "Carpenter", "Shepherd", "Tax collector"],
        "correct": 1,
        "reference": "Mark 6:3",
        "difficulty": "easy",
        "category": "new_testament"
    },
    {
        "question": "Who was the first person to see Jesus after he rose from the dead?",
        "options": ["Peter", "Mary Magdalene", "John", "Thomas"],
        "correct": 1,
        "reference": "John 20:11-18",
        "difficulty": "easy",
        "category": "new_testament"
    },
    {
        "question": "What is the first book of the New Testament?",
        "options": ["Mark", "Matthew", "Luke", "John"],
        "correct": 1,
        "reference": "Matthew",
        "difficulty": "easy",
        "category": "bible_facts"
    },
    {
        "question": "How many Gospels are in the New Testament?",
        "options": ["3", "4", "5", "6"],
        "correct": 1,
        "reference": "Matthew, Mark, Luke, John",
        "difficulty": "easy",
        "category": "bible_facts"
    },
    {
        "question": "What did Jesus ride into Jerusalem?",
        "options": ["Horse", "Donkey", "Camel", "Chariot"],
        "correct": 1,
        "reference": "Matthew 21:7",
        "difficulty": "easy",
        "category": "new_testament"
    },
    {
        "question": "Who betrayed Jesus?",
        "options": ["Peter", "Judas", "Thomas", "John"],
        "correct": 1,
        "reference": "Matthew 26:14-16",
        "difficulty": "easy",
        "category": "new_testament"
    },
    
    # MORE MEDIUM - Old Testament
    {
        "question": "What was the name of the place where Jacob wrestled with God?",
        "options": ["Peniel", "Bethel", "Gilead", "Mizpah"],
        "correct": 0,
        "reference": "Genesis 32:30",
        "difficulty": "medium",
        "category": "old_testament"
    },
    {
        "question": "How many sons did Jacob have?",
        "options": ["10", "12", "14", "16"],
        "correct": 1,
        "reference": "Genesis 35:22-26",
        "difficulty": "medium",
        "category": "old_testament"
    },
    {
        "question": "What was the name of the golden calf that Aaron made?",
        "options": ["Baal", "Moloch", "No specific name", "Asherah"],
        "correct": 2,
        "reference": "Exodus 32:4",
        "difficulty": "medium",
        "category": "old_testament"
    },
    {
        "question": "Who was the first judge of Israel?",
        "options": ["Gideon", "Samson", "Othniel", "Deborah"],
        "correct": 2,
        "reference": "Judges 3:9",
        "difficulty": "medium",
        "category": "old_testament"
    },
    {
        "question": "What was the name of Ruth's mother-in-law?",
        "options": ["Naomi", "Orpah", "Esther", "Sarah"],
        "correct": 0,
        "reference": "Ruth 1:2",
        "difficulty": "medium",
        "category": "old_testament"
    },
    {
        "question": "Who was the prophet that anointed Saul as king?",
        "options": ["Nathan", "Elijah", "Samuel", "Elisha"],
        "correct": 2,
        "reference": "1 Samuel 10:1",
        "difficulty": "medium",
        "category": "old_testament"
    },
    {
        "question": "What was the name of David's best friend?",
        "options": ["Absalom", "Jonathan", "Joab", "Nathan"],
        "correct": 1,
        "reference": "1 Samuel 18:1",
        "difficulty": "medium",
        "category": "old_testament"
    },
    {
        "question": "How many years did David reign as king?",
        "options": ["30 years", "40 years", "50 years", "60 years"],
        "correct": 1,
        "reference": "1 Kings 2:11",
        "difficulty": "medium",
        "category": "old_testament"
    },
    {
        "question": "What was the name of the queen who visited Solomon?",
        "options": ["Queen of Sheba", "Queen of Egypt", "Queen of Persia", "Queen of Babylon"],
        "correct": 0,
        "reference": "1 Kings 10:1",
        "difficulty": "medium",
        "category": "old_testament"
    },
    {
        "question": "Who was the prophet that was fed by ravens?",
        "options": ["Elisha", "Elijah", "Isaiah", "Jeremiah"],
        "correct": 1,
        "reference": "1 Kings 17:6",
        "difficulty": "medium",
        "category": "old_testament"
    },
    
    # MORE MEDIUM - New Testament
    {
        "question": "What was the name of the man who was raised from the dead by Jesus?",
        "options": ["Lazarus", "Jairus' daughter", "The widow's son", "All of the above"],
        "correct": 3,
        "reference": "John 11:43-44, Mark 5:41-42, Luke 7:14-15",
        "difficulty": "medium",
        "category": "new_testament"
    },
    {
        "question": "Who was the disciple that Jesus called 'the Rock'?",
        "options": ["John", "Peter", "James", "Andrew"],
        "correct": 1,
        "reference": "Matthew 16:18",
        "difficulty": "medium",
        "category": "new_testament"
    },
    {
        "question": "What was the name of the tax collector who climbed a tree to see Jesus?",
        "options": ["Matthew", "Zacchaeus", "Levi", "Simon"],
        "correct": 1,
        "reference": "Luke 19:2-4",
        "difficulty": "medium",
        "category": "new_testament"
    },
    {
        "question": "How many times did Jesus appear to his disciples after his resurrection?",
        "options": ["3 times", "5 times", "10 times", "Many times"],
        "correct": 3,
        "reference": "Various Gospels and Acts",
        "difficulty": "medium",
        "category": "new_testament"
    },
    {
        "question": "What was the name of the place where Jesus ascended to heaven?",
        "options": ["Mount of Olives", "Mount Sinai", "Mount Zion", "Mount Tabor"],
        "correct": 0,
        "reference": "Acts 1:12",
        "difficulty": "medium",
        "category": "new_testament"
    },
    {
        "question": "Who wrote the book of Acts?",
        "options": ["Paul", "Luke", "John", "Peter"],
        "correct": 1,
        "reference": "Acts 1:1",
        "difficulty": "medium",
        "category": "new_testament"
    },
    {
        "question": "What was the name of the first Gentile church?",
        "options": ["Antioch", "Corinth", "Ephesus", "Rome"],
        "correct": 0,
        "reference": "Acts 11:26",
        "difficulty": "medium",
        "category": "new_testament"
    },
    {
        "question": "How many missionary journeys did Paul take?",
        "options": ["2", "3", "4", "5"],
        "correct": 1,
        "reference": "Acts 13-21",
        "difficulty": "medium",
        "category": "new_testament"
    },
    
    # MORE HARD - Old Testament
    {
        "question": "What was the name of the king who had Daniel thrown into the lions' den?",
        "options": ["Nebuchadnezzar", "Belshazzar", "Darius", "Cyrus"],
        "correct": 2,
        "reference": "Daniel 6:16",
        "difficulty": "hard",
        "category": "old_testament"
    },
    {
        "question": "How many years did the Israelites spend in Egypt?",
        "options": ["200 years", "300 years", "400 years", "430 years"],
        "correct": 3,
        "reference": "Exodus 12:40",
        "difficulty": "hard",
        "category": "old_testament"
    },
    {
        "question": "What was the name of the prophet who was thrown into a well?",
        "options": ["Jeremiah", "Ezekiel", "Daniel", "Isaiah"],
        "correct": 0,
        "reference": "Jeremiah 38:6",
        "difficulty": "hard",
        "category": "old_testament"
    },
    {
        "question": "Who was the king that had the handwriting on the wall interpreted?",
        "options": ["Nebuchadnezzar", "Belshazzar", "Darius", "Cyrus"],
        "correct": 1,
        "reference": "Daniel 5:5-28",
        "difficulty": "hard",
        "category": "old_testament"
    },
    {
        "question": "What was the name of the valley where the dry bones came to life?",
        "options": ["Valley of Elah", "Valley of Jezreel", "Valley of Dry Bones", "No specific name"],
        "correct": 3,
        "reference": "Ezekiel 37:1-2",
        "difficulty": "hard",
        "category": "old_testament"
    },
    {
        "question": "How many chapters are in the book of Isaiah?",
        "options": ["60", "66", "70", "72"],
        "correct": 1,
        "reference": "Isaiah (66 chapters)",
        "difficulty": "hard",
        "category": "bible_facts"
    },
    {
        "question": "What was the name of the prophet who married Gomer?",
        "options": ["Hosea", "Amos", "Micah", "Nahum"],
        "correct": 0,
        "reference": "Hosea 1:3",
        "difficulty": "hard",
        "category": "old_testament"
    },
    {
        "question": "Who was the last judge of Israel?",
        "options": ["Samson", "Samuel", "Eli", "Deborah"],
        "correct": 1,
        "reference": "1 Samuel 7:15",
        "difficulty": "hard",
        "category": "old_testament"
    },
    {
        "question": "What was the name of the mountain where Abraham was told to sacrifice Isaac?",
        "options": ["Mount Moriah", "Mount Sinai", "Mount Zion", "Mount Carmel"],
        "correct": 0,
        "reference": "Genesis 22:2",
        "difficulty": "hard",
        "category": "old_testament"
    },
    {
        "question": "How many years did the Israelites wander in the wilderness before entering the Promised Land?",
        "options": ["30 years", "40 years", "50 years", "70 years"],
        "correct": 1,
        "reference": "Numbers 14:33",
        "difficulty": "hard",
        "category": "old_testament"
    },
    
    # MORE HARD - New Testament
    {
        "question": "What was the name of the high priest who questioned Jesus?",
        "options": ["Annas", "Caiaphas", "Ananias", "Gamaliel"],
        "correct": 1,
        "reference": "Matthew 26:57",
        "difficulty": "hard",
        "category": "new_testament"
    },
    {
        "question": "How many times did Peter deny Jesus?",
        "options": ["Once", "Twice", "Three times", "Four times"],
        "correct": 2,
        "reference": "Matthew 26:69-75",
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
        "question": "Who was the first Gentile convert mentioned in Acts?",
        "options": ["Cornelius", "Lydia", "The Ethiopian eunuch", "Timothy"],
        "correct": 0,
        "reference": "Acts 10:1-48",
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
        "question": "How many people were baptized on the Day of Pentecost?",
        "options": ["About 3,000", "About 5,000", "About 10,000", "About 1,000"],
        "correct": 0,
        "reference": "Acts 2:41",
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
        "question": "Who wrote the book of Hebrews?",
        "options": ["Paul", "Unknown", "Peter", "Luke"],
        "correct": 1,
        "reference": "Hebrews (author unknown)",
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
        "question": "How many times is the word 'love' mentioned in 1 Corinthians 13?",
        "options": ["7 times", "9 times", "13 times", "15 times"],
        "correct": 1,
        "reference": "1 Corinthians 13",
        "difficulty": "hard",
        "category": "new_testament"
    },
    
    # EXPANDED COVERAGE - Minor Prophets
    {
        "question": "Which minor prophet's book is the shortest in the Old Testament?",
        "options": ["Obadiah", "Nahum", "Haggai", "Zephaniah"],
        "correct": 0,
        "reference": "Obadiah (1 chapter)",
        "difficulty": "medium",
        "category": "old_testament"
    },
    {
        "question": "Which prophet warned Nineveh about its destruction?",
        "options": ["Jonah", "Nahum", "Habakkuk", "Zephaniah"],
        "correct": 1,
        "reference": "Nahum 1:1",
        "difficulty": "medium",
        "category": "old_testament"
    },
    {
        "question": "Which prophet asked God 'Why do you make me look at injustice?'",
        "options": ["Habakkuk", "Micah", "Nahum", "Zephaniah"],
        "correct": 0,
        "reference": "Habakkuk 1:3",
        "difficulty": "hard",
        "category": "old_testament"
    },
    {
        "question": "Which prophet prophesied about the Day of the Lord?",
        "options": ["Zephaniah", "Haggai", "Malachi", "Obadiah"],
        "correct": 0,
        "reference": "Zephaniah 1:14-18",
        "difficulty": "hard",
        "category": "old_testament"
    },
    {
        "question": "Which prophet encouraged rebuilding the temple?",
        "options": ["Haggai", "Zechariah", "Malachi", "Joel"],
        "correct": 0,
        "reference": "Haggai 1:8",
        "difficulty": "medium",
        "category": "old_testament"
    },
    {
        "question": "Which prophet had visions of a golden lampstand?",
        "options": ["Zechariah", "Daniel", "Ezekiel", "Jeremiah"],
        "correct": 0,
        "reference": "Zechariah 4:2",
        "difficulty": "hard",
        "category": "old_testament"
    },
    {
        "question": "Which prophet asked 'Where is the God of justice?'",
        "options": ["Malachi", "Micah", "Amos", "Hosea"],
        "correct": 0,
        "reference": "Malachi 2:17",
        "difficulty": "hard",
        "category": "old_testament"
    },
    
    # EXPANDED COVERAGE - Wisdom Literature
    {
        "question": "What is the main theme of the book of Ecclesiastes?",
        "options": ["Love", "Wisdom", "Everything is meaningless", "Prophecy"],
        "correct": 2,
        "reference": "Ecclesiastes 1:2",
        "difficulty": "medium",
        "category": "old_testament"
    },
    {
        "question": "Who wrote most of the book of Proverbs?",
        "options": ["David", "Solomon", "Moses", "Isaiah"],
        "correct": 1,
        "reference": "Proverbs 1:1",
        "difficulty": "easy",
        "category": "old_testament"
    },
    {
        "question": "What is the fear of the Lord according to Proverbs?",
        "options": ["The beginning of wisdom", "The end of knowledge", "A burden", "A curse"],
        "correct": 0,
        "reference": "Proverbs 9:10",
        "difficulty": "medium",
        "category": "old_testament"
    },
    {
        "question": "How many friends came to comfort Job?",
        "options": ["2", "3", "4", "5"],
        "correct": 1,
        "reference": "Job 2:11",
        "difficulty": "medium",
        "category": "old_testament"
    },
    {
        "question": "What was the name of Job's wife?",
        "options": ["Not named in the Bible", "Sarah", "Rebekah", "Rachel"],
        "correct": 0,
        "reference": "Job 2:9",
        "difficulty": "hard",
        "category": "old_testament"
    },
    {
        "question": "What is the Song of Solomon also known as?",
        "options": ["Song of Songs", "Song of David", "Song of Love", "Song of Wisdom"],
        "correct": 0,
        "reference": "Song of Solomon 1:1",
        "difficulty": "medium",
        "category": "old_testament"
    },
    {
        "question": "How many chapters are in the book of Proverbs?",
        "options": ["28", "30", "31", "33"],
        "correct": 2,
        "reference": "Proverbs (31 chapters)",
        "difficulty": "hard",
        "category": "bible_facts"
    },
    
    # EXPANDED COVERAGE - Less-Known Books
    {
        "question": "Who was Ruth's husband?",
        "options": ["Boaz", "Mahlon", "Elimelek", "Obed"],
        "correct": 1,
        "reference": "Ruth 1:4",
        "difficulty": "hard",
        "category": "old_testament"
    },
    {
        "question": "What was the name of Esther's cousin who raised her?",
        "options": ["Mordecai", "Haman", "Xerxes", "Zeresh"],
        "correct": 0,
        "reference": "Esther 2:7",
        "difficulty": "medium",
        "category": "old_testament"
    },
    {
        "question": "Who wrote the book of Lamentations?",
        "options": ["Jeremiah", "Ezekiel", "Isaiah", "Daniel"],
        "correct": 0,
        "reference": "Lamentations (traditionally attributed to Jeremiah)",
        "difficulty": "hard",
        "category": "old_testament"
    },
    {
        "question": "What was the name of the Persian king in the book of Esther?",
        "options": ["Darius", "Cyrus", "Xerxes", "Artaxerxes"],
        "correct": 2,
        "reference": "Esther 1:1",
        "difficulty": "hard",
        "category": "old_testament"
    },
    {
        "question": "What did Ruth say to Naomi that became famous?",
        "options": ["Where you go I will go", "Your people will be my people", "Your God will be my God", "All of the above"],
        "correct": 3,
        "reference": "Ruth 1:16-17",
        "difficulty": "medium",
        "category": "old_testament"
    },
    
    # EXPANDED COVERAGE - New Testament Epistles
    {
        "question": "What is the main theme of the book of Romans?",
        "options": ["Love", "Justification by faith", "The church", "End times"],
        "correct": 1,
        "reference": "Romans 3:28",
        "difficulty": "medium",
        "category": "new_testament"
    },
    {
        "question": "What is the fruit of the Spirit mentioned in Galatians?",
        "options": ["Love, joy, peace, patience, kindness, goodness, faithfulness, gentleness, self-control", "Faith, hope, love", "Wisdom, understanding, knowledge", "Righteousness, holiness, purity"],
        "correct": 0,
        "reference": "Galatians 5:22-23",
        "difficulty": "medium",
        "category": "new_testament"
    },
    {
        "question": "Which epistle talks about the armor of God?",
        "options": ["Ephesians", "Colossians", "Philippians", "1 Thessalonians"],
        "correct": 0,
        "reference": "Ephesians 6:11",
        "difficulty": "medium",
        "category": "new_testament"
    },
    {
        "question": "What did Paul say he could do through Christ?",
        "options": ["All things", "Some things", "Nothing", "Everything except sin"],
        "correct": 0,
        "reference": "Philippians 4:13",
        "difficulty": "easy",
        "category": "new_testament"
    },
    {
        "question": "Which epistle emphasizes that Christ is the head of the church?",
        "options": ["Ephesians", "Colossians", "1 Corinthians", "Galatians"],
        "correct": 1,
        "reference": "Colossians 1:18",
        "difficulty": "hard",
        "category": "new_testament"
    },
    {
        "question": "What is the main theme of 1 Corinthians 13?",
        "options": ["Love", "Faith", "Hope", "Wisdom"],
        "correct": 0,
        "reference": "1 Corinthians 13:1-13",
        "difficulty": "easy",
        "category": "new_testament"
    },
    {
        "question": "Which epistle talks about the rapture?",
        "options": ["1 Thessalonians", "2 Thessalonians", "Revelation", "1 Corinthians"],
        "correct": 0,
        "reference": "1 Thessalonians 4:17",
        "difficulty": "hard",
        "category": "new_testament"
    },
    {
        "question": "What are the three things that remain according to 1 Corinthians 13?",
        "options": ["Faith, hope, and love", "Love, joy, and peace", "Wisdom, understanding, and knowledge", "Righteousness, holiness, and purity"],
        "correct": 0,
        "reference": "1 Corinthians 13:13",
        "difficulty": "medium",
        "category": "new_testament"
    },
    {
        "question": "Which epistle was written to a slave owner about a runaway slave?",
        "options": ["Philemon", "Titus", "1 Timothy", "2 Timothy"],
        "correct": 0,
        "reference": "Philemon 1:10-16",
        "difficulty": "hard",
        "category": "new_testament"
    },
    {
        "question": "What does James say faith without works is?",
        "options": ["Dead", "Incomplete", "Weak", "Useless"],
        "correct": 0,
        "reference": "James 2:26",
        "difficulty": "medium",
        "category": "new_testament"
    },
    {
        "question": "Which epistle talks about the great cloud of witnesses?",
        "options": ["Hebrews", "1 Peter", "2 Peter", "Jude"],
        "correct": 0,
        "reference": "Hebrews 12:1",
        "difficulty": "hard",
        "category": "new_testament"
    },
    {
        "question": "What does 1 Peter say believers are?",
        "options": ["A chosen people, a royal priesthood", "Sinners saved by grace", "Children of God", "All of the above"],
        "correct": 0,
        "reference": "1 Peter 2:9",
        "difficulty": "hard",
        "category": "new_testament"
    },
    {
        "question": "Which epistle warns about false teachers?",
        "options": ["2 Peter", "Jude", "1 John", "All of the above"],
        "correct": 3,
        "reference": "2 Peter 2:1, Jude 1:4, 1 John 4:1",
        "difficulty": "hard",
        "category": "new_testament"
    },
    {
        "question": "What does 1 John say God is?",
        "options": ["Love", "Light", "Spirit", "All of the above"],
        "correct": 0,
        "reference": "1 John 4:8",
        "difficulty": "medium",
        "category": "new_testament"
    },
    
    # EXPANDED COVERAGE - Major Prophets (More Detail)
    {
        "question": "What did Isaiah see in his vision in chapter 6?",
        "options": ["The Lord seated on a throne", "A burning bush", "A wheel within a wheel", "A valley of dry bones"],
        "correct": 0,
        "reference": "Isaiah 6:1",
        "difficulty": "medium",
        "category": "old_testament"
    },
    {
        "question": "What did Jeremiah buy to illustrate God's message?",
        "options": ["A field", "A pot", "A belt", "A yoke"],
        "correct": 0,
        "reference": "Jeremiah 32:7",
        "difficulty": "hard",
        "category": "old_testament"
    },
    {
        "question": "What did Ezekiel see in his vision?",
        "options": ["A wheel within a wheel", "A valley of dry bones", "The glory of the Lord", "All of the above"],
        "correct": 3,
        "reference": "Ezekiel 1:16, 37:1, 1:28",
        "difficulty": "hard",
        "category": "old_testament"
    },
    {
        "question": "What did Isaiah prophesy about the Messiah?",
        "options": ["He would be born of a virgin", "He would be called Immanuel", "He would be a suffering servant", "All of the above"],
        "correct": 3,
        "reference": "Isaiah 7:14, 9:6, 53:3-5",
        "difficulty": "medium",
        "category": "old_testament"
    },
    {
        "question": "What was Jeremiah known as?",
        "options": ["The weeping prophet", "The major prophet", "The prophet of doom", "The prophet of hope"],
        "correct": 0,
        "reference": "Jeremiah (often called the weeping prophet)",
        "difficulty": "medium",
        "category": "old_testament"
    },
    
    # EXPANDED COVERAGE - Chronicles and Kings
    {
        "question": "How many times did the temple get destroyed?",
        "options": ["Once", "Twice", "Three times", "Never"],
        "correct": 1,
        "reference": "2 Kings 25:9, 2 Chronicles 36:19",
        "difficulty": "hard",
        "category": "old_testament"
    },
    {
        "question": "Which king found the Book of the Law in the temple?",
        "options": ["Josiah", "Hezekiah", "Jehoshaphat", "Asa"],
        "correct": 0,
        "reference": "2 Kings 22:8",
        "difficulty": "hard",
        "category": "old_testament"
    },
    {
        "question": "What did King Hezekiah do when he was sick?",
        "options": ["Prayed to God", "Asked Isaiah to pray", "Turned his face to the wall", "All of the above"],
        "correct": 3,
        "reference": "2 Kings 20:2-3",
        "difficulty": "hard",
        "category": "old_testament"
    },
    
    # EXPANDED COVERAGE - More Bible Facts
    {
        "question": "What is the shortest book in the New Testament?",
        "options": ["2 John", "3 John", "Philemon", "Jude"],
        "correct": 1,
        "reference": "3 John (1 chapter, 14 verses)",
        "difficulty": "hard",
        "category": "bible_facts"
    },
    {
        "question": "How many letters did Paul write?",
        "options": ["10", "13", "15", "21"],
        "correct": 1,
        "reference": "13 Pauline epistles",
        "difficulty": "medium",
        "category": "bible_facts"
    },
    {
        "question": "What is the longest chapter in the Bible?",
        "options": ["Psalm 119", "Psalm 23", "Isaiah 53", "1 Corinthians 13"],
        "correct": 0,
        "reference": "Psalm 119 (176 verses)",
        "difficulty": "medium",
        "category": "bible_facts"
    },
    {
        "question": "What is the shortest chapter in the Bible?",
        "options": ["Psalm 117", "Psalm 23", "John 11:35", "1 Thessalonians 5"],
        "correct": 0,
        "reference": "Psalm 117 (2 verses)",
        "difficulty": "hard",
        "category": "bible_facts"
    },
    {
        "question": "Which book comes between Malachi and Matthew?",
        "options": ["None - they are consecutive", "Revelation", "Acts", "There is no book between them"],
        "correct": 3,
        "reference": "Malachi is last OT book, Matthew is first NT book",
        "difficulty": "medium",
        "category": "bible_facts"
    },
    
    # COMPLETE COVERAGE - Missing Old Testament Books
    
    # Leviticus
    {
        "question": "What is the main theme of the book of Leviticus?",
        "options": ["History", "Laws and sacrifices", "Prophecy", "Wisdom"],
        "correct": 1,
        "reference": "Leviticus (book of laws and sacrifices)",
        "difficulty": "medium",
        "category": "old_testament"
    },
    {
        "question": "What did the Day of Atonement (Yom Kippur) involve?",
        "options": ["Feasting", "Sacrifices and fasting", "Dancing", "Singing"],
        "correct": 1,
        "reference": "Leviticus 16:29-30",
        "difficulty": "hard",
        "category": "old_testament"
    },
    {
        "question": "What were the clean and unclean animals laws about?",
        "options": ["Dietary restrictions", "Sacrificial animals", "Pets", "Wildlife"],
        "correct": 0,
        "reference": "Leviticus 11",
        "difficulty": "easy",
        "category": "old_testament"
    },
    
    # Numbers
    {
        "question": "Why is the book of Numbers called 'Numbers'?",
        "options": ["It counts the Israelites", "It has many numbers in it", "It's about mathematics", "It counts the days"],
        "correct": 0,
        "reference": "Numbers 1:2-3",
        "difficulty": "easy",
        "category": "old_testament"
    },
    {
        "question": "How many spies were sent to explore the Promised Land?",
        "options": ["10", "12", "14", "15"],
        "correct": 1,
        "reference": "Numbers 13:1-2",
        "difficulty": "medium",
        "category": "old_testament"
    },
    {
        "question": "What happened to the Israelites who complained in the wilderness?",
        "options": ["They were blessed", "They were punished", "They found water", "They reached the Promised Land"],
        "correct": 1,
        "reference": "Numbers 11:1",
        "difficulty": "medium",
        "category": "old_testament"
    },
    
    # Deuteronomy
    {
        "question": "What does 'Deuteronomy' mean?",
        "options": ["Second law", "First law", "New law", "Old law"],
        "correct": 0,
        "reference": "Deuteronomy (second giving of the law)",
        "difficulty": "hard",
        "category": "old_testament"
    },
    {
        "question": "What is the Shema found in Deuteronomy?",
        "options": ["A prayer", "A command to love God", "A song", "A prophecy"],
        "correct": 1,
        "reference": "Deuteronomy 6:4-5",
        "difficulty": "medium",
        "category": "old_testament"
    },
    {
        "question": "Who wrote the book of Deuteronomy?",
        "options": ["Moses", "Joshua", "Aaron", "God"],
        "correct": 0,
        "reference": "Deuteronomy 1:1",
        "difficulty": "easy",
        "category": "old_testament"
    },
    
    # Joshua
    {
        "question": "What was Joshua's role after Moses died?",
        "options": ["Priest", "Judge", "Leader of Israel", "Prophet"],
        "correct": 2,
        "reference": "Joshua 1:1-2",
        "difficulty": "easy",
        "category": "old_testament"
    },
    {
        "question": "What happened at the battle of Jericho?",
        "options": ["The walls fell down", "The city surrendered", "Joshua was killed", "The Israelites lost"],
        "correct": 0,
        "reference": "Joshua 6:20",
        "difficulty": "easy",
        "category": "old_testament"
    },
    {
        "question": "What did Joshua say before he died?",
        "options": ["'As for me and my household, we will serve the Lord'", "'Choose this day whom you will serve'", "'The Lord is my shepherd'", "'Love the Lord your God'"],
        "correct": 1,
        "reference": "Joshua 24:15",
        "difficulty": "medium",
        "category": "old_testament"
    },
    
    # Ezra
    {
        "question": "What did Ezra lead the people to do?",
        "options": ["Rebuild the temple", "Return from exile", "Read the Law", "All of the above"],
        "correct": 3,
        "reference": "Ezra 7:10, 3:8, 7:6",
        "difficulty": "medium",
        "category": "old_testament"
    },
    {
        "question": "Which Persian king allowed the Jews to return to Jerusalem?",
        "options": ["Cyrus", "Darius", "Xerxes", "Artaxerxes"],
        "correct": 0,
        "reference": "Ezra 1:1",
        "difficulty": "hard",
        "category": "old_testament"
    },
    {
        "question": "What was Ezra's profession?",
        "options": ["Priest", "Scribe", "Prophet", "King"],
        "correct": 1,
        "reference": "Ezra 7:6",
        "difficulty": "hard",
        "category": "old_testament"
    },
    
    # Nehemiah
    {
        "question": "What did Nehemiah rebuild?",
        "options": ["The temple", "The walls of Jerusalem", "The ark", "The tabernacle"],
        "correct": 1,
        "reference": "Nehemiah 2:17",
        "difficulty": "easy",
        "category": "old_testament"
    },
    {
        "question": "What was Nehemiah's job in Persia?",
        "options": ["King", "Cupbearer to the king", "Soldier", "Merchant"],
        "correct": 1,
        "reference": "Nehemiah 1:11",
        "difficulty": "medium",
        "category": "old_testament"
    },
    {
        "question": "How long did it take to rebuild the walls of Jerusalem?",
        "options": ["7 days", "52 days", "1 year", "2 years"],
        "correct": 1,
        "reference": "Nehemiah 6:15",
        "difficulty": "hard",
        "category": "old_testament"
    },
    
    # 1 Chronicles
    {
        "question": "What does 1 Chronicles primarily contain?",
        "options": ["Prophecies", "Genealogies and history", "Laws", "Poetry"],
        "correct": 1,
        "reference": "1 Chronicles 1-9",
        "difficulty": "medium",
        "category": "old_testament"
    },
    {
        "question": "Who is the main focus of 1 Chronicles?",
        "options": ["Moses", "David", "Solomon", "Saul"],
        "correct": 1,
        "reference": "1 Chronicles (focuses on David's reign)",
        "difficulty": "hard",
        "category": "old_testament"
    },
    
    # 2 Chronicles
    {
        "question": "What does 2 Chronicles focus on?",
        "options": ["The northern kingdom", "The southern kingdom of Judah", "The exile", "The return"],
        "correct": 1,
        "reference": "2 Chronicles (history of Judah)",
        "difficulty": "hard",
        "category": "old_testament"
    },
    {
        "question": "Which king's reign does 2 Chronicles end with?",
        "options": ["Hezekiah", "Josiah", "Zedekiah", "Cyrus"],
        "correct": 2,
        "reference": "2 Chronicles 36:11",
        "difficulty": "hard",
        "category": "old_testament"
    },
    
    # Joel
    {
        "question": "What did Joel prophesy about?",
        "options": ["The Day of the Lord", "The exile", "The temple", "The flood"],
        "correct": 0,
        "reference": "Joel 1:15",
        "difficulty": "medium",
        "category": "old_testament"
    },
    {
        "question": "What natural disaster did Joel describe?",
        "options": ["Flood", "Locust plague", "Earthquake", "Fire"],
        "correct": 1,
        "reference": "Joel 1:4",
        "difficulty": "hard",
        "category": "old_testament"
    },
    
    # Amos
    {
        "question": "What was Amos's profession before he became a prophet?",
        "options": ["Priest", "Shepherd", "Farmer", "King"],
        "correct": 1,
        "reference": "Amos 1:1",
        "difficulty": "medium",
        "category": "old_testament"
    },
    {
        "question": "What did Amos prophesy about?",
        "options": ["Judgment on Israel", "Blessing on Israel", "The temple", "The exile"],
        "correct": 0,
        "reference": "Amos 2:6",
        "difficulty": "medium",
        "category": "old_testament"
    },
    {
        "question": "What famous phrase did Amos use?",
        "options": ["'Let justice roll down like waters'", "'The Lord is my shepherd'", "'In the beginning'", "'Love your neighbor'"],
        "correct": 0,
        "reference": "Amos 5:24",
        "difficulty": "hard",
        "category": "old_testament"
    },
    
    # Micah
    {
        "question": "What did Micah prophesy about the birthplace of the Messiah?",
        "options": ["Jerusalem", "Nazareth", "Bethlehem", "Bethany"],
        "correct": 2,
        "reference": "Micah 5:2",
        "difficulty": "medium",
        "category": "old_testament"
    },
    {
        "question": "What does the Lord require according to Micah?",
        "options": ["Sacrifices", "To act justly, love mercy, walk humbly", "Prayers", "Tithing"],
        "correct": 1,
        "reference": "Micah 6:8",
        "difficulty": "medium",
        "category": "old_testament"
    },
    
    # COMPLETE COVERAGE - Missing New Testament Books
    
    # 2 Corinthians
    {
        "question": "What is a main theme of 2 Corinthians?",
        "options": ["Paul's defense of his ministry", "The church", "End times", "Love"],
        "correct": 0,
        "reference": "2 Corinthians (Paul defends his apostleship)",
        "difficulty": "hard",
        "category": "new_testament"
    },
    {
        "question": "What did Paul say about a thorn in his flesh?",
        "options": ["It was removed", "God's grace is sufficient", "It was a curse", "It was healed"],
        "correct": 1,
        "reference": "2 Corinthians 12:9",
        "difficulty": "medium",
        "category": "new_testament"
    },
    
    # 2 Thessalonians
    {
        "question": "What is a main theme of 2 Thessalonians?",
        "options": ["The second coming of Christ", "Love", "Faith", "Hope"],
        "correct": 0,
        "reference": "2 Thessalonians 2:1-2",
        "difficulty": "hard",
        "category": "new_testament"
    },
    {
        "question": "What did Paul warn about in 2 Thessalonians?",
        "options": ["False teachers", "The man of lawlessness", "Sin", "Idolatry"],
        "correct": 1,
        "reference": "2 Thessalonians 2:3",
        "difficulty": "hard",
        "category": "new_testament"
    },
    
    # 1 Timothy
    {
        "question": "What is 1 Timothy primarily about?",
        "options": ["Church leadership", "The end times", "Love", "Faith"],
        "correct": 0,
        "reference": "1 Timothy (instructions for church leadership)",
        "difficulty": "medium",
        "category": "new_testament"
    },
    {
        "question": "What did Paul say about money in 1 Timothy?",
        "options": ["It's evil", "The love of money is a root of all kinds of evil", "It's good", "It's neutral"],
        "correct": 1,
        "reference": "1 Timothy 6:10",
        "difficulty": "easy",
        "category": "new_testament"
    },
    {
        "question": "What qualifications did Paul give for church leaders?",
        "options": ["Rich and powerful", "Above reproach, faithful", "Educated", "Old"],
        "correct": 1,
        "reference": "1 Timothy 3:2",
        "difficulty": "medium",
        "category": "new_testament"
    },
    
    # 2 Timothy
    {
        "question": "What is 2 Timothy known as?",
        "options": ["Paul's last letter", "His first letter", "A love letter", "A prophecy"],
        "correct": 0,
        "reference": "2 Timothy (Paul's final letter)",
        "difficulty": "medium",
        "category": "new_testament"
    },
    {
        "question": "What did Paul tell Timothy to do with the Scriptures?",
        "options": ["Ignore them", "Preach the word", "Hide them", "Change them"],
        "correct": 1,
        "reference": "2 Timothy 4:2",
        "difficulty": "medium",
        "category": "new_testament"
    },
    {
        "question": "What did Paul say all Scripture is?",
        "options": ["Useful", "God-breathed and useful", "Old", "Difficult"],
        "correct": 1,
        "reference": "2 Timothy 3:16",
        "difficulty": "easy",
        "category": "new_testament"
    },
    
    # Titus
    {
        "question": "What is the book of Titus about?",
        "options": ["Church organization", "End times", "Love", "Faith"],
        "correct": 0,
        "reference": "Titus (instructions for church organization)",
        "difficulty": "hard",
        "category": "new_testament"
    },
    {
        "question": "What did Paul tell Titus to do?",
        "options": ["Leave Crete", "Appoint elders", "Build a church", "Write a book"],
        "correct": 1,
        "reference": "Titus 1:5",
        "difficulty": "hard",
        "category": "new_testament"
    },
    
    # 2 John
    {
        "question": "What is 2 John primarily about?",
        "options": ["Love and truth", "The end times", "Church leadership", "Money"],
        "correct": 0,
        "reference": "2 John 1:1-3",
        "difficulty": "hard",
        "category": "new_testament"
    },
    {
        "question": "What did John warn about in 2 John?",
        "options": ["False teachers", "Sin", "Money", "The end times"],
        "correct": 0,
        "reference": "2 John 1:7",
        "difficulty": "hard",
        "category": "new_testament"
    },
    
    # More Psalms coverage
    {
        "question": "Who wrote 'The Lord is my shepherd'?",
        "options": ["Solomon", "David", "Moses", "Asaph"],
        "correct": 1,
        "reference": "Psalm 23:1",
        "difficulty": "easy",
        "category": "old_testament"
    },
    {
        "question": "What is Psalm 119 about?",
        "options": ["Love", "The law of God", "War", "Nature"],
        "correct": 1,
        "reference": "Psalm 119 (longest chapter, about God's law)",
        "difficulty": "medium",
        "category": "old_testament"
    },
    {
        "question": "What did David say in Psalm 51 after his sin?",
        "options": ["Create in me a clean heart", "I am perfect", "I don't need forgiveness", "God doesn't care"],
        "correct": 0,
        "reference": "Psalm 51:10",
        "difficulty": "medium",
        "category": "old_testament"
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
