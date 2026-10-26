"""
basketball app ke fixed values (choices) aur source-data ke codes.

Ye values raw data (ESPN / data engineer ka dump) se aati hain. Spec ke
business rules yahan NAHI hain; woh analytics/constants.py mein hain.
"""
from django.db import models


# ESPN ka season_type code. 2 = regular season.
# Note: season_type=2 mein conference tournaments bhi hote hain, unhein
# tournament_id se alag kiya jata hai (dekhein Game.objects.regular_season()).
REGULAR_SEASON_TYPE = 2


class Zone(models.TextChoices):
    """
    Court par shot ki jagah. Assisted share isi ke hisaab se nikalta hai.

    rim   = layup, dunk ya tip (basket ke bilkul paas)
    mid   = baaqi har 2-pointer
    three = 3-point line ke bahar se
    """
    RIM = "rim", "Rim"
    MID = "mid", "Mid-range"
    THREE = "three", "Three"
