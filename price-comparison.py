from web3 import Web3
import json
from datetime import datetime

def get_eth_price_uniswap():
    """Get ETH price from Uniswap V2"""
    infura_url = "https://mainnet.infura.io/v3/ef3d835ffe9a4a76891a9f1ea09c51bb"
    w3 = Web3(Web3.HTTPProvider(infura_url))
    
    pool_address = "0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc"  # Uniswap ETH/USDC pool
    pool_abi = json.loads(
        '[{"constant":true,"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},'
        '{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],'
        '"payable":false,"stateMutability":"view","type":"function"}]'
    )
    
    pool = w3.eth.contract(address=pool_address, abi=pool_abi)
    reserves = pool.functions.getReserves().call()
    
    usdc_reserve = reserves[0] / 1e6  # USDC has 6 decimals
    eth_reserve = reserves[1] / 1e18  # ETH has 18 decimals
    price = usdc_reserve / eth_reserve
    
    return price, usdc_reserve, eth_reserve

def get_eth_price_sushiswap():
    """Get ETH price from SushiSwap (USDC/ETH pool)"""
    infura_url = "https://mainnet.infura.io/v3/ef3d835ffe9a4a76891a9f1ea09c51bb"
    w3 = Web3(Web3.HTTPProvider(infura_url))
    
    # SushiSwap USDC/ETH pool address
    pool_address = "0x397FF1542f962076d0BFE58eA045FfA2d347ACa0"  # USDC/ETH pool
    pool_abi = json.loads(
        '[{"constant":true,"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},'
        '{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],'
        '"payable":false,"stateMutability":"view","type":"function"}]'
    )
    
    pool = w3.eth.contract(address=pool_address, abi=pool_abi)
    
    try:
        reserves = pool.functions.getReserves().call()
        print(f"SushiSwap Raw Reserves: {reserves}")  # Debugging output
        
        # Raw values
        reserve0 = reserves[0]  # USDC reserve
        reserve1 = reserves[1]  # ETH reserve
        
        print(f"Raw USDC Reserve (reserve0): {reserve0}")
        print(f"Raw ETH Reserve (reserve1): {reserve1}")
        
        # USDC Reserve is reserve0 (scaled by 1e6) and ETH is reserve1 (scaled by 1e18)
        usdc_reserve = reserve0 / 1e6  # USDC has 6 decimals
        eth_reserve = reserve1 / 1e18  # ETH has 18 decimals
        
        print(f"USDC Reserve (scaled): {usdc_reserve}")
        print(f"ETH Reserve (scaled): {eth_reserve}")
        
        # Ensure reserves are valid
        if eth_reserve == 0 or usdc_reserve == 0:
            raise ValueError("Invalid reserve values detected.")
        
        # Calculate price
        price = usdc_reserve / eth_reserve
        
        return price, usdc_reserve, eth_reserve
    except Exception as e:
        print(f"Error while fetching SushiSwap price: {str(e)}")
        return None, None, None

# Main comparison
print("\n" + "="*60)
print(f"ETH PRICE COMPARISON - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*60)

# Get prices
uniswap_price, uni_usdc, uni_eth = get_eth_price_uniswap()
sushi_price, sushi_usdc, sushi_eth = get_eth_price_sushiswap()

# Display results
print(f"\n📊 UNISWAP V2:")
print(f"   ETH Price: ${uniswap_price:,.2f}")
print(f"   Pool Size: ${uni_usdc:,.0f} USDC / {uni_eth:,.2f} ETH")

print(f"\n📊 SUSHISWAP:")
if sushi_price:
    print(f"   ETH Price: ${sushi_price:,.2f}")
    print(f"   Pool Size: ${sushi_usdc:,.0f} USDC / {sushi_eth:,.2f} ETH")
else:
    print("   Error fetching SushiSwap price.")

# Calculate spread
if sushi_price:
    spread = abs(uniswap_price - sushi_price)
    spread_pct = (spread / uniswap_price) * 100

    print(f"\n⚖️  ANALYSIS:")
    print(f"   Price Spread: ${spread:.2f} ({spread_pct:.3f}%)")

    if spread > 10:
        print(f"   🚨 ARBITRAGE OPPORTUNITY!")
        print(f"   Potential profit: ${spread:.2f} per ETH")
    elif spread > 5:
        print(f"   ⚠️  Notable spread - watch this")
    else:
        print(f"   ✅ Prices are well aligned")

print("\n" + "="*60 + "\n")
