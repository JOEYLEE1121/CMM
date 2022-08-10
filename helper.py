from table2ascii import table2ascii, PresetStyle, Alignment

def ascii_table(items):
    output = table2ascii(
        body=[[key, str(items[key])] for key in items],
        first_col_heading=True,
        alignments=[Alignment.LEFT, Alignment.LEFT],
        style=PresetStyle.ascii_borderless,
    )
    return output

