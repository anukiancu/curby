from py3pin.Pinterest import Pinterest
import random

BOARD_ID = "271904964941663628"


def get_random_kirby_pic():
    print("Fetching pictures of Kirby from Pinterest.")
    p = Pinterest()
    pins = p.board_feed(board_id=BOARD_ID)
    random_image = random.choice(pins)
    return random_image["images"]["orig"]["url"]
