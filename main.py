import requests
import gzip
import xml.etree.ElementTree as ET
from io import BytesIO

# Bugünlük senin verdiğin listeyi "indis" gibi kullanıyoruz
# Yarın bu liste yerine doğrudan M3U dosyanı okuyacağız
SEARCH_TERMS = [
    "TRT", "NOW", "KANAL D", "STAR", "ATV", "A2", "TV8", "TV 8", "TLC", "DMAX", "CNBC",
    "NTV", "CNN", "HABER TURK", "BEYAZ", "KANAL 7", "360", "TV 4", "TELE 1", "SZC",
    "HALK", "BLOOMBERG", "BEIN", "SPOR", "TIVIBU", "SINEMA TV", "SHOW", "EURO D",
    "DISCOVERY", "RTL", "PRO 7", "VOX", "SAT 1", "ZDF", "M6", "ALPHA", "SKAI", "MEGA"
]

def build_smart_epg():
    urls = [
        "https://epgshare01.online/epgshare01/epg_ripper_TR1.xml.gz",
        "https://epgshare01.online/epgshare01/epg_ripper_TR3.xml.gz",
        "https://epgshare01.online/epgshare01/epg_ripper_DE1.xml.gz"
    ]
    
    root_new = ET.Element("tv", {"generator-info-name": "GeminiSmartEPG-V1"})
    found_channels = set()

    for url in urls:
        print(f"📥 Kaynak taranıyor: {url}")
        try:
            resp = requests.get(url, timeout=30)
            with gzip.open(BytesIO(resp.content), 'rb') as f:
                root = ET.parse(f).getroot()

            # 1. Kanalları filtrele
            for channel in root.findall('channel'):
                display_name = ""
                dn_element = channel.find('display-name')
                if dn_element is not None:
                    display_name = dn_element.text or ""
                
                ch_id = channel.get('id')
                
                # Akıllı arama (Büyük/Küçük harf duyarsız)
                if any(term.upper() in display_name.upper() for term in SEARCH_TERMS) or \
                   any(term.lower() in ch_id.lower() for term in SEARCH_TERMS):
                    if ch_id not in found_channels:
                        root_new.append(channel)
                        found_channels.add(ch_id)

            # 2. Programları ekle
            for prog in root.findall('programme'):
                if prog.get('channel') in found_channels:
                    root_new.append(prog)
        except Exception as e:
            print(f"⚠️ {url} hatası: {e}")

    # Dosyayı kaydet
    ET.ElementTree(root_new).write("epg.xml", encoding="utf-8", xml_declaration=True)
    print(f"\n✨ İşlem Başarılı! {len(found_channels)} kanal için hafifletilmiş EPG oluşturuldu.")

if __name__ == "__main__":
    build_smart_epg()
