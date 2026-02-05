import requests
import gzip
import xml.etree.ElementTree as ET
from io import BytesIO

def download_and_parse(url):
    print(f"📥 İndiriliyor: {url}")
    try:
        response = requests.get(url, timeout=30)
        # Gzip sıkıştırılmış dosyayı açıyoruz
        with gzip.open(BytesIO(response.content), 'rb') as f:
            xml_content = f.read()
        return ET.fromstring(xml_content)
    except Exception as e:
        print(f"❌ Hata oluştu ({url}): {e}")
        return None

def build_mega_epg():
    urls = [
        "https://epgshare01.online/epgshare01/epg_ripper_TR1.xml.gz",
        "https://epgshare01.online/epgshare01/epg_ripper_TR3.xml.gz",
        "https://epgshare01.online/epgshare01/epg_ripper_DE1.xml.gz"
    ]
    
    # Ana XML yapısını kuruyoruz
    root_new = ET.Element("tv")
    channels_added = set()
    program_count = 0

    for url in urls:
        root_data = download_and_parse(url)
        if root_data is None: continue

        # Önce kanalları (channel) ekleyelim (kopya olmasın diye kontrol ederek)
        for channel in root_data.findall('channel'):
            ch_id = channel.get('id')
            if ch_id not in channels_added:
                root_new.append(channel)
                channels_added.add(ch_id)

        # Sonra programları (programme) ekleyelim
        for programme in root_data.findall('programme'):
            root_new.append(programme)
            program_count += 1

    # Dosyayı kaydet
    tree = ET.ElementTree(root_new)
    tree.write("epg.xml", encoding="utf-8", xml_declaration=True)
    print(f"\n✅ İşlem Tamamlandı!")
    print(f"📡 Toplam Kanal: {len(channels_added)}")
    print(f"📺 Toplam Program: {program_count}")

if __name__ == "__main__":
    build_mega_epg()
