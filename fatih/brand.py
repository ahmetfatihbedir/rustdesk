"""Fatih Destek: sunucu adresi, anahtar ve uygulama adini derleme oncesi isler.

Sunucu adresi fatih/sunucu.txt, acik anahtar fatih/anahtar.txt dosyasindan okunur.
FATIH_SERVER / FATIH_KEY ortam degiskenleri (GitHub secret) varsa onlar onceliklidir.
"""
import os
import pathlib
import sys

APP_NAME = "FatihDestek"

def ayar(env, dosya):
    deger = os.environ.get(env, "").strip()
    if not deger:
        f = pathlib.Path("fatih") / dosya
        deger = f.read_text(encoding="utf-8").strip() if f.exists() else ""
    if not deger:
        sys.exit(f"HATA: {env} / fatih/{dosya} bos.")
    return deger


server = ayar("FATIH_SERVER", "sunucu.txt")
key = ayar("FATIH_KEY", "anahtar.txt")

path = pathlib.Path("libs/hbb_common/src/config.rs")
src = path.read_text(encoding="utf-8")

replacements = [
    ('APP_NAME: RwLock<String> = RwLock::new("RustDesk".to_owned());',
     f'APP_NAME: RwLock<String> = RwLock::new("{APP_NAME}".to_owned());'),
    ('pub const RENDEZVOUS_SERVERS: &[&str] = &["rs-ny.rustdesk.com"];',
     f'pub const RENDEZVOUS_SERVERS: &[&str] = &["{server}"];'),
    ('pub const RS_PUB_KEY: &str = "OeVuKk5nlHiXp+APNn0Y3pC1Iwpwn44JGqrQCsWqmBw=";',
     f'pub const RS_PUB_KEY: &str = "{key}";'),
]
for old, new in replacements:
    if src.count(old) != 1:
        sys.exit(f"HATA: beklenen satir bulunamadi: {old}")
    src = src.replace(old, new)

path.write_text(src, encoding="utf-8")
print(f"Marka uygulandi: {APP_NAME} -> {server}")
