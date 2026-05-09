import { createClient } from 'genlayer-js';
import { studionet } from 'genlayer-js/chains';
import { TransactionStatus } from 'genlayer-js/types';

// ============================================
// GENLAYER CONFIGURATION
// ============================================
const CONTRACT_ADDRESS = "0xA8d1086D8711A8d5C1D5393053927Ad3A9C0710c";

// Mock mode untuk testing UI (set true kalau contract error)
const MOCK_MODE = false;

// ============================================
// FISH EMOJI & COLOR MAPPING
// ============================================
const FISH_EMOJIS = {
    // Common fish
    'Sardine': '🐟',
    'Anchovy': '🐟',
    'Carp': '🐟',
    'Tilapia': '🐟',
    'Mackerel': '🐟',
    'Herring': '🐟',
    // Uncommon fish
    'Bass': '🐠',
    'Trout': '🐠',
    'Salmon': '🐟',
    'Snapper': '🐠',
    'Pike': '🐟',
    'Cod': '🐟',
    // Rare fish
    'Tuna': '🐟',
    'Swordfish': '🐡',
    'Shark': '🦈',
    'Barracuda': '🐟',
    'Marlin': '🐟',
    'Sturgeon': '🐟',
    // Legendary fish
    'Golden Koi': '🎏',
    'Kraken': '🦑',
    'Leviathan': '🐋',
    'Giant Squid': '🦑'
};

const FISH_COLORS = {
    // Common fish - varied gray/blue tones
    'Sardine': '#7aa8b0',
    'Anchovy': '#8ba8b0',
    'Carp': '#a8a8a8',
    'Tilapia': '#7aa8b0',
    'Mackerel': '#6a98a0',
    'Herring': '#8ab0b8',
    // Uncommon fish - varied green/orange tones
    'Bass': '#4caf50',
    'Trout': '#66bb6a',
    'Salmon': '#ff7043',
    'Snapper': '#ff8a65',
    'Pike': '#81c784',
    'Cod': '#a5d6a7',
    // Rare fish - varied blue/purple tones
    'Tuna': '#2196f3',
    'Swordfish': '#42a5f5',
    'Shark': '#607d8b',
    'Barracuda': '#26a69a',
    'Marlin': '#00bcd4',
    'Sturgeon': '#0097a7',
    // Legendary fish - varied gold/purple/red tones
    'Golden Koi': '#ffd700',
    'Kraken': '#9c27b0',
    'Leviathan': '#e91e63',
    'Giant Squid': '#673ab7'
};

function getFishEmoji(fishName) {
    return FISH_EMOJIS[fishName] || '🐟';
}

function getFishColor(fishName) {
    return FISH_COLORS[fishName] || '#aaa';
}

// ============================================
// GENLAYER CLIENTS
// ============================================
let readClient = null;
let writeClient = null;
let userAddress = null;

// Initialize GenLayer clients
function initGenLayerClients() {
    if (!window.ethereum) {
        console.error('MetaMask not found');
        return;
    }

    // Read client - no wallet needed
    readClient = createClient({
        chain: studionet,
    });

    // Write client - will be configured when wallet connects
    // We'll set this in connectWallet()
}

// ============================================
// RPC HELPERS (GENLAYER SDK)
// ============================================
async function genCall(method, args = []) {
    console.log('genCall:', method, args, 'MOCK_MODE:', MOCK_MODE);

    if (MOCK_MODE) {
        // Return mock data for testing UI
        if (method === 'get_leaderboard') {
            return [
                {address: '0x1234...5678', name: 'FisherKing', points: 1250},
                {address: '0xabcd...efgh', name: 'OceanMaster', points: 980},
                {address: '0x9999...0000', name: 'DeepDiver', points: 750}
            ];
        }
        if (method === 'get_stats') {
            return {
                debug: {
                    original_input: args[0],
                    normalized: args[0],
                    exists_in_players: true,
                    player_count: 1
                },
                name: 'TestPlayer',
                balance: 100,
                total_earned: 0,
                total_casts: 0,
                rod: 'bamboo',
                bait: 'none',
                inventory: {
                    rods: ['bamboo'],
                    baits: []
                },
                recent_catches: []
            };
        }
        // Mock cast - return random fish
        if (method === 'cast') {
            const fishTypes = [
                {fish: 'Sardine', rarity: 'common', points: 10},
                {fish: 'Anchovy', rarity: 'common', points: 12},
                {fish: 'Bass', rarity: 'uncommon', points: 40},
                {fish: 'Tuna', rarity: 'rare', points: 200},
                {fish: 'Shark', rarity: 'rare', points: 500},
                {fish: 'Golden Koi', rarity: 'legendary', points: 1200}
            ];
            const randomFish = fishTypes[Math.floor(Math.random() * fishTypes.length)];
            return randomFish;
        }
        return {};
    }

    if (!readClient) {
        throw new Error('GenLayer read client not initialized');
    }

    try {
        // Use GenLayer SDK readContract
        const result = await readClient.readContract({
            address: CONTRACT_ADDRESS,
            functionName: method,
            args: args
        });

        console.log('GenLayer readContract result:', result);
        return result;
    } catch (e) {
        console.error('genCall error:', e);
        throw e;
    }
}

