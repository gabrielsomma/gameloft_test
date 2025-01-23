profiles = []
campaigns = []


class Campaign:
    def __init__(self, name, matchers):
        self.name = name
        self.matchers = matchers

    def match_profile(self, profile):
        if not (self.matchers["level"]["min"] <= profile.level <= self.matchers["level"]["max"]):
            return False
        if not(profile.country in self.matchers["has"]["country"]):
            return False
        for item in self.matchers["has"]["items"]:
            if profile.inventory.get(item) is None:
                return False
        for item in self.matchers["does_not_have"]["items"]:
            if profile.inventory.get(item) is not None:
                return False

        profile.add_active_campaign(self.name)
        return True


class Profile:
    def __init__(self, player_id, active_campaigns, level, country, inventory):
        self.player_id = player_id
        self.active_campaigns = active_campaigns
        self.level = level
        self.country = country
        self.inventory = inventory

    def add_active_campaign(self, active_campaign):
        if active_campaign in self.active_campaigns:
            return
        self.active_campaigns.append(active_campaign)
