
import DeletedItem
import Item
from MyDatabase import *

def init_all_tables():
    db.connect();
    db.create_tables([Item.Item, DeletedItem.DeletedItem], safe=True);
    Item.all_items = Item.Item.select();
    DeletedItem.all_deleted_items = DeletedItem.DeletedItem.select();

