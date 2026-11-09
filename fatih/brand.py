"""Fatih Destek: sunucu adresi, anahtar ve uygulama adini derleme oncesi isler.

GitHub deposunda iki secret gerekir:
  FATIH_SERVER  -> sunucu IP adresi veya alan adi
  FATIH_KEY     -> sunucudaki id_ed25519.pub icerigi
"""
import os
import pathlib
import sys

APP_NAME = "FatihDestek"

server = os.environ.get("FATIH_SERVER", "").strip()
key = os.environ.get("FATIH_KEY", "").strip()
if not server or not key:
    sys.exit("HATA: FATIH_SERVER ve FATIH_KEY secret'lari tanimli degil.")

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
