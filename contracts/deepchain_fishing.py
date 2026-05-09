# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *
import json

FISH_BY_RARITY = {
    "common": ["Sardine","Anchovy","Carp","Tilapia","Mackerel","Herring"],
    "uncommon": ["Bass","Trout","Salmon","Snapper","Pike","Cod"],
    "rare": ["Tuna","Swordfish","Shark","Barracuda","Marlin","Sturgeon"],
    "legendary": ["Golden Koi","Kraken","Leviathan","Giant Squid"]
}

FISH_POINTS = {
    "Sardine":10,"Anchovy":12,"Carp":15,"Tilapia":18,"Mackerel":20,"Herring":22,
    "Bass":40,"Trout":60,"Salmon":80,"Snapper":90,"Pike":100,"Cod":110,
    "Tuna":200,"Swordfish":300,"Shark":500,"Barracuda":400,"Marlin":600,"Sturgeon":700,
    "Golden Koi":1200,"Kraken":3000,"Leviathan":5000,"Giant Squid":2000
}

RODS = {
    "bamboo": {"price":0,"rare":0,"legendary":0,"catch_bonus":10},
    "platinum": {"price":50,"rare":15,"legendary":5,"catch_bonus":15},
    "adamantite": {"price":150,"rare":30,"legendary":10,"catch_bonus":20},
    "mythic": {"price":500,"rare":50,"legendary":25,"catch_bonus":30}
}

BAITS = {
    "none": {"price":0,"catch":0,"rare":0},
    "worm": {"price":10,"catch":20,"rare":0},
    "shrimp": {"price":20,"catch":30,"rare":10},
    "magic_lure": {"price":50,"catch":40,"rare":20},
    "golden_bait": {"price":100,"catch":60,"rare":40}
}

