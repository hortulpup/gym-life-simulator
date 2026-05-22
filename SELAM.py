import pygame
import sys
import os
import random

# system 
pygame.init()
GENISLIK, YUKSEKLIK = 1000, 750
ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Gym Life Simulator: Ultra Grafik Edition")
clock = pygame.time.Clock()

# Renkler
BEYAZ, SIYAH, YESIL = (255, 255, 255), (0, 0, 0), (0, 255, 0)
KIRMIZI, MAVI, GRI = (255, 50, 50), (0, 128, 255), (40, 40, 40)
ALTIN, TURUNCU = (255, 215, 0), (255, 165, 0)
ACIK_MAVI = (100, 100, 255)

# fonts here
font_hud = pygame.font.SysFont("Consolas", 18, bold=True)
font_mesaj = pygame.font.SysFont("Arial", 22, bold=True)
font_ipucu = pygame.font.SysFont("Arial", 16, bold=True)
font_bitis = pygame.font.SysFont("Impact", 60)

# uploading photos here
def resim_yukle(dosya_adi, ebat, yedek_renk):
    if os.path.exists(dosya_adi):
        resim = pygame.image.load(dosya_adi).convert_alpha()
        return pygame.transform.scale(resim, ebat)
    else:
        yuzey = pygame.Surface(ebat)
        yuzey.fill(yedek_renk)
        return yuzey

# all photos here

img_yatak_ortopedik = resim_yukle("yatak_ortopedik.png", (160, 100), (80, 80, 200))
img_pc = resim_yukle("pc.png", (80, 80), ACIK_MAVI)
img_ayakkabi = resim_yukle("ayakkabi.png", (100, 100), YESIL)
img_kemer = resim_yukle("kemer.png", (100, 100), GRI)
bg_ev = resim_yukle("ev_arka_plan.jpg", (GENISLIK, YUKSEKLIK), (60, 30, 30))
bg_cadde = resim_yukle("cadde_arka_plan.jfif", (GENISLIK, YUKSEKLIK), (50, 50, 50))
bg_gym = resim_yukle("gym_arka_plan.jfif", (GENISLIK, YUKSEKLIK), (20, 20, 20))
bg_market = resim_yukle("market_arka_plan.jpg", (GENISLIK, YUKSEKLIK), (180, 180, 140))

img_oyuncu = resim_yukle("oyuncu.png", (60, 60), MAVI)
img_oyuncu_yeni = resim_yukle("oyuncu_kasli.png", (60, 60), YESIL) 

img_yatak = resim_yukle("yatak.jfif", (160, 100), (30, 30, 150))
img_yatak_ortopedik = resim_yukle("yatak_ortopedik.png", (160, 100), (80, 80, 200)) # YENİ
img_dolap = resim_yukle("dolap.png", (100, 150), GRI)
img_pc = resim_yukle("pc.png", (80, 80), ACIK_MAVI) # YENİ EŞYA
img_kapi = resim_yukle("kapi.png", (20, 200), SIYAH)
img_kapi_yatay = resim_yukle("kapi_yatay.png", (100, 20), SIYAH)

img_dis_ev = resim_yukle("dis_ev.jpg", (120, 300), (80, 40, 40)) 
img_dis_gym = resim_yukle("dis_gym.jpg", (120, 300), (40, 40, 80))
img_dis_market = resim_yukle("dis_market.jfif", (240, 120), (40, 80, 40))

img_lat = resim_yukle("lat_pulldown.png", (80, 80), KIRMIZI)
img_bench = resim_yukle("bench_press.png", (80, 80), KIRMIZI)
img_leg = resim_yukle("leg_press.png", (80, 80), KIRMIZI)
img_biceps = resim_yukle("biceps_curl.png", (80, 80), KIRMIZI)
img_kosu = resim_yukle("kosu_bandi.png", (120, 60), KIRMIZI)
img_squat = resim_yukle("squat_rack.png", (100, 100), KIRMIZI)

img_kreatin = resim_yukle("kreatin.png", (100, 100), BEYAZ)
img_tavuk = resim_yukle("tavuk_pilav.png", (100, 100), TURUNCU)
img_muz = resim_yukle("muz.png", (100, 100), ALTIN)
img_pre = resim_yukle("pre_workout.png", (100, 100), MAVI)
img_ayakkabi = resim_yukle("ayakkabi.png", (100, 100), YESIL) # YENİ
img_kemer = resim_yukle("kemer.png", (100, 100), GRI) # YENİ

