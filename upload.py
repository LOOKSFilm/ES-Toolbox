import os
import xml.etree.ElementTree as et
from tkinter import filedialog
import dearpygui.dearpygui as dpg
import boto3
import threading
import datetime
import json
from EditShareAPI import FlowMetadata

s3 = boto3.resource('s3')
bucket = s3.Bucket("s3-vtn-progress-editshare-or-1")
def selectFolder():
    global path
    path = filedialog.askdirectory()
    dpg.set_item_label(item="uploadFolderbtn", label=path)
    dpg.add_text(default_value="Loading files", parent="uploadconsole", tag="loadingmsg")
    for file in os.listdir(path):
        if file == "export.xml":
            filepath = f"{path}/export.xml" 
            tree = et.parse(filepath)
            root = tree.findall('clip')
            for xml in root:
                clipname = xml.find('clipname')
                proxyname = clipname.text+".xml"
                header = '<?xml version="1.0" encoding="UTF-8"?>\n<flow version="2">\n\t'
                header = str.encode(header)
                clip = et.tostring(xml, encoding='utf-8')
                closer = "</flow>"
                closer = str.encode(closer)
                newxml = header+clip+closer
                with open(f"{path}/{proxyname}", 'wb') as f:
                    f.write(newxml)
            os.remove(filepath)
    dpg.delete_item(item="loadingmsg")
    for file in sorted(os.listdir(path)):
        with dpg.table_row(parent="uploadTable", label=file, tag=file):
            dpg.add_text(default_value=file)

def uploadFiles():
    for file in sorted(os.listdir(path)):
        try:
            name, ftype = file.split(".")
        except ValueError:
            continue
        if ftype == "xml":
            tree = et.parse(f"{path}/{file}")
            customfields = tree.findall("clip/custom/customfield")
            for customfield in customfields:
                if customfield.attrib["id"] == "field_233":
                    assetid = customfield.text
        dpg.add_progress_bar(overlay=f"uploading {ftype}", parent=file, default_value=0, tag=f"prog{file}")
        filesize = os.path.getsize(f"{path}/{file}")
        bucket.upload_file(f"{path}/{file}", file, Callback=uploadStatus(filesize, file))
        uploadedpath = f"{path.split(':')[0]}:/uploaded"
        dpg.configure_item(item=f"prog{file}", overlay="Done")
        if file.endswith(".xml"):
            os.replace(f"{path}/{file}", f"{uploadedpath}/{file}")
        else:
            os.remove(f"{path}/{file}")
        try:
            x = datetime.datetime.now()
            date = f"{x.date()} {x.strftime('%X')}"
            data = dict()
            data["custom"] = dict()
            data["custom"]["field_58"] = True
            data["custom"]["field_237"] = date
            data = json.dumps(data)
            FlowMetadata.updateAsset(assetid, data)
        except:
            pass

def uploadStatus(filesize, file):
    bytesstatus = 0
    lock = threading.Lock()
    def call(bytes_amount):
        with lock:
            nonlocal bytesstatus
            bytesstatus += bytes_amount
            prog = bytesstatus / filesize
            dpg.configure_item(item=f"prog{file}", default_value=prog)
    return call

            
    #print(clips)
    # pairs = tuple()
    # uploadpkg = list()
    # for clip in clips[1]:
    #     name = dpg.get_item_alias(item=clip)
    #     for file in sorted(os.listdir(path)):
    #         if file.startswith(name):
    #             if file.endswith(".mp4"):
    #                 video = file
    #             else:
    #                 sidecar = file
    #     if not video:
    #         video = ""
    #     if not sidecar:
    #         sidecar = ""
    #     pairs = video, sidecar
    #     uploadpkg.append(pairs)
    


        #print(dpg.get_item_label(item=clip))
        #print(clip)
