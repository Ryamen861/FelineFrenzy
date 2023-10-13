import pygame
import os
import json
from json import JSONDecodeError
import math
from enum import Enum

import catmanager
from button import Button
from catmanager import CatManager
from encoders import CMEncoder
pygame.font.init()

# if day is monday, this icon, tuesday, this icon (would be fun to make)
FelineFrenzyIcon = pygame.image.load(os.path.join("Assets", "johnny_cat.png"))
pygame.display.set_icon(FelineFrenzyIcon)


class WindowState(Enum):
    HOME = 1
    STORE = 2
    CONFIRM_WIN = 3
    PLACE_ITEM_WIN = 4
    ALREADY_BOUGHT_WIN = 5
    NOT_ENOUGH_MONEY_WIN = 6
    CAT_BOOK = 7
    NEXT_LEVEL = 8


win_state = WindowState.HOME

FONT = pygame.font.SysFont("comicsans", 40)
S_FONT = pygame.font.SysFont("comicsans", 29)
WIDTH, HEIGHT = 900, 600
FPS = 20

flag_event = []

LEVEL = 0
LEVELS = [20, 40, 80, 140, 220, 320, 440, 580, 700]
XP = 0
# CURR_SCREEN = None
FISH_COINS = 0

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

# make an Encoder
Encoder = CMEncoder()

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
    # "cat palace": cat_tree_image,
    # "catnip forest": 39,
}

ITEMS = [key for key, value in PRICES.items()]

CURR_ITEM = ""

# Side Funcs _______________________________________________


def draw_confirm_window(item):
    """Opens up the confirm window to confirm purchases from the store"""
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
    """renders the new value of FISH_COINS"""
    global coin_text
    # set up and render the new value
    coin_text = S_FONT.render(f"${FISH_COINS}", True, WHITE)

    # reload the current page to see the new change
    match win_state:
        case WindowState.STORE:
            store_button_func()
        case WindowState.HOME:
            home_button_func()


def update_XP():
    """renders the new value of XP"""
    global XP_text
    # set up and render the new value
    XP_text = S_FONT.render(f"{XP} XP", True, WHITE)

    # reload the current page to see the new change
    match win_state:
        case WindowState.STORE:
            store_button_func()
        case WindowState.HOME:
            home_button_func()


def update_level():
    """renders the new value of LEVEL"""
    global level_text
    # set up and render the new value
    level_text = S_FONT.render(f"Level: {LEVEL}", True, WHITE)
    
    # reload the current page to see the new change
    match win_state:
        case WindowState.STORE:
            store_button_func()
        case WindowState.HOME:
            home_button_func()


def can_afford(cost):
    """determines if an item the user wants to buy can be afforded"""
    global FISH_COINS
    return not FISH_COINS - cost < 0


def draw_place_toy_window():
    """Setting up the page for a user to place their newly purchsased toy"""
    global win_state
    win_state = WindowState.PLACE_ITEM_WIN
    WIN.blit(PLACE_TOY_BG, (0, 0))

    # if the spot has no toy, draw the plus button there to indicate the user can put it there
    if CM.SM.spot2.toy == "":
        foothill_button.draw()
    if CM.SM.spot3.toy == "":
        tophill_button.draw()
    if CM.SM.spot4.toy == "":
        downhill_button.draw()

    # since we sealed a screen over the home button
    store_button.draw()


