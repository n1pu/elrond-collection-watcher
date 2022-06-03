from datetime import datetime
import requests
import discord
import time
import time
import os
import config
from dotenv import load_dotenv
from discord.ext import tasks


client = discord.Client()


@client.event
async def on_ready():
    print("Bot active.")
    if not main.is_running():
        main.start()


@tasks.loop(seconds=config.FREQUENCY)
async def main():
    json = requests.post("https://gateway.deadrare.io/",
                         json={"query": config.QUERY}).json()
    egld_price = requests.get("https://api.elrond.com/mex-pairs/WEGLD-bd4d79/USDC-c76f1f").json()["basePrice"]

    # Post transactions
    for sale in json["data"]["listSales"]['results']:
        if sale["timestamp"] > time.time() - config.FREQUENCY - 1:
            id = int(sale["nftNonce"], 16)
            price = sale['salePrice']
            hash = sale['id']

            emb = discord.Embed()
            emb.title = f"{config.NAME} #{id} was just sold!"
            # emb.description = f"{collection}-{sale['nftNonce']} sold for {price} EGLD on Deadrare"
            emb.color = 0x2ECC40
            emb.set_thumbnail(
                url=f"https://gateway.pinata.cloud/ipfs/{config.IPFS}/{id}.png")
            emb.add_field(name="Transaction",
                        value=f"[{hash[:4]}...{hash[-4:]}](https://explorer.elrond.com/transactions/{hash})", inline=True)
            emb.add_field(
                name="Price", value=f"{round(price, 2)} EGLD / {round(price * egld_price, 1)} USD", inline=True)
            # emb.add_field(
            #     name="Marketplace", value="Deadrare", inline=True)
            emb.timestamp = datetime.fromtimestamp(sale["timestamp"])
            await client.get_channel(config.POST_CHANNEL).send(embed=emb)

    # Edit channels
    floor = json["data"]["floorPrice"]
    volume = json["data"]["stats"]["allTimeStats"]["totalPrice"]
    holders = json["data"]["listOwners"]["count"]
    await client.get_channel(config.FLOOR_CHANNEL).edit(name=f"💱• Floor: {floor}")
    await client.get_channel(config.VOLUME_CHANNEL).edit(name=f"📊• Volume: {round(volume)} EGLD")
    await client.get_channel(config.HOLDERS_CHANNEL).edit(name=f"👻• Owners: {holders}")

load_dotenv()
client.run(os.getenv("BOT_KEY"))
