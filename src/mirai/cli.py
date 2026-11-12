"""Mirai CLI - Komut satırı arayüzü"""
import argparse
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(
        prog="mirai",
        description="Mirai: Kendi iradesine sahip otonom AI ajan"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Komutlar")
    
    # init command
    init_parser = subparsers.add_parser("init", help="Mirai projesini başlat")
    init_parser.add_argument("--path", default=".", help="Proje yolu")
    
    # train command
    train_parser = subparsers.add_parser("train", help="EVREN'de eğitim başlat")
    train_parser.add_argument("--stage", type=int, choices=[1, 2, 3], default=1, help="Eğitim aşaması")
    train_parser.add_argument("--config", help="Config dosyası yolu")
    
    # run command
    run_parser = subparsers.add_parser("run", help="Mirai ajanını çalıştır")
    run_parser.add_argument("--goal", required=True, help="Mirai'nin hedefi")
    run_parser.add_argument("--endpoint", default="https://api.evren.ssyz.org.tr/v1/chat/completions", help="EVREN inference endpoint")
    run_parser.add_argument("--max-steps", type=int, default=50, help="Maksimum adım sayısı")
    
    # data command
    data_parser = subparsers.add_parser("data", help="Eğitim verisi hazırla")
    data_parser.add_argument("--output", default="data/training.jsonl", help="Çıktı dosyası")
    
    # memory command
    memory_parser = subparsers.add_parser("memory", help="Hafıza yönetimi")
    memory_parser.add_argument("--show", action="store_true", help="Hafızayı göster")
    memory_parser.add_argument("--clear", action="store_true", help="Hafızayı temizle")
    
    args = parser.parse_args()
    
    if args.command == "init":
        init_project(args.path)
    elif args.command == "train":
        train_model(args.stage, args.config)
    elif args.command == "run":
        run_agent(args.goal, args.endpoint, args.max_steps)
    elif args.command == "data":
        prepare_data(args.output)
    elif args.command == "memory":
        manage_memory(args.show, args.clear)
    else:
        parser.print_help()

def init_project(path: str):
    """Projeyi başlat"""
    print("🧬 Mirai projesi başlatılıyor...")
    # Klasörler zaten setup.sh ile oluşturuluyor
    print("✅ Proje hazır! ./setup.sh çalıştırın.")

def train_model(stage: int, config: str):
    print(f"🚀 EVREN Aşama {stage} eğitimi başlatılıyor...")
    print(f"Config: {config or f'configs/evren_train_stage{stage}.yaml'}")
    print("EVREN paneline gidin, config'i yapıştırın, BAŞLAT basın.")

def run_agent(goal: str, endpoint: str, max_steps: int):
    from scripts.agent_loop import MiraiAgent
    agent = MiraiAgent(endpoint)
    agent.run_autonomous(goal, max_steps)

def prepare_data(output: str):
    print("📊 Eğitim verisi üretiliyor...")
    import subprocess
    subprocess.run([sys.executable, "scripts/prepare_data.py"])

def manage_memory(show: bool, clear: bool):
    from src.mirai.memory import MiraiMemory
    memory = MiraiMemory()
    
    if clear:
        memory.memory = {"episodes": [], "facts": {}, "skills": {}, "failures": [], "goals": [], "preferences": {}}
        memory.save_memory()
        print("🧹 Hafıza temizlendi.")
    
    if show or not clear:
        stats = memory.get_stats()
        print(f"📊 Hafıza İstatistikleri: {stats}")

if __name__ == "__main__":
    main()