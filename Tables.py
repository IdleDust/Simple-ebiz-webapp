
import DeletedItem
import Item
from MyDatabase import *

# ---------------------
# ---for test only use with caution---
# ---------------------
def drop_all_tables():
    db.drop_tables([Item.Item, DeletedItem.DeletedItem]);


def init_all_tables():
    db.connect();
    db.create_tables([Item.Item, DeletedItem.DeletedItem], safe=True);
    # drop_all_tables();
    Item.all_items = Item.Item.select();
    count = 0;
    for i in Item.all_items:
    	count = count + 1;
    print("Item表格共有行数：");
    print (count);
    
    q = Item.Item.update(buyer="4k").where(Item.Item.buyer == "李旭");
    q.execute();

    DeletedItem.all_deleted_items = DeletedItem.DeletedItem.select();

