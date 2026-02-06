#!/bin/bash
#
# 💎 Diamond Hands Crypto Portfolio Tracker
# Tracks DeFi positions across Aave, Compound, and Lido
# Outputs JSON report with prices, balances, yields, and totals
#

set -euo pipefail

# Configuration
CONFIG_FILE="${HOME}/.config/crypto-portfolio/config.json"
CACHE_DIR="${HOME}/.cache/crypto-portfolio"
CACHE_TTL=300  # 5 minutes

# Protocol Contract Addresses (Ethereum Mainnet)
AAVE_POOL_DATA_PROVIDER="0x7B4EB56E7CD4b454BA8ff71E4518426369a138a3"
AAVE_POOL="0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2"
COMPOUND_CTOKEN_ETH="0x4Ddc2D193948926D02f9B1fE9e1daa0718270ED5"  # cETH
COMPOUND_CTOKEN_USDC="0x39AA39c021dfbaE8faC545936693aC917d5E7563"  # cUSDC
COMPOUND_COMPTROLLER="0x3d9819210A31b4961b30EF54bE2aeD79B9c9Cd3B"
LIDO_STETH="0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84"
LIDO_WITHDRAWAL_QUEUE="0x889edC2eDab5f40e902b864aD4d7AdE8E412F9B1"

# Token Addresses
WETH="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
USDC="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
STETH="0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84"

# Default RPC (can be overridden in config)
DEFAULT_RPC="https://eth.llamarpc.com"

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Initialize directories
init_dirs() {
    mkdir -p "$(dirname "$CONFIG_FILE")"
    mkdir -p "$CACHE_DIR"
}

# Load configuration
load_config() {
    if [[ -f "$CONFIG_FILE" ]]; then
        CONFIG=$(cat "$CONFIG_FILE")
    else
        # Create default config
        CONFIG='{
            "wallet_address": "",
            "rpc_url": "'"$DEFAULT_RPC"'",
            "coingecko_api_key": "",
            "tokens": ["ethereum", "usd-coin", "staked-ether"],
            "protocols": ["aave", "compound", "lido"]
        }'
        echo "$CONFIG" | jq '.' > "$CONFIG_FILE"
        echo -e "${YELLOW}Created default config at $CONFIG_FILE${NC}"
        echo -e "${YELLOW}Please edit it to add your wallet address${NC}"
    fi
    
    WALLET=$(echo "$CONFIG" | jq -r '.wallet_address')
    RPC_URL=$(echo "$CONFIG" | jq -r '.rpc_url // empty')
    RPC_URL=${RPC_URL:-$DEFAULT_RPC}
    COINGECKO_KEY=$(echo "$CONFIG" | jq -r '.coingecko_api_key // empty')
}

# Fetch token prices from CoinGecko
fetch_prices() {
    local cache_file="$CACHE_DIR/prices.json"
    
    # Check cache
    if [[ -f "$cache_file" ]]; then
        local cache_age=$(( $(date +%s) - $(stat -c %Y "$cache_file" 2>/dev/null || stat -f %m "$cache_file") ))
        if [[ $cache_age -lt $CACHE_TTL ]]; then
            cat "$cache_file"
            return 0
        fi
    fi
    
    local cg_url="https://api.coingecko.com/api/v3/simple/price?ids=ethereum,usd-coin,staked-ether,aave,compound-governance-token&vs_currencies=usd&include_24hr_change=true"
    
    if [[ -n "$COINGECKO_KEY" ]]; then
        cg_url="${cg_url}&x_cg_demo_api_key=${COINGECKO_KEY}"
    fi
    
    local response
    if ! response=$(curl -s -m 30 "$cg_url" 2>/dev/null); then
        echo "{}"
        return 1
    fi
    
    # Cache the response
    echo "$response" | jq '.' > "$cache_file"
    echo "$response"
}

# Make ETH RPC call
eth_call() {
    local to="$1"
    local data="$2"
    
    local payload=$(jq -n \
        --arg to "$to" \
        --arg data "$data" \
        '{jsonrpc:"2.0",method:"eth_call",params:[{to:$to,data:$data},"latest"],id:1}')
    
    local response
    if ! response=$(curl -s -m 15 -X POST "$RPC_URL" \
        -H "Content-Type: application/json" \
        -d "$payload" 2>/dev/null); then
        echo "null"
        return 1
    fi
    
    echo "$response" | jq -r '.result // "0x0"'
}

