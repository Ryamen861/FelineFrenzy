import pygame
import os
import json
from enum import Enum

import catmanager
from button import Button
from catmanager import CatManager
pygame.font.init()


class WindowState(Enum):
    HOME = 1
    STORE = 2
    CONFIRM_WIN = 3
    PLACE_ITEM_WIN = 4
    ALREADY_BOUGHT_WIN = 5
    NOT_ENOUGH_MONEY_WIN = 6
    CAT_BOOK = 7


win_state = WindowState.HOME

FONT = pygame.font.SysFont("comicsans", 40)
S_FONT = pygame.font.SysFont("comicsans", 29)
WIDTH, HEIGHT = 900, 600
FPS = 20

LEVEL = 0
LEVELS = [20, 40, 80, 140, 220, 320, 440, 580, 700]
XP = 0
# CURR_SCREEN = None
FISH_COINS = 0
time_passed_ms = 0

# colors
SECONDARY_COLOR = (244, 229, 97)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
NAVY = (36, 55, 99)
STORE_BG_COLOR = (79, 187, 148)

# rectangles
STORE_BG = pygame.Rect(0, 0, WIDTH, HEIGHT)
store_banner = pygame.Rect(0, 0, WIDTH, 150)
store_confirm_window = pygame.Rect(150, 50, 600, 400)

# text
banner_text = FONT.render("Store", True, STORE_BG_COLOR)
yes_text = FONT.render("Yes", True, WHITE)
no_text = FONT.render("No", True, WHITE)
coin_text = S_FONT.render(f"${FISH_COINS}", True, WHITE)
XP_text = S_FONT.render(f"{XP} XP", True, WHITE)
level_text = S_FONT.render(f"Level: {LEVEL}", True, WHITE)
ok_text = FONT.render("Ok", True, WHITE)

# cat book text
johnny_text = FONT.render("Johnny Cat", True, STORE_BG_COLOR)
sarah_text = FONT.render("Sarah Cat", True, STORE_BG_COLOR)
oscar_text = FONT.render("Oscar Cat", True, STORE_BG_COLOR)
may_text = FONT.render("May Cat", True, STORE_BG_COLOR)
happy_text = FONT.render("Happy Cat", True, STORE_BG_COLOR)
curious_text = FONT.render("Curious Cat", True, STORE_BG_COLOR)
cool_cat_coby_text = FONT.render("Cool Cat Coby", True, STORE_BG_COLOR)
sus_text = FONT.render("Sus Cat", True, STORE_BG_COLOR)

cat_book_rows = [johnny_text, sarah_text, oscar_text, may_text, happy_text, curious_text, cool_cat_coby_text, sus_text]

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Feline Frenzy")

# make a CatManager
CM = CatManager()

# load images
BG = pygame.image.load(os.path.join("Assets", "FelineFrenzyBackground.png"))
CAT_BOOK_BG = pygame.image.load(os.path.join("Assets", "cat_book_wallpaper.png"))
PLACE_TOY_BG = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "place_wallpaper.png")), (900, 600))
store_button_image = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "store_button.png")), (150, 100))
home_button_image = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "home_button.png")), (150, 100))
book_button_image = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "book_button_image.png")),
                                           (150, 100))

# store images
water_bottle_image = pygame.image.load(os.path.join("Assets", "water_bottle.png"))
cardboard_image = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "scratchy_cardboard.jpg")),
                                         (270, 175))
plush_toy_image = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "teddy_bear.png")), (300, 200))
cat_track_image = pygame.image.load(os.path.join("Assets", "cat_track_toy.png"))
feather_stick_image = pygame.image.load(os.path.join("Assets", "feather_on_a_stick.png"))
tube_image = pygame.image.load(os.path.join("Assets", "tube.png"))
cat_tree_image = pygame.image.load(os.path.join("Assets", "cat_tree.png"))
catnip_forest_image = pygame.image.load(os.path.join("Assets", "catnip_forest.png"))

# add place buttons
place_image = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "plus_button.png")), (150, 150))

PRICES = {
    "plastic bottle": 20,
    "scratchy cardboard": 40,
    "plush toy": 80,
    "cat track": 115,
    "feather on a stick": 150,
    "crawl tube": 185,
    "cat palace": 250,
    "catnip forest": 390,
}

ITEM_IMAGE_LINK = {
    "plastic bottle": water_bottle_image,
    "scratchy cardboard": cardboard_image,
    "plush toy": plush_toy_image,
    "cat track": cat_track_image,
    "feather on a stick": feather_stick_image,
    "crawl tube": tube_image,
    "cat palace": cat_tree_image,
    "catnip forest": 39,
}

ITEMS = [key for key, value in PRICES.items()]

CURR_ITEM = ""

