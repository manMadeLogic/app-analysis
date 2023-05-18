# Some constant values for the query
APP_STORE_CATEGORY_CASE_STATEMENT = """
CASE
    WHEN category = 'Games' THEN 'Game'
    WHEN category = 'Music' THEN 'Music'
    WHEN category = 'Health & Fitness' THEN 'Health'
END
"""
APP_STORE_CATEGORY_FILTER_STATEMENT = """
category IN ('Games', 'Music', 'Health & Fitness')
"""
GOOGLE_PLAY_CATEGORY_CASE_STATEMENT = """
CASE
    WHEN category IN ('Games', 'Action', 'Adventure', 'Arcade',
                      'Board', 'Card', 'Casino, Casual',
                      'Educational', 'Music', 'Puzzle', 'Racing',
                      'Role Playing', 'Simulation', 'Sports',
                      'Strategy', 'Trivia', 'Word') THEN 'Game'
    WHEN category = 'Music & Audio' THEN 'Music'
    WHEN category = 'Health & Fitness' THEN 'Health'
END
"""
GOOGLE_PLAY_CATEGORY_FILTER_STATEMENT = """
category IN ('Games', 'Action', 'Adventure', 'Arcade',
                      'Board', 'Card', 'Casino, Casual',
                      'Educational', 'Music', 'Puzzle', 'Racing',
                      'Role Playing', 'Simulation', 'Sports',
                      'Strategy', 'Trivia', 'Word', 'Music & Audio', 'Health & Fitness')
"""
