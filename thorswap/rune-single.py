import os
import json
import requests
import decimal
from web3 import Web3
import discord
from discord.ext import commands, tasks
from pycoingecko import CoinGeckoAPI

BOT_TOKEN = os.environ["DISCORD_BOT_TOKEN_RUNE_SINGLE"]

# Initialize Discord client
intents = discord.Intents.all()
intents.members = True
client = commands.Bot(intents=intents, help_command=None)

# Initialize web3
INFURA_TOKEN = os.environ['WEB3_INFURA_TOKEN_4']
infuraURL = f'https://mainnet.infura.io/v3/{INFURA_TOKEN}'
web3 = Web3(Web3.HTTPProvider(infuraURL))

# Price APIs
cg = CoinGeckoAPI()


def contract_info(bond_address, baseTokenPrice, payoutTokenPrice=0, maxReached=False, noFunds=False):
    if maxReached == True or noFunds == True:
        return(-999)
    else:
        try:
            print(f'baseToken Price:{baseTokenPrice}')
            print(f'payoutToken Price: {payoutTokenPrice}')
            
            #retrieve bond prices and current discount
            address = bond_address
            abi = json.loads('[{"inputs":[{"internalType":"address","name":"_customTreasury","type":"address"},{"internalType":"address","name":"_payoutToken","type":"address"},{"internalType":"address","name":"_principalToken","type":"address"},{"internalType":"address","name":"_olympusTreasury","type":"address"},{"internalType":"address","name":"_subsidyRouter","type":"address"},{"internalType":"address","name":"_initialOwner","type":"address"},{"internalType":"address","name":"_olympusDAO","type":"address"},{"internalType":"uint256[]","name":"_tierCeilings","type":"uint256[]"},{"internalType":"uint256[]","name":"_fees","type":"uint256[]"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"deposit","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"payout","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"expires","type":"uint256"}],"name":"BondCreated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"internalPrice","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"debtRatio","type":"uint256"}],"name":"BondPriceChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"recipient","type":"address"},{"indexed":false,"internalType":"uint256","name":"payout","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"remaining","type":"uint256"}],"name":"BondRedeemed","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"initialBCV","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"newBCV","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"adjustment","type":"uint256"},{"indexed":false,"internalType":"bool","name":"addition","type":"bool"}],"name":"ControlVariableAdjustment","type":"event"},{"inputs":[],"name":"adjustment","outputs":[{"internalType":"bool","name":"add","type":"bool"},{"internalType":"uint256","name":"rate","type":"uint256"},{"internalType":"uint256","name":"target","type":"uint256"},{"internalType":"uint256","name":"buffer","type":"uint256"},{"internalType":"uint256","name":"lastBlock","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"bondInfo","outputs":[{"internalType":"uint256","name":"payout","type":"uint256"},{"internalType":"uint256","name":"vesting","type":"uint256"},{"internalType":"uint256","name":"lastBlock","type":"uint256"},{"internalType":"uint256","name":"truePricePaid","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"bondPrice","outputs":[{"internalType":"uint256","name":"price_","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_olympusTreasury","type":"address"}],"name":"changeOlympusTreasury","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"currentDebt","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"currentOlympusFee","outputs":[{"internalType":"uint256","name":"currentFee_","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"debtDecay","outputs":[{"internalType":"uint256","name":"decay_","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"debtRatio","outputs":[{"internalType":"uint256","name":"debtRatio_","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"},{"internalType":"uint256","name":"_maxPrice","type":"uint256"},{"internalType":"address","name":"_depositor","type":"address"}],"name":"deposit","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_controlVariable","type":"uint256"},{"internalType":"uint256","name":"_vestingTerm","type":"uint256"},{"internalType":"uint256","name":"_minimumPrice","type":"uint256"},{"internalType":"uint256","name":"_maxPayout","type":"uint256"},{"internalType":"uint256","name":"_maxDebt","type":"uint256"},{"internalType":"uint256","name":"_initialDebt","type":"uint256"}],"name":"initializeBond","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"lastDecay","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"maxPayout","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"paySubsidy","outputs":[{"internalType":"uint256","name":"payoutSinceLastSubsidy_","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_value","type":"uint256"}],"name":"payoutFor","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_depositor","type":"address"}],"name":"pendingPayoutFor","outputs":[{"internalType":"uint256","name":"pendingPayout_","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_depositor","type":"address"}],"name":"percentVestedFor","outputs":[{"internalType":"uint256","name":"percentVested_","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"policy","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_depositor","type":"address"}],"name":"redeem","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"_addition","type":"bool"},{"internalType":"uint256","name":"_increment","type":"uint256"},{"internalType":"uint256","name":"_target","type":"uint256"},{"internalType":"uint256","name":"_buffer","type":"uint256"}],"name":"setAdjustment","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"enum CustomBond.PARAMETER","name":"_parameter","type":"uint8"},{"internalType":"uint256","name":"_input","type":"uint256"}],"name":"setBondTerms","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"terms","outputs":[{"internalType":"uint256","name":"controlVariable","type":"uint256"},{"internalType":"uint256","name":"vestingTerm","type":"uint256"},{"internalType":"uint256","name":"minimumPrice","type":"uint256"},{"internalType":"uint256","name":"maxPayout","type":"uint256"},{"internalType":"uint256","name":"maxDebt","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalDebt","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalPayoutGiven","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalPrincipalBonded","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_newOwner","type":"address"}],"name":"transferManagment","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"trueBondPrice","outputs":[{"internalType":"uint256","name":"price_","type":"uint256"}],"stateMutability":"view","type":"function"}]')
            bond = web3.eth.contract(address=address, abi=abi)

            print('Bonds:')
            TrueBondPrice = baseTokenPrice*bond.functions.trueBondPrice().call()/1e7
            Disc = (decimal.Decimal(payoutTokenPrice) - decimal.Decimal(TrueBondPrice)) / decimal.Decimal(TrueBondPrice)
            print(f' TrueBondPrice: {TrueBondPrice}')
            print(f'      Discount: {100 * Disc:,.2f} %')
            return(Disc)

        except Exception as e:
            print("contract_info error")
            print(e)