async function sendTransaction(method, args = []) {
    if (!userAddress) throw new Error('Wallet not connected');

    // Mock mode for testing
    if (MOCK_MODE) {
        showStatus('Processing transaction (mock)...', '');
        await new Promise(resolve => setTimeout(resolve, 1000));

        if (method === 'register') {
            // Simulate successful registration
            playerData.nickname = args[0].replace(/"/g, '');
            isRegistered = true;
            showStatus('Registration successful!', 'success');
            return '0xmock_transaction_hash';
        }

        if (method === 'cast') {
            // Simulate cast with random fish
            const fishTypes = [
                {fish: 'Sardine', rarity: 'common', points: 10, emoji: '🐟'},
                {fish: 'Anchovy', rarity: 'common', points: 12, emoji: '🐠'},
                {fish: 'Bass', rarity: 'uncommon', points: 40, emoji: '🐟'},
                {fish: 'Tuna', rarity: 'rare', points: 200, emoji: '🐠'},
                {fish: 'Shark', rarity: 'rare', points: 500, emoji: '🦈'},
                {fish: 'Golden Koi', rarity: 'legendary', points: 1200, emoji: '👑'}
            ];
            const randomFish = fishTypes[Math.floor(Math.random() * fishTypes.length)];

            // Update player data
            playerData.tokens += randomFish.points;
            playerData.totalFish += 1;
            playerData.bestCatch = randomFish;

            showStatus('Transaction confirmed!', 'success');
            return '0xmock_transaction_hash';
        }

        if (method === 'buy_rod' || method === 'buy_bait') {
            showStatus('Purchase successful!', 'success');
            return '0xmock_transaction_hash';
        }

        return '0xmock_transaction_hash';
    }

    if (!writeClient) {
        throw new Error('GenLayer write client not initialized');
    }

    showStatus('Processing transaction...', '');

    try {
        console.log('Sending transaction:', method, args);

        // Use GenLayer SDK writeContract
        const txHash = await writeClient.writeContract({
            address: CONTRACT_ADDRESS,
            functionName: method,
            args: args,
            value: BigInt(0)
        });

        showStatus('Transaction sent! Waiting for consensus...', '');

        // Wait for transaction to be accepted
        await readClient.waitForTransactionReceipt({
            hash: txHash,
            status: TransactionStatus.ACCEPTED
        });

        showStatus('Transaction confirmed!', 'success');
        return txHash;
    } catch (error) {
        console.error('Transaction error details:', error);
        showStatus('Transaction failed: ' + error.message, 'error');
        throw error;
    }
}

// ============================================
// FISH DATA (Matching Contract)
// ============================================
const FISH_TYPES = {
    // Common
    'small_fish': { emoji: '🐟', name: 'Small Fish', tokens: 1, rarity: 'common' },
    'sardine': { emoji: '🐠', name: 'Sardine', tokens: 1, rarity: 'common' },
    'anchovy': { emoji: '🐡', name: 'Anchovy', tokens: 2, rarity: 'common' },
    
    // Rare
    'dolphin': { emoji: '🐬', name: 'Dolphin', tokens: 5, rarity: 'rare' },
    'tuna': { emoji: '🐠', name: 'Tuna', tokens: 4, rarity: 'rare' },
    'octopus': { emoji: '🐙', name: 'Octopus', tokens: 6, rarity: 'rare' },
    
    // Epic
    'shark': { emoji: '🦈', name: 'Shark', tokens: 12, rarity: 'epic' },
    'whale': { emoji: '🐋', name: 'Whale', tokens: 15, rarity: 'epic' },
    
    // Legendary
    'sea_dragon': { emoji: '🐉', name: 'Sea Dragon', tokens: 30, rarity: 'legendary' },
    'golden_fish': { emoji: '👑', name: 'Golden Fish', tokens: 25, rarity: 'legendary' }
};

// 🛒 SHOP SYSTEM
const SHOP_ITEMS = {
    rod_upgrade: {
        name: 'Rod Upgrade',
        getCost: (level) => level * 20,
        description: 'Upgrade fishing rod (Lv1→Lv2: 20, Lv2→Lv3: 40, Lv3→Lv4: 80)',
        action: 'upgradeRod'
    },
    bait: {
        name: 'Bait',
        cost: 5,
        description: 'Buy 3 bait (gives +1 token bonus)',
        action: 'buyBait'
    }
};

// STATE
let isConnected = false;
let isRegistered = false;
let playerData = {
    nickname: '',
    tokens: 0,
    rodLevel: 1,
    bait: 0,
    totalFish: 0,
    bestCatch: null
};

// 🏆 LEADERBOARD SYSTEM
let leaderboardData = [];

// Load saved data from localStorage
function loadGameData() {
    const savedData = localStorage.getItem('fishingGameData');
    if (savedData) {
        const data = JSON.parse(savedData);
        playerData = { ...playerData, ...data };
    }
    
    // Load leaderboard
    const savedLeaderboard = localStorage.getItem('fishingGameLeaderboard');
    if (savedLeaderboard) {
        leaderboardData = JSON.parse(savedLeaderboard);
    }
}

// Save game data to localStorage
function saveGameData() {
    const dataToSave = {
        nickname: playerData.nickname,
        tokens: playerData.tokens,
        rodLevel: playerData.rodLevel,
        bait: playerData.bait,
        totalFish: playerData.totalFish,
        bestCatch: playerData.bestCatch
    };
    localStorage.setItem('fishingGameData', JSON.stringify(dataToSave));
}

// Update leaderboard
function updateLeaderboard() {
    if (!userAddress || !playerData.nickname) return;
    
    // Find existing player in leaderboard
    const existingPlayerIndex = leaderboardData.findIndex(p => p.address === userAddress);
    
    const playerEntry = {
        address: userAddress,
        nickname: playerData.nickname,
        tokens: playerData.tokens,
        totalFish: playerData.totalFish,
        lastUpdated: Date.now()
    };
    
    if (existingPlayerIndex >= 0) {
        // Update existing player
        leaderboardData[existingPlayerIndex] = playerEntry;
    } else {
        // Add new player
        leaderboardData.push(playerEntry);
    }
    
    // Sort by tokens (descending)
    leaderboardData.sort((a, b) => b.tokens - a.tokens);
    
    // Keep only top 50 players
    leaderboardData = leaderboardData.slice(0, 50);
    
    // Save to localStorage
    localStorage.setItem('fishingGameLeaderboard', JSON.stringify(leaderboardData));
    
    // Update UI
    renderLeaderboard();
}

// Render leaderboard
function renderLeaderboard() {
    const leaderboardList = document.getElementById('leaderboardList');
    
    if (leaderboardData.length === 0) {
        leaderboardList.innerHTML = `
            <div class="leaderboard-item">
                <span class="leaderboard-rank">-</span>
                <span class="leaderboard-name">No players yet</span>
                <span class="leaderboard-tokens">0</span>
            </div>
        `;
        return;
    }
    
    leaderboardList.innerHTML = leaderboardData.slice(0, 10).map((player, index) => {
        const rankClass = index === 0 ? 'gold' : index === 1 ? 'silver' : index === 2 ? 'bronze' : '';
        const isCurrentPlayer = player.address === userAddress;
        
        return `
            <div class="leaderboard-item ${isCurrentPlayer ? 'current-player' : ''}">
                <span class="leaderboard-rank ${rankClass}">
                    ${index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : `${index + 1}th`}
                </span>
                <span class="leaderboard-name">${player.nickname}</span>
                <span class="leaderboard-tokens">${player.tokens.toLocaleString()}</span>
            </div>
        `;
    }).join('');
}

// ELEMENTS
const walletBtn = document.getElementById('connectWalletBtn');
const nicknameInput = document.getElementById('nicknameInput');
const fishingScreen = document.getElementById('fishingScreen');
const castBtn = document.getElementById('castBtn');

// STATUS
function showStatus(message, type = '') {
    const statusBar = document.getElementById('statusBar');
    if (!statusBar) return;

    statusBar.textContent = message;
    statusBar.className = type;
    statusBar.style.display = 'block';

    if (type === 'success') {
        setTimeout(() => statusBar.style.display = 'none', 3000);
    }
}

// LOADING SPINNER
function showLoading(text = 'Processing...', showFishingAnim = false) {
    const loadingOverlay = document.getElementById('loadingOverlay');
    const loadingText = document.getElementById('loadingText');
    const fishingAnimation = document.getElementById('fishingAnimation');
    const spinner = document.querySelector('.spinner');

    if (loadingOverlay) {
        loadingOverlay.style.display = 'flex';
    }
    if (loadingText) {
        loadingText.textContent = text;
    }

    if (showFishingAnim) {
        if (fishingAnimation) {
            fishingAnimation.style.display = 'block';
        }
        if (spinner) {
            spinner.style.display = 'none';
        }
    } else {
        if (fishingAnimation) {
            fishingAnimation.style.display = 'none';
        }
        if (spinner) {
            spinner.style.display = 'block';
        }
    }
}

function hideLoading() {
    const loadingOverlay = document.getElementById('loadingOverlay');
    const fishingAnimation = document.getElementById('fishingAnimation');
    const spinner = document.querySelector('.spinner');

    if (loadingOverlay) {
        loadingOverlay.style.display = 'none';
    }

    // Reset animation visibility
    if (fishingAnimation) {
        fishingAnimation.style.display = 'none';
    }
    if (spinner) {
        spinner.style.display = 'block';
    }
}

// ERROR MODAL
let currentRetryAction = null;

function showErrorModal(message, retryAction = null) {
    const errorModal = document.getElementById('errorModal');
    const errorMessage = document.getElementById('errorMessage');
    const retryBtn = document.getElementById('retryBtn');

    if (errorMessage) {
        errorMessage.textContent = message;
    }

    if (retryBtn) {
        retryBtn.style.display = retryAction ? 'inline-block' : 'none';
    }

    currentRetryAction = retryAction;

    if (errorModal) {
        errorModal.style.display = 'flex';
    }
}

function closeErrorModal() {
    const errorModal = document.getElementById('errorModal');
    if (errorModal) {
        errorModal.style.display = 'none';
    }
    currentRetryAction = null;
}

async function retryAction() {
    if (currentRetryAction) {
        closeErrorModal();
        try {
            await currentRetryAction();
        } catch (e) {
            showErrorModal('Retry failed: ' + e.message, currentRetryAction);
        }
    }
}

// WALLET
async function connectWallet() {
    if (!window.ethereum) {
        showStatus('MetaMask not found. Please install MetaMask.', 'error');
        return;
    }

    try {
        const accounts = await window.ethereum.request({ method: "eth_requestAccounts" });
        userAddress = accounts[0];
        isConnected = true;

        // Initialize write client with wallet
        writeClient = createClient({
            chain: studionet,
            account: userAddress,
            provider: window.ethereum
        });

        // Switch to correct network
        await writeClient.connect("studionet");

        const walletAddress = document.getElementById('walletAddress');
        if (walletAddress) {
            walletAddress.textContent = `🦊 ${userAddress.substring(0,6)}...${userAddress.slice(-4)}`;
        }

        const connectBtn = document.getElementById('connectWalletBtn');
        const disconnectBtn = document.getElementById('disconnectWalletBtn');
        if (connectBtn) {
            connectBtn.style.display = 'none';
            connectBtn.style.pointerEvents = 'none';
        }
        if (disconnectBtn) {
            disconnectBtn.style.display = 'inline-block';
            disconnectBtn.style.pointerEvents = 'auto';
            console.log('Disconnect button set to visible');
        }

        // Auto-load player data from contract
        await loadPlayerData();

        showStatus('Wallet connected!', 'success');
    } catch (e) {
        showStatus('Connection failed: ' + e.message, 'error');
        console.error('Wallet connection error:', e);
    }
}

function disconnectWallet() {
    userAddress = null;
    isConnected = false;
    isRegistered = false;
    playerData = {
        nickname: '',
        tokens: 0,
        rodLevel: 1,
        bait: 0,
        totalFish: 0,
        bestCatch: null
    };

    const walletAddress = document.getElementById('walletAddress');
    if (walletAddress) {
        walletAddress.textContent = '';
    }

    const connectBtn = document.getElementById('connectWalletBtn');
    const disconnectBtn = document.getElementById('disconnectWalletBtn');
    if (connectBtn) {
        connectBtn.style.display = 'inline-block';
        connectBtn.style.pointerEvents = 'auto';
    }
    if (disconnectBtn) {
        disconnectBtn.style.display = 'none';
        disconnectBtn.style.pointerEvents = 'none';
    }

    // Show registration form
    document.querySelector('.center-box').style.display = 'block';
    fishingScreen.style.display = 'none';
    document.body.classList.remove('fishing-active');

    showStatus('Wallet disconnected', 'success');
}

// LOAD PLAYER DATA FROM CONTRACT
async function loadPlayerData(retryCount = 0) {
    if (!userAddress) return;

    const normalizedAddr = userAddress.toLowerCase();
    console.log('Loading stats for address:', normalizedAddr);

    try {
        const stats = await genCall('get_stats', [normalizedAddr]);
        console.log('Stats loaded:', stats);
        console.log('Stats type:', typeof stats);

        // Parse JSON string if needed
        let statsObj = stats;
        if (typeof stats === 'string') {
            try {
                statsObj = JSON.parse(stats);
                console.log('Parsed stats:', statsObj);
            } catch (e) {
                console.error('Failed to parse stats JSON:', e);
                statsObj = {};
            }
        }

        console.log('Stats name:', statsObj?.name);
        console.log('Stats balance:', statsObj?.balance);
        console.log('Stats rod:', statsObj?.rod);
        console.log('Stats inventory:', statsObj?.inventory);

        // Check if player is registered - name should not be 'Unknown' or empty
        // Also check if stats object has valid data
        const hasValidName = statsObj && statsObj.name && statsObj.name !== 'Unknown' && statsObj.name !== '';
        const hasValidData = statsObj && (statsObj.balance !== undefined || statsObj.total_earned !== undefined);

        console.log('Has valid name:', hasValidName);
        console.log('Has valid data:', hasValidData);

        if (hasValidName && hasValidData) {
            isRegistered = true;

            // Calculate rod level based on inventory
            const rodNames = ['bamboo', 'platinum', 'adamantite', 'mythic'];
            const ownedRods = statsObj.inventory?.rods || ['bamboo'];
            const currentRod = statsObj.rod || 'bamboo';
            const rodLevel = rodNames.indexOf(currentRod) + 1 || 1;

            console.log('Owned rods:', ownedRods);
            console.log('Current rod:', currentRod);
            console.log('Calculated rod level:', rodLevel);

            playerData = {
                nickname: statsObj.name,
                tokens: statsObj.balance || statsObj.total_earned || 100,
                rodLevel: rodLevel,
                bait: statsObj.bait === 'none' ? 0 : 3,
                totalFish: statsObj.recent_catches ? statsObj.recent_catches.filter(c => c.fish !== 'empty').length : 0,
                bestCatch: statsObj.recent_catches && statsObj.recent_catches.length > 0
                    ? statsObj.recent_catches.filter(c => c.fish !== 'empty').reduce((best, c) =>
                        c.points > (best?.points || 0) ? c : best, null)
                    : null
            };
            nicknameInput.value = playerData.nickname;
            console.log('Player data loaded from contract:', playerData);
            console.log('isRegistered set to: true');

            // Auto-show fishing screen if registered
            showFishingScreen();
        } else {
            console.log('Player not registered yet - stats:', statsObj);
            isRegistered = false;
            console.log('isRegistered set to: false');

            // Show registration form
            document.querySelector('.center-box').style.display = 'block';
            fishingScreen.style.display = 'none';
            document.body.classList.remove('fishing-active');
        }
    } catch (e) {
        console.log('Error loading player data:', e);
        console.error('Error details:', e);
        // Player not registered - this is OK
        isRegistered = false;
        console.log('isRegistered set to: false (error)');

        // Show registration form
        document.querySelector('.center-box').style.display = 'block';
        fishingScreen.style.display = 'none';
        document.body.classList.remove('fishing-active');
    }
}

// LOAD LEADERBOARD FROM CONTRACT
async function loadLeaderboard() {
    try {
        // Pass empty array - genCall will add () automatically
        const leaderboard = await genCall('get_leaderboard', []);
        console.log('Leaderboard raw result:', leaderboard);
        console.log('Leaderboard type:', typeof leaderboard);
        console.log('Is array?', Array.isArray(leaderboard));

        // Parse JSON string if needed
        let leaderboardArray = leaderboard;
        if (typeof leaderboard === 'string') {
            try {
                leaderboardArray = JSON.parse(leaderboard);
                console.log('Parsed leaderboard:', leaderboardArray);
            } catch (e) {
                console.error('Failed to parse leaderboard JSON:', e);
                leaderboardArray = [];
            }
        }

        const listEl = document.getElementById('leaderboardList');

        if (!leaderboardArray || !Array.isArray(leaderboardArray) || leaderboardArray.length === 0) {
            listEl.innerHTML = '<p style="text-align: center; color: #999;">No players yet</p>';
            return;
        }

        listEl.innerHTML = leaderboardArray.map((player, index) => {
            const rankClass = index === 0 ? 'gold' : index === 1 ? 'silver' : index === 2 ? 'bronze' : '';
            const isCurrentPlayer = player.address === userAddress;

            return `
                <div class="leaderboard-item ${isCurrentPlayer ? 'current-player' : ''}">
                    <span class="leaderboard-rank ${rankClass}">
                        ${index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : `${index + 1}th`}
                    </span>
                    <span class="leaderboard-name">${player.name || 'Unknown'}</span>
                    <span class="leaderboard-tokens">${player.points || 0}</span>
                </div>
            `;
        }).join('');
    } catch (e) {
        console.log('Leaderboard error:', e.message);
        console.error('Leaderboard error details:', e);
        // Don't show error in UI, just empty state
        const listEl = document.getElementById('leaderboardList');
        if (listEl) {
            listEl.innerHTML = '<p style="text-align: center; color: #999;">Leaderboard loading...</p>';
        }
    }
}

// 🎣 GAME FUNCTIONS (GENLAYER INTEGRATION)
async function startGame() {
    const nickname = nicknameInput.value.trim();

    if (!nickname) {
        showStatus('Enter nickname', 'error');
        return;
    }

    if (!isConnected) {
        showStatus('Connect wallet first', 'error');
        return;
    }

    try {
        if (!isRegistered) {
            console.log('Registering player:', nickname);
            showLoading('Registering...');
            await sendTransaction('register', [nickname]);
            await new Promise(resolve => setTimeout(resolve, 8000));
            hideLoading();
        }

        playerData.nickname = nickname;
        await loadPlayerData(0);

        if (playerData.nickname === 'Unknown' || !playerData.nickname) {
            showStatus('Registration pending... Please try again', 'error');
            return;
        }

        showFishingScreen();
        await loadLeaderboard();
    } catch (e) {
        hideLoading();
        showStatus('Registration failed: ' + e.message, 'error');
    }
}

function showFishingScreen() {
    document.querySelector('.center-box').style.display = 'none';
    fishingScreen.style.display = 'block';
    
    // 🔥 AKTIFKAN FISHING BACKGROUND
    document.body.classList.add('fishing-active');
    
    const playerName = document.getElementById('playerName');
    if (playerName) {
        playerName.textContent = `${playerData.nickname}'s Fishing Game`;
    }
    
    updateStats();
    updateShop();
    renderLeaderboard(); // Show leaderboard when game starts
}

function updateStats() {
    const playerStats = document.getElementById('playerStats');
    if (playerStats) {
        playerStats.textContent =
            `Tokens: ${playerData.tokens} | Rod Level: ${playerData.rodLevel} | Bait: ${playerData.bait}`;
    }

    const statsContent = document.getElementById('statsContent');
    if (statsContent) {
        statsContent.innerHTML = `
            <p>Total Fish: ${playerData.totalFish}</p>
            <p>Best Catch: ${playerData.bestCatch ? playerData.bestCatch.fish : 'None'}</p>
        `;
    }

    // Update equipment
    updateEquipment();

    // Load leaderboard
    loadLeaderboard();
}

function updateEquipment() {
    const equipmentContent = document.getElementById('equipmentContent');
    if (!equipmentContent) return;

    const rodNames = ['bamboo', 'platinum', 'adamantite', 'mythic'];

    // Get owned rods from contract data if available
    let ownedRods = ['bamboo']; // Default
    let currentRod = 'bamboo';

    // Try to get from contract by calling get_stats
    if (userAddress) {
        genCall('get_stats', [userAddress.toLowerCase()]).then(stats => {
            let statsObj = stats;
            if (typeof stats === 'string') {
                try {
                    statsObj = JSON.parse(stats);
                } catch (e) {
                    console.error('Failed to parse stats in updateEquipment:', e);
                }
            }
            if (statsObj?.inventory?.rods) {
                ownedRods = statsObj.inventory.rods;
                console.log('Owned rods from contract:', ownedRods);
            }
            if (statsObj?.rod) {
                currentRod = statsObj.rod;
                console.log('Current rod from contract:', currentRod);
            }
            renderEquipment(ownedRods, currentRod);
        }).catch(e => {
            console.error('Error getting stats for equipment:', e);
            renderEquipment(ownedRods, currentRod);
        });
    } else {
        renderEquipment(ownedRods, currentRod);
    }
}

function renderEquipment(ownedRods, currentRod) {
    const equipmentContent = document.getElementById('equipmentContent');
    if (!equipmentContent) return;

    const rodNames = ['bamboo', 'platinum', 'adamantite', 'mythic'];

    let equipHTML = '';

    // Show owned rods
    equipHTML += '<div style="margin-bottom: 15px;"><strong>Rods:</strong></div>';
    ownedRods.forEach(rod => {
        const isEquipped = rod === currentRod;
        equipHTML += `
            <div class="shop-item">
                <span>${rod.charAt(0).toUpperCase() + rod.slice(1)} Rod ${isEquipped ? '(Equipped)' : ''}</span>
                ${!isEquipped ? `<button onclick="window.equipRod('${rod}')">Equip</button>` : ''}
            </div>
        `;
    });

    // Show bait
    equipHTML += '<div style="margin-bottom: 15px; margin-top: 15px;"><strong>Bait:</strong></div>';
    equipHTML += `
        <div class="shop-item">
            <span>Worm Bait</span>
            <span>${playerData.bait} owned</span>
        </div>
    `;

    equipmentContent.innerHTML = equipHTML;
}

function updateShop() {
    const shopContent = document.getElementById('shopContent');
    if (!shopContent) return;
    
    // Rod prices
    const rodPrices = { bamboo: 0, platinum: 50, adamantite: 150, mythic: 500 };
    const rodNames = ['bamboo', 'platinum', 'adamantite', 'mythic'];
    const currentRod = rodNames[playerData.rodLevel - 1] || 'bamboo';
    
    let shopHTML = '';
    
    // Available rods to buy
    rodNames.forEach((rod, index) => {
        if (index >= playerData.rodLevel) {
            const price = rodPrices[rod];
            const canBuy = playerData.tokens >= price;
            shopHTML += `
                <div class="shop-item">
                    <span>${rod.charAt(0).toUpperCase() + rod.slice(1)} Rod - ${price} tokens</span>
                    <button onclick="window.buyRod('${rod}')" ${!canBuy ? 'disabled' : ''}>
                        ${canBuy ? 'Buy' : 'Need ' + price}
                    </button>
                </div>
            `;
        }
    });
    
    // Owned rods (show with Equip button)
    const ownedRods = rodNames.slice(0, playerData.rodLevel);
    if (ownedRods.length > 1) {
        shopHTML += '<div style="margin-top: 15px; padding-top: 10px; border-top: 1px solid rgba(255,255,255,0.2);"><strong>Owned Rods:</strong></div>';
        ownedRods.forEach(rod => {
            const isEquipped = rod === currentRod;
            shopHTML += `
                <div class="shop-item">
                    <span>${rod.charAt(0).toUpperCase() + rod.slice(1)} Rod ${isEquipped ? '(Equipped)' : ''}</span>
                    ${!isEquipped ? `<button onclick="window.equipRod('${rod}')">Equip</button>` : ''}
                </div>
            `;
        });
    }
    
    // Bait
    const baitTypes = [
        { name: 'Worm', price: 10, catch: 20, rare: 0, desc: '+20% catch rate' },
        { name: 'Shrimp', price: 20, catch: 30, rare: 10, desc: '+30% catch, +10% rare' },
        { name: 'Magic Lure', price: 50, catch: 40, rare: 20, desc: '+40% catch, +20% rare' },
        { name: 'Golden Bait', price: 100, catch: 60, rare: 40, desc: '+60% catch, +40% rare' }
    ];

    shopHTML += '<div style="margin-top: 15px; padding-top: 10px; border-top: 1px solid rgba(255,255,255,0.2);"><strong>Bait:</strong></div>';

    baitTypes.forEach(bait => {
        const canBuy = playerData.tokens >= bait.price;
        shopHTML += `
            <div class="shop-item">
                <span>${bait.name} - ${bait.price} tokens</span>
                <button onclick="window.buyBait('${bait.name.toLowerCase().replace(' ', '_')}')" ${!canBuy ? 'disabled' : ''}>
                    ${canBuy ? 'Buy' : 'Need ' + bait.price}
                </button>
            </div>
            <div style="font-size: 11px; color: #888; padding-left: 5px; margin-top: -5px; margin-bottom: 8px;">
                ${bait.desc}
            </div>
        `;
    });

    // Show current bait count
    if (playerData.bait > 0) {
        shopHTML += `
            <div class="shop-item">
                <span>Bait: ${playerData.bait}</span>
                <span style="color: #00cfff;">Owned</span>
            </div>
        `;
    }

    shopContent.innerHTML = shopHTML || '<p>Nothing to buy!</p>';
}

// 🎣 CAST LINE (GENLAYER CONTRACT)
async function castLine() {
    if (!userAddress) {
        showStatus('Connect wallet first', 'error');
        return;
    }

    if (!isRegistered) {
        showStatus('Please register first by starting the game!', 'error');
        return;
    }

    const addressBeforeCast = userAddress;
    console.log('Cast started with address:', addressBeforeCast);

    castBtn.disabled = true;
    castBtn.textContent = '🎣 Fishing...';

    const fishResult = document.getElementById('fishResult');
    fishResult.innerHTML = `
        <p>🎣 Casting line...</p>
        <p><small>Calling GenLayer contract with Web Fetching...</small></p>
    `;

    try {
        // Call contract cast() - triggers web weather + LLM story
        showLoading('Casting line...', true);
        await sendTransaction('cast', []);

        // Wait for GenLayer consensus (LLM + web fetch take time)
        showLoading('Waiting for validators...', true);
        await new Promise(resolve => setTimeout(resolve, 15000));

        // Reload data from contract (skip in MOCK_MODE since data is already updated)
        showLoading('Loading results...', true);
        if (!MOCK_MODE) {
            await loadPlayerData(0);
        }

        console.log('Address after cast:', userAddress);
        console.log('Address changed?', userAddress !== addressBeforeCast);
        console.log('Address before:', addressBeforeCast);
        console.log('Address after:', userAddress);

        hideLoading();

        // Get the recent catch
        const recentCatch = playerData.bestCatch;

        if (!recentCatch || recentCatch.fish === 'empty') {
            fishResult.innerHTML = `
                <div class="fish-emoji">💨</div>
                <h3>Missed!</h3>
                <p>The fish got away... Try again!</p>
            `;
        } else {
            // Get AI story for rare/legendary fish
            let storyHTML = '';
            let weatherHTML = '';
            if (recentCatch.rarity === 'rare' || recentCatch.rarity === 'legendary') {
                try {
                    const weather = recentCatch.weather || 'sunny';
                    const aiStory = await genCall('get_catch_story', [recentCatch.fish, recentCatch.rarity, weather]);
                    if (aiStory) {
                        storyHTML = `<p style="font-style: italic; color: #00cfff; margin-top: 10px;">"${aiStory}"</p>`;
                    }
                    if (weather) {
                        weatherHTML = `<p><small>🌤️ Weather: ${weather}</small></p>`;
                    }
                } catch (e) {
                    console.log('Story generation failed:', e);
                }
            }

            const rarityColors = {
                'common': '#aaa',
                'uncommon': '#4caf50',
                'rare': '#2196f3',
                'legendary': '#ff9800'
            };
            const rarityColor = rarityColors[recentCatch.rarity] || '#333';
            const fishColor = getFishColor(recentCatch.fish);

            fishResult.innerHTML = `
                <div class="fish-emoji">${getFishEmoji(recentCatch.fish)}</div>
                <h3 style="color: ${fishColor};">${recentCatch.fish}</h3>
                <p><strong>Rarity:</strong> <span style="color: ${rarityColor};">${recentCatch.rarity.toUpperCase()}</span></p>
                <p><strong>+${recentCatch.points} tokens</strong></p>
                ${weatherHTML}
                ${storyHTML}
                <p><small>Powered by GenLayer LLM & Web Fetching</small></p>
            `;

            updateStats();
            updateShop();
            await loadLeaderboard();

            showStatus(`Caught ${recentCatch.fish}! +${recentCatch.points} tokens`, 'success');
        }

        castBtn.disabled = false;
        castBtn.textContent = '🎣 Cast Line';

    } catch (e) {
        hideLoading();
        castBtn.disabled = false;
        castBtn.textContent = '🎣 Cast Line';
        showStatus('Fishing failed: ' + e.message, 'error');
        console.error('Cast error:', e);
    }
}

// 🛒 SHOP ACTIONS (GENLAYER CONTRACT)
async function buyBait(baitName) {
    try {
        showLoading(`Buying ${baitName}...`);
        await sendTransaction('buy_bait', [baitName]);
        await new Promise(resolve => setTimeout(resolve, 8000));
        await loadPlayerData(0);
        updateStats();
        updateShop();
        hideLoading();
        showStatus(`Bought ${baitName}!`, 'success');
    } catch (e) {
        hideLoading();
        showStatus('Purchase failed: ' + e.message, 'error');
    }
}

async function equipRod(rodName) {
    try {
        showLoading(`Equipping ${rodName}...`);
        await sendTransaction('equip_rod', [rodName]);
        await new Promise(resolve => setTimeout(resolve, 8000));
        await loadPlayerData(0);
        updateStats();
        updateEquipment();
        updateShop();
        hideLoading();
        showStatus(`Equipped ${rodName}!`, 'success');
    } catch (e) {
        hideLoading();
        showStatus('Equip failed: ' + e.message, 'error');
    }
}

async function buyRod(rodName) {
    try {
        console.log('Buying rod:', rodName);
        console.log('Current tokens before:', playerData.tokens);
        console.log('Current rod level before:', playerData.rodLevel);

        showLoading(`Buying ${rodName} rod...`);
        await sendTransaction('buy_rod', [rodName]);
        console.log('Transaction sent, waiting for confirmation...');

        await new Promise(resolve => setTimeout(resolve, 8000));
        console.log('Wait completed, reloading player data...');

        await loadPlayerData(0);
        console.log('Player data reloaded');
        console.log('New tokens:', playerData.tokens);
        console.log('New rod level:', playerData.rodLevel);

        updateStats();
        updateEquipment();
        updateShop();
        hideLoading();
        showStatus(`Bought ${rodName} rod!`, 'success');
    } catch (e) {
        console.error('Buy rod error:', e);
        hideLoading();
        showStatus('Purchase failed: ' + e.message, 'error');
    }
}

// ============================================
// INITIALIZATION
// ============================================
// Initialize GenLayer clients on page load
initGenLayerClients();

// Load game data from localStorage
loadGameData();

// Check wallet connection
if (window.ethereum) {
    console.log('MetaMask detected');
    window.ethereum.request({ method: 'eth_accounts' }).then(accounts => {
        if (accounts.length > 0) {
            console.log('MetaMask is unlocked but waiting for manual connection');
        }
    });
} else {
    console.log('MetaMask not detected');
    showStatus('MetaMask not found. Please install MetaMask extension.', 'error');
}

// Load leaderboard from contract
loadLeaderboard();

// ============================================
// EVENT LISTENERS
// ============================================
// Add event listeners after DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const connectWalletBtn = document.getElementById('connectWalletBtn');
    const disconnectWalletBtn = document.getElementById('disconnectWalletBtn');
    const startGameBtn = document.getElementById('startGameBtn');
    const castBtn = document.getElementById('castBtn');

    console.log('DOM loaded, attaching event listeners...');

    if (connectWalletBtn) {
        connectWalletBtn.addEventListener('click', connectWallet);
        console.log('Connect wallet button listener attached');
    } else {
        console.log('Connect wallet button not found');
    }

    if (disconnectWalletBtn) {
        disconnectWalletBtn.addEventListener('click', (e) => {
            e.preventDefault();
            console.log('Disconnect button clicked');
            disconnectWallet();
        });
        // Also add inline onclick as fallback
        disconnectWalletBtn.onclick = (e) => {
            e.preventDefault();
            console.log('Disconnect button clicked via onclick');
            disconnectWallet();
        };
        console.log('Disconnect wallet button listener attached');
        console.log('Disconnect button display:', disconnectWalletBtn.style.display);
    } else {
        console.log('Disconnect wallet button not found');
    }

    if (startGameBtn) {
        startGameBtn.addEventListener('click', startGame);
        console.log('Start game button listener attached');
    } else {
        console.log('Start game button not found');
    }

    if (castBtn) {
        castBtn.addEventListener('click', castLine);
        console.log('Cast button listener attached');
    } else {
        console.log('Cast button not found');
    }
});

// ============================================
// GLOBAL EXPOSE (untuk ES module compatibility)
// ============================================
// Expose immediately when module loads
window.connectWallet = connectWallet;
window.disconnectWallet = disconnectWallet;
window.startGame = startGame;
window.showFishingScreen = showFishingScreen;
window.castLine = castLine;
window.updateStats = updateStats;
window.buyRod = buyRod;
window.buyBait = buyBait;
window.equipRod = equipRod;
window.showErrorModal = showErrorModal;
window.closeErrorModal = closeErrorModal;
window.retryAction = retryAction;

console.log('Functions exposed to window:', {
    connectWallet: typeof window.connectWallet,
    disconnectWallet: typeof window.disconnectWallet,
    startGame: typeof window.startGame,
    castLine: typeof window.castLine
});
