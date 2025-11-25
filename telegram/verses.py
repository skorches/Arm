"""
Bible Verses Database
Popular and inspiring Bible verses
"""

POPULAR_VERSES = [
    {
        "reference": "John 3:16",
        "verse": "For God so loved the world that he gave his one and only Son, that whoever believes in him shall not perish but have eternal life.",
        "topic": "Salvation"
    },
    {
        "reference": "Philippians 4:13",
        "verse": "I can do all this through him who gives me strength.",
        "topic": "Strength"
    },
    {
        "reference": "Jeremiah 29:11",
        "verse": "For I know the plans I have for you, declares the Lord, plans to prosper you and not to harm you, plans to give you hope and a future.",
        "topic": "Hope"
    },
    {
        "reference": "Proverbs 3:5-6",
        "verse": "Trust in the Lord with all your heart and lean not on your own understanding; in all your ways submit to him, and he will make your paths straight.",
        "topic": "Trust"
    },
    {
        "reference": "Romans 8:28",
        "verse": "And we know that in all things God works for the good of those who love him, who have been called according to his purpose.",
        "topic": "God's Plan"
    },
    {
        "reference": "Isaiah 40:31",
        "verse": "But those who hope in the Lord will renew their strength. They will soar on wings like eagles; they will run and not grow weary, they will walk and not be faint.",
        "topic": "Strength"
    },
    {
        "reference": "Matthew 6:33",
        "verse": "But seek first his kingdom and his righteousness, and all these things will be given to you as well.",
        "topic": "Priorities"
    },
    {
        "reference": "1 Corinthians 13:4-5",
        "verse": "Love is patient, love is kind. It does not envy, it does not boast, it is not proud. It does not dishonor others, it is not self-seeking, it is not easily angered, it keeps no record of wrongs.",
        "topic": "Love"
    },
    {
        "reference": "Joshua 1:9",
        "verse": "Have I not commanded you? Be strong and courageous. Do not be afraid; do not be discouraged, for the Lord your God will be with you wherever you go.",
        "topic": "Courage"
    },
    {
        "reference": "Psalm 23:1",
        "verse": "The Lord is my shepherd, I lack nothing.",
        "topic": "Provision"
    },
    {
        "reference": "2 Timothy 1:7",
        "verse": "For the Spirit God gave us does not make us timid, but gives us power, love and self-discipline.",
        "topic": "Power"
    },
    {
        "reference": "Ephesians 2:8-9",
        "verse": "For it is by grace you have been saved, through faith—and this is not from yourselves, it is the gift of God—not by works, so that no one can boast.",
        "topic": "Salvation"
    },
    {
        "reference": "1 John 4:19",
        "verse": "We love because he first loved us.",
        "topic": "Love"
    },
    {
        "reference": "Proverbs 16:3",
        "verse": "Commit to the Lord whatever you do, and he will establish your plans.",
        "topic": "Commitment"
    },
    {
        "reference": "Matthew 11:28",
        "verse": "Come to me, all you who are weary and burdened, and I will give you rest.",
        "topic": "Rest"
    },
    {
        "reference": "Psalm 46:10",
        "verse": "Be still, and know that I am God; I will be exalted among the nations, I will be exalted in the earth.",
        "topic": "Peace"
    },
    {
        "reference": "Romans 12:2",
        "verse": "Do not conform to the pattern of this world, but be transformed by the renewing of your mind. Then you will be able to test and approve what God's will is—his good, pleasing and perfect will.",
        "topic": "Transformation"
    },
    {
        "reference": "Galatians 2:20",
        "verse": "I have been crucified with Christ and I no longer live, but Christ lives in me. The life I now live in the body, I live by faith in the Son of God, who loved me and gave himself for me.",
        "topic": "Faith"
    },
    {
        "reference": "Hebrews 11:1",
        "verse": "Now faith is confidence in what we hope for and assurance about what we do not see.",
        "topic": "Faith"
    },
    {
        "reference": "Psalm 119:105",
        "verse": "Your word is a lamp for my feet, a light on my path.",
        "topic": "God's Word"
    },
    {
        "reference": "Isaiah 41:10",
        "verse": "So do not fear, for I am with you; do not be dismayed, for I am your God. I will strengthen you and help you; I will uphold you with my righteous right hand.",
        "topic": "Fear"
    },
    {
        "reference": "Colossians 3:23",
        "verse": "Whatever you do, work at it with all your heart, as working for the Lord, not for human masters.",
        "topic": "Work"
    },
    {
        "reference": "1 Peter 5:7",
        "verse": "Cast all your anxiety on him because he cares for you.",
        "topic": "Anxiety"
    },
    {
        "reference": "James 1:2-3",
        "verse": "Consider it pure joy, my brothers and sisters, whenever you face trials of many kinds, because you know that the testing of your faith produces perseverance.",
        "topic": "Trials"
    },
    {
        "reference": "Micah 6:8",
        "verse": "He has shown you, O mortal, what is good. And what does the Lord require of you? To act justly and to love mercy and to walk humbly with your God.",
        "topic": "Requirements"
    },
    {
        "reference": "Psalm 37:4",
        "verse": "Take delight in the Lord, and he will give you the desires of your heart.",
        "topic": "Delight"
    },
    {
        "reference": "Proverbs 31:25",
        "verse": "She is clothed with strength and dignity; she can laugh at the days to come.",
        "topic": "Strength"
    },
    {
        "reference": "Deuteronomy 31:6",
        "verse": "Be strong and courageous. Do not be afraid or terrified because of them, for the Lord your God goes with you; he will never leave you nor forsake you.",
        "topic": "Courage"
    },
    {
        "reference": "Matthew 28:20",
        "verse": "And surely I am with you always, to the very end of the age.",
        "topic": "Presence"
    },
    {
        "reference": "Psalm 34:8",
        "verse": "Taste and see that the Lord is good; blessed is the one who takes refuge in him.",
        "topic": "Goodness"
    },
    {
        "reference": "Romans 15:13",
        "verse": "May the God of hope fill you with all joy and peace as you trust in him, so that you may overflow with hope by the power of the Holy Spirit.",
        "topic": "Hope"
    },
]

def get_verse_of_the_day():
    """Get verse of the day (same for all users, changes daily)"""
    import random
    from datetime import date
    
    # Use date as seed so same verse appears all day
    today = date.today()
    random.seed(today.toordinal())
    
    return random.choice(POPULAR_VERSES)

def search_verses(keyword):
    """Search verses by keyword"""
    keyword_lower = keyword.lower()
    matches = []
    
    for verse_data in POPULAR_VERSES:
        if (keyword_lower in verse_data['verse'].lower() or 
            keyword_lower in verse_data['reference'].lower() or
            keyword_lower in verse_data['topic'].lower()):
            matches.append(verse_data)
    
    return matches

def get_verse_by_reference(reference):
    """Get verse by reference (e.g., 'John 3:16')"""
    reference_clean = reference.strip().lower()
    
    for verse_data in POPULAR_VERSES:
        if verse_data['reference'].lower() == reference_clean:
            return verse_data
    
    return None

