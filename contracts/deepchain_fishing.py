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
    "bamboo": {"price":0,"rare":0,"legendary":0},
    "platinum": {"price":50,"rare":15,"legendary":5},
    "adamantite": {"price":150,"rare":30,"legendary":10},
    "mythic": {"price":500,"rare":50,"legendary":25}
}

BAITS = {
    "none": {"price":0,"catch":0,"rare":0},
    "worm": {"price":10,"catch":20,"rare":0},
    "shrimp": {"price":20,"catch":30,"rare":10},
    "magic_lure": {"price":50,"catch":40,"rare":20},
    "golden_bait": {"price":100,"catch":60,"rare":40}
}

def pick(seed, catch, rare, legendary):
    roll = seed % 100

    empty = max(0, 30 - catch)
    legendary_chance = 2 + legendary
    rare_chance = 15 + rare
    uncommon_chance = 25

    if roll < empty:
        return "empty","empty",0

    elif roll < empty + legendary_chance:
        fish = FISH_BY_RARITY["legendary"][seed % len(FISH_BY_RARITY["legendary"])]
        return fish,"legendary",FISH_POINTS[fish]

    elif roll < empty + legendary_chance + rare_chance:
        fish = FISH_BY_RARITY["rare"][seed % len(FISH_BY_RARITY["rare"])]
        return fish,"rare",FISH_POINTS[fish]

    elif roll < empty + legendary_chance + rare_chance + uncommon_chance:
        fish = FISH_BY_RARITY["uncommon"][seed % len(FISH_BY_RARITY["uncommon"])]
        return fish,"uncommon",FISH_POINTS[fish]

    else:
        fish = FISH_BY_RARITY["common"][seed % len(FISH_BY_RARITY["common"])]
        return fish,"common",FISH_POINTS[fish]


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

    def _get(self,a):
        if a not in self.players:
            return {
                "balance":100,
                "total_earned":0,
                "rod":"bamboo",
                "bait":"none",
                "inventory":{"rods":["bamboo"],"baits":[]},
                "catches":[],
                "total_casts":0
            }
        return json.loads(self.players[a])

    def _save(self,a,p):
        self.players[a]=json.dumps(p)
        self.leaderboard[a]=str(p["total_earned"])

    # ── REGISTER / RENAME ──
    @gl.public.write
    def register(self,name:str):
        a=str(gl.message.sender_address)

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

    # ── GAME ──
    @gl.public.write
    def cast(self):
        a=str(gl.message.sender_address)
        p=self._get(a)

        rod=RODS[p["rod"]]
        bait=BAITS[p["bait"]]

        seed=int(self.counter)+sum(ord(c) for c in a)
        self.counter=bigint(int(self.counter)+1)

        fish,rarity,pts = pick(seed,bait["catch"],rod["rare"]+bait["rare"],rod["legendary"])

        if p["bait"]!="none":
            p["bait"]="none"

        if fish!="empty":
            p["balance"]+=pts
            p["total_earned"]+=pts

        p["total_casts"]+=1

        c=p["catches"]
        if len(c)>=10:
            c=c[-9:]

        c.append({
            "fish":fish,
            "rarity":rarity,
            "points":pts,
            "message":"You caught "+fish if fish!="empty" else "Missed..."
        })

        p["catches"]=c
        self._save(a,p)

    # ── SHOP ──
    @gl.public.write
    def buy_rod(self,r:str):
        a=str(gl.message.sender_address)
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
        a=str(gl.message.sender_address)
        p=self._get(a)

        assert b in BAITS and b!="none"
        price=BAITS[b]["price"]

        assert p["balance"]>=price

        p["balance"]-=price
        p["bait"]=b

        self._save(a,p)

    @gl.public.write
    def equip_rod(self,r:str):
        a=str(gl.message.sender_address)
        p=self._get(a)

        assert r in p["inventory"]["rods"]

        p["rod"]=r
        self._save(a,p)

    # ── VIEW ──
    @gl.public.view
    def get_stats(self,a:str):
        p=self._get(a)
        name=self.names.get(a,"Unknown")

        return json.dumps({
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
