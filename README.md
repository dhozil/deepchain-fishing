# 🎣 DeepChain Fishing

![Status](https://img.shields.io/badge/status-live-brightgreen)
![Network](https://img.shields.io/badge/network-GenLayer-blue)
![License](https://img.shields.io/badge/license-MIT-yellow)
![Built With](https://img.shields.io/badge/built%20with-Vite%20%2B%20GenLayer%20SDK-orange)

**DeepChain Fishing** is a fully on-chain fishing game built on **GenLayer Intelligent Contracts**.
Every action — from casting your line to upgrading gear — is executed and stored directly on the blockchain.

---

##  Features

* 🎣 **Fully On-Chain Gameplay**
  * Every fishing action is processed by a smart contract
  * Transparent and verifiable results

* 🏷️ **Player Identity System**
  * Choose your own nickname
  * Linked permanently to your wallet address

* 🛒 **Shop & Equipment**
  * Buy rods with rarity bonuses and catch rate improvements
  * Use bait to increase catch rates and rare fish chances
  * Equip different rods for better performance

* 🐟 **Rich Fish System**
  * Multiple fish with rarity tiers (Common, Uncommon, Rare, Legendary)
  * Each fish has unique emoji and color
  * AI-generated stories for rare/legendary catches
  * Weather-based fishing conditions

* 🌤️ **Real-Time Weather Integration**
  * Web fetching for live weather data
  * Weather affects fishing conditions

* 🧠 **AI Story Generation**
  * LLM generates unique stories for rare/legendary catches
  * Powered by GenLayer's AI capabilities

* 🏆 **Global Leaderboard**
  * Ranked by total points
  * Fully stored on-chain

* ✨ **Modern UI/UX**
  * Loading spinner with fishing animation
  * Error modal with retry functionality
  * Disconnect wallet support
  * Responsive design

---

## ⚙️ Tech Stack

* Frontend: HTML, CSS, Vanilla JavaScript
* Build Tool: Vite
* Blockchain: GenLayer Studio
* SDK: genlayer-js
* Wallet: MetaMask
* Smart Contract: Python (GenLayer Intelligent Contracts)

---

## 🔗 Contract Information

* Network: GenLayer Studio (studionet)
* Chain ID: `0xF22F` (61999)
* Contract Address: `0x449fdBA5FBc4271E3bE01E9340EaA59246039d24`

---

## 🚀 How to Play

1. Connect your MetaMask wallet
2. Switch to GenLayer Studio network
3. Register your nickname
4. Click **Cast Line 🎣**
5. Catch fish and earn points
6. Upgrade your gear in the shop
7. Climb the leaderboard

---

## 🧠 Game Mechanics

### 🎲 Randomness

Fishing results are based on:

* Player wallet address
* Global cast count
* Real-time weather conditions
* Rod quality (catch bonus)
* Bait type (catch & rare bonuses)

This ensures:

* Deterministic outcomes
* No client-side manipulation

---

### 🐟 Rarity System

| Rarity    | Base Chance |
| --------- | ----------- |
| Empty     | ~20%        |
| Common    | ~28%        |
| Uncommon  | ~25%        |
| Rare      | ~15%        |
| Legendary | ~2%         |

Modifiers from rods and bait will influence outcomes.

---

### 🎣 Rods

| Rod        | Price  | Catch Bonus | Rare Bonus | Legendary Bonus |
| ---------- | ------ | ---------- | --------- | --------------- |
| Bamboo     | 0      | +10%       | 0%        | 0%              |
| Platinum   | 50     | +15%       | 15%       | 5%              |
| Adamantite | 150    | +20%       | 30%       | 10%             |
| Mythic     | 500    | +30%       | 50%       | 25%             |

---

### 🪱 Bait

| Bait        | Price | Catch Bonus | Rare Bonus |
| ----------- | ----- | ---------- | ---------- |
| Worm        | 10    | +20%       | 0%         |
| Shrimp      | 20    | +30%       | 10%        |
| Magic Lure  | 50    | +40%       | 20%        |
| Golden Bait | 100   | +60%       | 40%        |

---

## 🛠️ Local Setup

Clone the repository:

```bash
git clone https://github.com/dhozil/deepchain-fishing.git
cd deepchain-fishing
```

Install dependencies:

```bash
npm install
```

Run development server:

```bash
npm run dev
```

Build for production:

```bash
npm run build
```

---

## � Project Structure

```
deepchain-fishing/
│── contracts/
│   └── deepchain_fishing.py
│── src/
│   └── main.js
│── index.html
│── style.css
│── package.json
│── vite.config.js
│── README.md
```

---

## 🔌 RPC Endpoint

GenLayer Studio RPC is handled automatically via the genlayer-js SDK.

---

## ⚠️ Known Limitations

* ⏳ Transaction delay (8–15 seconds for consensus)
* 🌐 Depends on GenLayer validators
* 🦊 MetaMask may require manual network switching

---

## 🔮 Future Roadmap

* 🔊 Sound effects & immersive feedback
* 🎨 Advanced animations
* 🧠 Skill & leveling system
* 🎁 NFT fish collectibles
* ⚔️ PvP tournaments & seasonal leaderboard
* � PWA support for mobile

---

## 🤝 Contributing

Contributions are welcome!

* Fork the repo
* Create a new branch
* Submit a pull request

---

## 👨‍💻 Author

Built by **dhozil** for the GenLayer community 🚀

---

## 📜 License

MIT License
