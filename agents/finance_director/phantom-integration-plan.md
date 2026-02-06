# 💎 Phantom Wallet Integration Plan - Life OS Finance Director

> "HODL the vision, automate the mission!" 🚀

This document outlines the complete battle plan for integrating Phantom wallet into Life OS for automated crypto operations, DeFi interactions, and portfolio management.

---

## 📊 Executive Summary

Phantom is a leading multi-chain crypto wallet supporting Solana, Ethereum, Polygon, Base, Bitcoin, and more. The Phantom Connect SDK suite provides enterprise-grade infrastructure for wallet integration with embedded wallet creation, social login options, and robust security measures.

### Key Capabilities:
- ✅ Multi-chain support (Solana + EVM chains)
- ✅ Browser extension + Mobile app integration
- ✅ Embedded wallet creation (Google/Apple OAuth)
- ✅ Transaction signing & automation
- ✅ Auto-confirm for trusted operations
- ✅ Real-time transaction simulation & risk detection

---

## 🌐 1. Supported Chains & Networks

| Chain | Mainnet | Testnet | Status |
|-------|---------|---------|--------|
| **Solana** | ✅ | Devnet, Testnet | Live |
| **Ethereum** | ✅ | Sepolia | Live |
| **Polygon** | ✅ | Amoy | Live |
| **Base** | ✅ | Sepolia | Live |
| **Arbitrum** | ✅ | Sepolia | Live |
| **Bitcoin** | 🔄 | - | Coming Soon |
| **Sui** | 🔄 | - | Coming Soon |
| **Monad** | ✅ | Testnet | Live |

### Chain IDs for EVM Networks:
```javascript
const EVM_CHAINS = {
  ETHEREUM_MAINNET: 1,
  ETHEREUM_SEPOLIA: 11155111,
  POLYGON_MAINNET: 137,
  POLYGON_AMOY: 80002,
  BASE_MAINNET: 8453,
  BASE_SEPOLIA: 84532,
  ARBITRUM_ONE: 42161,
  ARBITRUM_SEPOLIA: 421614,
  MONAD_MAINNET: 143,
  MONAD_TESTNET: 10143,
};
```

---

## 🔌 2. Integration Options

### 2.1 Browser Extension API (Injected Provider)

The OG way to connect - detects Phantom browser extension and injects provider into window object.

```javascript
// Detect Phantom extension
const isPhantomInstalled = window.phantom?.solana?.isPhantom;

// Connect to extension
const connectExtension = async () => {
  try {
    const provider = window.phantom.solana;
    const resp = await provider.connect();
    console.log("Connected! Public Key:", resp.publicKey.toString());
    return resp.publicKey;
  } catch (err) {
    console.error("Connection failed:", err);
  }
};

// Sign message
const signMessage = async (message) => {
  const provider = window.phantom.solana;
  const encodedMessage = new TextEncoder().encode(message);
  const signedMessage = await provider.signMessage(encodedMessage, "utf8");
  return signedMessage.signature;
};
```

### 2.2 Phantom Connect SDK (Recommended)

The modern way - supports both extension AND embedded wallets with unified API.

#### Installation:
```bash
# For vanilla JS/Node.js
npm install @phantom/browser-sdk

# For React apps
npm install @phantom/react-sdk

# For React Native
npm install @phantom/react-native-sdk

# Dependencies
npm install @solana/web3.js viem
```

#### Browser SDK Setup:
```javascript
import { BrowserSDK, AddressType, NetworkId } from "@phantom/browser-sdk";

// Initialize SDK
const sdk = new BrowserSDK({
  providers: ["google", "apple", "injected", "deeplink"],
  addressTypes: [AddressType.solana, AddressType.ethereum],
  appId: "your-app-id-from-phantom-portal",
  authOptions: {
    redirectUrl: "https://yourapp.com/auth/callback",
  },
  autoConnect: true, // Reconnect to existing session
});

// Connect with specific provider
const { addresses } = await sdk.connect({ provider: "google" });
```

