import xml.etree.ElementTree as ET
from .models import IpcModelSymbol


def read_xml_file(file):
    tree = ET.parse(file)
    root = tree.getroot()

    namespace = {'ipc': 'http://www.wipo.int/classifications/ipc/masterfiles'}

    ipc_entries = root.findall('.//ipc:ipcEntry', namespace)
    bulk_data = []
    data = 0
    for ipc_entry in ipc_entries:
        # data += 1
        # kind = ipc_entry.get('kind')
        symbol = ipc_entry.get('symbol')
        edition = ipc_entry.get('edition')
        entry_type = ipc_entry.get('entryType')
        # Use find method to get the child element
        text_body3 = ipc_entry.find(".//ipc:textBody", namespace)
        text_body = text_body3.findall(".//ipc:text", namespace)
        entry_reference = text_body3.findall(".//ipc:entryReference", namespace)
        referncee = text_body3.findall(".//ipc:references", namespace)


        text = []
        entery_text = []
        for i in text_body:
           
            text.append(i.text)

        for j in entry_reference:
          
            sref = j.find(".//ipc:sref", namespace)
           
            if sref is not None and "ref" in sref.attrib:
                entery_text.append(sref.attrib["ref"])  # Append "@ref" value
            
            text.append(j.text)  # Append "#text" value

        for k in referncee:
            sref = k.find(".//ipc:sref", namespace)
            # print(sref,'----------------------------')
            # print(sref.attrib,'----------------------------')
            if sref is not None and "@ref" in sref.attrib:
                entery_text.append(sref.attrib["@ref"])  # Append "@ref" value
            text.append(k.text)


        ipc_data = {
                'edition': edition,
                'symbol': symbol,
                'text_body': text,
                'ref':entery_text
            }
        # print('#----#')
        # print(ipc_data)

        ipc_instance = IpcModelSymbol(**ipc_data)
        bulk_data.append(ipc_instance)
            # Bulk create the instances

        # if data == 50:
        #     break
        # print(data)
    # print(text)
    # IpcModelSymbol.objects.bulk_create(bulk_data)

