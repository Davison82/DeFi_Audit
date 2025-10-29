from web3 import Web3
import json
from datetime import datetime

def get_eth_price_uniswap():
    """Get ETH price from Uniswap V2"""
    infura_url = "https://mainnet.infura.io/v3/ef3d835ffe9a4a76891a9f1ea09c51bb"
    w3 = Web3(Web3.HTTPProvider(infura_url))
    
    pool_address = "0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc"
    pool_abi = json.loads('[{"constant":true,"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"}]')
    
    pool = w3.eth.contract(address=pool_address, abi=pool_abi)
    reserves = pool.functions.getReserves().call()
    
    usdc_reserve = reserves[0] / 1e6
    eth_reserve = reserves[1] / 1e18
    price = usdc_reserve / eth_reserve
    
    return price, usdc_reserve, eth_reserve

def get_eth_price_sushiswap():
    """Get ETH price from SushiSwap"""
    infura_url = "https://mainnet.infura.io/v3/ef3d835ffe9a4a76891a9f1ea09c51bb"
    w3 = Web3(Web3.HTTPProvider(infura_url))
    
    # SushiSwap ETH/USDC pool
    pool_address = "0x397FF1542f962076d0BFE58eA045FfA2d347ACa0"
    pool_abi = json.loads('[{"constant":true,"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"}]')
    
    pool = w3.eth.contract(address=pool_address, abi=pool_abi)
    reserves = pool.functions.getReserves().call()
    
    # Note: SushiSwap has reversed order - ETH is first
    eth_reserve = reserves[0] / 1e18
    usdc_reserve = reserves[1] / 1e6
    price = usdc_reserve / eth_reserve
    
    return price, usdc_reserve, eth_reserve

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
print(f"   ETH Price: ${sushi_price:,.2f}")
print(f"   Pool Size: ${sushi_usdc:,.0f} USDC / {sushi_eth:,.2f} ETH")

# Calculate spread
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