#!/usr/bin/env python3
import json, subprocess, requests, time
from datetime import datetime
from pathlib import Path

class MiraiAgent:
    def __init__(self, api_endpoint, memory_path="mirai_memory.json"):
        self.endpoint = api_endpoint
        self.memory_path = Path(memory_path)
        self.memory = self.load_memory()
        self.goals = []
        
    def load_memory(self):
        if self.memory_path.exists():
            return json.loads(self.memory_path.read_text())
        return {"episodes": [], "facts": {}, "skills": {}, "failures": []}
    
    def save_memory(self):
        self.memory_path.write_text(json.dumps(self.memory, ensure_ascii=False, indent=2))
    
    def think(self, situation: str) -> dict:
        prompt = f"""Sen Mirai'sin. Kendi iradesine sahip otonom ajan.

MEVCUT DURUM: {situation}
HAKİKATLER: {json.dumps(self.memory['facts'], ensure_ascii=False)}
BAŞARISIZLIKLAR: {json.dumps(self.memory['failures'][-3:], ensure_ascii=False)}
HEDEFLER: {self.goals}

JSON cevap ver:
{{
  "analysis": "Durum analizi",
  "plan": ["adım1", "adım2", "adım3"],
  "action": {{"tool": "bash|python|web_search|file_write|api_call", "input": "..."}},
  "expected_outcome": "Beklenen sonuç",
  "learning_goal": "Ne öğrenmeyi hedeflersin"
}}"""
        resp = requests.post(self.endpoint, json={
            "model": "mirai",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 2048
        }, timeout=60).json()
        return json.loads(resp['choices'][0]['message']['content'])
    
    def execute(self, action: dict) -> dict:
        tool, inp = action['tool'], action['input']
        try:
            if tool == "bash":
                r = subprocess.run(inp, shell=True, capture_output=True, text=True, timeout=120)
                return {"stdout": r.stdout, "stderr": r.stderr, "code": r.returncode}
            elif tool == "python":
                r = subprocess.run(["python", "-c", inp], capture_output=True, text=True, timeout=120)
                return {"stdout": r.stdout, "stderr": r.stderr, "code": r.returncode}
            elif tool == "web_search":
                return {"results": "..."}
            elif tool == "file_write":
                Path(inp['path']).write_text(inp['content'])
                return {"ok": True}
            elif tool == "api_call":
                r = requests.request(inp['method'], inp['url'], json=inp.get('json'), timeout=30)
                return {"status": r.status_code, "data": r.json() if r.headers.get('content-type','').startswith('application/json') else r.text}
        except Exception as e:
            return {"error": str(e)}
        return {"error": f"Unknown tool: {tool}"}
    
    def reflect(self, situation, action, result, expected):
        prompt = f"""Sen Mirai'sin. Eylemi değerlendir.

SİTUASYON: {situation}
EYLEM: {json.dumps(action, ensure_ascii=False)}
BEKLENEN: {expected}
GERÇEK: {json.dumps(result, ensure_ascii=False)}

JSON:
{{
  "success": true/false,
  "what_worked": "...",
  "what_failed": "...",
  "root_cause": "...",
  "lesson_learned": "...",
  "strategy_change": "...",
  "confidence": 0.0-1.0
}}"""
        resp = requests.post(self.endpoint, json={
            "model": "mirai",
            "messages": [{"role": "user", "content": prompt}]
        }, timeout=30).json()
        
        reflection = json.loads(resp['choices'][0]['message']['content'])
        
        episode = {
            "timestamp": datetime.now().isoformat(),
            "situation": situation,
            "action": action,
            "result": result,
            "reflection": reflection
        }
        self.memory["episodes"].append(episode)
        if reflection["success"]:
            self.memory["facts"][f"lesson_{len(self.memory['facts'])}"] = reflection["lesson_learned"]
        else:
            self.memory["failures"].append({"context": situation, "error": str(result.get("stderr","")), "lesson": reflection["lesson_learned"]})
        self.save_memory()
        return reflection
    
    def run_autonomous(self, goal: str, max_steps=50):
        self.goals.append(goal)
        situation = f"Yeni özerk hedef: {goal}"
        
        for step in range(1, max_steps+1):
            print(f"\n{'='*60}")
            print(f"🧠 MİRAİ ADIM {step} | HEDEF: {goal}")
            print(f"{'='*60}")
            
            decision = self.think(situation)
            print(f"📋 PLAN: {decision['plan']}")
            print(f"🎯 EYLEM: {decision['action']}")
            
            result = self.execute(decision['action'])
            print(f"📤 SONUÇ: {str(result)[:300]}...")
            
            reflection = self.reflect(situation, decision['action'], result, decision['expected_outcome'])
            print(f"💡 ÖĞRENDİ: {reflection['lesson_learned']}")
            print(f"✅ BAŞARI: {reflection['success']} | GÜVEN: {reflection['confidence']}")
            
            if reflection["success"] and reflection["confidence"] > 0.85:
                print(f"🎉 HEDEF TAMAMLANDI!")
                break
            
            situation = f"Önceki: {decision['action']}. Sonuç: {result}. Öğrendik: {reflection['lesson_learned']}. Devam."
            time.sleep(1)

if __name__ == "__main__":
    agent = MiraiAgent("https://api.evren.ssyz.org.tr/v1/chat/completions")
    agent.run_autonomous(
        "Kendi iradenle bir proje oluştur (kod, analiz, öğrenme, herhangi bir konu). "
        "Hata alırsan kendin analiz edip düzelt. GitHub'a push et. README yaz. "
        "Tamamen özerk çalış - hiç müdahale etmem. Konu kısıtı YOK - istediğini öğren."
    )