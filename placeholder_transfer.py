from EditShareAPI import FlowMetadata
import dearpygui.dearpygui as dpg
import functions
import json
import time
import upload
import threading
import datetime


def transferdata():
    idinput = dpg.get_value("inputID")
    #Check if input is Empty
    if idinput == "":
        functions.cprint('Enter ID: Single value "DEFA00001" or multiple values comma seperated "DEFA00001,DEFA00002,DEFA00003,..."', "red")
    else:
        #Make list of Input, needed for multiple Values
        ids = idinput.split(",")
        for id in ids:
            #remove spaces if entry was something like: "DEFA00001, DEFA00002,  DEFA00004"
            id = id.replace(" ", "")
            #block for search request: Mediaspace: Progress Placeholder, field_50 (001 identifier) equals ID
            data = {
                    "combine": "MATCH_ALL",
                    "filters": [
                        {
                            "field": {
                                "fixed_field": "MEDIA_SPACES_NAMES",
                                "group": "SEARCH_FILES"
                            },
                            "match": "EQUAL_TO",
                            "search": "Progress Placeholder"
                        },
                        {
                            "field": {
                                "custom_field": "field_50",
                                "fixed_field": "CUSTOM_field_50",
                                "group": "SEARCH_ASSETS"
                            },
                            "match": "EQUAL_TO",
                            "search": id
                        } 
                    ]
                }
            data = json.dumps(data)
            functions.cprint("Searching for Placeholder...", "yellow")
            psearch = FlowMetadata.searchAdvanced(data)
            #Check if search found Placeholder, if not search for Existing Clip on Einspiel Spaces, else stop
            placeholder = True
            if len(psearch) == 0:
                placeholder = False
                functions.cprint('There is no Placeholder with this ID: "'+id+'"', "red")
                functions.cprint("Searching for existing Clip...", "yellow")
                data = {
                    "combine": "MATCH_ALL",
                    "filters": [
                        {
                            "field": {
                                "fixed_field": "MEDIA_SPACES_NAMES",
                                "group": "SEARCH_FILES"
                            },
                            "match": "CONTAINS",
                            "search": "Progress Einspiel",
                        },
                        {
                            "field": {
                                "custom_field": "field_50",
                                "fixed_field": "CUSTOM_field_50",
                                "group": "SEARCH_ASSETS"
                            },
                            "match": "EQUAL_TO",
                            "search": id
                        },
                        {
                            "field": {
                                "custom_field": "field_242",
                                "fixed_field": "CUSTOM_field_242",
                                "group": "SEARCH_ASSETS"
                            },
                            "match": "EQUAL_TO",
                            "search": True
                        }
                    ]
                }
                data = json.dumps(data)
                psearch = FlowMetadata.searchAdvanced(data)
                if len(psearch) == 0:
                   functions.cprint('There is no Clip with this ID: "'+id+'"', "red")
                   functions.cprint("-----------------------------------------------------------------------------------------------------", "green")
                   break
            clipdata = FlowMetadata.getClipData(psearch[0]["clip_id"])
            #grab metadata and clipname
            
            metadata = clipdata.asset["custom"]
            try:
               del metadata["field_58"]
            except:
                pass
            try:
               del metadata["field_237"]
            except:
                pass
            try:
               del metadata["field_86"]
            except:
                pass
            try:
               del metadata["field_87"]
            except:
                pass
            try:
               del metadata["field_88"]
            except:
                pass 
            try:
               del metadata["field_89"]
            except:
                pass
            try:
               del metadata["field_90"]
            except:
                pass 
            try:
               del metadata["field_238"]
            except:
                pass 
            try:
               del metadata["field_239"]
            except:
                pass
            try:
               del metadata["field_241"]
            except:
                pass
            try:
               del metadata["field_92"]
            except:
                pass     
            #get Placeholder clipname ("new" clipname) to rename the Asset
            placeholdername = clipdata.display_name
            functions.cprint("Grabbing metadata...", "yellow")
            #block for search request: Mediaspace: Progress Einspiel 2020, 001 Identifier == id
            data = {
                    "combine": "MATCH_ALL",
                    "filters": [
                        {
                            "field": {
                                "fixed_field": "MEDIA_SPACES_NAMES",
                                "group": "SEARCH_FILES"
                            },
                            "match": "CONTAINS",
                            "search": "Progress Einspiel"
                        },
                        {
                            "field": {
                                "custom_field": "field_50",
                                "fixed_field": "CUSTOM_field_50",
                                "group": "SEARCH_ASSETS"
                            },
                            "match": "CONTAINS",
                            "search": id
                        } 
                    ]
                }
            data = json.dumps(data)
            functions.cprint("Searching for Clip...", "yellow")
            asearch = FlowMetadata.searchAdvanced(data)
            #iterate through search results([{"clip_id": 000000}])
            for clip in asearch:
                clipid = clip["clip_id"]
                #EditShareAPI call: return Clipdata
                clipdata = FlowMetadata.getClipData(clipid)
                #get assetid, needed for update Metadata & Metadatafield entry
                assetid = clipdata.asset["asset_id"]
                identifier = clipdata.asset["custom"]["field_50"]
                #get captureid, uuid for metadatafield entry
                captureid = clipdata.capture["capture_id"]
                uuid = clipdata.asset['uuid']
                #get "old" display_name for namechange msg
                oldclipname = clipdata.display_name
                #get metadata_id for namechange api call
                metadataid = clipdata.metadata["metadata_id"]
                functions.cprint("Copy metadata to "+oldclipname+"...", "yellow")
                #create dictionary for updating assets metadata
                data = dict()
                data["custom"] = metadata
                data["custom"]["field_50"] = identifier
                data["custom"]["field_51"] = True
                data["custom"]["field_231"] = clipid
                data["custom"]["field_233"] = assetid
                data["custom"]["field_235"] = captureid
                data["custom"]["field_127"] = uuid
                data["custom"]["field_242"] = True
                #set modified date
                x = datetime.datetime.now()
                date = f"{x.date()} {x.strftime('%X')}"
                data["custom"]["field_60"] = date
                #set user
                from login import user
                data["custom"]["field_62"] = user
                #digitised true
                data["custom"]["field_91"] = True
                #dict to json
                data = json.dumps(data)
                #apicall to update the metadata
                r = FlowMetadata.updateAsset(assetid, data)
                functions.cprint("Copied Metadata: "+r.text, "green")
                time.sleep(2)
                if placeholder:
                    splitidentifier = identifier.split("_")
                    placeholdername = placeholdername.replace(splitidentifier[0], "")
                    placeholdername = placeholdername.replace(":", "").replace("\\", "-").replace("/", "-").replace(";","").replace(",", "").replace(".", "").replace("?","").replace("!","").replace("ß","sz").replace("ä","ae").replace("ü","ue").replace("ö","oe").replace("'","").replace('"',"")
                    clipname = identifier+placeholdername
                else:
                    try:
                        title = metadata["field_63"]
                    except KeyError:
                        try:
                            title = metadata["field_64"]
                        except KeyError:
                            try:
                                title = metadata["field_65"]
                            except KeyError:
                                try:
                                    title = metadata["field_66"]
                                except KeyError:
                                    try:
                                        title = metadata["field_67"]
                                    except KeyError:
                                        functions.cprint("No Title found.", "red")
                    title = title.replace(":", "").replace("\\", "-").replace("/", "-").replace(";","").replace(",", "").replace(".", "").replace("?","").replace("!","").replace("ß","sz").replace("ä","ae").replace("ü","ue").replace("ö","oe").replace("'","").replace('"',"")
                    clipname = identifier+"__"+title
                data = {
                        "clip_name": clipname
                        }
                data = json.dumps(data)
                #api call to update metadata
                r = FlowMetadata.updateMetadata(metadataid, data)
                functions.cprint("Renamed Clip to "+clipname+": "+r, "green")
                functions.cprint("-----------------------------------------------------------------------------------------------------", "green")
