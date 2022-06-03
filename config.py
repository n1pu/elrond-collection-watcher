NAME = "8-Bit Heroes"
COLLECTION = "8BITHEROES-d3022d"
IPFS = "QmWV5jdF4jWMArAXzUk2b6wDXSmrcKx1DohbeHNLKCDxLz"
POST_CHANNEL = 932671441776803861
FLOOR_CHANNEL = 712833962472505389
VOLUME_CHANNEL = 967360180633350154
HOLDERS_CHANNEL = 967360238690897951

QUERY = f"""
query {{
    floorPrice(collection: "{COLLECTION}")
    stats(filters: {{collection: "{COLLECTION}"}}) {{allTimeStats {{totalPrice}} }}
    listSales(filters: {{collection: "{COLLECTION}"}} pagination: {{}}) {{results {{nftNonce, salePrice, timestamp, id}}, count}}
    listOwners( filters: {{collection: "{COLLECTION}"}} pagination: {{}}) {{count}}
}}
"""

FREQUENCY = 600