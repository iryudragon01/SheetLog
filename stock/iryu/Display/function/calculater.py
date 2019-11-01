
def volume_sale(item,start,end):
    if item.type == 1:
        return end-start
    elif item.type == 2:
        return end
    else:
        return start-end

def item_money(item,start,end):
    return item.price*volume_sale(item,start,end)