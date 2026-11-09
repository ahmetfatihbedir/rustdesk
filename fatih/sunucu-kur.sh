#!/bin/bash
# Fatih Bilgisayar Uzaktan Destek - Sunucu kurulumu (RustDesk hbbs + hbbr)
# Oracle Cloud Ubuntu sunucusunda calistirin:  bash sunucu-kur.sh
set -e
export DEBIAN_FRONTEND=noninteractive

echo ">>> Paketler kuruluyor..."
sudo apt-get update -y
sudo apt-get install -y docker.io iptables-persistent curl
sudo systemctl enable --now docker

echo ">>> RustDesk sunucusu baslatiliyor..."
sudo mkdir -p /opt/fatih-destek
sudo docker rm -f hbbs hbbr 2>/dev/null || true
sudo docker run -d --name hbbs --restart unless-stopped --net=host \
  -v /opt/fatih-destek:/root rustdesk/rustdesk-server hbbs
sudo docker run -d --name hbbr --restart unless-stopped --net=host \
  -v /opt/fatih-destek:/root rustdesk/rustdesk-server hbbr

echo ">>> Guvenlik duvari portlari aciliyor..."
for p in 21115 21116 21117 21118 21119; do
  sudo iptables -C INPUT -p tcp --dport $p -j ACCEPT 2>/dev/null || \
  sudo iptables -I INPUT 1 -p tcp --dport $p -j ACCEPT
done
sudo iptables -C INPUT -p udp --dport 21116 -j ACCEPT 2>/dev/null || \
sudo iptables -I INPUT 1 -p udp --dport 21116 -j ACCEPT
sudo netfilter-persistent save

echo ">>> Anahtar olusturuluyor..."
for i in $(seq 1 20); do
  [ -f /opt/fatih-destek/id_ed25519.pub ] && break
  sleep 1
done

echo
echo "=============================================="
echo " KURULUM TAMAM - asagidaki iki satiri Claude'a gonderin"
echo "=============================================="
echo "SUNUCU IP : $(curl -s https://ifconfig.me)"
echo "ANAHTAR   : $(sudo cat /opt/fatih-destek/id_ed25519.pub)"
echo "=============================================="