#### React SDK Setup:
```jsx
import { PhantomProvider, ConnectButton, usePhantom, darkTheme } from "@phantom/react-sdk";
import { AddressType } from "@phantom/browser-sdk";

function App() {
  return (
    <PhantomProvider
      config={{
        providers: ["google", "apple", "injected", "deeplink"],
        appId: "your-app-id",
        addressTypes: [AddressType.solana, AddressType.ethereum],
        authOptions: {
          redirectUrl: "https://yourapp.com/auth/callback",
        },
      }}
      theme={darkTheme}
      appIcon="https://your-app.com/icon.png"
      appName="Life OS Finance Director"
    >
      <WalletComponent />
    </PhantomProvider>
  );
}

function WalletComponent() {
  const { isConnected, addresses, user } = usePhantom();
  
  return (
    <div>
      {isConnected ? (
        <div>
          <p>Connected Addresses:</p>
          {addresses.map(addr => (
            <p key={addr.address}>{addr.addressType}: {addr.address}</p>
          ))}
        </div>
      ) : (
        <ConnectButton fullWidth />
      )}
    </div>
  );
}
```

### 2.3 Mobile Deep Linking

For mobile app integration, Phantom supports deep links:

```javascript
// Mobile deep link provider
const sdk = new BrowserSDK({
  providers: ["deeplink"], // Opens Phantom mobile app
  addressTypes: [AddressType.solana],
  appId: "your-app-id",
});

// Or construct manual deep links
const deepLink = `https://phantom.app/ul/v1/connect?app_url=${encodeURIComponent(appUrl)}&dapp_encryption_public_key=${pubKey}`;
window.location.href = deepLink;
```

### 2.4 Server-Side SDK (Backend Operations)

For server-side wallet management and automation:

```javascript
import { ServerSDK, NetworkId } from "@phantom/server-sdk";

const sdk = new ServerSDK({
  organizationId: process.env.PHANTOM_ORG_ID,
  appId: process.env.PHANTOM_APP_ID,
  apiPrivateKey: process.env.PHANTOM_PRIVATE_KEY,
  apiBaseUrl: "https://api.phantom.app/v1/wallets",
});

// Create managed wallet
const wallet = await sdk.createWallet("Life OS Automation Wallet");

// Sign message
const signature = await sdk.signMessage({
  walletId: wallet.walletId,
  message: "Automated Life OS Transaction",
  networkId: NetworkId.SOLANA_MAINNET,
});

// Sign and send transaction
const result = await sdk.signAndSendTransaction({
  walletId: wallet.walletId,
  transaction: solanaTransaction, // Web3.js Transaction object
  networkId: NetworkId.SOLANA_MAINNET,
});
```

---

## 💰 3. Transaction Automation Examples

### 3.1 Solana Transactions (Web3.js)

```javascript
import { Connection, PublicKey, Transaction, SystemProgram, LAMPORTS_PER_SOL } from "@solana/web3.js";

// Setup connection
const connection = new Connection("https://api.mainnet-beta.solana.com", "confirmed");

// Create transfer transaction
const createTransferTx = async (fromPubkey, toPubkey, amountSol) => {
  const transaction = new Transaction().add(
    SystemProgram.transfer({
      fromPubkey: new PublicKey(fromPubkey),
      toPubkey: new PublicKey(toPubkey),
      lamports: amountSol * LAMPORTS_PER_SOL,
    })
  );
  
  transaction.feePayer = new PublicKey(fromPubkey);
  const { blockhash } = await connection.getLatestBlockhash();
  transaction.recentBlockhash = blockhash;
  
  return transaction;
};

