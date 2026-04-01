# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *
import json

FISH_BY_RARITY = {
    "empty": ["empty"],
    "common": ["Sardine", "Catfish", "Carp"],
    "uncommon": ["Bass", "Trout", "Salmon"],
    "rare": ["Tuna", "Swordfish", "Shark"],
    "legendary": ["Golden Koi", "Giant Squid", "Kraken"],
}

FISH_CATALOG = {
    "Sardine": {"rarity": "common", "points": 10},
    "Catfish": {"rarity": "common", "points": 20},
    "Carp": {"rarity": "common", "points": 30},
    "Bass": {"rarity": "uncommon", "points": 50},
    "Trout": {"rarity": "uncommon", "points": 80},
    "Salmon": {"rarity": "uncommon", "points": 100},
    "Tuna": {"rarity": "rare", "points": 200},
    "Swordfish": {"rarity": "rare", "points": 350},
    "Shark": {"rarity": "rare", "points": 500},
    "Golden Koi": {"rarity": "legendary", "points": 1000},
    "Giant Squid": {"rarity": "legendary", "points": 2000},
    "Kraken": {"rarity": "legendary", "points": 5000},
}

RODS = {
    "bamboo": {"price": 0, "rare_bonus": 0, "legendary_bonus": 0},
    "platinum": {"price": 50, "rare_bonus": 15, "legendary_bonus": 5},
    "adamantite": {"price": 150, "rare_bonus": 30, "legendary_bonus": 10},
}

BAITS = {
    "none": {"price": 0, "catch_bonus": 0, "rare_bonus": 0},
    "worm": {"price": 10, "catch_bonus": 20, "rare_bonus": 0},
    "shrimp": {"price": 20, "catch_bonus": 30, "rare_bonus": 10},
    "magic_lure": {"price": 50, "catch_bonus": 40, "rare_bonus": 20},
}

def pick_fish(seed: int, catch_bonus: int, rare_bonus: int, legendary_bonus: int) -> str:
    roll = (seed * 1103515245 + 12345) % 100
    fish_idx = (seed * 6364136223846793005 + 1442695040888963407) % 1000
    empty_chance = max(0, 30 - catch_bonus)
    legendary_chance = 2 + legendary_bonus
    rare_chance = 15 + rare_bonus
    uncommon_chance = 25
    
    if roll < empty_chance:
        return "empty"
    elif roll < empty_chance + legendary_chance:
        idx = int(fish_idx) % len(FISH_BY_RARITY["legendary"])
        return FISH_BY_RARITY["legendary"][idx]
    elif roll < empty_chance + legendary_chance + rare_chance:
        idx = int(fish_idx) % len(FISH_BY_RARITY["rare"])
        return FISH_BY_RARITY["rare"][idx]
    elif roll < empty_chance + legendary_chance + rare_chance + uncommon_chance:
        idx = int(fish_idx) % len(FISH_BY_RARITY["uncommon"])
        return FISH_BY_RARITY["uncommon"][idx]
    else:
        idx = int(fish_idx) % len(FISH_BY_RARITY["common"])
        return FISH_BY_RARITY["common"][idx]