# Side Funcs _______________________________________________


def draw_confirm_window(item):
    global win_state
    win_state = WindowState.CONFIRM_WIN
    cost = PRICES[item]

    pygame.draw.rect(WIN, NAVY, store_confirm_window)
    confirm_text = S_FONT.render("Are you sure you want to buy ", True, WHITE)
    confirm_text_2 = S_FONT.render(f"the {item} for ${cost} dollars?", True, WHITE)
    WIN.blit(confirm_text, (WIDTH / 2 - confirm_text.get_width() / 2, 100))
    WIN.blit(confirm_text_2, (WIDTH / 2 - confirm_text_2.get_width() / 2, 102 + confirm_text.get_height()))

    yes_button.draw()
    no_button.draw()


def update_coins():
    global coin_text
    coin_text = S_FONT.render(f"${FISH_COINS}", True, WHITE)

    match win_state:
        case WindowState.STORE:
            store_button_func()
        case WindowState.HOME:
            home_button_func()


def update_XP():
    global XP_text
    XP_text = S_FONT.render(f"{XP} XP", True, WHITE)

    match win_state:
        case WindowState.STORE:
            store_button_func()
        case WindowState.HOME:
            home_button_func()


def update_level():
    global level_text
    level_text = S_FONT.render(f"Level: {LEVEL}", True, WHITE)

    match win_state:
        case WindowState.STORE:
            store_button_func()
        case WindowState.HOME:
            home_button_func()


def is_buyable(cost):
    global FISH_COINS
    return not FISH_COINS - cost < 0


def draw_place_toy_window():
    global win_state
    win_state = WindowState.PLACE_ITEM_WIN
    WIN.blit(PLACE_TOY_BG, (0, 0))

    if CM.SM.spot2.item_name == "":
        foothill_button.draw()
    if CM.SM.spot3.item_name == "":
        tophill_button.draw()
    if CM.SM.spot4.item_name == "":
        downhill_button.draw()

    # make the code above into a for loop

    # since we sealed a screen over the home button
    store_button.draw()


def item_placer():
    # update whatever that needs to be on screen items/toys
    for item in CM.SM.curr_items:

        if item != "default box":

            if item == "plastic bottle":
                new_image = pygame.transform.scale(water_bottle_image, (150, 75))
            elif item == "scratchy cardboard":
                new_image = pygame.transform.scale(cardboard_image, (180, 117))
            elif item == "plush toy":
                new_image = pygame.transform.scale(plush_toy_image, (150, 100))
            elif item == "cat track":
                new_image = pygame.transform.scale(cat_track_image, (150, 113))
            else:
                new_image = ITEM_IMAGE_LINK[item]

            for spot_object in CM.SM.spots:
                if spot_object.item_name == item:
                    x, y = spot_object.coor
                    new_x = x - new_image.get_width()/2
                    new_y = y - new_image.get_height()/2
                    WIN.blit(new_image, (new_x, new_y))


def plus_button_func(place_description, item):
    CM.insert_toy(place_description, item)
    home_button_func()


def sorry_not_enough_money_window():
    global win_state
    win_state = WindowState.NOT_ENOUGH_MONEY_WIN

    # store confirm window because it is the same format/style we want
    pygame.draw.rect(WIN, NAVY, store_confirm_window)
    sorry_text = S_FONT.render("It looks like you do not have enough", True, WHITE)
    sorry_text_2 = S_FONT.render(f"money for the {CURR_ITEM}.", True, WHITE)

    WIN.blit(sorry_text, (WIDTH / 2 - sorry_text.get_width() / 2, 100))
    WIN.blit(sorry_text_2, (WIDTH / 2 - sorry_text_2.get_width() / 2, 102 + sorry_text.get_height()))

    ok_button.draw()


def you_already_bought_window():
    global win_state
    win_state = WindowState.ALREADY_BOUGHT_WIN

    # store confirm window because it is the same format/style we want
    pygame.draw.rect(WIN, NAVY, store_confirm_window)
    already_bought_text = S_FONT.render("It looks like you already bought this item", True, WHITE)

    WIN.blit(already_bought_text, (WIDTH / 2 - already_bought_text.get_width() / 2, 150))

    ok_button.draw()


# Recover Func ________________________________________________

def save_changes():
    try:
        with open("Logs.saved_changes.json", "w") as file:
            new_changes = {
                "fish_coins": FISH_COINS,
                "xp": XP,
                "level": LEVEL,
                "unlocked_cats": CM.unlocked_cats,
                "items on set": CM.SM.curr_items,
                "bought items": CM.SM.unlocked_items,
                "p_name_to_s_object_link": catmanager.return_place_name_to_object_link(),
                "c_item_to_p_name_link": CM.SM.curr_item_place_name_link,
            }
            
    except FileNotFoundError:
        # if there is no file, make the file and run this again
        with open("Logs.saved_changes.json", "w"):
            save_changes()
    else:
        json.dump(new_changes, file)