# degiskenler / variables
sahne = "EV"
oyuncu_pos = [400, 350]
hiz = 6
enerji, max_enerji = 100, 100
kas, para, gun = 10, 100, 1
kira_miktari = 150
enerji_maliyeti_carpani = 1.0 # Kemer için

envanter = []
envanter_acik = False
hud_gorunur = True 
oyun_bitti = False 
kayip_mesaji = ""
bekleme_bitis_zamani = 0
beklemede_mi = False
su_an_yapilan_is = ""
BEKLEME_SURESI = 5000 
ekran_mesaji = "Güne başlamak için dışarı çık! (7 Günde bir kira: 150$)"
mesaj_zamani = pygame.time.get_ticks()

aktif_oyuncu_img = img_oyuncu 

# QTE (minigame) variables
qte_aktif = False
qte_hedef_makine = None
qte_imlec_x = 0
qte_imlec_yon = 8
qte_hedef_x = 100
qte_hedef_w = 50

# types and effects have been added 
market_esyalari = [
    {"isim": "Kreatin", "fiyat": 30, "enerji": 100, "resim": img_kreatin, "tur": "tuketim"},
    {"isim": "Tavuk Pilav", "fiyat": 20, "enerji": 50, "resim": img_tavuk, "tur": "tuketim"},
    {"isim": "Muz", "fiyat": 5, "enerji": 15, "resim": img_muz, "tur": "tuketim"},
    {"isim": "Pre-Workout", "fiyat": 25, "enerji": 80, "resim": img_pre, "tur": "tuketim"},
    {"isim": "Orto. Yatak", "fiyat": 200, "enerji": 0, "resim": img_yatak_ortopedik, "tur": "kalici", "etki": "yatak"},
    {"isim": "Spor Ayakkabı", "fiyat": 100, "enerji": 0, "resim": img_ayakkabi, "tur": "kalici", "etki": "hiz"},
    {"isim": "Ağırlık Kemeri", "fiyat": 150, "enerji": 0, "resim": img_kemer, "tur": "kalici", "etki": "enerji_tasarrufu"}
]

gym_makineleri = [
    [100, 150, 80, 80, "Lat Pulldown", 20, 5, img_lat],
    [300, 150, 80, 80, "Bench Press", 25, 7, img_bench],
    [500, 150, 80, 80, "Leg Press", 20, 5, img_leg],
    [700, 150, 80, 80, "Biceps Curl", 15, 4, img_biceps],
    [100, 450, 120, 60, "Kosu Bandi", 30, 2, img_kosu],
    [750, 450, 100, 100, "Squat Rack", 35, 10, img_squat]
]

def mesaj_ekle(metin):
    global ekran_mesaji, mesaj_zamani
    ekran_mesaji = metin
    mesaj_zamani = pygame.time.get_ticks()

