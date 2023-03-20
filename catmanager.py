import pygame
import os
import random

coors = [(120, 530), (344, 495), (563, 353), (798, 498)]
spot_descriptions = ["default_box_place", "foothill", "tophill", "downhill"]

# it's going to look like    "default box": spot_object
place_name_to_spot_object_link = {}


def return_place_name_to_object_link():
    return place_name_to_spot_object_link


class Spot:

    def __init__(self):
        self.description = spot_descriptions[0]
        self.coor = coors[0]

        coors.pop(0)
        spot_descriptions.pop(0)
        place_name_to_spot_object_link[self.description] = self

        # variable, not permanent
        self.cat_in_it = ""
        self.item_name = ""  # semi-permanent
        self.is_filled = False  # this is indicating if it is filled by a CAT, not an item


class SpotManager:

    def __init__(self):
        self.spot1 = Spot()
        self.spot2 = Spot()
        self.spot3 = Spot()
        self.spot4 = Spot()

        self.spots = [self.spot1, self.spot2, self.spot3, self.spot4]

        # do we even need this list?
        self.curr_items = ["default box"]
        self.unlocked_items = ["default box"]

        self.curr_item_place_name_link = {
            "default box": "default_box_place"
        }

    def find_open_curr_spots(self):
        # open_spots will be a list of open spot_objects
        open_spots = []
        for item in self.curr_items:
            place_name = self.curr_item_place_name_link[item]
            spot_object = place_name_to_spot_object_link[place_name]
            if not spot_object.is_filled:
                open_spots.append(spot_object)
        return open_spots


pygame.transform.scale(pygame.image.load(os.path.join("Assets", "store_button.png")), (150, 100))
johnny_cat_image = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "johnny_cat.png")), (100, 100))
sarah_cat_image = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "sarah_cat.png")), (100, 100))
oscar_cat_image = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "oscar_cat.png")), (100, 100))
may_cat_image = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "may_cat.png")), (100, 100))
happy_cat_image = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "happy_cat.png")), (100, 150))
curious_cat_image = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "curious_cat.png")), (100, 100))
cool_cat_coby_image = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "cool_cat_coby.png")), (100, 100))
sus_cat_image = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "sus_cat.png")), (150, 120))


cats_XP = {

    "Johnny Cat": 5,
    "Sarah Cat": 10,
    "Oscar Cat": 20,
    "May Cat": 30,
    "Happy Cat": 45,
    "Curious Cat": 55,
    "Cool Cat Coby": 70,
    "Sus Cat": 100,

}

# we technically do not need the default box specification
location_name_to_xy = {
    "default box": (72, 450),
    "uphill": (200, 400),
    "foot_of_hill": (450, 450),
    "downhill": (700, 450),
}

# cat_names = ["Johnny Cat", "Sarah Cat", "Oscar Cat", "May Cat", "Happy Cat", "Curious Cat", "Cool Cat Coby", "Sus Cat"]
# cat_images = [johnny_cat_image, sarah_cat_image, oscar_cat_image, may_cat_image, happy_cat_image, curious_cat_image,
#               cool_cat_coby_image, sus_cat_image]


COIN = (True, False)


class Cat:

    def __init__(self, name, image):
        self.name = name
        self.image = image

        # not permanent
        self.xy = None
        self.item_at = None
        self.birthday = None
        self.stay_time = None