// Sign and send via Phantom SDK
const sendSolanaTx = async () => {
  const tx = await createTransferTx(
    "FROM_ADDRESS",
    "TO_ADDRESS", 
    0.1 // 0.1 SOL
  );
  
  const result = await sdk.solana.signAndSendTransaction(tx);
  console.log("Transaction sent:", result.signature);
  return result;
};
```

### 3.2 Ethereum/EVM Transactions (Viem/Ethers.js)

```javascript
// Using Phantom SDK's Ethereum API
const sendEthTransaction = async () => {
  const result = await sdk.ethereum.sendTransaction({
    to: "0x742d35Cc6634C0532925a3b8D4C8db86fB5C4A7E",
    value: "1000000000000000000", // 1 ETH in wei
    gas: "21000",
    data: "0x", // Optional contract data
  });
  
  return result;
};

// Switch networks
await sdk.ethereum.switchChain(137); // Switch to Polygon

// Sign typed data (EIP-712)
const typedData = {
  domain: {
    name: "Life OS",
    version: "1",
    chainId: 1,
  },
  types: {
    Message: [
      { name: "action", type: "string" },
      { name: "amount", type: "uint256" },
    ],
  },
  message: {
    action: "automated_transfer",
    amount: 1000000000000000000n,
  },
};

const signature = await sdk.ethereum.signTypedData(typedData, userAddress);
```

### 3.3 Auto-Confirm for Trusted Operations

```javascript
import { NetworkId } from "@phantom/browser-sdk";

// Enable auto-confirm for specific chains (requires injected provider)
const enableAutoConfirm = async () => {
  const result = await sdk.enableAutoConfirm({
    chains: [NetworkId.SOLANA_MAINNET, NetworkId.ETHEREUM_MAINNET]
  });
  
  console.log("Auto-confirm enabled until:", new Date(result.expiresAt));
  return result;
};

// Disable auto-confirm
await sdk.disableAutoConfirm();

// Check status
const status = await sdk.getAutoConfirmStatus();
```

⚠️ **Warning:** Auto-confirm bypasses manual approval - only enable for low-risk, pre-validated operations!

---

## 📈 4. Wallet Monitoring & Alerts

### 4.1 Balance Monitoring

```javascript
// Solana balance check
const getSolanaBalance = async (publicKey) => {
  const connection = new Connection("https://api.mainnet-beta.solana.com");
  const balance = await connection.getBalance(new PublicKey(publicKey));
  return balance / LAMPORTS_PER_SOL; // Convert to SOL
};

// EVM balance check (using Viem)
import { createPublicClient, http, formatEther } from "viem";
import { mainnet } from "viem/chains";

const publicClient = createPublicClient({
  chain: mainnet,
  transport: http(),
});

const getEthBalance = async (address) => {
  const balance = await publicClient.getBalance({ address });
  return formatEther(balance); // Returns ETH as string
};

// Token balance (SPL tokens on Solana)
import { getAssociatedTokenAddress, getAccount } from "@solana/spl-token";

const getTokenBalance = async (walletPubkey, mintPubkey) => {
  const tokenAccount = await getAssociatedTokenAddress(
    new PublicKey(mintPubkey),
    new PublicKey(walletPubkey)
  );
  
  const account = await getAccount(connection, tokenAccount);
  return Number(account.amount) / (10 ** account.decimals);
};
```

### 4.2 Transaction Monitoring

```javascript
// Listen for balance changes
const watchBalance = (publicKey, callback) => {
  connection.onAccountChange(
    new PublicKey(publicKey),
    (accountInfo) => {
      const balance = accountInfo.lamports / LAMPORTS_PER_SOL;
      callback(balance);
    },
    "confirmed"
  );
};

// Monitor transaction confirmations
const waitForConfirmation = async (signature) => {
  const latestBlockhash = await connection.getLatestBlockhash();
  
  await connection.confirmTransaction({
    signature,
    ...latestBlockhash,
  }, "confirmed");
  
  console.log("Transaction confirmed! 🎉");
};
```

### 4.3 Alert Automation Structure

```javascript
class WalletMonitor {
  constructor(sdk, config) {
    this.sdk = sdk;
    this.config = {
      minBalanceAlert: 0.1, // SOL
      largeTransactionThreshold: 10, // SOL
      ...config,
    };
    this.alerts = [];
  }
  
