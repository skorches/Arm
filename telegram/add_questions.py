#!/usr/bin/env python3
"""
Script to add 500 new questions to quiz_questions.py
"""

import re

# Generate 500 questions (split: ~167 easy, ~167 medium, ~166 hard)
questions = []

# EASY QUESTIONS (~167)
easy_qs = [
    {"question": "Who was the first woman created by God?", "options": ["Eve", "Sarah", "Rebecca", "Rachel"], "correct": 0, "reference": "Genesis 2:22", "difficulty": "easy", "category": "old_testament"},
    {"question": "What was the name of Abraham's wife?", "options": ["Sarah", "Rebecca", "Rachel", "Leah"], "correct": 0, "reference": "Genesis 17:15", "difficulty": "easy", "category": "old_testament"},
    {"question": "Who was Isaac's son?", "options": ["Jacob", "Esau", "Joseph", "Benjamin"], "correct": 0, "reference": "Genesis 25:26", "difficulty": "easy", "category": "old_testament"},
    {"question": "What was Jacob's name changed to?", "options": ["Israel", "Judah", "Joseph", "Benjamin"], "correct": 0, "reference": "Genesis 32:28", "difficulty": "easy", "category": "old_testament"},
    {"question": "How many sons did Jacob have?", "options": ["10", "12", "14", "16"], "correct": 1, "reference": "Genesis 35:22-26", "difficulty": "easy", "category": "old_testament"},
    {"question": "What was the name of Joseph's colorful coat?", "options": ["Coat of many colors", "Royal robe", "Priestly garment", "Warrior's cloak"], "correct": 0, "reference": "Genesis 37:3", "difficulty": "easy", "category": "old_testament"},
    {"question": "Who was Moses' sister?", "options": ["Miriam", "Deborah", "Esther", "Ruth"], "correct": 0, "reference": "Exodus 15:20", "difficulty": "easy", "category": "old_testament"},
    {"question": "What did God give to the Israelites in the wilderness?", "options": ["Manna", "Bread", "Fish", "Meat"], "correct": 0, "reference": "Exodus 16:15", "difficulty": "easy", "category": "old_testament"},
    {"question": "Who was the first judge of Israel?", "options": ["Othniel", "Ehud", "Deborah", "Gideon"], "correct": 0, "reference": "Judges 3:9", "difficulty": "easy", "category": "old_testament"},
    {"question": "What was the name of David's father?", "options": ["Jesse", "Saul", "Samuel", "Eli"], "correct": 0, "reference": "1 Samuel 16:1", "difficulty": "easy", "category": "old_testament"},
    {"question": "Who was David's best friend?", "options": ["Jonathan", "Saul", "Samuel", "Nathan"], "correct": 0, "reference": "1 Samuel 18:1", "difficulty": "easy", "category": "old_testament"},
    {"question": "What was the name of Solomon's father?", "options": ["David", "Saul", "Rehoboam", "Jeroboam"], "correct": 0, "reference": "1 Kings 1:39", "difficulty": "easy", "category": "old_testament"},
    {"question": "Who was known for his great wisdom?", "options": ["Solomon", "David", "Moses", "Samuel"], "correct": 0, "reference": "1 Kings 3:12", "difficulty": "easy", "category": "old_testament"},
    {"question": "What was the name of the prophet who anointed David?", "options": ["Samuel", "Nathan", "Elijah", "Elisha"], "correct": 0, "reference": "1 Samuel 16:13", "difficulty": "easy", "category": "old_testament"},
    {"question": "Who was thrown into a pit by his brothers?", "options": ["Joseph", "Benjamin", "Judah", "Reuben"], "correct": 0, "reference": "Genesis 37:24", "difficulty": "easy", "category": "old_testament"},
    {"question": "How many commandments did God give to Moses?", "options": ["7", "10", "12", "15"], "correct": 1, "reference": "Exodus 20:1-17", "difficulty": "easy", "category": "old_testament"},
    {"question": "What was the name of the promised land?", "options": ["Canaan", "Egypt", "Babylon", "Assyria"], "correct": 0, "reference": "Genesis 12:5", "difficulty": "easy", "category": "old_testament"},
    {"question": "Who was the strongest man in the Bible?", "options": ["Samson", "Goliath", "David", "Saul"], "correct": 0, "reference": "Judges 16:17", "difficulty": "easy", "category": "old_testament"},
    {"question": "What was Samson's weakness?", "options": ["His hair", "His strength", "His eyes", "His hands"], "correct": 0, "reference": "Judges 16:17", "difficulty": "easy", "category": "old_testament"},
    {"question": "What was the name of the city where Jesus was crucified?", "options": ["Jerusalem", "Bethlehem", "Nazareth", "Capernaum"], "correct": 0, "reference": "John 19:20", "difficulty": "easy", "category": "new_testament"},
    {"question": "Who was the first disciple Jesus called?", "options": ["Peter and Andrew", "James and John", "Matthew", "Philip"], "correct": 0, "reference": "Matthew 4:18-19", "difficulty": "easy", "category": "new_testament"},
    {"question": "What was the name of Jesus' earthly father?", "options": ["Joseph", "David", "Jacob", "Eli"], "correct": 0, "reference": "Matthew 1:16", "difficulty": "easy", "category": "new_testament"},
    {"question": "Where was Jesus born?", "options": ["Bethlehem", "Nazareth", "Jerusalem", "Capernaum"], "correct": 0, "reference": "Luke 2:4-7", "difficulty": "easy", "category": "new_testament"},
    {"question": "Who visited Jesus when he was a baby?", "options": ["Wise men", "Shepherds", "Both wise men and shepherds", "Angels"], "correct": 2, "reference": "Matthew 2:1, Luke 2:8", "difficulty": "easy", "category": "new_testament"},
    {"question": "How many people did Jesus feed with 5 loaves and 2 fish?", "options": ["1000", "3000", "5000", "10000"], "correct": 2, "reference": "Matthew 14:21", "difficulty": "easy", "category": "new_testament"},
    {"question": "Who walked on water with Jesus?", "options": ["Peter", "John", "James", "Andrew"], "correct": 0, "reference": "Matthew 14:29", "difficulty": "easy", "category": "new_testament"},
    {"question": "What was the name of the tax collector who became a disciple?", "options": ["Matthew", "Zacchaeus", "Levi", "Judas"], "correct": 0, "reference": "Matthew 9:9", "difficulty": "easy", "category": "new_testament"},
    {"question": "Who was known as the doubting disciple?", "options": ["Thomas", "Peter", "Judas", "Philip"], "correct": 0, "reference": "John 20:24-25", "difficulty": "easy", "category": "new_testament"},
    {"question": "What happened to Jesus after he died?", "options": ["He rose from the dead", "He stayed in the tomb", "He was buried forever", "He went to heaven immediately"], "correct": 0, "reference": "Matthew 28:6", "difficulty": "easy", "category": "new_testament"},
    {"question": "Who was the first person to see Jesus after he rose?", "options": ["Mary Magdalene", "Peter", "John", "Thomas"], "correct": 0, "reference": "John 20:14-16", "difficulty": "easy", "category": "new_testament"},
    {"question": "What is the shortest book in the Bible?", "options": ["3 John", "2 John", "Philemon", "Jude"], "correct": 0, "reference": "3 John (1 chapter)", "difficulty": "easy", "category": "bible_facts"},
    {"question": "How many gospels are in the New Testament?", "options": ["3", "4", "5", "6"], "correct": 1, "reference": "Matthew, Mark, Luke, John", "difficulty": "easy", "category": "bible_facts"},
    {"question": "What are the first four books of the New Testament called?", "options": ["The Gospels", "The Epistles", "The Prophets", "The Psalms"], "correct": 0, "reference": "Matthew, Mark, Luke, John", "difficulty": "easy", "category": "bible_facts"},
    {"question": "Who wrote the book of Acts?", "options": ["Luke", "Paul", "John", "Peter"], "correct": 0, "reference": "Acts 1:1", "difficulty": "easy", "category": "bible_facts"},
    {"question": "How many letters did Paul write in the New Testament?", "options": ["10", "13", "15", "20"], "correct": 1, "reference": "Bible Facts", "difficulty": "easy", "category": "bible_facts"},
]

# Add more easy questions to reach ~167
# I'll generate a comprehensive list programmatically
for i in range(len(easy_qs), 167):
    # Placeholder - we'll add real questions
    pass

questions.extend(easy_qs)

print(f"Generated {len(questions)} questions so far")
print("This script needs to be expanded with all 500 questions")


