import pygame
import os
import random

coors = [(120, 530), (344, 495), (563, 353), (798, 498)]
spot_descriptions = ["default_box_place", "foothill", "tophill", "downhill"]

class Spot:

    def __init__(self, id):
        self.id = id
        self.description = spot_descriptions[0]
        self.coor = coors[0]

        coors.pop(0)
        spot_descriptions.pop(0)
        # place_name_to_spot_object_link[self.description] = self

        # variable, not permanent
        self.cat_in_it = ""
        self.toy = ""
        self.is_filled = False  # this is indicating if it is filled by a CAT, not an item


class SpotManager:

    def __init__(self):
        self.spot1 = Spot(0)
        self.spot1.toy = "default box"

        self.spot2 = Spot(1)
        self.spot3 = Spot(2)
        self.spot4 = Spot(3)

        self.spots = [self.spot1, self.spot2, self.spot3, self.spot4]

        self.curr_items = ["default box"]
        self.unlocked_items = ["default box"]

    def get_num_open_spots(self) -> int:
        """returns a list of open spot_objects that a new cat can be placed"""
        num_of_open_spots = 0
        for spot in self.spots:
            if not spot.is_filled and spot.toy != "":
                num_of_open_spots += 1

        return num_of_open_spots



        # open_spots = []
        # for item in self.curr_items:
        #     # finding where the item is located
        #     place_name = self.curr_item_place_name_link[item]
        #     # finding the object at that location
        #     spot_object = place_name_to_spot_object_link[place_name]
        #     # if that object is not filled, append
        #     if not spot_object.is_filled:
        #         open_spots.append(spot_object)
        # return open_spots


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
id_to_xy = {
    0: (72, 450),
    1: (200, 400),
    2: (450, 450),
    3: (700, 450),
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
        self.xy = ()
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

        # to keep track of unlocked cats
        self.unlocked_cats = [self.johnny_cat]

        # to keep track of cats that the user has met
        self.cats_met = []

        # why need self.cats_met when we have self.unlocked_cats? Because a cat can be unlocked, but it might not have visited yet
        # in which case the cat should not show up in the cat book

        self.current_cats = []

        self.curr_time = 0

    def next_level_cat(self):
        if len(self.unlocked_cats) < 8:
            newly_unlocked_cat = self.all_cats[len(self.unlocked_cats)]
            self.unlocked_cats.append(newly_unlocked_cat)
            return newly_unlocked_cat.name
        else:
            return "no more cats"

    def leave_cat(self):
        profit = None
        ######################################## could just return zero, change profit = random.randint(0, 10) to profit = random.randint(1, 10)
        saved_current_cats = self.current_cats.copy()

        for cat in saved_current_cats:
            if self.curr_time - cat.birthday >= cat.stay_time:
                self.current_cats.remove(cat)
                cat.xy = ()
                cat.birthday = None
                cat.stay_time = None
                print("cat left")


                for spot_object in self.SM.spots:
                    if spot_object.cat_in_it == cat.name:
                        spot_object.cat_in_it = ""
                        spot_object.is_filled = False
                        break

                # the cat gives a tip
                profit = random.randint(200, 300) ######################################################################

        # if profit == None, then nothing changed, if it is zero to 80, then a cat left
        return profit

    def make_new_cat(self):
        """Creates a new random cat to show up randomly, decide where it will chill, decide when it leaves"""
        profit_XP = None

        if random.choices(COIN, weights=[1, 9])[0]:  # make sure the chances say yes
            if len(self.current_cats) < 4:  # make sure we aren't adding more cats than we can have
                if len(self.current_cats) != len(self.unlocked_cats):
                    # if all the unlocked cats came, there shouldn't be more coming
                    if self.SM.get_num_open_spots() > 0:  # if there are any open spots left

                        cat_chosen = False
                        while not cat_chosen:

                            new_cat = random.choice(self.unlocked_cats)
                            # new cat is a cat object

                            # if the cat is not already one of the cats meant to be on screen
                            if new_cat not in self.current_cats:

                                # assign the cat a place to chill
                                self.spot_chooser(new_cat)

                                # assign it its b-day
                                new_cat.birthday = self.curr_time

                                # if the user hasn't met the cat yet, put it now in their cat book
                                self.cats_met.append(new_cat) if new_cat not in self.cats_met else None

                                # add the cat to the self.current_cats
                                self.current_cats.append(new_cat)

                                # decide how long the cat will stay there, multiplying by 1000 bc pygame takes it in milliseconds
                                new_cat.stay_time = random.randint(10 * 1000, 40 * 1000)

                                # reset XP
                                profit_XP = cats_XP[new_cat.name]

                                print("New cat came")

                                cat_chosen = True
        return profit_XP

    def spot_chooser(self, new_cat):
        """Chooses a random place for a just-arrived-cat to chill, assigns it its coordinates"""
        # Note: it has always been previously checked in make_new_cat() that there will be an open spot
        spot_chose = False
        while not spot_chose:

            random.shuffle(self.SM.spots)

            for spot in self.SM.spots:    # iterate thru each spot to see...
                if spot.toy != "" and not spot.is_filled: # if there is a toy there and it is not occupied
                    spot.cat_in_it = new_cat.name
                    spot.is_filled = True

                    # we assign the coordinates, based on where the item is placed
                    new_cat.xy = spot.coor

                    spot_chose = True
                    break


            # new_item = random.choice(self.SM.curr_items)
            # # new_item is a string, the name of the item

            # place_name = self.SM.curr_item_place_name_link[new_item]  # we find the address of the item

            # # new_spot is a Spot object, here we find the spot where the description is
            # new_spot = place_name_to_spot_object_link[place_name]  # we find the acre of land that is there

            # # now that we have the spot, check if it is filled
            # if not new_spot.is_filled:
            #     new_spot.cat_in_it = new_cat.name

            #     new_spot.item_name = new_item
            #     new_spot.is_filled = True

            #     return new_item

    def cat_placer(self, screen):
        for cat in self.current_cats:
            x, y = cat.xy
            new_x = x - cat.image.get_width()/2
            new_y = y - cat.image.get_height()/2
            screen.blit(cat.image, (new_x, new_y))

        pygame.display.update()

    def add_item_to_inventory(self, item):
        # this is called by the "Yes", "No" buttons
        self.SM.unlocked_items.append(item)
        

    def insert_toy(self, spot_object_id: int, item: str):
        '''link a newly bought item to a spot object'''

        # STEP 1: identify the spot_object
        spot_object = None
        
        # find the spot with the id
        for spot in self.SM.spots:
            if spot.id == spot_object_id:
                spot_object = spot

        # STEP 2: place the item there, whether you have to replace something or not
        if spot_object.toy != "":
            # if there is, replace it, remove it from curr.items
            toy_to_replace = spot_object.toy

            self.SM.curr_items.remove(toy_to_replace)
            self.SM.curr_items.append(item)
            spot_object.toy = item

        else:
            # else just add the new item
            self.SM.curr_items.append(item)
            spot_object.toy = item

    def daximouse_present(self):
        for spot in self.SM.spots:
            if spot.toy == "Daximouse Chime":
                return True
        return False