# Button Funcs ______________________________________________________________________


def store_button_func():
    global win_state
    # the current screen is now the store
    win_state = WindowState.STORE

    # set the background color
    pygame.draw.rect(WIN, STORE_BG_COLOR, STORE_BG)

    # add the banner
    pygame.draw.rect(WIN, SECONDARY_COLOR, store_banner)
    WIN.blit(banner_text, (WIDTH/2.3, 70))

    # add the coin and XP labels
    WIN.blit(coin_text, (5, 5))
    WIN.blit(XP_text, (5, coin_text.get_height() + 5))
    WIN.blit(level_text, (5, coin_text.get_height() + XP_text.get_height() + 5))

    # add the home button
    home_button.draw()

    # the item buttons
    water_bottle_button.draw()
    cardboard_button.draw()
    plush_toy_button.draw()

    cat_track_button.draw()
    feather_stick_button.draw()
    tube_button.draw()

    pygame.display.update()


def cat_book_func():
    global win_state
    win_state = WindowState.CAT_BOOK
    WIN.blit(CAT_BOOK_BG, (0, 0))
    caty = 60
    unlocked_list_len = len(CM.unlocked_cats)

    if unlocked_list_len > 4:
        for i in range(0, 4):
            # 0, 1, 2, 3     - which is the first four in terms of indexing
            new_text = cat_book_rows[i]
            WIN.blit(new_text, (100, caty))
            WIN.blit(CM.unlocked_cats[i].image, (100 + new_text.get_width(), caty))
            caty += 112
        # reset the y value because we start at the top of the other page, now
        caty = 60
        for i in range(4, unlocked_list_len):
            new_text = cat_book_rows[i]
            WIN.blit(new_text, (500, caty))
            WIN.blit(CM.unlocked_cats[i].image, (500 + new_text.get_width(), caty))
            caty += 112
    else:
        # print(f"The length of unlocked cats {len(CM.unlocked_cats)}, and we are here")
        # this means that the number of unlocked cats is less than or equal to 4
        for i in range(0, len(CM.unlocked_cats)):
            # print(f"drawing {CM.unlocked_cats[i]}")
            new_text = cat_book_rows[i]
            WIN.blit(new_text, (100, caty))
            WIN.blit(CM.unlocked_cats[i].image, (100 + new_text.get_width(), caty))
            caty += 112

    home_button.draw()

    pygame.display.update()


def home_button_func():
    global win_state
    # the screen now turns into the store screen
    win_state = WindowState.HOME

    # the background
    WIN.blit(BG, (0, 0))

    # add the coin and XP labels
    WIN.blit(coin_text, (WIDTH - coin_text.get_width() - 10, 5))
    WIN.blit(XP_text, (WIDTH - XP_text.get_width() - 10, coin_text.get_height() + 5))
    WIN.blit(level_text, (WIDTH - level_text.get_width() - 10, coin_text.get_height() + XP_text.get_height() + 5))

    # DRAW buttons on the home screen
    store_button.draw()
    book_button.draw()

    # draw back the items and cats that are supposed to be on screen
    item_placer()
    CM.cat_placer(WIN)

    pygame.display.update()


def buy_if_able(item):
    """This is called by all the toy funcs in the store"""
    global FISH_COINS
    global XP
    global CURR_ITEM

    CURR_ITEM = item
    cost = PRICES[item]

    # check if the item is already bought
    if CURR_ITEM in CM.SM.unlocked_items:
        you_already_bought_window()

    elif not is_buyable(cost):
        sorry_not_enough_money_window()

    else:
        # if they can afford it...
        draw_confirm_window(CURR_ITEM)


def actual_buy(decider):
    ''' This will be called by the "Yes" or "No" Buttons '''

    if decider:
        global FISH_COINS
        global XP
        global CURR_ITEM

        item = CURR_ITEM

        cost = PRICES[item]

        FISH_COINS -= cost
        XP += 5
        home_button_func()

        # set up the screen so that the person can choose where to put the new toy
        draw_place_toy_window()

        return item
        # return item so that the button can also call the CM to add the item
    else:
        store_button_func()


# Level Funcs __________________________________________________________

def check_new_level():
    global XP
    global LEVEL
    global FISH_COINS

    previous_level = LEVEL

    for level in LEVELS:
        if XP >= level:
            next_index = LEVELS.index(level) + 1
            if XP < LEVELS[next_index]:
                LEVEL = next_index  # it should be the index, but index start at 0, so plus 1.
        else:
            break

    # there has been a level up
    if LEVEL > previous_level:
        new_level_congratulations(LEVEL)
        update_level()
        FISH_COINS += 10
        CM.next_level_cat()