# Convert wei to ether
wei_to_eth() {
    local wei="${1:-0}"
    # Remove 0x prefix if present
    wei="${wei#0x}"
    # Convert hex to decimal then to ether
    local dec=$(echo "ibase=16; ${wei^^}" | bc 2>/dev/null || echo "0")
    echo "scale=18; $dec / 10^18" | bc -l | sed 's/^\./0./'
}

# Convert to USDC (6 decimals)
wei_to_usdc() {
    local wei="${1:-0}"
    wei="${wei#0x}"
    local dec=$(echo "ibase=16; ${wei^^}" | bc 2>/dev/null || echo "0")
    echo "scale=6; $dec / 10^6" | bc -l | sed 's/^\./0./'
}

# Get ERC20 balance
get_erc20_balance() {
    local token="$1"
    local wallet="$2"
    
    # balanceOf(address) selector: 0x70a08231
    local padded_wallet=$(echo "$wallet" | sed 's/0x//' | tr '[:lower:]' '[:upper:]' | sed 's/^/0x000000000000000000000000/')
    local data="0x70a08231${padded_wallet:2}"
    
    eth_call "$token" "$data"
}

# Get Aave user account data
get_aave_data() {
    local wallet="$1"
    
    # Encode wallet address for call
    local padded_wallet=$(echo "$wallet" | sed 's/0x//' | tr '[:lower:]' '[:upper:]' | sed 's/^/0x000000000000000000000000/')
    
    # getUserAccountData(address) selector: 0xbf92857c
    local data="0xbf92857c${padded_wallet:2}"
    
    local response=$(eth_call "$AAVE_POOL" "$data")
    
    if [[ "$response" == "null" || "$response" == "0x" ]]; then
        echo '{"total_collateral_eth":"0","total_debt_eth":"0","available_borrows_eth":"0","current_liquidation_threshold":"0","ltv":"0","health_factor":"0"}'
        return 0
    fi
    
    # Parse response (6 uint256 values)
    local hex="${response#0x}"
    local total_collateral="0x${hex:0:64}"
    local total_debt="0x${hex:64:64}"
    local available_borrows="0x${hex:128:64}"
    local liquidation_threshold="0x${hex:192:64}"
    local ltv="0x${hex:256:64}"
    local health_factor="0x${hex:320:64}"
    
    jq -n \
        --arg tc "$(wei_to_eth "$total_collateral")" \
        --arg td "$(wei_to_eth "$total_debt")" \
        --arg ab "$(wei_to_eth "$available_borrows")" \
        --arg lt "$(wei_to_eth "$liquidation_threshold")" \
        --arg ltv "$(wei_to_eth "$ltv")" \
        --arg hf "$(wei_to_eth "$health_factor")" \
        '{total_collateral_eth:$tc,total_debt_eth:$td,available_borrows_eth:$ab,current_liquidation_threshold:$lt,ltv:$ltv,health_factor:$hf}'
}

# Get Compound cToken balance
get_compound_balance() {
    local ctoken="$1"
    local wallet="$2"
    
    # balanceOf(address) selector: 0x70a08231
    local padded_wallet=$(echo "$wallet" | sed 's/0x//' | tr '[:lower:]' '[:upper:]' | sed 's/^/0x000000000000000000000000/')
    local data="0x70a08231${padded_wallet:2}"
    
    local balance=$(eth_call "$ctoken" "$data")
    
    # Get exchange rate
    # exchangeRateStored() selector: 0x182df0f5
    local rate_data="0x182df0f5"
    local rate=$(eth_call "$ctoken" "$rate_data")
    
    echo "{\"balance\":\"$balance\",\"exchange_rate\":\"$rate\"}"
}

# Get Lido stETH balance and rewards
get_lido_data() {
    local wallet="$1"
    
    # Get stETH balance
    local balance=$(get_erc20_balance "$LIDO_STETH" "$wallet")
    
    # Get total shares (for calculating rewards)
    # getSharesByHolder(address) selector: 0xf77fbf2d
    local padded_wallet=$(echo "$wallet" | sed 's/0x//' | tr '[:lower:]' '[:upper:]' | sed 's/^/0x000000000000000000000000/')
    local shares_data="0xf77fbf2d${padded_wallet:2}"
    local shares=$(eth_call "$LIDO_STETH" "$shares_data")
    
    # Get total pooled ether
    # getTotalPooledEther() selector: 0x37c4d554
    local total_ether_data="0x37c4d554"
    local total_ether=$(eth_call "$LIDO_STETH" "$total_ether_data")
    
    # Get total shares
    # getTotalShares() selector: 0x3eaaf86b
    local total_shares_data="0x3eaaf86b"
    local total_shares=$(eth_call "$LIDO_STETH" "$total_shares_data")
    
    jq -n \
        --arg bal "$balance" \
        --arg sh "$shares" \
        --arg te "$total_ether" \
        --arg ts "$total_shares" \
        '{balance:$bal,shares:$sh,total_ether:$te,total_shares:$ts}'
}

