
import DeleteItem
import Item
from MyDatabase import *

def init_all_tables():
    db.connect();
    db.create_tables([Item.Item, DeleteItem.DeletedItem], safe=True);
    Item.all_items = Item.Item.select();
    DeleteItem.all_deleted_items = DeleteItem.DeletedItem.select();