def maxDebtReached(bond_address):
    address = bond_address
    abi = json.loads('[{"inputs":[{"internalType":"address","name":"_customTreasury","type":"address"},{"internalType":"address","name":"_payoutToken","type":"address"},{"internalType":"address","name":"_principalToken","type":"address"},{"internalType":"address","name":"_olympusTreasury","type":"address"},{"internalType":"address","name":"_subsidyRouter","type":"address"},{"internalType":"address","name":"_initialOwner","type":"address"},{"internalType":"address","name":"_olympusDAO","type":"address"},{"internalType":"uint256[]","name":"_tierCeilings","type":"uint256[]"},{"internalType":"uint256[]","name":"_fees","type":"uint256[]"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"deposit","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"payout","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"expires","type":"uint256"}],"name":"BondCreated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"internalPrice","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"debtRatio","type":"uint256"}],"name":"BondPriceChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"recipient","type":"address"},{"indexed":false,"internalType":"uint256","name":"payout","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"remaining","type":"uint256"}],"name":"BondRedeemed","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"initialBCV","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"newBCV","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"adjustment","type":"uint256"},{"indexed":false,"internalType":"bool","name":"addition","type":"bool"}],"name":"ControlVariableAdjustment","type":"event"},{"inputs":[],"name":"adjustment","outputs":[{"internalType":"bool","name":"add","type":"bool"},{"internalType":"uint256","name":"rate","type":"uint256"},{"internalType":"uint256","name":"target","type":"uint256"},{"internalType":"uint256","name":"buffer","type":"uint256"},{"internalType":"uint256","name":"lastBlock","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"bondInfo","outputs":[{"internalType":"uint256","name":"payout","type":"uint256"},{"internalType":"uint256","name":"vesting","type":"uint256"},{"internalType":"uint256","name":"lastBlock","type":"uint256"},{"internalType":"uint256","name":"truePricePaid","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"bondPrice","outputs":[{"internalType":"uint256","name":"price_","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_olympusTreasury","type":"address"}],"name":"changeOlympusTreasury","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"currentDebt","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"currentOlympusFee","outputs":[{"internalType":"uint256","name":"currentFee_","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"debtDecay","outputs":[{"internalType":"uint256","name":"decay_","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"debtRatio","outputs":[{"internalType":"uint256","name":"debtRatio_","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"},{"internalType":"uint256","name":"_maxPrice","type":"uint256"},{"internalType":"address","name":"_depositor","type":"address"}],"name":"deposit","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_controlVariable","type":"uint256"},{"internalType":"uint256","name":"_vestingTerm","type":"uint256"},{"internalType":"uint256","name":"_minimumPrice","type":"uint256"},{"internalType":"uint256","name":"_maxPayout","type":"uint256"},{"internalType":"uint256","name":"_maxDebt","type":"uint256"},{"internalType":"uint256","name":"_initialDebt","type":"uint256"}],"name":"initializeBond","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"lastDecay","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"maxPayout","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"paySubsidy","outputs":[{"internalType":"uint256","name":"payoutSinceLastSubsidy_","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_value","type":"uint256"}],"name":"payoutFor","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_depositor","type":"address"}],"name":"pendingPayoutFor","outputs":[{"internalType":"uint256","name":"pendingPayout_","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_depositor","type":"address"}],"name":"percentVestedFor","outputs":[{"internalType":"uint256","name":"percentVested_","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"policy","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_depositor","type":"address"}],"name":"redeem","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"_addition","type":"bool"},{"internalType":"uint256","name":"_increment","type":"uint256"},{"internalType":"uint256","name":"_target","type":"uint256"},{"internalType":"uint256","name":"_buffer","type":"uint256"}],"name":"setAdjustment","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"enum CustomBond.PARAMETER","name":"_parameter","type":"uint8"},{"internalType":"uint256","name":"_input","type":"uint256"}],"name":"setBondTerms","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"terms","outputs":[{"internalType":"uint256","name":"controlVariable","type":"uint256"},{"internalType":"uint256","name":"vestingTerm","type":"uint256"},{"internalType":"uint256","name":"minimumPrice","type":"uint256"},{"internalType":"uint256","name":"maxPayout","type":"uint256"},{"internalType":"uint256","name":"maxDebt","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalDebt","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalPayoutGiven","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalPrincipalBonded","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_newOwner","type":"address"}],"name":"transferManagment","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"trueBondPrice","outputs":[{"internalType":"uint256","name":"price_","type":"uint256"}],"stateMutability":"view","type":"function"}]')
    bond = web3.eth.contract(address=address, abi=abi)
    try:
        currentDebt = bond.functions.currentDebt().call()
        maxDebt = bond.functions.terms().call()
        if currentDebt >= maxDebt[4]:
            return(True)
        else:
            return(False)

    except Exception as e:
        print("maxDebtReached error")
        print(e)    


