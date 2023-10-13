import json
from catmanager import CatManager

class CMEncoder(json.JSONEncoder):
    
    def encode(self, CMObject):
        if isinstance(CMObject, CatManager):
            return {
                "unlocked_cats": [cat.name for cat in CMObject.unlocked_cats], # list of cat objects, JSON sterilize
                "current cats": {spot_object.id: spot_object.cat_in_it for spot_object in CMObject.SM.spots},
                "cats met": [cat.name for cat in CMObject.cats_met], # list of cat objects, JSON sterilize
                "items on set": CMObject.SM.curr_items,  # list of strings
                "bought items": CMObject.SM.unlocked_items,       # list of strings
                "spots with their items": {spot_object.id: spot_object.toy for spot_object in CMObject.SM.spots},
                "spots with their cats": {spot_object.id: spot_object.cat_in_it for spot_object in CMObject.SM.spots},
                "cats with their times": {cat_object.name: CMObject.curr_time - cat_object.birthday for cat_object in CMObject.current_cats},
                                                            # this will essentially give stay_time
            }
        return super().default(CMObject)