def new_level_congratulations(level):
    # new window that congratulates
    # - new level
    # let them know they have received a few fish_coins
    # let them know they have unlocked a new cat
    # make an ok button for this
    pass


# create all the buttons (but don't draw them yet)
store_button = Button(15, 0, store_button_image, WIN, store_button_func)
home_button = Button(WIDTH - home_button_image.get_width(), 15, home_button_image, WIN, home_button_func)
book_button = Button(15, 110, book_button_image, WIN, cat_book_func)

# store buttons
water_bottle_button = Button(0, 200, water_bottle_image, WIN, lambda: buy_if_able("plastic bottle"))
cardboard_button = Button(water_bottle_image.get_width(), 200, cardboard_image, WIN,
                          lambda: buy_if_able("scratchy cardboard"))
plush_toy_button = Button(water_bottle_image.get_width() + cardboard_image.get_width(), 200, plush_toy_image, WIN,
                          lambda: buy_if_able("plush toy"))
cat_track_button = Button(30, water_bottle_image.get_height() + 250, cat_track_image, WIN, lambda: buy_if_able("cat track"))

feather_stick_button = Button(cat_track_image.get_width() + 125, cardboard_image.get_height() + 220, feather_stick_image, WIN,
                              lambda: buy_if_able("feather on a stick"))

tube_button = Button(cat_track_image.get_width() + feather_stick_image.get_width() + 230,
                     plush_toy_image.get_height() + 190, tube_image, WIN, lambda: buy_if_able("crawl tube"))
# tube_image = pygame.image.load(os.path.join("Assets", "tube.png"))
# cat_palace_image = pygame.image.load(os.path.join("Assets", "cat_tree.png"))
# catnip_forest_image = pygame.image.load(os.path.join("Assets", "catnip_forest.png"))

# for confirm window
yes_button = Button(700 - yes_text.get_width(), 300, yes_text, WIN, lambda: CM.add_item_to_inventory(CURR_ITEM) if actual_buy(True) else None)
no_button = Button(200, 300, no_text, WIN, lambda: actual_buy(False))

# for the toy placing process
foothill_button = Button(270, 420, place_image, WIN, lambda: plus_button_func("foothill", CURR_ITEM))
tophill_button = Button(485, 280, place_image, WIN, lambda: plus_button_func("tophill", CURR_ITEM))
downhill_button = Button(720, 422, place_image, WIN, lambda: plus_button_func("downhill", CURR_ITEM))

# for not enough money window/you already bought window
ok_button = Button(WIDTH/2 - ok_text.get_width()/2, 250, ok_text, WIN, store_button_func)


def main():
    global XP
    global FISH_COINS
    global time_passed_ms

    run = True
    clock = pygame.time.Clock()

    # to draw the home screen
    home_button_func()

    while run:
        clock.tick(FPS)
        time_passed_ms += clock.get_time()
        previous_XP = XP
        previous_coins = FISH_COINS

        match win_state:
            case WindowState.HOME:
                store_button.check_click()
                book_button.check_click()

            case WindowState.STORE:
                home_button.check_click()

                water_bottle_button.check_click()
                cardboard_button.check_click()
                plush_toy_button.check_click()

                cat_track_button.check_click()
                feather_stick_button.check_click()
                tube_button.check_click()

            case WindowState.CAT_BOOK:
                home_button.check_click()

            case WindowState.CONFIRM_WIN:
                yes_button.check_click()
                no_button.check_click()

            case WindowState.PLACE_ITEM_WIN:
                store_button.check_click()

                foothill_button.check_click()
                tophill_button.check_click()
                downhill_button.check_click()

            case WindowState.ALREADY_BOUGHT_WIN:
                ok_button.check_click()

            case WindowState.NOT_ENOUGH_MONEY_WIN:
                ok_button.check_click()

        # make a new cat based on T/F
        new_make_val = CM.make_new_cat(time_passed_ms)
        if type(new_make_val) == int:
            # that means an XP value was returned, therefore a cat was made
            XP += new_make_val
            update_XP()
            # match win_state:
            #     case WindowState.HOME:
            #         home_button_func()

        # make a cat leave based on T/F
        new_leave_val = CM.leave_cat(time_passed_ms)
        if type(new_leave_val) == int:
            # that means a money value was returned, therefore a cat left
            FISH_COINS += new_leave_val
            update_coins()
            # match win_state:
            #     case WindowState.HOME:
            #         home_button_func()

        check_new_level()

        # update the coins if there has been a change
        if previous_coins != FISH_COINS:
            update_coins()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                pass

        pygame.display.update()


if __name__ == "__main__":
    main()
