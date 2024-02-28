import numpy as np
import pandas as pd   
from IPython.display import display_html 

def display_side_by_side(*args):
    html_str = ''
    for df, caption in args:
        df_styler = df.head().style.set_table_attributes("style='display:inline'").set_caption(caption)
        html_str += df_styler._repr_html_()
    
    display_html(html_str, raw=True)