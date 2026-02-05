import requests
from datetime import datetime
import xml.etree.ElementTree as ET

def get_epg_data(api_url, channel_id, channel_display_name):
    try:
        response = requests.get(api_url, timeout=15)
        data = response.json()
        
        program_list = []
        # TRT ve CNBC-e API yapıları benzerse bu döngü çalışır
        # Değilse her kanal için küçük modifiyeler yaparız
        items = data.get('items', [])
        
        for item in items:
            title = item.get('title', 'Belirsiz Program')
            description = item.get('description', 'Açıklama bulunamadı.')
            start_time = item.get('startDate')
            end_time = item.get('endDate')
            
            if start_time and end_time:
                st = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y%m%d%H%M%S") + " +0300"
                et = datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y%m%d%H%M%S") + " +0300"
                
                prog_xml = f"""  <programme start="{st}" stop="{et}" channel="{channel_id}">
    <title lang="tr">{title}</title>
    <desc lang="tr">{description}</desc>
  </programme>"""
                program_list.append(prog_xml)
            
        print(f"✅ {channel_display_name}: {len(program_list)} program çekildi.")
        return program_list
    except Exception as e:
        print(f"❌ {channel_display_name} hatası: {e}")
        return []

def build_xml():
    # Kanal Tanımlamaları
    channels = [
        {"id": "trt2.hd.tr", "name": "TRT 2", "url": "https://api-izle.trt.net.tr/v1/broadcast/trt-2/daily"},
        {"id": "cnbce.hd.tr", "name": "CNBC-E", "url": "https://api-izle.trt.net.tr/v1/broadcast/cnbc-e/daily"} 
        # Not: CNBC-e için TRT altyapısı örnektir, gerekirse URL'i güncelleyeceğiz.
    ]
    
    xml_header = '<?xml version="1.0" encoding="UTF-8"?>\n<tv>\n'
    
    # Kanal başlıklarını oluştur
    for ch in channels:
        xml_header += f'  <channel id="{ch["id"]}">\n    <display-name>{ch["name"]}</display-name>\n  </channel>\n'
    
    # Programları topla
    all_programs = []
    for ch in channels:
        all_programs.extend(get_epg_data(ch["url"], ch["id"], ch["name"]))
    
    xml_footer = "\n</tv>"
    
    with open("epg.xml", "w", encoding="utf-8") as f:
        f.write(xml_header + "\n".join(all_programs) + xml_footer)
    
    print(f"\n🚀 Toplam {len(all_programs)} yayın akışı epg.xml dosyasına kaydedildi!")

if __name__ == "__main__":
    build_xml()
