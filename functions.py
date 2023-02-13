import json
import dearpygui.dearpygui as dpg
from EditShareAPI import FlowMetadata

def pretty(input):
    pjson = json.dumps(input, indent=4, sort_keys=True)
    return pjson

def cprint(message, color):
    if color == "red":
        color = (245, 87, 66)
    if color == "yellow":
        color = (247, 225, 111)
    if color == "green":
        color = (66, 245, 155)
    
    dpg.add_text(default_value=message, parent='console', tracked=True, track_offset=1.0, color=color)

def ctabprint(mapto, val, res):
    with dpg.group(track_offset=1.0, tracked=True, parent='console'):
        with dpg.table(header_row=False):
            dpg.add_table_column(width_fixed=True, width=0)
            dpg.add_table_column(width_fixed=True, width=0)
            dpg.add_table_column(width_stretch=True, width=0)
            with dpg.table_row():
                dpg.add_text(default_value=str(mapto)+': ', color=(66, 191, 245))
                dpg.add_text(default_value=str(val), color=(215, 215, 215))
                if res == '"OK"':
                    dpg.add_text(default_value=' '+str(res), color=(66, 245, 155))
                else:
                    dpg.add_text(default_value=' '+str(res), color=(245, 87, 66))
    consoleitems = dpg.get_item_children(item="console")
    if len(consoleitems[1]) > 300:
        dpg.delete_item(item=consoleitems[1][0])

def mapfield(esfield, sfield, esassetid):
    data = {
            "custom": {
                esfield: sfield
            }
    }
    asset = FlowMetadata.updateAsset(esassetid, data)
    #print(esfield, sfield, asset.text)