class CatManager:
    # the CatManager also handles drawing the items/toys onto the screen, their locations

    def __init__(self):
        self.SM = SpotManager()
        self.johnny_cat = Cat("Johnny Cat", johnny_cat_image)
        self.sarah_cat = Cat("Sarah Cat", sarah_cat_image)
        self.oscar_cat = Cat("Oscar Cat", oscar_cat_image)
        self.may_cat = Cat("May Cat", may_cat_image)
        self.happy_cat = Cat("Happy Cat", happy_cat_image)
        self.curious_cat = Cat("Curious Cat", curious_cat_image)
        self.cool_cat_coby = Cat("Cool Cat Coby", cool_cat_coby_image)
        self.sus_cat = Cat("Sus Cat", sus_cat_image)

        # total of 8 cats
        self.all_cats = [self.johnny_cat, self.sarah_cat, self.oscar_cat, self.may_cat, self.happy_cat,
                         self.curious_cat, self.cool_cat_coby, self.sus_cat]

        self.unlocked_cats = [self.johnny_cat]
        self.cats_met = []

        self.current_cats = []

        # self.counter = 0

    def next_level_cat(self):
        # print("we are trying to update level")
        if len(self.unlocked_cats) < 8:
            newly_unlocked_cat = self.all_cats[len(self.unlocked_cats)]
            self.unlocked_cats.append(newly_unlocked_cat)
            return newly_unlocked_cat.name
        else:
            return "no more cats"

    def leave_cat(self, curr_time):
        profit = None

        saved_current_cats = self.current_cats.copy()

        for cat in saved_current_cats:
            if curr_time - cat.birthday >= cat.stay_time:
                self.current_cats.remove(cat)
                cat.xy = None
                cat.item_at = None
                cat.birthday = None
                cat.stay_time = None

                for spot_object in self.SM.spots:
                    if spot_object.cat_in_it == cat.name:
                        spot_object.cat_in_it = None
                        # print("we reset spot_object.cat_in_it")
                        # we don't do anything to spot_object.item_name bc we don't change the item, just the cat in it
                        spot_object.is_filled = False
                        break

                # the cat pays money
                profit = 0
                profit += random.randint(0, 80)

        # if profit == None, then nothing changed, if it is zero to 80, then a cat left
        return profit

    def make_new_cat(self, time_passed_ms):
        profit_XP = None

        if random.choices(COIN, weights=[1, 90])[0]:  # make sure the chances say yes
            if len(self.current_cats) < 4:  # make sure we aren't adding more cats than we can have
                if len(self.current_cats) != len(self.unlocked_cats):
                    # if all the cats came, there shouldn't be more coming
                    if len(self.SM.find_open_curr_spots()) > 0:  # if there are any open spots left

                        cat_chosen = False
                        while not cat_chosen:
                            # print("...looking for a cat...")
                            new_cat = random.choice(self.unlocked_cats)
                            # new cat is a cat object

                            # print(f"unlocked cats = {self.unlocked_cats}\ncurrent cats {self.current_cats}")

                            # if the cat is not already one of the cats meant to be on screen
                            if new_cat not in self.current_cats:
                                # print("we have entered the cat making process")
                                # we assign it an item
                                new_cat.item_at = self.item_chooser(new_cat)

                                # we assign the coordinates, based on where the item is placed
                                for spot_object in self.SM.spots:
                                    if spot_object.item_name == new_cat.item_at:
                                        new_cat.xy = spot_object.coor

                                # assign it its b-day
                                new_cat.birthday = time_passed_ms

                                # if the user hasn't met the cat yet, put it now in their cat book
                                self.cats_met.append(new_cat) if new_cat not in self.cats_met else None

                                # add the cat to the self.current_cats
                                self.current_cats.append(new_cat)

                                # decide how long the cat will stay there, multiplying by 1000 bc pygame takes it in milliseconds
                                # is should be (30 * 1000, 1000 * 1000)
                                new_cat.stay_time = random.randint(5 * 1000, 10 * 1000)

                                # reset XP
                                profit_XP = cats_XP[new_cat.name]

                                cat_chosen = True
        return profit_XP

    def item_chooser(self, new_cat):

        item_chose = False
        while not item_chose:
            # print("looking for a new item")
            # print(f"curr items: {self.SM.curr_items}")
            new_item = random.choice(self.SM.curr_items)  # we find the building
            # new_item is a string, the name of the item

            place_name = self.SM.curr_item_place_name_link[new_item]  # we find the address
            # print(f"place name: {place_name}, new_item = {new_item}")

            # new_spot is a Spot object, here we find the spot where the description is
            new_spot = place_name_to_spot_object_link[place_name]  # we find the acre of land that is there

            # print(f"the spot.is_filled {new_spot.is_filled}")
            # now that we have the spot, check if it is filled
            if not new_spot.is_filled:
                new_spot.cat_in_it = new_cat.name
                # print(f"The name of the cat is {new_cat.name}")
                new_spot.item_name = new_item
                new_spot.is_filled = True

                return new_item

    def cat_placer(self, screen):
        # why do we even check curr_screen
        # if curr_screen == 1:
        # print("Here we place the cats")

        for cat in self.current_cats:
            x, y = cat.xy
            new_x = x - cat.image.get_width()/2
            new_y = y - cat.image.get_height()/2
            screen.blit(cat.image, (new_x, new_y))

        pygame.display.update()

    def add_item_to_inventory(self, item):
        # this is called by the "Yes", "No" buttons
        self.SM.unlocked_items.append(item)

    def already_a_toy(self, place_name: str) -> list:
        spot_object = place_name_to_spot_object_link[place_name]
        if spot_object.item_name == "":
            # if the string is empty, then there is no object in it
            return [False, spot_object]
        else:
            return [True, spot_object]

    def insert_toy(self, place_name: str, item: str):
        '''basically link a newly added item to a location'''

        # we have to check if that location already has something in it

        data_package = self.already_a_toy(place_name)
        spot_object = data_package[1]

        if data_package[0]:
            # if there is, replace it, remove it from curr.items
            toy_to_replace = spot_object.item_name

            self.SM.curr_items.remove(toy_to_replace)
            self.SM.curr_items.append(item)
            spot_object.item_name = item
            self.SM.curr_item_place_name_link[item] = self.SM.curr_item_place_name_link[toy_to_replace]
            del self.SM.curr_item_place_name_link[toy_to_replace]

        else:
            # else just add the new item
            self.SM.curr_items.append(item)
            spot_object.item_name = item
            self.SM.curr_item_place_name_link[item] = place_name
