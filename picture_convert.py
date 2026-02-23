import base64

# Dönüştürülecek dosyaların listesi
files = [
    {
        "variable_name": "background_img",
        "path": r"C:/Users/Emine/Desktop/CF/wallpaperflare.com_wallpaper.jpg"
    },
    {
        "variable_name": "background_img2",
        "path": r"C:/Users/Emine/Desktop/CF/wallhaven-qr2zq7_3840x2160.png"
    },
    {
        "variable_name": "background_img3",
        "path": r"C:/Users/Emine/Desktop/CF/wallpaperflare.com_wallpaper (3).jpg"
    },
    {
        "variable_name": "pdf_icon_img",
        "path": r"C:/Users/Emine/Desktop/CF/PDF_file_icon.svg.png"
    }
]

output_file = "resources.py"

with open(output_file, "w", encoding="utf-8") as f:
    f.write("# Bu dosya otomatik oluşturulmuştur. Resimlerin Base64 hallerini içerir.\n\n")
    
    for item in files:
        try:
            with open(item["path"], "rb") as image_file:
                # Resmi oku ve base64'e çevir
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                
                # Dosyaya yaz
                f.write(f'{item["variable_name"]} = b"""{encoded_string}"""\n\n')
                print(f"{item['path']} başarıyla dönüştürüldü.")
        except FileNotFoundError:
            print(f"HATA: Dosya bulunamadı -> {item['path']}")
            f.write(f'{item["variable_name"]} = b"" # Dosya bulunamadı\n\n')

print(f"\nİşlem tamamlandı! '{output_file}' dosyası oluşturuldu.")