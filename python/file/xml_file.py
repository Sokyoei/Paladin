from xml.dom import minidom
from xml.etree import ElementTree as ET

from Ahri.Paladin import SOKYOEI_DATA_DIR

xml_file_path = str(SOKYOEI_DATA_DIR / "Ahri/Ahri.xml")

########################################################################################################################
# xml.dom
########################################################################################################################
Ahri_Skins = minidom.parse(xml_file_path).documentElement
print(Ahri_Skins)
for skin in Ahri_Skins.childNodes:
    if skin.nodeType == minidom.Node.ELEMENT_NODE:
        print(skin.nodeName)

########################################################################################################################
# xml.etree
########################################################################################################################
Ahri_Skins = ET.parse(xml_file_path).getroot()
print(Ahri_Skins.tag)
# for skin in Ahri_Skins:
#     print(skin)

########################################################################################################################
# xml.sax
########################################################################################################################
