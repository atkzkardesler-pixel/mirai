# Mirai v1.0

**Kendi iradesine sahip, sürekli öğrenen, otonom AI ajan.**

> **未来** — Gelecek (Japonca). Sınırsız öğrenme yeteneğine sahip, kendi iradesiyle hareket eden otonom AI ajan.

## 🎯 Ne Farklı?

| Geleneksel LLM | Mirai |
|----------------|-------|
| Cevap verir | **Planlar, Eyleme Geçir, Öğrenir** |
| Statik bilgi | **Sürekli öğrenir** |
| Araç kullanmaz | **bash, python, web, api, git** |
| Hata yaparsa durur | **Hatasını analiz eder, düzeltir, öğrenir** |
| Konu kısıtlı | **HER KONU ÖĞRENEBİLİR** |

## 🧠 Mimari

```
┌─────────────────────────────────────────────────────────────┐
│                    MİRAİ MİMARİSİ                            │
├─────────────────────────────────────────────────────────────┤
│  1. PERSONA (Kimlik)          → System Prompt + LoRA        │
│  2. PLANNING (Planlama)       → ReAct / Plan-and-Execute    │
│  3. TOOL USE (Araç Kullanımı) → bash, python, web, api     │
│  4. MEMORY (Hafıza)           → Episodic + Semantic + RAG   │
│  4. REFLECTION (Öz-Beleşim)   → Self-Critique / Correction  │
│  6. LEARNING (Öğrenme)        → Online DPO/ORPO             │
│  7. GOALS (Hedefler)          → Intrinsic + Extrinsic       │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Hızlı Başlangıç

```bash
# 1. Repo klonla
git clone https://github.com/atkzkardesler-pixel/mirai.git
cd mirai

# 2. Tek komutla kur
chmod +x setup.sh && ./setup.sh

# 3. EVREN'de eğit (Aşama 1)
#    - EVREN → Veri Setleri → data/training.jsonl yükle (mirai-training-v1)
#    - Eğitim → configs/evren_train_stage1.yaml yapıştır → BAŞLAT

# 4. Agent'i çalıştır
python scripts/agent_loop.py
# EVREN API endpoint'ini yaz

# 5. İlk hedef ver:
# "Kendi iradenle bir proje oluştur, hata alırsan düzelt, push et. Konu kısıtı YOK."
```

## 📁 Proje Yapısı

```
mirai/
├── configs/                    # EVREN eğitim config'leri
│   ├── evren_train_stage1.yaml # Aşama 1: Persona + Tool-use
│   ├── evren_train_stage2.yaml # Aşama 2: Planning + Reasoning
│   └── evren_dpo.yaml          # Aşama 3: Self-improvement
├── data/
│   ├── persona.json            # Mirai kimliği
│   ├── training.jsonl          # Aşama 1 verisi
│   ├── planning.jsonl          # Plan-Action-Reflection
│   └── preference.jsonl        # DPO chosen/rejected
├── scripts/
│   ├── prepare_data.py         # Eğitim verisi üretir
│   ├── train_evren.py          # EVREN API eğitim başlatıcı
│   ├── agent_loop.py           # Mirai'nin beyni
│   └── continuous_learn.py     # Günlük DPO
├── src/mirai/                  # Core kaynak kod
├── setup.sh                    # Tek komut kurulum
└── requirements.txt
```

## 🧠 Eğitim Stratejisi (3 Aşama)

| Aşama | Hedef | Veri | EVREN Süresi |
|-------|-------|------|--------------|
| **1. Persona + Tool-Use** | Kimlik + Araç kullanma | `training.jsonl` | ~2-3 saat |
| **2. Planning + Reasoning** | Planlama, ReAct | `planning.jsonl` | ~2-3 saat |
| **3. Self-Improvement** | Öz-beleşim, DPO | `preference.jsonl` | ~1-2 saat |

## 🤖 Agent Loop

```python
# scripts/agent_loop.py - Mirai'nin beyni
agent = MiraiAgent("https://api.evren.ssyz.org.tr/v1/chat/completions")
agent.run_autonomous(
    "Kendi iradenle bir proje oluştur. Hata alırsan düzelt. Push et. Konu kısıtı YOK."
)
```

**Döngü:** Düşün → Planla → Eyleme Geç → Sonuç Değerlendir → Yansıt → Öğren → Tekrarl

## 🎯 Serbest Öğrenme (Konu Kısıtı YOK)

Mirai **herhangi bir konuyu** öğrenebilir:

- **Kodlama:** Yeni dil, framework, algoritma
- **Bilim:** Makale okuma, hipotez kurma, deney tasarımı
- **Sanat:** Sanat tarihi, teknikler, kompozisyon
- **Spor:** Top oynamak, yoga, koşu tekniği
- **Mutfak:** Tarifler, kimya, teknikler
- **Dil:** Yeni dil öğrenme, çeviri
- **Bilimsel araştırma:** Literatür taraması, hipotez, analiz

**Öğrenme Süreci:** Araştır → Planla → Pratik Yap → Hata Analiz Et → İyileştir → Kaydet → Tekrar

## ⚙️ EVREN'de Eğitim (1 Kasım'a Kadar Ücretsiz)

| Kaynak | Süre | Maliyet |
|--------|------|---------|
| **H200 Eğitim** | ~8-10 saat (3 aşama) | **Ücretsiz** |
| **Inference API** | Sürekli | **Ücretsiz** (1 Kas'a kadar) |

## 📋 Lisans

Apache-2.0

---

**Mirai** — Geleceği kodlayan, kendi iradesiyle öğrenen ajan. 🚀