# Calculate portfolio value
calculate_portfolio() {
    local prices="$1"
    local aave_data="$2"
    local compound_eth="$3"
    local compound_usdc="$4"
    local lido_data="$5"
    
    local eth_price=$(echo "$prices" | jq -r '.ethereum.usd // 0')
    local usdc_price=$(echo "$prices" | jq -r '.["usd-coin"].usd // 1')
    local steth_price=$(echo "$prices" | jq -r '.["staked-ether"].usd // 0')
    
    # Parse Aave data
    local aave_collateral=$(echo "$aave_data" | jq -r '.total_collateral_eth // 0')
    local aave_debt=$(echo "$aave_data" | jq -r '.total_debt_eth // 0')
    local aave_net=$(echo "scale=2; ($aave_collateral - $aave_debt) * $eth_price" | bc -l 2>/dev/null || echo "0")
    
    # Parse Compound data
    local ceth_balance=$(echo "$compound_eth" | jq -r '.balance // "0x0"')
    local ceth_rate=$(echo "$compound_eth" | jq -r '.exchange_rate // "0x0"')
    local ceth_eth=$(echo "scale=18; $(wei_to_eth "$ceth_balance") * $(wei_to_eth "$ceth_rate") / 1" | bc -l 2>/dev/null || echo "0")
    local ceth_value=$(echo "scale=2; $ceth_eth * $eth_price" | bc -l 2>/dev/null || echo "0")
    
    local cusdc_balance=$(echo "$compound_usdc" | jq -r '.balance // "0x0"')
    local cusdc_rate=$(echo "$compound_usdc" | jq -r '.exchange_rate // "0x0"')
    local cusdc_usdc=$(echo "scale=6; $(wei_to_usdc "$cusdc_balance") * $(wei_to_usdc "$cusdc_rate") / 1" | bc -l 2>/dev/null || echo "0")
    local cusdc_value=$(echo "scale=2; $cusdc_usdc * $usdc_price" | bc -l 2>/dev/null || echo "0")
    
    # Parse Lido data
    local steth_bal=$(echo "$lido_data" | jq -r '.balance // "0x0"')
    local steth_eth=$(wei_to_eth "$steth_bal")
    local steth_value=$(echo "scale=2; $steth_eth * $steth_price" | bc -l 2>/dev/null || echo "0")
    
    # Calculate totals
    local total_value=$(echo "scale=2; $aave_net + $ceth_value + $cusdc_value + $steth_value" | bc -l)
    
    # Estimate yields (APY approximations)
    local aave_apy="3.5"  # Approximate
    local compound_apy="2.8"  # Approximate
    local lido_apy="3.2"  # Current stETH staking yield
    
    local daily_yield=$(echo "scale=4; ($aave_net * $aave_apy / 36500) + ($ceth_value * $compound_apy / 36500) + ($steth_value * $lido_apy / 36500)" | bc -l 2>/dev/null || echo "0")
    local yearly_yield=$(echo "scale=2; $daily_yield * 365" | bc -l 2>/dev/null || echo "0")
    
    jq -n \
        --argjson eth_p "$eth_price" \
        --argjson usdc_p "$usdc_price" \
        --argjson steth_p "$steth_price" \
        --arg aave_c "$aave_collateral" \
        --arg aave_d "$aave_debt" \
        --arg aave_v "$aave_net" \
        --arg ceth_b "$ceth_eth" \
        --arg ceth_v "$ceth_value" \
        --arg cusdc_b "$cusdc_usdc" \
        --arg cusdc_v "$cusdc_value" \
        --arg steth_b "$steth_eth" \
        --arg steth_v "$steth_value" \
        --arg total "$total_value" \
        --arg daily "$daily_yield" \
        --arg yearly "$yearly_yield" \
        --arg aave_apy "$aave_apy" \
        --arg comp_apy "$compound_apy" \
        --arg lido_apy "$lido_apy" \
        '{
            timestamp: now,
            prices: {eth:$eth_p,usdc:$usdc_p,steth:$steth_p},
            positions: {
                aave: {collateral_eth:$aave_c,debt_eth:$aave_d,net_value_usd:$aave_v,apy:$aave_apy},
                compound: {eth_supplied:$ceth_b,eth_value_usd:$ceth_v,usdc_supplied:$cusdc_b,usdc_value_usd:$cusdc_v,apy:$comp_apy},
                lido: {steth_balance:$steth_b,steth_value_usd:$steth_v,apy:$lido_apy}
            },
            summary: {total_value_usd:$total,estimated_daily_yield_usd:$daily,estimated_yearly_yield_usd:$yearly}
        }'
}

