import unittest

from dotmng.config  import cfg
from dotmng.modules import DataBase


db = DataBase(cfg.DB_PATH)

def get_cat(category: str=None, parent: int=None):
    cat_id = db.get_categories_app(category=category, parent_id=parent)
    return cat_id

def set_cat(category: str, parent: int=None):
    cat_id = db.set_categories(category=category, parent_id=parent)
    return cat_id

def del_cat(category: str=None, parent: int=None):
    cat = db.del_categories(category=category, parent_id=parent)
    return cat


class TestCat(unittest.TestCase):
    data = {
        'category': 'TestCat',
        'subcategory': 'TestSubCat'
    }

    def testCategory(self):
        id_cat = set_cat(self.data["category"])
        self.assertIsNotNone(id_cat)

        main_cat = {"id_cat": id_cat, "category": self.data["category"], "parent_id": None}
        self.assertEqual(get_cat(self.data["category"]), main_cat)

        id_subcat = set_cat(self.data["subcategory"], parent=id_cat)
        self.assertIsNotNone(id_subcat)

        sub_cat = {"id_cat": id_subcat, "category": self.data["subcategory"], "parent_id": id_cat}
        self.assertEqual(get_cat(self.data["subcategory"], parent=id_cat), sub_cat)

        self.assertIsNone(del_cat(parent=id_subcat))
        self.assertIsNone(get_cat(self.data["subcategory"]))

        self.assertIsNone(del_cat(self.data["category"]))
        self.assertIsNone(get_cat(self.data["category"]))


if __name__ == "__main__":
    unittest.main()