def emptyTreasaury(treasury_address, payout_token_address, payout_token_price):
    abi = json.loads('[{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"_owner","type":"address"},{"indexed":true,"internalType":"address","name":"_spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"_value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"_from","type":"address"},{"indexed":true,"internalType":"address","name":"_to","type":"address"},{"indexed":false,"internalType":"uint256","name":"_value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MAX_SUPPLY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"claimOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"mint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pendingOwner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner_","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"},{"internalType":"bool","name":"direct","type":"bool"},{"internalType":"bool","name":"renounce","type":"bool"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
    token = web3.eth.contract(address=payout_token_address, abi=abi)
    try:
        tokensLeft = token.functions.balanceOf(treasury_address).call()
        if tokensLeft/1e18 * payout_token_price < 1000:
            return(True)
        else:
            return(False)

    except Exception as e:
        print("emptyTreasaury error")
        print(e)


def get_prices():
    #retrieve prices from CoinGecko
    baseTokenPrice = cg.get_price(ids='thorchain', vs_currencies='usd')['thorchain']['usd']
    payoutTokenPrice = cg.get_price(ids='thorswap', vs_currencies='usd')['thorswap']['usd']

    bondClosed = maxDebtReached(bond_address='0x3Ea7eBDcf8Ce93903420e5db4036d0899564cE5E')
    bondEmpty = emptyTreasaury(treasury_address='0x68619d4C962D3EE76277b5bC685E161917EE7561', payout_token_address='0xa5f2211B9b8170F694421f2046281775E8468044', payout_token_price=payoutTokenPrice)
    bondDisc = contract_info(bond_address='0x3Ea7eBDcf8Ce93903420e5db4036d0899564cE5E', baseTokenPrice=baseTokenPrice, payoutTokenPrice=payoutTokenPrice, maxReached=bondClosed, noFunds=bondEmpty)
    return(bondDisc)


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    if not check_discounts.is_running():
        check_discounts.start()


@tasks.loop(seconds = 60)
async def check_discounts():
    bondDisc = get_prices()
    
    for guild in client.guilds:
        guser = guild.get_member(client.user.id)
        try:
            if bondDisc == -999:
                await guser.edit(nick=f'Sold Out!')
                await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f'⛔ RUNE Bonds'))
            elif bondDisc < 0:
                await guser.edit(nick=f'{-100*bondDisc:,.2f}% Premium')
                await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f'RUNE Bonds'))
            else:
                await guser.edit(nick=f'{100*bondDisc:,.2f}% Discount')
                await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f'RUNE Bonds'))

        except Exception as e:
            print("check_discounts error")
            print(e)


client.run(BOT_TOKEN)