def item_placer():
    """update toys that needs to be on home screen """
    for spot_object in CM.SM.spots:
        if spot_object.toy != "" and spot_object.id != 0:

            match spot_object.toy:
                case "plastic bottle":
                    new_image = pygame.transform.scale(water_bottle_image, (150, 75))
                case "scratchy cardboard":
                    new_image = pygame.transform.scale(cardboard_image, (180, 117))
                case "plush toy":
                    new_image = pygame.transform.scale(plush_toy_image, (150, 100))
                case "cat track":
                    new_image = pygame.transform.scale(cat_track_image, (150, 113))
                case _:
                    new_image = ITEM_IMAGE_LINK[spot_object.toy] ################################################

            x, y = spot_object.coor
            new_x = x - new_image.get_width()/2
            new_y = y - new_image.get_height()/2
            WIN.blit(new_image, (new_x, new_y))


    # for item in CM.SM.curr_items:

    #     if item != "default box":

    #         if item == "plastic bottle":
    #             new_image = pygame.transform.scale(water_bottle_image, (150, 75))
    #         elif item == "scratchy cardboard":
    #             new_image = pygame.transform.scale(cardboard_image, (180, 117))
    #         elif item == "plush toy":
    #             new_image = pygame.transform.scale(plush_toy_image, (150, 100))
    #         elif item == "cat track":
    #             new_image = pygame.transform.scale(cat_track_image, (150, 113))
    #         else:
    #             new_image = ITEM_IMAGE_LINK[item]

    #         for spot_object in CM.SM.spots:
    #             if spot_object.item_name == item:
    #                 x, y = spot_object.coor
    #                 new_x = x - new_image.get_width()/2
    #                 new_y = y - new_image.get_height()/2
    #                 WIN.blit(new_image, (new_x, new_y))


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


# Recover/Save Funcs ________________________________________________

def save_changes():
    file_path = os.path.join("Logs", "saved_changes.json")

    try:
        # see if there is a file
        with open(file_path, "w") as file:
            to_be_saved = Encoder.encode(CM)
            to_be_saved["fish_coins"] = FISH_COINS
            to_be_saved["xp"] = XP
            to_be_saved["level"] = LEVEL
                                
            json.dump(to_be_saved, file, indent=4)

    except FileNotFoundError:
        # if there is no file, make the file and run this again
        with open(file_path, "w"):
            save_changes()


def recover():
    global FISH_COINS
    global XP
    global LEVEL

    file_path = os.path.join("Logs", "saved_changes.json")

    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            if data != "":
                # assign the values
                FISH_COINS = data["fish_coins"]  # int
                XP = data["xp"]        # int
                LEVEL = data["level"]  # int

                # restore unlocked_cats
                names_of_unlocked_cats = data["unlocked_cats"]       # list of strings
                for name in names_of_unlocked_cats:
                    for cat_object in CM.all_cats:
                        if cat_object.name != "Johnny Cat":
                            if name == cat_object.name:
                                CM.unlocked_cats.append(cat_object)
                                break

                # restore current cats along with their xy coors
                names_of_current_cats = data["current cats"]        # dictionary

                for spot_object_id, cat_name in names_of_current_cats.items():
                    for cat_object in CM.all_cats:
                        if cat_name == cat_object.name:

                            spot_object = ""

                            for spot_o in CM.SM.spots:
                                if spot_o.id == int(spot_object_id):
                                    spot_object = spot_o
                                    break

                            cat_object.xy = spot_object.coor
                            CM.current_cats.append(cat_object)
                            break

                # restore cats_met
                names_of_cats_met = data["cats met"]                 # list of strings
                for name in names_of_cats_met:
                    for cat_object in CM.all_cats:
                        if name == cat_object.name:
                            CM.cats_met.append(cat_object)
                            break

                CM.SM.curr_items = data["items on set"]        # list of strings
                CM.SM.unlocked_items = data["bought items"]    # list of strings

                # restore toys
                spots_item_link = data["spots with their items"]  # dictionary
                for spot_id, toy in spots_item_link.items():
                    for spot_object in CM.SM.spots:
                        if int(spot_object.id) != 0:
                            if int(spot_id) == spot_object.id:
                                spot_object.toy = toy
                                break

                # restore cats
                spots_cat_link = data["spots with their cats"]    # dictionary
                for k, v in spots_cat_link.items():
                    for spot_object in CM.SM.spots:
                        if int(k) == spot_object.id:
                            spot_object.cat_in_it = v
                            spot_object.is_filled = True
                            break

                # cats with their times
                cats_time_link = data["cats with their times"]
                for cat_name, cat_stay_time in cats_time_link.items():
                    for cat_object in CM.current_cats:
                        if cat_name == cat_object.name:
                            cat_object.stay_time = cat_stay_time
                            cat_object.birthday = 0

                # update them on screen
                update_coins()
                update_level()
                update_XP()
                item_placer()
                CM.cat_placer(WIN)

    except FileNotFoundError:
        with open(file_path, "w") as file:
            # just make the file
            pass


