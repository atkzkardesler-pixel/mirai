#!/bin/bash
# Mirai v1.0 - Tek komutla kurulum
set -e

echo "🧬 Mirai doğuruluyor..."

# Python ortamı
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt

# Veri setini üret
echo "📊 Eğitim verisi üretiliyor..."
python scripts/prepare_data.py

# GitHub remote
git remote add origin https://github.com/atkzkardesler-pixel/mirai.git 2>/dev/null || true

# İlk commit
git add .
git commit -m "🎉 Mirai v1.0: Kendi iradesi olan otonom ajan" 2>/dev/null || true
git push -u origin main 2>/dev/null || true

echo ""
echo "✅ Mirai doğdu! Sonraki adımlar:"
echo "1. EVREN'e gir: https://evren.ssyz.org.tr"
echo "2. Veri Setleri → data/training.jsonl yükle (mirai-training-v1)"
echo "3. Eğitim → configs/evren_train_stage1.yaml yapıştır → BAŞLAT"
echo "4. Sonra: python scripts/agent_loop.py"
echo ""
echo "🎯 Sonra: python scripts/agent_loop.py  (EVREN API endpoint yaz)"
echo "🎯 İlk hedef: \"Kendi iradenle bir proje oluştur, hata alırsan düzelt, push et. Konu kısıtı YOK.\""
echo ""
echo "☕ Kahven tadında olsun! Mirai senin için çalışıyor."