class FishingGame(gl.Contract):

    players: TreeMap[str,str]
    names: TreeMap[str,str]
    name_map: TreeMap[str,str]
    leaderboard: TreeMap[str,str]
    counter: bigint

    def __init__(self):
        self.players = TreeMap()
        self.names = TreeMap()
        self.name_map = TreeMap()
        self.leaderboard = TreeMap()
        self.counter = bigint(0)

    def _normalize_addr(self, a: str) -> str:
        return str(a).lower()

    def _get(self, a: str):
        a = self._normalize_addr(a)
        if a not in self.players:
            return {
                "balance":100,
                "total_earned":0,
                "rod":"bamboo",
                "bait":"none",
                "bait_count":0,
                "bait_inventory":{},
                "inventory":{"rods":["bamboo"],"baits":[]},
                "catches":[],
                "total_casts":0,
                "fishing_stories":[]
            }
        return json.loads(self.players[a])

    def _save(self, a: str, p: dict):
        a = self._normalize_addr(a)
        self.players[a]=json.dumps(p)
        self.leaderboard[a]=str(p["total_earned"])

    # ── WEATHER FETCH: wrapped in gl.eq_principle.web_based ──
    # FIX: moved gl.get_web into a function passed to gl.eq_principle.web_based
    # so all validators reconcile on the same value before any storage write.
    def _get_fishing_conditions(self) -> dict:
        def fetch_temperature():
            response = gl.get_web(
                "https://api.open-meteo.com/v1/forecast"
                "?latitude=-6.2088&longitude=106.8456&current_weather=true"
            )
            data = json.loads(response)
            return data.get("current_weather", {}).get("temperature", 25)

        try:
            temp = float(gl.eq_principle.web_based(fetch_temperature))
        except Exception:
            # Deterministic fallback — counter-based so validators still agree
            temp = 25.0 + float(int(self.counter) % 10)

        condition = "sunny" if temp > 25 else "cloudy" if temp > 20 else "rainy"
        fishing_bonus = 10 if condition == "sunny" else 5 if condition == "cloudy" else 0

        return {
            "condition": condition,
            "temperature": temp,
            "fishing_bonus": fishing_bonus
        }

    # ── AI STORY GENERATION (view) ──
    # FIX: replaced plain string concat with gl.nondet.exec_prompt
    # wrapped in gl.eq_principle.prompt_comparative for validator consensus.
    @gl.public.view
    def get_catch_story(self, fish: str, rarity: str, weather: str) -> str:
        prompt = (
            f"You are a fishing game narrator. A player just caught a {rarity}-rarity {fish} "
            f"during {weather} weather conditions. "
            f"Write an exciting, flavourful 1-2 sentence story about this catch. "
            f"Be vivid and match the drama to the rarity: legendary > rare > common."
        )
        raw = gl.nondet.exec_prompt(prompt)
        return gl.eq_principle.prompt_comparative(
            raw,
            principle=(
                "The stories describe catching the same fish species with an excitement level "
                "appropriate to its rarity. Minor wording differences are acceptable."
            )
        )

    # ── AI PLAYER ANALYSIS (view) ──
    # FIX: replaced template string with gl.nondet.exec_prompt
    # wrapped in gl.eq_principle.prompt_comparative.
    @gl.public.view
    def get_player_analysis(self, a: str) -> str:
        a = self._normalize_addr(a)
        p = self._get(a)
        name = self.names.get(a, "Unknown")

        catches = p.get("catches", [])
        total_catches = len([c for c in catches if c["fish"] != "empty"])
        rare_catches = len([c for c in catches if c["rarity"] in ["rare", "legendary"]])

        prompt = (
            f"You are a fishing game coach. Analyse the performance of player '{name}': "
            f"{p['total_casts']} total casts, {total_catches} successful catches, "
            f"{rare_catches} rare or legendary catches, {p['balance']} tokens in balance. "
            f"Give personalised, encouraging advice in 2-3 sentences. "
            f"Mention specific stats and suggest what they should do next."
        )
        raw = gl.nondet.exec_prompt(prompt)
        analysis = gl.eq_principle.prompt_comparative(
            raw,
            principle=(
                "The analyses reference the same player statistics and give similarly "
                "encouraging advice. Minor phrasing differences are acceptable."
            )
        )

        return json.dumps({
            "name": name,
            "analysis": analysis,
            "stats": {
                "total_casts": p["total_casts"],
                "successful_catches": total_catches,
                "rare_catches": rare_catches,
                "balance": p["balance"]
            }
        })

    # ── REGISTER / RENAME ──
    @gl.public.write
    def register(self, name: str):
        a = self._normalize_addr(gl.message.sender_address)

        if name in self.name_map:
            assert self.name_map[name] == a, "Name taken"

        if a in self.names:
            old = self.names[a]
            if old in self.name_map:
                del self.name_map[old]

        self.names[a] = name
        self.name_map[name] = a

        p = self._get(a)
        self._save(a, p)

    @gl.public.write
    def set_name(self, name: str):
        self.register(name)

    # ── CAST (write) ──
    # FIX: weather is now fetched via gl.eq_principle.web_based (inside
    # _get_fishing_conditions) so the temperature value — which drives the
    # seed and the catch outcome — is identical across all validators before
    # any state is written.
    # FIX: rare/legendary stories are generated with gl.nondet.exec_prompt +
    # gl.eq_principle.prompt_comparative so the stored story is also agreed
    # upon by all validators.
    @gl.public.write
    def cast(self):
        a = self._normalize_addr(gl.message.sender_address)
        p = self._get(a)

        rod  = RODS[p["rod"]]
        bait = BAITS[p["bait"]]

        # Weather resolved via eq_principle — all validators see the same value
        conditions   = self._get_fishing_conditions()
        weather_bonus = conditions["fishing_bonus"]

        seed = int(self.counter) + sum(ord(c) for c in a) + int(conditions["temperature"])
        self.counter = bigint(int(self.counter) + 1)

        empty_chance     = max(0, 30 - bait["catch"] - weather_bonus - rod.get("catch_bonus", 0))
        legendary_chance = 2  + rod["legendary"]
        rare_chance      = 15 + rod["rare"] + bait["rare"]
        uncommon_chance  = 25

        roll = seed % 100

        if roll < empty_chance:
            fish, rarity, pts = "empty", "empty", 0
        elif roll < empty_chance + legendary_chance:
            fish   = FISH_BY_RARITY["legendary"][seed % len(FISH_BY_RARITY["legendary"])]
            rarity, pts = "legendary", FISH_POINTS[fish]
        elif roll < empty_chance + legendary_chance + rare_chance:
            fish   = FISH_BY_RARITY["rare"][seed % len(FISH_BY_RARITY["rare"])]
            rarity, pts = "rare", FISH_POINTS[fish]
        elif roll < empty_chance + legendary_chance + rare_chance + uncommon_chance:
            fish   = FISH_BY_RARITY["uncommon"][seed % len(FISH_BY_RARITY["uncommon"])]
            rarity, pts = "uncommon", FISH_POINTS[fish]
        else:
            fish   = FISH_BY_RARITY["common"][seed % len(FISH_BY_RARITY["common"])]
            rarity, pts = "common", FISH_POINTS[fish]

        if p["bait"] != "none":
            inv = p.get("bait_inventory", {})
            current = p["bait"]
            inv[current] = inv.get(current, 1) - 1
            if inv[current] <= 0:
                del inv[current]
                p["bait"] = "none"
            p["bait_inventory"] = inv

        story   = ""
        message = "Missed..."

        if fish != "empty":
            p["balance"]      += pts
            p["total_earned"] += pts
            p["total_fish"]    = p.get("total_fish", 0) + 1
            message = f"You caught a {fish}!"

            # AI-generated story for rare / legendary catches
            # Uses gl.nondet.exec_prompt + gl.eq_principle.prompt_comparative
            # so validators agree on the stored story before writing state.
            if rarity in ["rare", "legendary"]:
                prompt = (
                    f"You are a fishing game narrator. A player just caught a "
                    f"{rarity}-rarity {fish} in {conditions['condition']} weather. "
                    f"Write an exciting 1-2 sentence story about this legendary moment."
                )
                raw_story = gl.nondet.exec_prompt(prompt)
                story = gl.eq_principle.prompt_comparative(
                    raw_story,
                    principle=(
                        "The stories describe the same fish catch with excitement "
                        "appropriate to its rarity. Minor wording differences are fine."
                    )
                )

        p["total_casts"] += 1

        c = p["catches"]
        if len(c) >= 10:
            c = c[-9:]

        c.append({
            "fish":    fish,
            "rarity":  rarity,
            "points":  pts,
            "message": message,
            "weather": conditions["condition"],
            "story":   story
        })

        p["catches"] = c
        self._save(a, p)

    # ── SHOP ──
    @gl.public.write
    def buy_rod(self, r: str):
        a = self._normalize_addr(gl.message.sender_address)
        p = self._get(a)

        assert r in RODS
        price = RODS[r]["price"]

        assert p["balance"] >= price
        assert r not in p["inventory"]["rods"]

        p["balance"] -= price
        p["inventory"]["rods"].append(r)

        self._save(a, p)

    @gl.public.write
    def buy_bait(self, b: str):
        a = self._normalize_addr(gl.message.sender_address)
        p = self._get(a)

        assert b in BAITS and b != "none"
        price = BAITS[b]["price"]
        assert p["balance"] >= price

        p["balance"] -= price

        # Add to bait inventory — does NOT auto-equip
        inv = p.get("bait_inventory", {})
        inv[b] = inv.get(b, 0) + 1
        p["bait_inventory"] = inv

        self._save(a, p)

    @gl.public.write
    def equip_bait(self, b: str):
        a = self._normalize_addr(gl.message.sender_address)
        p = self._get(a)

        if b == "none":
            p["bait"] = "none"
        else:
            inv = p.get("bait_inventory", {})
            assert inv.get(b, 0) > 0, "You don't own this bait"
            p["bait"] = b

        self._save(a, p)

    @gl.public.write
    def equip_rod(self, r: str):
        a = self._normalize_addr(gl.message.sender_address)
        p = self._get(a)

        assert r in p["inventory"]["rods"]

        p["rod"] = r
        self._save(a, p)

    # ── VIEW ──
    @gl.public.view
    def get_stats(self, a: str):
        original_a = a
        a = self._normalize_addr(a)
        exists = a in self.players
        p = self._get(a)
        name = self.names.get(a, "Unknown")

        return json.dumps({
            "debug": {
                "original_input":    original_a,
                "normalized":        a,
                "exists_in_players": exists,
                "player_count":      len(self.players)
            },
            "name":          name,
            "balance":       p["balance"],
            "total_earned":  p["total_earned"],
            "total_casts":   p["total_casts"],
            "rod":           p["rod"],
            "bait":          p["bait"],
            "bait_count":    p.get("bait_count", 0),
            "bait_inventory": p.get("bait_inventory", {}),
            "inventory":     p["inventory"],
            "recent_catches": p["catches"]
        })

    @gl.public.view
    def get_leaderboard(self):
        arr = []
        for a in self.leaderboard:
            arr.append({
                "address": a,
                "name":    self.names.get(a, "Unknown"),
                "points":  int(self.leaderboard[a])
            })
        arr.sort(key=lambda x: x["points"], reverse=True)
        return json.dumps(arr[:10])

    @gl.public.view
    def get_current_weather(self):
        conditions = self._get_fishing_conditions()
        return json.dumps(conditions)

    # ── DEBUG ──
    @gl.public.view
    def debug_check_player(self, a: str):
        a = self._normalize_addr(a)
        exists  = a in self.players
        has_name = a in self.names

        if exists:
            raw_data = self.players[a]
            return json.dumps({
                "address_normalized":  a,
                "exists_in_players":   exists,
                "has_name_registered": has_name,
                "raw_data":            raw_data,
                "parsed":              json.loads(raw_data)
            })
        else:
            return json.dumps({
                "address_normalized":  a,
                "exists_in_players":   exists,
                "has_name_registered": has_name,
                "message":             "Player not found in storage"
            })

    @gl.public.view
    def debug_list_registered(self):
        addresses = []
        for addr in self.players:
            name = self.names.get(addr, "Unknown")
            addresses.append({"address": addr, "name": name})
        return json.dumps(addresses)
