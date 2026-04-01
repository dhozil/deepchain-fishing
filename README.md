# 🎣 Deep Chain Fishing Game

A blockchain-based fishing game built on GenLayer with smart contracts and web interface.

## 🎮 Game Features

- **Fishing Mechanics**: Cast your line and catch various fish with different rarities
- **Equipment System**: Buy and upgrade fishing rods and baits
- **Economy**: Earn points from catches and spend on better equipment
- **Leaderboard**: Compete with other players for the highest score
- **Smart Contract**: Fully decentralized game logic on GenLayer

## 🐟 Fish Collection

### Common Fish
- **Sardine** - 10 points
- **Catfish** - 20 points  
- **Carp** - 30 points

### Uncommon Fish
- **Bass** - 50 points
- **Trout** - 80 points
- **Salmon** - 100 points

### Rare Fish
- **Tuna** - 200 points
- **Swordfish** - 350 points
- **Shark** - 500 points

### Legendary Fish
- **Golden Koi** - 1,000 points
- **Giant Squid** - 2,000 points
- **Kraken** - 5,000 points

## 🎣 Equipment

### Fishing Rods
| Rod | Price | Rare Bonus | Legendary Bonus |
|-----|-------|------------|----------------|
| Bamboo | Free | 0% | 0% |
| Platinum | 50 points | 15% | 5% |
| Adamantite | 150 points | 30% | 10% |

### Baits
| Bait | Price | Catch Bonus | Rare Bonus |
|------|-------|-------------|------------|
| None | Free | 0% | 0% |
| Worm | 10 points | 20% | 0% |
| Shrimp | 20 points | 30% | 10% |
| Magic Lure | 50 points | 40% | 20% |

## 🚀 Getting Started

### Prerequisites
- Node.js (v14 or higher)
- Python (v3.8 or higher)
- GenLayer CLI
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/genlayer-fishing-game.git
   cd genlayer-fishing-game
   ```

2. **Install dependencies**
   ```bash
   # Frontend dependencies
   cd frontend
   npm install
   
   # Backend dependencies (if needed)
   cd ../contracts
   pip install -r requirements.txt
   ```

3. **Deploy Smart Contract**
   ```bash
   # Using GenLayer CLI
   genlayer deploy contracts/FishingGameFixed.py
   ```

4. **Configure Frontend**
   ```bash
   # Update contract address in frontend/src/config.js
   # Add your deployed contract address
   ```

5. **Start the application**
   ```bash
   # Start frontend
   cd frontend
   npm start
   
   # Or use web version
   # Open web-version/index.html in browser
   ```

## 🎯 How to Play

1. **Register**: Create your account with a unique name
2. **Cast Line**: Click "Cast" to try catching fish
3. **Earn Points**: Get points based on fish rarity
4. **Upgrade Equipment**: Buy better rods and baits to improve catch rates
5. **Compete**: Climb the leaderboard by earning the most points

### Game Mechanics

- **Catch Rates**: Base 30% empty, 25% common, 15% uncommon, 15% rare, 2% legendary
- **Bonuses**: Equipment improves your chances of catching rarer fish
- **Bait Consumption**: Bait is consumed after each cast (except "None")
- **Inventory**: You own all purchased equipment permanently

## 🏗️ Project Structure

```
genlayer-fishing-game/
├── contracts/                 # Smart contracts
│   ├── FishingGameFixed.py    # Main game contract (WORKING)
│   ├── FishingGameSimple.py   # Simplified version
│   └── FixedFishingCore.py    # Original version
├── frontend/                  # React frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── App.js           # Main app component
│   │   └── index.js         # Entry point
│   └── package.json
├── web-version/              # Static web version
│   └── index.html          # Single HTML file
└── README.md               # Documentation
```

## 🔧 Smart Contract API

### Write Functions
- `register(name)` - Register new player
- `cast()` - Cast fishing line
- `buy_rod(rod_type)` - Purchase fishing rod
- `buy_bait(bait_type)` - Purchase bait
- `equip_rod(rod_type)` - Equip owned rod

### View Functions
- `get_stats(address)` - Get player statistics
- `get_leaderboard()` - Get top 10 players
- `get_catalog()` - Get fish catalog
- `get_shop()` - Get available equipment

## 🌐 Web Version

A simplified web version is available in `web-version/index.html` that can be run directly in any modern browser without setup.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 Development

### Smart Contract Development
```bash
# Test contract locally
cd contracts
python -m unittest test_fishing_game.py

# Deploy to testnet
genlayer deploy --network testnet FishingGameFixed.py
```

### Frontend Development
```bash
cd frontend
npm start          # Development server
npm run build      # Production build
npm test          # Run tests
```

## 🐛 Troubleshooting

### Common Issues

1. **Contract Schema Loading Error**
   - Ensure runner comment is at top: `# { "runner": "python" }`
   - Check dependency comment: `# { "Depends": "py-genlayer:..." }`
   - Use `bigint` for storage variables

2. **Frontend Connection Issues**
   - Verify contract address in config
   - Check network connection
   - Ensure MetaMask/wallet is connected

3. **Transaction Failures**
   - Check wallet balance
   - Verify gas fees
   - Ensure correct function parameters

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- GenLayer team for the blockchain platform
- Community contributors and testers
- Open source libraries used in this project

## 🔗 Links

- [GenLayer Documentation](https://docs.genlayer.com)
- [Contract Demo](https://demo.genlayer.com/your-contract)
- [Live Game](https://yourgame.com)

---

**Made with ❤️ for the GenLayer ecosystem**

## 📋 Deployment Checklist

### GitHub Pages Setup
- [ ] Upload repository to GitHub
- [ ] Enable GitHub Pages
- [ ] Set source to `/web-version` folder
- [ ] Update contract address in web version
- [ ] Test live deployment

### Contract Deployment
- [ ] Deploy `FishingGameFixed.py` to GenLayer
- [ ] Verify contract on explorer
- [ ] Update contract address in README
- [ ] Test all contract functions

### Final Testing
- [ ] Test web version locally
- [ ] Test MetaMask integration
- [ ] Verify all game mechanics
- [ ] Check mobile responsiveness
- [ ] Validate leaderboard functionality
