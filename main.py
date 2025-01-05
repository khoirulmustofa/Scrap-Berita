import requests
from bs4 import BeautifulSoup

def scrape_article(url):
    try:
        # Mengirim permintaan GET ke URL
        response = requests.get(url)
        response.raise_for_status()  # Memastikan tidak ada kesalahan HTTP
        
        # Parsing konten HTML menggunakan BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Menentukan elemen artikel (sesuaikan sesuai struktur HTML situs target)
        title = soup.find('h1').get_text(strip=True) if soup.find('h1') else 'Judul tidak ditemukan'
        content = soup.find_all('p')  # Mengambil semua paragraf artikel

        # Menghapus elemen dengan kata-kata seperti "ADVERTISEMENT" atau "SCROLL TO CONTINUE"
        filtered_content = [
            paragraph.get_text(strip=True) 
            for paragraph in content 
            if "ADVERTISEMENT" not in paragraph.get_text(strip=True).upper() and
               "SCROLL TO CONTINUE" not in paragraph.get_text(strip=True).upper()
        ]

        # Menggabungkan paragraf ke dalam satu string
        article_content = '\n'.join(filtered_content) if filtered_content else 'Konten tidak ditemukan'
        
        return {
            "title": title,
            "content": article_content
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"Request error: {e}"}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}

# Meminta input URL dari pengguna
url = input("Masukkan URL artikel yang ingin di-scrape: ")

if url:
    article = scrape_article(url)

    if "error" in article:
        print("Terjadi kesalahan:", article["error"])
    else:
        print("\nJudul Artikel:", article["title"])
        
        # Simpan hasil ke dalam file hasil.txt
        with open("hasil.txt", "w", encoding="utf-8") as file:
            file.write(f"Hasilkan opsi judul yang menarik perhatian, deskripsi yang menawan, tag yang relevan, dan tagar yang menarik untuk serangkaian rangkuman video pendek berdasarkan artikel yang disediakan, yang dirancang untuk menarik minat pemirsa dan memikat mereka untuk menonton konten lengkapnya.\n\n")

            file.write(f"Judul Artikel:\n{article['title']}\n\n")
            file.write(f"Konten Artikel:\n{article['content']}\n")
        
        print("\nHasil scraping telah disimpan ke file 'hasil.txt'.")
else:
    print("URL tidak valid atau kosong!")
