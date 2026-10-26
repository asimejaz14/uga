"""
Role (Step 1) pipeline — spec v9.1.

Layout
------
loaders.py       the ONLY place that talks to the database (read -> DataFrame, DataFrame -> write)
possessions.py   Step 1: possessions on the floor per player-season   -> PlayerSeasonPossessions
assist_share.py  Step 2: national assisted share per season and zone  -> NationalAssistShare
pooling.py       Step 3: qualified flag + pooled counts (in memory; --dump-dir to see it)
play_types.py    Step 4: play types, rates per 100, percentiles (in memory)
shares.py        Step 5: lead, lead2, inside, inside2, front           -> PlayerOnfloorShares
groups.py        Step 6a: seven groups, raw score, group score         -> PlayerGroupScore
rules.py         Step 6b: each group's ordered rule -> proposed role
placement.py     Steps 7-8: guardrails, close calls, tiebreakers, final role -> RolePlacement
tests.py         unit tests, no database:  python manage.py test talent_acquisiton.role_pipeline

Every step module is pure pandas: DataFrames in, DataFrames out, no Django.
That keeps each step testable on its own with a hand-made DataFrame.
"""
