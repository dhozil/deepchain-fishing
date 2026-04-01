# 🎣 DeepChain Fishing

![Status](https://img.shields.io/badge/status-live-brightgreen)
![Network](https://img.shields.io/badge/network-GenLayer-blue)
![License](https://img.shields.io/badge/license-MIT-yellow)
![Built With](https://img.shields.io/badge/built%20with-JavaScript-orange)

**DeepChain Fishing** is a fully on-chain fishing game built on **GenLayer Intelligent Contracts**.
Every action — from casting your line to upgrading gear — is executed and stored directly on the blockchain.

---

## 🎮 Game Preview

> Add your gameplay screenshot or GIF here
> Example:
> ![preview](./assets/preview.gif)

---

## 🌊 Features

* 🎣 **Fully On-Chain Gameplay**

  * Every fishing action is processed by a smart contract
  * Transparent and verifiable results

* 🏷️ **Player Identity System**

  * Choose your own nickname
  * Linked permanently to your wallet address

* 🛒 **Shop & Equipment**

  * Buy rods with rarity bonuses
  * Use bait to increase catch rates

* 🐟 **Rich Fish System**

  * Multiple fish with rarity tiers:

    * Common
    * Uncommon
    * Rare
    * Legendary
  * Each fish gives different rewards

* 🏆 **Global Leaderboard**

  * Ranked by total points
  * Fully stored on-chain

---

## ⚙️ Tech Stack

* Frontend: HTML, CSS, Vanilla JavaScript
* Blockchain: GenLayer Studio
* Wallet: MetaMask
* Smart Contract: Python (GenLayer Intelligent Contracts)

---

## 🔗 Contract Information

* Network: GenLayer Studio
* Chain ID: `0xF22F` (61999)
* Contract Address:
  `0xA258E47F6A2D3CAf0469127677E5963093fbCA62`

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

This ensures:

* Deterministic outcomes
* No client-side manipulation

---

### 🐟 Rarity System

| Rarity    | Base Chance |
| --------- | ----------- |
| Empty     | ~30%        |
| Common    | ~28%        |
| Uncommon  | ~25%        |
| Rare      | ~15%        |
| Legendary | ~2%         |

Modifiers from rods and bait will influence outcomes.

---

## 🛠️ Local Setup

Clone the repository:

git clone https://github.com/dhozil/deepchain-fishing.git
cd deepchain-fishing

Run the game:

Open `index.html` in your browser

---

## 🔌 RPC Endpoint

https://studio.genlayer.com/api

Used for:

* `gen_call` → read contract
* `eth_sendTransaction` → write contract

---

## ⚠️ Known Limitations

* ⏳ Transaction delay (5–10 seconds)
* 🌐 Depends on GenLayer validators
* 🦊 MetaMask may require manual network switching

---

## 🔮 Future Roadmap

* 🔊 Sound effects & immersive feedback
* 🎨 Advanced animations
* 🧠 Skill & leveling system
* 🎁 NFT fish collectibles
* ⚔️ PvP tournaments & seasonal leaderboard

---

## 📁 Project Structure

```
deepchain-fishing/
│── index.html
│── README.md
│── assets/
│   ├── preview.png
│   └── preview.gif
```

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
