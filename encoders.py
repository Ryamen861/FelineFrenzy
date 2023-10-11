import json
from catmanager import CatManager

class CMEncoder(json.JSONEncoder):
    
    def encode(self, CMObject):
        if isinstance(CMObject, CatManager):
            return {
                "unlocked_cats": [cat.name for cat in CMObject.unlocked_cats], # list of cat objects, JSON sterilize
                "cats met": [cat.name for cat in CMObject.cats_met], # list of cat objects, JSON sterilize
                "items on set": CMObject.SM.curr_items,  # list of strings
                "bought items": CMObject.SM.unlocked_items,       # list of strings
                "c_item_to_p_name_link": CMObject.SM.curr_item_place_name_link,            # dict of string: string

            }
        return super().default(CMObject)

    def encodeSpotDict(self, dictionary):
        return {k: spotObject.id for k, spotObject in dictionary.items()}