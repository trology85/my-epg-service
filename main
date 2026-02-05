import requests
from datetime import datetime
import xml.etree.ElementTree as ET

def get_trt2_epg():
    # TRT'nin resmi yayın akışı API adresi (Örnektir, stabil uç kullanılır)
    # Bu adres doğrudan JSON veri döndürür, site kazımaz.
    api_url = "https://api-izle.trt.net.tr/v1/broadcast/trt-2/daily" 
    
    try:
        response = requests.get(api_url, timeout=10)
        data = response.json()
        
        program_list = []
        
        # Gelen JSON içindeki her bir programı döngüye alıyoruz
        for item in data.get('items', []):
            title = item.get('title')
            description = item.get('description', 'Detay bulunamadı.')
            start_time = item.get('startDate') # Örn: 2026-02-06T12:00:00Z
            end_time = item.get('endDate')
            
            # Zaman formatını XMLTV standartına (+0300) çevirme işlemi
            # Örn: 20260206120000 +0300
            st = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y%m%d%H%M%S") + " +0300"
            et = datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y%m%d%H%M%S") + " +0300"
            
            # XML bloğunu oluşturma
            prog_xml = f"""  <programme start="{st}" stop="{et}" channel="trt2.hd.tr">
    <title lang="tr">{title}</title>
    <desc lang="tr">{description}</desc>
  </programme>"""
            program_list.append(prog_xml)
            
        return "\n".join(program_list)
    except Exception as e:
        print(f"TRT 2 Verisi çekilemedi: {e}")
        return ""

# Ana XML Taslağı
def build_xml():
    xml_header = '<?xml version="1.0" encoding="UTF-8"?>\n<tv>\n  <channel id="trt2.hd.tr">\n    <display-name>TRT 2</display-name>\n  </channel>\n'
    content = get_trt2_epg()
    xml_footer = "\n</tv>"
    
    with open("epg.xml", "w", encoding="utf-8") as f:
        f.write(xml_header + content + xml_footer)
    print("epg.xml başarıyla oluşturuldu!")

if __name__ == "__main__":
    build_xml()