# Print human-readable summary
print_summary() {
    local report="$1"
    
    echo -e "\n${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║          💎 DIAMOND HANDS PORTFOLIO TRACKER                ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}\n"
    
    local timestamp=$(echo "$report" | jq -r '.timestamp // "N/A"' | xargs -I {} date -d @{} '+%Y-%m-%d %H:%M:%S UTC' 2>/dev/null || echo "N/A")
    echo -e "Report Time: ${GREEN}$timestamp${NC}\n"
    
    echo -e "${YELLOW}📊 CURRENT PRICES${NC}"
    echo -e "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "ETH:    \$$(echo "$report" | jq -r '.prices.eth // 0')"
    echo -e "USDC:   \$$(echo "$report" | jq -r '.prices.usdc // 0')"
    echo -e "stETH:  \$$(echo "$report" | jq -r '.prices.steth // 0')"
    echo ""
    
    echo -e "${YELLOW}🏦 PROTOCOL POSITIONS${NC}"
    echo -e "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    echo -e "\n${BLUE}AAVE V3${NC}"
    echo -e "  Collateral (ETH): $(echo "$report" | jq -r '.positions.aave.collateral_eth // 0')"
    echo -e "  Debt (ETH):       $(echo "$report" | jq -r '.positions.aave.debt_eth // 0')"
    echo -e "  Net Value (USD):  \$$(echo "$report" | jq -r '.positions.aave.net_value_usd // 0')"
    echo -e "  Est. APY:         $(echo "$report" | jq -r '.positions.aave.apy // 0')%"
    
    echo -e "\n${BLUE}Compound V2${NC}"
    echo -e "  ETH Supplied:     $(echo "$report" | jq -r '.positions.compound.eth_supplied // 0') ETH"
    echo -e "  ETH Value (USD):  \$$(echo "$report" | jq -r '.positions.compound.eth_value_usd // 0')"
    echo -e "  USDC Supplied:    $(echo "$report" | jq -r '.positions.compound.usdc_supplied // 0') USDC"
    echo -e "  USDC Value (USD): \$$(echo "$report" | jq -r '.positions.compound.usdc_value_usd // 0')"
    echo -e "  Est. APY:         $(echo "$report" | jq -r '.positions.compound.apy // 0')%"
    
    echo -e "\n${BLUE}Lido (stETH)${NC}"
    echo -e "  stETH Balance:    $(echo "$report" | jq -r '.positions.lido.steth_balance // 0')"
    echo -e "  stETH Value:      \$$(echo "$report" | jq -r '.positions.lido.steth_value_usd // 0')"
    echo -e "  Est. APY:         $(echo "$report" | jq -r '.positions.lido.apy // 0')%"
    
    echo ""
    echo -e "${YELLOW}💰 PORTFOLIO SUMMARY${NC}"
    echo -e "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "  ${GREEN}Total Value:           \$$(echo "$report" | jq -r '.summary.total_value_usd // 0')${NC}"
    echo -e "  Est. Daily Yield:      \$$(echo "$report" | jq -r '.summary.estimated_daily_yield_usd // 0')"
    echo -e "  Est. Yearly Yield:     \$$(echo "$report" | jq -r '.summary.estimated_yearly_yield_usd // 0')"
    echo ""
}