  async checkBalance(address) {
    const balance = await getSolanaBalance(address);
    
    if (balance < this.config.minBalanceAlert) {
      this.triggerAlert("LOW_BALANCE", {
        address,
        balance,
        threshold: this.config.minBalanceAlert,
      });
    }
    
    return balance;
  }
  
  triggerAlert(type, data) {
    const alert = {
      type,
      timestamp: new Date(),
      data,
    };
    
    this.alerts.push(alert);
    
    // Hook into Life OS notification system
    console.log(`🚨 ALERT: ${type}`, data);
    
    // Send to Telegram/Discord/email
    // this.notifyUser(alert);
  }
}
```

---

## 🖼️ 5. NFT Tracking

### 5.1 Fetch NFT Holdings

```javascript
// Using Metaplex (Solana)
import { Metaplex } from "@metaplex-foundation/js";

const metaplex = Metaplex.make(connection);

const getNFTs = async (ownerAddress) => {
  const nfts = await metaplex.nfts().findAllByOwner({
    owner: new PublicKey(ownerAddress),
  });
  
  return nfts.map(nft => ({
    mint: nft.address.toString(),
    name: nft.name,
    symbol: nft.symbol,
    image: nft.json?.image,
    collection: nft.collection?.address?.toString(),
  }));
};

// Using Alchemy (EVM chains)
const getEVMNFTs = async (ownerAddress) => {
  const response = await fetch(
    `https://eth-mainnet.g.alchemy.com/nft/v2/${ALCHEMY_API_KEY}/getNFTs?owner=${ownerAddress}`
  );
  
  const data = await response.json();
  return data.ownedNfts;
};
```

### 5.2 NFT Price Tracking

```javascript
// Using Magic Eden API (Solana)
const getNFTFloorPrice = async (collectionSymbol) => {
  const response = await fetch(
    `https://api-mainnet.magiceden.dev/v2/collections/${collectionSymbol}/stats`
  );
  
  const data = await response.json();
  return {
    floorPrice: data.floorPrice / 1e9, // Convert lamports to SOL
    listedCount: data.listedCount,
    volumeAll: data.volumeAll / 1e9,
  };
};
```

---

## 🔒 6. Security Best Practices

### 6.1 Environment Variables & Secrets

```bash
# .env file - NEVER commit this!
PHANTOM_APP_ID=your_app_id_here
PHANTOM_ORG_ID=your_org_id_here
PHANTOM_PRIVATE_KEY=your_private_key_here
ALCHEMY_API_KEY=your_alchemy_key
HELIUS_API_KEY=your_helius_key
ENCRYPTION_KEY=your_encryption_key_for_local_storage
```

```javascript
// Load from environment
const config = {
  appId: process.env.PHANTOM_APP_ID,
  orgId: process.env.PHANTOM_ORG_ID,
  privateKey: process.env.PHANTOM_PRIVATE_KEY,
};
```

### 6.2 Transaction Validation

```javascript
class TransactionValidator {
  // Validate recipient address
  static isValidSolanaAddress(address) {
    try {
      new PublicKey(address);
      return true;
    } catch {
      return false;
    }
  }
  
  static isValidEthereumAddress(address) {
    return /^0x[a-fA-F0-9]{40}$/.test(address);
  }
  
  // Check for known scam addresses (implement your own blacklist)
  static isBlacklistedAddress(address) {
    const blacklist = [
      // Add known scam addresses
    ];
    return blacklist.includes(address.toLowerCase());
  }
  
  // Validate transaction amount
  static validateAmount(amount, maxAmount) {
    if (amount <= 0) throw new Error("Amount must be positive");
    if (amount > maxAmount) throw new Error(`Amount exceeds maximum: ${maxAmount}`);
    return true;
  }
}
```

### 6.3 Spending Limits & Rate Limiting

```javascript
class SpendingGuard {
  constructor(dailyLimitUsd = 1000) {
    this.dailyLimit = dailyLimitUsd;
    this.spentToday = 0;
    this.lastReset = new Date().toDateString();
  }
  
