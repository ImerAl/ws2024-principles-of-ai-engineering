import random as r
from datetime import datetime
def generate_id(i):
    now = datetime.now()

    year = now.year
    month = now.month
    day = now.day
    number = r.randint(0, 9999)
    id = f'{year}{month}{day}{number}{i}'
    return int(id)
