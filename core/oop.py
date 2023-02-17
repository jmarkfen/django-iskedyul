from .models import Block

class Cell:

    def __init__(self, text='', tags=[]):
        self.text = text
        self.tags = tags

def blocks_by_day(set_id):
    blocks = Block.objects.filter(set=set_id)
    by_days = {
        'Mon': [], 
        'Tue': [], 
        'Wed': [], 
        'Thu': [], 
        'Fri': [], 
        'Sat': [], 
        'Sun': [], 
        }
    for block in blocks:
        by_days[block.day].append(block)
    return by_days

# group 
def to_time_rows(blocks: Block):
    pass