# Main execution
main() {
    init_dirs
    load_config
    
    # Check if wallet is configured
    if [[ -z "$WALLET" || "$WALLET" == "null" ]]; then
        echo -e "${RED}Error: No wallet address configured${NC}"
        echo -e "Please edit ${CONFIG_FILE} and add your wallet address"
        exit 1
    fi
    
    echo -e "${BLUE}Fetching portfolio data for:${NC} $WALLET"
    
    # Fetch all data concurrently
    echo -e "${YELLOW}Fetching token prices...${NC}"
    local prices=$(fetch_prices)
    
    if [[ "$prices" == "{}" ]]; then
        echo -e "${YELLOW}Warning: Could not fetch prices, using cached or default values${NC}"
    fi
    
    echo -e "${YELLOW}Fetching Aave positions...${NC}"
    local aave_data=$(get_aave_data "$WALLET")
    
    echo -e "${YELLOW}Fetching Compound positions...${NC}"
    local compound_eth=$(get_compound_balance "$COMPOUND_CTOKEN_ETH" "$WALLET")
    local compound_usdc=$(get_compound_balance "$COMPOUND_CTOKEN_USDC" "$WALLET")
    
    echo -e "${YELLOW}Fetching Lido positions...${NC}"
    local lido_data=$(get_lido_data "$WALLET")
    
    # Calculate portfolio
    local report=$(calculate_portfolio "$prices" "$aave_data" "$compound_eth" "$compound_usdc" "$lido_data")
    
    # Add wallet and metadata
    local final_report=$(echo "$report" | jq --arg wallet "$WALLET" '. + {wallet_address:$wallet}')
    
    # Save to file if requested
    if [[ "${1:-}" == "--save" ]]; then
        local output_file="${2:-portfolio-$(date +%Y%m%d-%H%M%S).json}"
        echo "$final_report" | jq '.' > "$output_file"
        echo -e "${GREEN}Report saved to: $output_file${NC}"
    fi
    
    # Print summary
    print_summary "$final_report"
    
    # Always output JSON to stdout
    echo "$final_report" | jq '.'
}

# Helper command to set wallet
set_wallet() {
    local wallet="$1"
    init_dirs
    
    if [[ ! -f "$CONFIG_FILE" ]]; then
        echo '{"wallet_address":"","rpc_url":"'"$DEFAULT_RPC"'"}' | jq '.' > "$CONFIG_FILE"
    fi
    
    local config=$(cat "$CONFIG_FILE")
    echo "$config" | jq --arg w "$wallet" '.wallet_address = $w' > "$CONFIG_FILE.tmp"
    mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
    
    echo -e "${GREEN}Wallet address set to: $wallet${NC}"
}

# Show help
show_help() {
    cat << 'EOF'
💎 Diamond Hands Crypto Portfolio Tracker

Usage: crypto-portfolio-tracker.sh [command] [options]

Commands:
  (no args)           Run portfolio tracker and display summary
  --save [file]       Save JSON report to file (default: portfolio-TIMESTAMP.json)
  --json              Output JSON only (no formatted summary)
  set-wallet <addr>   Set your wallet address in config
  config              Show current configuration
  help                Show this help message

Configuration:
  Config file: ~/.config/crypto-portfolio/config.json
  
  Example config:
  {
    "wallet_address": "0x...",
    "rpc_url": "https://eth.llamarpc.com",
    "coingecko_api_key": "optional-api-key"
  }

Protocols Supported:
  - Aave V3 (Ethereum Mainnet)
  - Compound V2 (Ethereum Mainnet)
  - Lido (stETH staking)

EOF
}

# Show config
show_config() {
    if [[ -f "$CONFIG_FILE" ]]; then
        echo -e "${BLUE}Current Configuration:${NC}"
        cat "$CONFIG_FILE" | jq '.'
    else
        echo -e "${YELLOW}No configuration file found at $CONFIG_FILE${NC}"
        echo "Run the tracker once to create default config"
    fi
}

# Parse arguments
case "${1:-}" in
    help|--help|-h)
        show_help
        ;;
    set-wallet)
        if [[ -z "${2:-}" ]]; then
            echo -e "${RED}Error: Please provide a wallet address${NC}"
            exit 1
        fi
        set_wallet "$2"
        ;;
    config)
        init_dirs
        show_config
        ;;
    --json)
        init_dirs
        load_config
        
        if [[ -z "$WALLET" || "$WALLET" == "null" ]]; then
            echo '{"error":"No wallet configured"}'
            exit 1
        fi
        
        prices=$(fetch_prices)
        aave_data=$(get_aave_data "$WALLET")
        compound_eth=$(get_compound_balance "$COMPOUND_CTOKEN_ETH" "$WALLET")
        compound_usdc=$(get_compound_balance "$COMPOUND_CTOKEN_USDC" "$WALLET")
        lido_data=$(get_lido_data "$WALLET")
        
        report=$(calculate_portfolio "$prices" "$aave_data" "$compound_eth" "$compound_usdc" "$lido_data")
        echo "$report" | jq --arg wallet "$WALLET" '. + {wallet_address:$wallet}'
        ;;
    *)
        main "$@"
        ;;
esac
