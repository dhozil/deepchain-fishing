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
    weather_cache: TreeMap[str,str]  # Cache untuk data cuaca

    def __init__(self):
        self.players = TreeMap()
        self.names = TreeMap()
        self.name_map = TreeMap()
        self.leaderboard = TreeMap()
        self.counter = bigint(0)
        self.weather_cache = TreeMap()

    def _normalize_addr(self, a: str) -> str:
        """Normalize wallet address to lowercase for consistent storage
        
        Args:
            a: Wallet address (e.g., "0xAbC123..." or "0xabc123...")
        
        Returns:
            Lowercase address string (e.g., "0xabc123...")
        """
        return str(a).lower()

    def _get(self, a: str):
        # a = player wallet address (e.g., "0x1234...")
        a = self._normalize_addr(a)
        if a not in self.players:
            return {
                "balance":100,
                "total_earned":0,
                "rod":"bamboo",
                "bait":"none",
                "inventory":{"rods":["bamboo"],"baits":[]},
                "catches":[],
                "total_casts":0,
                "fishing_stories":[]
            }
        return json.loads(self.players[a])

    def _save(self, a: str, p: dict):
        # a = player wallet address (e.g., "0x1234...")
        a = self._normalize_addr(a)
        self.players[a]=json.dumps(p)
        self.leaderboard[a]=str(p["total_earned"])

    # ── STORY GENERATION: Simple template-based stories ──
    @gl.public.view
    def get_catch_story(self, fish: str, rarity: str, weather: str) -> str:
        """Generate fishing story based on catch details
        
        Args:
            fish: Fish name (e.g., "Tuna", "Swordfish")
            rarity: Rarity level (e.g., "common", "rare", "legendary")
            weather: Weather condition (e.g., "sunny", "rainy")
        """
        if rarity == "legendary":
            return "An incredible catch! The legendary " + fish + " put up an epic fight before surrendering to your skill in " + weather + " conditions."
        elif rarity == "rare":
            return "A rare beauty! The " + fish + " shimmered as you pulled it from the " + weather + " waters."
        return "You caught a " + fish + "! Great catch on this " + weather + " day!"

    # ── WEB FETCHING: Get Real Weather Data (GenLayer Feature) ──
    def _get_fishing_conditions(self) -> dict:
        # Equivalence Principle: Try web fetch, fallback to deterministic calculation
        # This ensures transaction never fails due to external API issues
        try:
            # Try to fetch real weather data (GenLayer web fetching feature)
            response = gl.get_web("https://api.open-meteo.com/v1/forecast?latitude=-6.2088&longitude=106.8456&current_weather=true")
            
            if response and len(response) > 0:
                weather_data = json.loads(response)
                
                temp = weather_data.get("current_weather", {}).get("temperature", 25)
                condition = "sunny" if temp > 25 else "cloudy" if temp > 20 else "rainy"
                
                # Better weather = better fishing bonus
                fishing_bonus = 10 if condition == "sunny" else 5 if condition == "cloudy" else 0
                
                return {
                    "condition": condition,
                    "temperature": temp,
                    "fishing_bonus": fishing_bonus,
                    "source": "web_fetch"  # Track data source
                }
        except:
            pass  # Silently fail to fallback (Equivalence Principle)
        
        # Fallback: Deterministic calculation based on counter (Equivalence Principle)
        # This ensures equivalent behavior even without web access
        conditions = ["sunny", "cloudy", "rainy"]
        condition = conditions[int(self.counter) % 3]
        
        fishing_bonus = 10 if condition == "sunny" else 5 if condition == "cloudy" else 0
        temp = 25 + (int(self.counter) % 10)
        
        return {
            "condition": condition,
            "temperature": temp,
            "fishing_bonus": fishing_bonus,
            "source": "fallback"  # Track data source
        }

    # ── REGISTER / RENAME ──
    @gl.public.write
    def register(self,name:str):
        a=self._normalize_addr(gl.message.sender_address)

        if name in self.name_map:
            assert self.name_map[name]==a,"Name taken"

        if a in self.names:
            old=self.names[a]
            if old in self.name_map:
                del self.name_map[old]

        self.names[a]=name
        self.name_map[name]=a

        p=self._get(a)
        self._save(a,p)

    @gl.public.write
    def set_name(self,name:str):
        self.register(name)

    # ── GAME with Web Fetching Integration ──
    @gl.public.write
    def cast(self):
        a=self._normalize_addr(gl.message.sender_address)
        p=self._get(a)
        player_name = self.names.get(a, "Unknown")

        rod=RODS[p["rod"]]
        bait=BAITS[p["bait"]]

        # WEB FETCHING: Get real-time fishing conditions
        conditions = self._get_fishing_conditions()
        weather_bonus = conditions["fishing_bonus"]

        seed=int(self.counter)+sum(ord(c) for c in a)+int(conditions["temperature"])
        self.counter=bigint(int(self.counter)+1)

        # Modified drop rates based on real weather and rod quality
        empty_chance = max(0, 30 - bait["catch"] - weather_bonus - rod.get("catch_bonus", 0))
        legendary_chance = 2 + rod["legendary"]
        rare_chance = 15 + rod["rare"] + bait["rare"]
        uncommon_chance = 25

        roll = seed % 100

        if roll < empty_chance:
            fish,rarity,pts = "empty","empty",0
        elif roll < empty_chance + legendary_chance:
            fish = FISH_BY_RARITY["legendary"][seed % len(FISH_BY_RARITY["legendary"])]
            rarity,pts = "legendary",FISH_POINTS[fish]
        elif roll < empty_chance + legendary_chance + rare_chance:
            fish = FISH_BY_RARITY["rare"][seed % len(FISH_BY_RARITY["rare"])]
            rarity,pts = "rare",FISH_POINTS[fish]
        elif roll < empty_chance + legendary_chance + rare_chance + uncommon_chance:
            fish = FISH_BY_RARITY["uncommon"][seed % len(FISH_BY_RARITY["uncommon"])]
            rarity,pts = "uncommon",FISH_POINTS[fish]
        else:
            fish = FISH_BY_RARITY["common"][seed % len(FISH_BY_RARITY["common"])]
            rarity,pts = "common",FISH_POINTS[fish]

        if p["bait"]!="none":
            p["bait"]="none"

        # Store catch data - story generated separately via LLM view method
        story = ""
        message = "Missed..."
        
        if fish!="empty":
            p["balance"]+=pts
            p["total_earned"]+=pts
            p["total_fish"]=p.get("total_fish",0)+1
            message = "You caught a " + fish + "!"
            # Story placeholder - call get_catch_story view method for LLM-generated story
            if rarity in ["rare", "legendary"]:
                story = "[Call get_catch_story for AI story]"

        p["total_casts"]+=1

        c=p["catches"]
        if len(c)>=10:
            c=c[-9:]

        catch_record = {
            "fish":fish,
            "rarity":rarity,
            "points":pts,
            "message":message,
            "weather":conditions["condition"],
            "story":story
        }
        c.append(catch_record)

        p["catches"]=c
        self._save(a,p)

    # ── SHOP ──
    @gl.public.write
    def buy_rod(self,r:str):
        a=self._normalize_addr(gl.message.sender_address)
        p=self._get(a)

        assert r in RODS
        price=RODS[r]["price"]

        assert p["balance"]>=price
        assert r not in p["inventory"]["rods"]

        p["balance"]-=price
        p["inventory"]["rods"].append(r)

        self._save(a,p)

    @gl.public.write
    def buy_bait(self,b:str):
        a=self._normalize_addr(gl.message.sender_address)
        p=self._get(a)

        assert b in BAITS and b!="none"
        price=BAITS[b]["price"]

        assert p["balance"]>=price

        p["balance"]-=price
        p["bait"]=b

        self._save(a,p)

    @gl.public.write
    def equip_rod(self,r:str):
        a=self._normalize_addr(gl.message.sender_address)
        p=self._get(a)

        assert r in p["inventory"]["rods"]

        p["rod"]=r
        self._save(a,p)

    # ── PLAYER ANALYSIS: Template-based performance analysis ──
    @gl.public.view
    def get_player_analysis(self, a: str) -> str:
        """Generate player performance analysis
        
        Args:
            a: Player wallet address (e.g., "0x1234...")
        """
        a = self._normalize_addr(a)
        p = self._get(a)
        name = self.names.get(a, "Unknown")
        
        catches = p.get("catches", [])
        if len(catches) == 0:
            return json.dumps({"name": name, "analysis": "No fishing data yet. Start casting!"})
        
        total_catches = len([c for c in catches if c["fish"] != "empty"])
        rare_catches = len([c for c in catches if c["rarity"] in ["rare", "legendary"]])
        
        # Template-based analysis
        if rare_catches > 5:
            analysis = "Amazing angler! You have caught " + str(rare_catches) + " rare fish. Your skill is truly impressive!"
        elif total_catches > 20:
            analysis = "Great progress! " + str(total_catches) + " successful catches shows dedication. Keep upgrading your gear!"
        else:
            analysis = "Keep fishing! Practice makes perfect. You have " + str(total_catches) + " catches so far."
        
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

    # ── VIEW ──
    @gl.public.view
    def get_stats(self, a: str):
        """Get player statistics
        
        Args:
            a: Player wallet address (e.g., "0x1234...")
        """
        original_a = a
        a=self._normalize_addr(a)
        exists = a in self.players
        p=self._get(a)
        name=self.names.get(a,"Unknown")

        return json.dumps({
            "debug":{
                "original_input":original_a,
                "normalized":a,
                "exists_in_players":exists,
                "player_count":len(self.players)
            },
            "name":name,
            "balance":p["balance"],
            "total_earned":p["total_earned"],
            "total_casts":p["total_casts"],
            "rod":p["rod"],
            "bait":p["bait"],
            "inventory":p["inventory"],
            "recent_catches":p["catches"]
        })

    @gl.public.view
    def get_leaderboard(self):
        arr=[]
        for a in self.leaderboard:
            arr.append({
                "address":a,
                "name":self.names.get(a,"Unknown"),
                "points":int(self.leaderboard[a])
            })

        arr.sort(key=lambda x:x["points"],reverse=True)
        return json.dumps(arr[:10])

    @gl.public.view
    def get_current_weather(self):
        conditions = self._get_fishing_conditions()
        return json.dumps(conditions)

    # ── DEBUG ──
    @gl.public.view
    def debug_check_player(self, a: str):
        """Debug method to check player storage status
        
        Args:
            a: Player wallet address (e.g., "0x1234...")
        """
        a = self._normalize_addr(a)
        exists = a in self.players
        has_name = a in self.names
        
        if exists:
            raw_data = self.players[a]
            return json.dumps({
                "address_normalized": a,
                "exists_in_players": exists,
                "has_name_registered": has_name,
                "raw_data": raw_data,
                "parsed": json.loads(raw_data)
            })
        else:
            return json.dumps({
                "address_normalized": a,
                "exists_in_players": exists,
                "has_name_registered": has_name,
                "message": "Player not found in storage"
            })

    @gl.public.view  
    def debug_list_registered(self):
        """List all registered addresses"""
        addresses = []
        for addr in self.players:
            name = self.names.get(addr, "Unknown")
            addresses.append({"address": addr, "name": name})
        return json.dumps(addresses)