# Button Funcs ______________________________________________________________________


def store_button_func():
    """Draws the store screen"""
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
    """Draws the cat book"""
    global win_state
    win_state = WindowState.CAT_BOOK
    WIN.blit(CAT_BOOK_BG, (0, 0))
    caty = 60
    num_of_cats_met = len(CM.cats_met)

    if num_of_cats_met >= 4:
        # if we need two pages for all of the cats...

        # display the first four on the left page
        for i in range(0, 4):
            new_text = cat_book_rows[i]
            WIN.blit(new_text, (100, caty))
            WIN.blit(CM.cats_met[i].image, (100 + new_text.get_width(), caty))
            caty += 112
            
        # display the rest on the page on the right
        caty = 60
        for i in range(4, num_of_cats_met):
            new_text = cat_book_rows[i]
            WIN.blit(new_text, (500, caty))
            WIN.blit(CM.cats_met[i].image, (500 + new_text.get_width(), caty))
            caty += 112
    else:
        # all cats displayed will be on the left side of the page
        for i in range(0, num_of_cats_met):
            new_text = cat_book_rows[i]
            WIN.blit(new_text, (100, caty))
            WIN.blit(CM.cats_met[i].image, (100 + new_text.get_width(), caty))
            caty += 112

    home_button.draw()

    pygame.display.update()


def home_button_func():
    """draws the homescreen"""
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

    elif not can_afford(cost):
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
        XP += 3
        update_XP()
        update_coins()
    
        home_button_func()

        # set up the screen so that the person can choose where to put the new toy
        draw_place_toy_window()

        return item
        # return item so that the button can also call the CM to add the item
    else:
        store_button_func()


# Level Funcs __________________________________________________________

def check_new_level():
    """Check if XP received (if any) should move the user to the next level"""
    global XP
    global LEVEL
    global FISH_COINS

    previous_level = LEVEL

    for level in LEVELS:
        if XP >= level:
            LEVEL = LEVELS.index(level)
            LEVEL += 1
        else:
            break

    # there has been a level up
    if LEVEL > previous_level:

        # if nothing else is going on right now
        # (we don't want to interrupt an item placing process)
        if win_state == WindowState.HOME:
            unlocked_cat = CM.next_level_cat()
            new_level_congratulations(LEVEL, unlocked_cat)
            
        else:
            # put it in line to be displayed later on when there is a chance
            flag_event.append(LEVEL)


def new_level_congratulations(level, unlocked_cat):
    """Make a window that congratulates the user on a new level, alert them of any rewards"""
    global win_state
    global FISH_COINS
    
    # receive rewards
    FISH_COINS += 5
    update_coins()
    update_level()

    # set up window, text for new cat
    win_state = WindowState.NEXT_LEVEL
    pygame.draw.rect(WIN, NAVY, store_confirm_window)
    new_cat_text = f"Look out for {unlocked_cat}" if unlocked_cat != "no more cats" else "No more cats to unlock!"

    # render alert of new level, coin reward, new unlocked cat
    new_level_text = S_FONT.render(f"New level unlocked!", True, WHITE)
    welcome_text = S_FONT.render(f"Welcome to level {level}!", True, WHITE)
    receive_text = S_FONT.render(f"Coins + 5", True, WHITE)
    new_cat_alert_text = S_FONT.render(new_cat_text, True, WHITE)

    # actually update it on screen
    WIN.blit(new_level_text, (WIDTH / 2 - new_level_text.get_width() / 2, 150))
    WIN.blit(welcome_text, (WIDTH / 2 - welcome_text.get_width() / 2, new_level_text.get_height() + 150 + 5))
    WIN.blit(receive_text, (WIDTH / 2 - receive_text.get_width() / 2, 150 + new_level_text.get_height() + welcome_text.get_height() + 5))
    WIN.blit(new_cat_alert_text, (WIDTH / 2 - new_cat_alert_text.get_width() / 2, 150 + receive_text.get_height() + new_level_text.get_height() + welcome_text.get_height() + 5))

    next_level_button.draw()