  canSpend(amountUsd) {
    this.resetIfNeeded();
    
    if (this.spentToday + amountUsd > this.dailyLimit) {
      throw new Error(`Daily limit exceeded! Spent: $${this.spentToday}, Limit: $${this.dailyLimit}`);
    }
    
    return true;
  }
  
  recordSpending(amountUsd) {
    this.spentToday += amountUsd;
  }
  
  resetIfNeeded() {
    const today = new Date().toDateString();
    if (today !== this.lastReset) {
      this.spentToday = 0;
      this.lastReset = today;
    }
  }
}
```

### 6.4 Secure Session Management

```javascript
// Session expires after 7 days (Phantom default)
const SESSION_DURATION = 7 * 24 * 60 * 60 * 1000;

class SecureSession {
  constructor() {
    this.session = null;
  }
  
  createSession(walletData) {
    this.session = {
      ...walletData,
      createdAt: Date.now(),
      expiresAt: Date.now() + SESSION_DURATION,
    };
    
    // Store encrypted in localStorage (use proper encryption!)
    localStorage.setItem("phantom_session", this.encrypt(this.session));
  }
  
  getSession() {
    const encrypted = localStorage.getItem("phantom_session");
    if (!encrypted) return null;
    
    const session = this.decrypt(encrypted);
    
    if (Date.now() > session.expiresAt) {
      this.clearSession();
      return null;
    }
    
    return session;
  }
  
  clearSession() {
    this.session = null;
    localStorage.removeItem("phantom_session");
  }
  
  encrypt(data) {
    // Implement proper encryption using crypto library
    return btoa(JSON.stringify(data)); // Placeholder - use real encryption!
  }
  
  decrypt(encrypted) {
    return JSON.parse(atob(encrypted));
  }
}
```

### 6.5 Transaction Simulation (Pre-flight Checks)

```javascript
// Simulate transaction before sending
const simulateTransaction = async (transaction) => {
  try {
    const simulation = await connection.simulateTransaction(transaction);
    
    if (simulation.value.err) {
      throw new Error(`Simulation failed: ${JSON.stringify(simulation.value.err)}`);
    }
    
    console.log("Simulation successful!");
    console.log("Estimated fee:", simulation.value.fee, "lamports");
    
    return simulation.value;
  } catch (error) {
    console.error("Transaction simulation failed:", error);
    throw error;
  }
};
```

---

## ⚠️ 7. Risk Warnings & Safeguards

### 🚨 CRITICAL WARNINGS:

1. **NEVER store private keys in code or config files**
   - Use environment variables
   - Use hardware wallets for large holdings
   - Use Phantom's Server SDK for backend operations

2. **Test on devnet/testnet FIRST**
   - Always test transactions on test networks
   - Verify amounts and addresses multiple times
   - Start with small amounts on mainnet

3. **Beware of phishing**
   - Only connect to trusted dApps
   - Verify domain names carefully
   - Phantom will never ask for your seed phrase

4. **Transaction reversibility**
   - Blockchain transactions are **IRREVERSIBLE**
   - Double-check ALL addresses before sending
   - Use address book for frequent recipients

5. **Smart contract risks**
   - Interacting with DeFi protocols carries risk
   - Always verify contract addresses
   - Start with small test transactions

6. **Auto-confirm dangers**
   - Only enable for pre-validated, trusted operations
   - Set strict spending limits
   - Regularly review and revoke permissions

### 🔐 Safeguard Checklist:

- [ ] Use hardware wallet for significant holdings
- [ ] Enable 2FA on Phantom account
- [ ] Set daily spending limits
- [ ] Maintain address whitelist
- [ ] Regular security audits
- [ ] Backup recovery phrase offline
- [ ] Monitor for unusual activity
- [ ] Keep software updated

---

## 🚀 8. Automation Possibilities

### 8.1 DeFi Automation Ideas

```javascript
// Automated yield farming harvester
class YieldOptimizer {
  async harvestAndCompound(poolAddress) {
    // 1. Check pending rewards
    const pendingRewards = await this.checkRewards(poolAddress);
    
    // 2. Harvest if above threshold
    if (pendingRewards > this.harvestThreshold) {
      await this.harvestRewards(poolAddress);
      
      // 3. Compound (re-stake) rewards
      await this.compoundRewards(pendingRewards);
      
      console.log("Harvested and compounded! 💰");
    }
  }
}