def draw_hud():
    if not hud_gorunur: return 
    pygame.draw.rect(ekran, GRI, (740, 10, 250, 150), border_radius=10)
    pygame.draw.rect(ekran, BEYAZ, (740, 10, 250, 150), 2, border_radius=10)
    ekran.blit(font_hud.render(f"ENERJI: {int(enerji)}/{max_enerji}", True, YESIL if enerji > 30 else KIRMIZI), (755, 25))
    ekran.blit(font_hud.render(f"KAS   : {kas}", True, MAVI), (755, 55))
    ekran.blit(font_hud.render(f"PARA  : {para}$", True, ALTIN), (755, 85))
    ekran.blit(font_hud.render(f"GUN   : {gun} | ENV: I", True, BEYAZ), (755, 115))
    ekran.blit(font_ipucu.render("Hareket: YÖN TUŞLARI | Etkileşim: E | Envanter: I", True, BEYAZ), (10, 10))

    if pygame.time.get_ticks() - mesaj_zamani < 3000:
        yazi = font_mesaj.render(ekran_mesaji, True, BEYAZ)
        rect = yazi.get_rect(center=(GENISLIK//2, YUKSEKLIK - 50))
        pygame.draw.rect(ekran, (20, 20, 20), rect.inflate(20, 10), border_radius=5)
        ekran.blit(yazi, rect)

    if beklemede_mi:
        simdi = pygame.time.get_ticks()
        kalan_ms = bekleme_bitis_zamani - simdi
        if kalan_ms > 0:
            oran = (BEKLEME_SURESI - kalan_ms) / BEKLEME_SURESI
            pygame.draw.rect(ekran, GRI, (GENISLIK//2 - 150, YUKSEKLIK//2 + 80, 300, 25))
            pygame.draw.rect(ekran, TURUNCU, (GENISLIK//2 - 150, YUKSEKLIK//2 + 80, 300 * oran, 25))
            yazi = font_hud.render(f"{su_an_yapilan_is} YAPILIYOR...", True, BEYAZ)
            ekran.blit(yazi, (GENISLIK//2 - 100, YUKSEKLIK//2 + 55))

    # QTE drawing
    if qte_aktif:
        pygame.draw.rect(ekran, GRI, (GENISLIK//2 - 150, YUKSEKLIK//2 - 50, 300, 30))
        pygame.draw.rect(ekran, YESIL, (GENISLIK//2 - 150 + qte_hedef_x, YUKSEKLIK//2 - 50, qte_hedef_w, 30))
        pygame.draw.rect(ekran, BEYAZ, (GENISLIK//2 - 150 + qte_imlec_x, YUKSEKLIK//2 - 60, 5, 50))
        ekran.blit(font_hud.render("YEŞİLDEYKEN SPACE'E BAS!", True, BEYAZ), (GENISLIK//2 - 110, YUKSEKLIK//2 - 15))

#  MAIN LOOP
while True:
    e_basildi = False
    ekran.fill(SIYAH)
    simdi = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e: e_basildi = True
            if event.key == pygame.K_i: envanter_acik = not envanter_acik
            if event.key == pygame.K_h: hud_gorunur = not hud_gorunur
            
            # QTE Etkileşimi (SPACE TUŞU)
            if event.key == pygame.K_SPACE and qte_aktif:
                if qte_hedef_x <= qte_imlec_x <= qte_hedef_x + qte_hedef_w:
                    # BAŞARILI! Ekstra kas, normal enerji harcaması.
                    kas += qte_hedef_makine[6] + 2 
                    enerji -= int(qte_hedef_makine[5] * enerji_maliyeti_carpani)
                    mesaj_ekle("MÜKEMMEL TEKRAR! +Ekstra Kas")
                else:
                    # BAŞARISIZ! Sakatlık.
                    enerji = 0
                    mesaj_ekle("SAKATLANDIN! Enerjin Sıfırlandı!")
                qte_aktif = False

            # --- ENVANTER KULLANIMI (1-4 TUŞLARI) ---
            if envanter_acik:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                    index = event.key - pygame.K_1
                    if index < len(envanter):
                        esya = envanter.pop(index)
                        enerji = min(max_enerji, enerji + esya['enerji'])
                        mesaj_ekle(f"{esya['isim']} kullanıldı! +{esya['enerji']} Enerji")

    # QTE cursor movement
    if qte_aktif:
        qte_imlec_x += qte_imlec_yon
        if qte_imlec_x <= 0 or qte_imlec_x >= 295:
            qte_imlec_yon *= -1

    if kas >= 100: 
        oyun_bitti = True
        kayip_mesaji = f"{gun}. günde devasa kaslara ulaştın!"

    if oyun_bitti:
        ekran.fill((10, 10, 10))
        renk = ALTIN if kas >= 100 else KIRMIZI
        baslik = "OYUNU BİTİRDİN! TEBRİKLER" if kas >= 100 else "GAME OVER!"
        
        tebrik_yazi = font_bitis.render(baslik, True, renk)
        tebrik_rect = tebrik_yazi.get_rect(center=(GENISLIK//2, YUKSEKLIK//2 - 50))
        ekran.blit(tebrik_yazi, tebrik_rect)
        
        skor_yazi = font_mesaj.render(kayip_mesaji, True, BEYAZ)
        skor_rect = skor_yazi.get_rect(center=(GENISLIK//2, YUKSEKLIK//2 + 30))
        ekran.blit(skor_yazi, skor_rect)
        
       
        ekran.blit(dev_yazi, (20, YUKSEKLIK - 40))
        pygame.display.flip()
        continue 

    if beklemede_mi and simdi >= bekleme_bitis_zamani:
        beklemede_mi = False
        mesaj_ekle(f"{su_an_yapilan_is} BITTI!")

    if not beklemede_mi and not envanter_acik and not qte_aktif:
        tuslar = pygame.key.get_pressed()
        if tuslar[pygame.K_LEFT]: oyuncu_pos[0] -= hiz
        if tuslar[pygame.K_RIGHT]: oyuncu_pos[0] += hiz
        if tuslar[pygame.K_UP]: oyuncu_pos[1] -= hiz
        if tuslar[pygame.K_DOWN]: oyuncu_pos[1] += hiz

    karakter_rect = pygame.Rect(oyuncu_pos[0], oyuncu_pos[1], 60, 60)

    # SCENES
    if sahne == "EV":
        ekran.blit(bg_ev, (0, 0))
        yatak = pygame.Rect(50, 50, 160, 100); dolap = pygame.Rect(300, 50, 100, 150)
        pc = pygame.Rect(550, 50, 80, 80); kapi = pygame.Rect(960, 250, 40, 200)
        
        ekran.blit(img_yatak, (yatak.x, yatak.y))
        ekran.blit(img_dolap, (dolap.x, dolap.y))
        ekran.blit(img_pc, (pc.x, pc.y))
        ekran.blit(img_kapi, (kapi.x, kapi.y))
        
        if karakter_rect.colliderect(yatak) and not beklemede_mi and not qte_aktif:
            ekran.blit(font_ipucu.render("[E] Uyu (Sonraki Gün)", True, BEYAZ), (yatak.x + 10, yatak.y - 25))
            if e_basildi:
                beklemede_mi = True; bekleme_bitis_zamani = simdi + 2000 # Uyku süresi hızlandırıldı
                su_an_yapilan_is = "UYKU"; enerji = max_enerji; gun += 1
                
                # Kira Sistemi
                if gun % 7 == 0:
                    if para >= kira_miktari:
                        para -= kira_miktari
                        mesaj_ekle(f"Kira Günü! Ev sahibine {kira_miktari}$ ödendi.")
                    else:
                        oyun_bitti = True
                        kayip_mesaji = f"Kirayı ödeyemedin ve evden atıldın! ({gun}. Gün)"
                
        if karakter_rect.colliderect(dolap) and not beklemede_mi and not qte_aktif:
            ekran.blit(font_ipucu.render("[E] Kıyafet Değiştir", True, BEYAZ), (dolap.x - 15, dolap.y - 25))
            if e_basildi:
                aktif_oyuncu_img = img_oyuncu_yeni if aktif_oyuncu_img == img_oyuncu else img_oyuncu
                mesaj_ekle("Görünüm değiştirildi!")

        if karakter_rect.colliderect(pc) and not beklemede_mi and not qte_aktif:
            ekran.blit(font_ipucu.render("[E] Freelance Çalış (Enerji: -30, Para: +50$)", True, BEYAZ), (pc.x - 50, pc.y - 25))
            if e_basildi:
                if enerji >= 30:
                    beklemede_mi = True; bekleme_bitis_zamani = simdi + 3000
                    su_an_yapilan_is = "YAZILIM KODLANIYOR"
                    enerji -= 30; para += 50
                else:
                    mesaj_ekle("Çalışmak için çok yorgunsun!")
                
        if karakter_rect.colliderect(kapi): 
            sahne = "CADDE"
            oyuncu_pos[0] = 60

    elif sahne == "CADDE":
        ekran.blit(bg_cadde, (0, 0))
        ev_k = pygame.Rect(0, 250, 40, 200); gym_k = pygame.Rect(960, 250, 40, 200); market_k = pygame.Rect(450, 0, 100, 40)
        ekran.blit(img_dis_ev, (0, 200)); ekran.blit(img_dis_gym, (880, 200)); ekran.blit(img_dis_market, (380, 0))
        
        if karakter_rect.colliderect(ev_k): sahne = "EV"; oyuncu_pos[0] = 890
        if karakter_rect.colliderect(gym_k): sahne = "GYM"; oyuncu_pos[0] = 60
        if karakter_rect.colliderect(market_k): sahne = "MARKET"; oyuncu_pos[1] = 650

    elif sahne == "GYM":
        ekran.blit(bg_gym, (0, 0))
        kapi = pygame.Rect(0, 250, 40, 200); ekran.blit(img_kapi, (kapi.x, kapi.y))
        for m in gym_makineleri:
            m_r = pygame.Rect(m[0], m[1], m[2], m[3]); ekran.blit(m[7], (m[0], m[1]))
            if karakter_rect.colliderect(m_r) and not beklemede_mi and not qte_aktif:
                maliyet = int(m[5] * enerji_maliyeti_carpani)
                ekran.blit(font_ipucu.render(f"[E] {m[4]} (Enerji: -{maliyet})", True, BEYAZ), (m[0] - 20, m[1] - 25))
                if e_basildi:
                    if enerji >= maliyet:
                        qte_aktif = True
                        qte_hedef_makine = m
                        qte_hedef_x = random.randint(20, 230)
                        qte_imlec_x = 0
                        qte_imlec_yon = 8 # DÜZELTME: Eski eksi (-) hızdan etkilenmemesi için yönü pozitife sıfırladık.
                    else: 
                        mesaj_ekle("Enerjin çok düşük!")
        if karakter_rect.colliderect(kapi): sahne = "CADDE"; oyuncu_pos[0] = 890

    elif sahne == "MARKET":
        ekran.blit(bg_market, (0, 0))
        kapi = pygame.Rect(450, 710, 100, 40); ekran.blit(img_kapi_yatay, (kapi.x, 730))
        
        silinecek_esya = None # DÜZELTME: Liste kaymasını engellemek için geçici bir silme değişkeni eklendi.
        
        # Eşyaları 2 satır halinde dizmek için algoritma
        for i, esya in enumerate(market_esyalari):
            satir = i // 4
            sutun = i % 4
            raf = pygame.Rect(50 + (sutun*230), 80 + (satir*200), 100, 100)
            
            # CORRECTION: We have applied the “Scale” function to ensure that images that are not 100x100 in size—such as those of beds—do not cause the gallery to overflow or appear as a block.
            ekran.blit(pygame.transform.scale(esya["resim"], (100, 100)), (raf.x, raf.y))
            
            if karakter_rect.colliderect(raf):
                ekran.blit(font_ipucu.render(f"[E] {esya['isim']} ({esya['fiyat']}$)", True, BEYAZ), (raf.x - 20, raf.y - 25))
                if e_basildi:
                    if para >= esya['fiyat']: 
                        para -= esya['fiyat']
                        if esya.get("tur") == "kalici":
                            if esya["etki"] == "yatak":
                                max_enerji = 150
                                img_yatak = img_yatak_ortopedik # Görseli de günceller
                                mesaj_ekle("Ortopedik Yatak kuruldu! Max Enerji 150 oldu.")
                            elif esya["etki"] == "hiz":
                                hiz += 4
                                mesaj_ekle("Spor Ayakkabı giyildi! Artık daha hızlısın.")
                            elif esya["etki"] == "enerji_tasarrufu":
                                enerji_maliyeti_carpani = 0.6
                                mesaj_ekle("Ağırlık Kemeri takıldı! Spor daha az yoracak.")
                            
                            silinecek_esya = esya 
                        else:
                            envanter.append(esya)
                            mesaj_ekle(f"{esya['isim']} alındı!")
                    else: 
                        mesaj_ekle("Yetersiz bakiye!")
        
        
        if silinecek_esya:
            market_esyalari.remove(silinecek_esya)
                        
        if karakter_rect.colliderect(kapi): 
            sahne = "CADDE"
            oyuncu_pos[1] = 60

    # --- ENVANTER ---
    if envanter_acik:
        pygame.draw.rect(ekran, (30, 30, 30), (250, 150, 500, 400), border_radius=15)
        ekran.blit(font_hud.render("ENVANTER (Kullanmak için 1-4 tuşlarına bas)", True, ALTIN), (280, 170))
        for i, item in enumerate(envanter):
            ekran.blit(font_hud.render(f"{i+1}. {item['isim']} (+{item['enerji']} Enerji)", True, BEYAZ), (300, 220 + (i*35)))

    if not beklemede_mi: ekran.blit(aktif_oyuncu_img, (karakter_rect.x, karakter_rect.y))
    draw_hud()
    pygame.display.flip()
    clock.tick(60)