# create all the buttons (but don't draw them yet)
store_button = Button(15, 0, store_button_image, WIN, store_button_func)
home_button = Button(WIDTH - home_button_image.get_width(), 15, home_button_image, WIN, home_button_func)
book_button = Button(15, 110, book_button_image, WIN, cat_book_func)

# store buttons
water_bottle_button = Button(0, 200, water_bottle_image, WIN, lambda: buy_if_able("plastic bottle"))
cardboard_button = Button(water_bottle_image.get_width(), 200, cardboard_image, WIN, lambda: buy_if_able("scratchy cardboard"))
plush_toy_button = Button(water_bottle_image.get_width() + cardboard_image.get_width(), 200, plush_toy_image, WIN, lambda: buy_if_able("plush toy"))
cat_track_button = Button(30, water_bottle_image.get_height() + 250, cat_track_image, WIN, lambda: buy_if_able("cat track"))
feather_stick_button = Button(cat_track_image.get_width() + 125, cardboard_image.get_height() + 220, feather_stick_image, WIN, 
                        lambda: buy_if_able("feather on a stick"))
tube_button = Button(cat_track_image.get_width() + feather_stick_image.get_width() + 230,
                    plush_toy_image.get_height() + 190, tube_image, WIN, lambda: buy_if_able("crawl tube"))

# buttons for confirm window
yes_button = Button(700 - yes_text.get_width(), 300, yes_text, WIN, lambda: CM.add_item_to_inventory(CURR_ITEM) if actual_buy(True) else None)
no_button = Button(200, 300, no_text, WIN, lambda: actual_buy(False))

# buttons for the toy placing process
foothill_button = Button(270, 420, place_image, WIN, lambda: plus_button_func(1, CURR_ITEM))
tophill_button = Button(485, 280, place_image, WIN, lambda: plus_button_func(2, CURR_ITEM))
downhill_button = Button(720, 422, place_image, WIN, lambda: plus_button_func(3, CURR_ITEM))

# buttons for not enough money window/you already bought window/congratulations window
ok_button = Button(WIDTH/2 - ok_text.get_width()/2, 250, ok_text, WIN, store_button_func)
next_level_button = Button(WIDTH/2 - ok_text.get_width()/2, 320, ok_text, WIN, home_button_func)


def main():
    global XP
    global FISH_COINS

    try:
        recover()
    except JSONDecodeError:
        pass

    run = True
    clock = pygame.time.Clock()

    # to draw the home screen
    home_button_func()

    while run:
        clock.tick(FPS)
        CM.curr_time += clock.get_time()

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

            case WindowState.NEXT_LEVEL:
                next_level_button.check_click()


        # make a new cat based on T/F        
        CM.make_new_cat()
        match win_state:
            case WindowState.HOME:
                CM.cat_placer(WIN)
            
        # make a cat leave based on T/F
        new_leave_val = CM.leave_cat()
        if isinstance(new_leave_val, int):
            # that means a money value was returned, therefore a cat left

            # reward coins
            FISH_COINS += new_leave_val
            update_coins()

            # reward XP
            XP += math.floor(new_leave_val / 2)
            update_XP()

            CM.cat_placer(WIN)

        check_new_level()

        # check the flag event
        if win_state == WindowState.HOME:
            if len(flag_event) > 0:
                level = flag_event[0]
                new_level_congratulations(level, CM.next_level_cat())
                flag_event.pop(0)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                save_changes()
                run = False
                pygame.quit()

            # if event.type == pygame.KEYDOWN:
            #     pass

        pygame.display.update()


if __name__ == "__main__":
    main()
