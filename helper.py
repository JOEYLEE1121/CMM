from datetime import datetime
import pytz
from table2ascii import table2ascii, PresetStyle, Alignment

def timestamp():
    tz_HK = pytz.timezone('Asia/Hong_Kong') 
    dtnow_HK = datetime.now(tz_HK)
    dtnow_HK_str = dtnow_HK.strftime("%Y-%m-%d %H:%M:%S")
    return dtnow_HK_str


def ascii_table(items):
    output = table2ascii(
        body=[[key, str(items[key])] for key in items],
        first_col_heading=True,
        alignments=[Alignment.LEFT, Alignment.LEFT],
        style=PresetStyle.ascii_borderless,
    )
    return output