class FishingGame(gl.Contract):
    players: TreeMap[str, str]
    leaderboard: TreeMap[str, str]
    player_names: TreeMap[str, str]
    cast_count: bigint

    def __init__(self):
        self.cast_count = bigint(0)

    def _get_player(self, address: str) -> dict:
        if address not in self.players:
            return {
                "balance": 100,
                "total_earned": 0,
                "rod": "bamboo",
                "bait": "none",
                "inventory": {"rods": ["bamboo"], "baits": []},
                "catches": [],
                "total_casts": 0,
            }
        return json.loads(self.players[address])

    def _save_player(self, address: str, data: dict) -> None:
        self.players[address] = json.dumps(data, sort_keys=True)
        self.leaderboard[address] = str(data["total_earned"])

    @gl.public.write
    def register(self, name: str) -> None:
        address = str(gl.message.sender_address)
        self.player_names[address] = name
        player = self._get_player(address)
        self._save_player(address, player)

    @gl.public.write
    def cast(self) -> None:
        address = str(gl.message.sender_address)
        player = self._get_player(address)
        rod_data = RODS[player["rod"]]
        bait_data = BAITS[player["bait"]]
        
        if player["bait"] != "none":
            player["bait"] = "none"
        
        rare_bonus = int(rod_data["rare_bonus"]) + int(bait_data["rare_bonus"])
        legendary_bonus = int(rod_data["legendary_bonus"])
        catch_bonus = int(bait_data["catch_bonus"])
        count = int(self.cast_count)
        seed = (count * 2654435761) ^ sum(ord(c) for c in address) ^ (count << 13)
        self.cast_count = bigint(count + 1)
        
        fish_name = pick_fish(seed, catch_bonus, rare_bonus, legendary_bonus)
        points = 0
        rarity = "empty"
        message = "The fish got away..."
        
        if fish_name != "empty" and fish_name in FISH_CATALOG:
            points = int(FISH_CATALOG[fish_name]["points"])
            rarity = FISH_CATALOG[fish_name]["rarity"]
            message = f"You caught a {fish_name}!"
            player["balance"] = int(player["balance"]) + points
            player["total_earned"] = int(player["total_earned"]) + points
            player["total_casts"] = int(player["total_casts"]) + 1
        
        catches = player["catches"]
        if len(catches) >= 10:
            catches = catches[-9:]
        catches.append({
            "fish": fish_name,
            "rarity": rarity,
            "points": points,
            "message": message,
        })
        player["catches"] = catches
        self._save_player(address, player)

    @gl.public.write
    def buy_rod(self, rod_type: str) -> None:
        assert rod_type in RODS, "Invalid rod type"
        assert rod_type != "bamboo", "Bamboo rod is free and already owned"
        address = str(gl.message.sender_address)
        player = self._get_player(address)
        price = int(RODS[rod_type]["price"])
        assert int(player["balance"]) >= price, "Insufficient balance"
        assert rod_type not in player["inventory"]["rods"], "Rod already owned"
        player["balance"] = int(player["balance"]) - price
        player["inventory"]["rods"].append(rod_type)
        self._save_player(address, player)

    @gl.public.write
    def buy_bait(self, bait_type: str) -> None:
        assert bait_type in BAITS and bait_type != "none", "Invalid bait type"
        address = str(gl.message.sender_address)
        player = self._get_player(address)
        price = int(BAITS[bait_type]["price"])
        assert int(player["balance"]) >= price, "Insufficient balance"
        player["balance"] = int(player["balance"]) - price
        player["bait"] = bait_type
        self._save_player(address, player)

    @gl.public.write
    def equip_rod(self, rod_type: str) -> None:
        address = str(gl.message.sender_address)
        player = self._get_player(address)
        assert rod_type in player["inventory"]["rods"], "Rod not owned"
        player["rod"] = rod_type
        self._save_player(address, player)

    @gl.public.view
    def get_stats(self, address: str) -> str:
        player = self._get_player(address)
        name = self.player_names.get(address, "Unknown")
        return json.dumps({
            "name": name,
            "balance": int(player["balance"]),
            "total_earned": int(player["total_earned"]),
            "total_casts": int(player["total_casts"]),
            "rod": player["rod"],
            "bait": player["bait"],
            "inventory": player["inventory"],
            "recent_catches": player["catches"],
        }, sort_keys=True)

    @gl.public.view
    def get_leaderboard(self) -> str:
        entries = []
        for address in self.leaderboard:
            name = self.player_names.get(address, "Unknown")
            entries.append({
                "address": address,
                "name": name,
                "points": int(self.leaderboard[address]),
            })
        entries.sort(key=lambda x: x["points"], reverse=True)
        return json.dumps(entries[:10], sort_keys=True)

    @gl.public.view
    def get_catalog(self) -> str:
        return json.dumps(FISH_CATALOG, sort_keys=True)

    @gl.public.view
    def get_shop(self) -> str:
        return json.dumps({"rods": RODS, "baits": BAITS}, sort_keys=True)