#UI
def main():
    dpg.set_viewport_resizable(True)
    with dpg.window(tag='mainwindow', no_scrollbar=True, menubar=True) as mainwindow:
        dpg.set_primary_window('mainwindow', True)
        with dpg.tab_bar():
            with dpg.tab(label = "Placeholder"):
                dpg.add_input_text(use_internal_label=True, on_enter=True, tag="inputID", callback=transferdata, hint='Input:"DEFA00001" or "DEFA00001,DEFA00002,DEFA00003"')
                dpg.add_button(label="Transfer Metadata", callback=transferdata)
                dpg.add_child_window(label='Console', tag='console')
            with dpg.tab(label = "Upload"):
                dpg.add_button(label="Select upload Folder", callback=upload.selectFolder, tag="uploadFolderbtn")
                uploadProcess = threading.Thread(target=upload.uploadFiles)
                dpg.add_button(label="Upload", callback=uploadProcess.start)
                with dpg.child_window(tag="uploadconsole"):
                    with dpg.table(tag="uploadTable"): 
                        dpg.add_table_column(label="Clip", width_stretch=True)
                        dpg.add_table_column(label="Status", width_stretch=True)
                        #dpg.add_child_window(label='Console', tag='uploadconsole')
    #MENUBAR
    with dpg.menu_bar(parent='mainwindow'):            
        with dpg.menu(label='File', tag='filemenu'):
            dpg.add_menu_item(label='Exit', callback=lambda: dpg.stop_dearpygui())
        with dpg.menu(label='Window', tag='windowmenu'):
            dpg.add_menu_item(label='toggle Fullscreen', callback=lambda: dpg.toggle_viewport_fullscreen())
        with dpg.menu(label='Help', tag='helpmenu'):
            # dpg.add_menu_item(label='Dearpy Commands', callback=lambda: dpg.show_documentation())
            # dpg.add_menu_item(label='Style Editor', callback=lambda: dpg.show_style_editor())
            # dpg.add_menu_item(label='Logs', callback=help)
            with dpg.menu(label='Version', tag='version'):
                dpg.add_text(default_value="v0.27 2023-01-11")