// Dollar-cost averaging (DCA) bot
class DCABot {
  constructor(config) {
    this.amount = config.amount;
    this.frequency = config.frequency; // 'daily', 'weekly'
    this.targetToken = config.targetToken;
  }
  
  async executeDCA() {
    // Swap stablecoins for target token
    const swapTx = await this.createSwapTransaction({
      from: "USDC",
      to: this.targetToken,
      amount: this.amount,
    });
    
    await sdk.solana.signAndSendTransaction(swapTx);
    console.log(`DCA executed: ${this.amount} USDC → ${this.targetToken}`);
  }
}
```

### 8.2 Alert System Integration

```javascript
// Life OS notification bridge
class CryptoAlerts {
  async sendPriceAlert(token, currentPrice, targetPrice) {
    const message = token === "SOL" && currentPrice >= targetPrice
      ? `🚀 SOL broke ${targetPrice}! To the moon!`
      : `📉 ${token} at ${currentPrice}`;
    
    // Send via Life OS notification system
    await this.notify(message);
  }
  
  async sendTransactionAlert(txType, amount, token) {
    const emoji = txType === "receive" ? "📥" : "📤";
    await this.notify(`${emoji} ${txType.toUpperCase()}: ${amount} ${token}`);
  }
}
```

---

## 📋 9. Setup Steps Summary

### Step 1: Create Phantom Portal Account
1. Go to https://phantom.com/portal/
2. Sign up with your email
3. Create a new app
4. Get your App ID

### Step 2: Configure Your App
1. Add allowed domains (e.g., `localhost:3000`, `yourapp.com`)
2. Add redirect URLs for OAuth callbacks
3. Upload app icon and set app name
4. Configure supported chains

### Step 3: Install Dependencies
```bash
npm install @phantom/browser-sdk @solana/web3.js viem
```

### Step 4: Initialize SDK
```javascript
import { BrowserSDK, AddressType } from "@phantom/browser-sdk";

const sdk = new BrowserSDK({
  providers: ["google", "apple", "injected"],
  addressTypes: [AddressType.solana, AddressType.ethereum],
  appId: process.env.PHANTOM_APP_ID,
});
```

### Step 5: Implement Connection Flow
```javascript
const connectWallet = async () => {
  try {
    const { addresses } = await sdk.connect({ provider: "injected" });
    console.log("Connected:", addresses);
    return addresses;
  } catch (error) {
    console.error("Connection failed:", error);
  }
};
```

### Step 6: Add Transaction Functions
- Implement balance checks
- Create transaction builders
- Add confirmation handling
- Set up monitoring

### Step 7: Security Hardening
- Add spending limits
- Implement address validation
- Set up rate limiting
- Enable transaction simulation

---

## 🔗 10. Useful Resources

- **Phantom Docs**: https://docs.phantom.com
- **GitHub SDK**: https://github.com/phantom/phantom-connect-sdk
- **Phantom Portal**: https://phantom.com/portal/
- **Solana Web3.js**: https://solana-labs.github.io/solana-web3.js/
- **Viem Docs**: https://viem.sh/
- **Metaplex**: https://metaplex.com/

---

## 🎯 Conclusion

This integration plan gives Life OS enterprise-grade wallet capabilities with Phantom's secure infrastructure. Start small, test thoroughly, and always prioritize security over convenience!

**Remember:** Not your keys, not your coins! 💎🙌

---

*Document created by 💎 Diamond Hands for Life OS Finance Director*
*Last updated: 2026-02-02*
