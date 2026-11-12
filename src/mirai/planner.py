"""Mirai Planner - Planlama modülü"""
import json
import requests
from typing import Dict, Any, List

class Planner:
    def __init__(self, api_endpoint: str):
        self.endpoint = api_endpoint
    
    def create_plan(self, goal: str, context: str = "") -> Dict[str, Any]:
        """Hedef için plan oluştur"""
        prompt = f"""Sen Mirai'sin. Verilen hedef için adım adım plan oluştur.

HEDEF: {goal}
BAĞLAM: {context}

Aşağıdaki JSON formatında plan oluştur:
{{
  "goal": "hedef",
  "steps": [
    {{"step": 1, "action": "ne yapılacak", "tool": "bash|python|web_search|file_write|api_call", "input": "...", "expected": "beklenen sonuç"}},
    ...
  ],
  "risks": ["risk1", "risk2"],
  "fallback": "plan B ne olacak?"
}}

KURALLAR:
- Adımlar atomik ve sıralı olmalı
- Her adımda hangi araç kullanılacak belirtilmeli
- Girdi (input) somut olmalı
- Beklenen çıktı net olmalı
- Riskler ve plan B düşünülmeli"""
        
        resp = requests.post(self.endpoint, json={
            "model": "mirai",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.5,
            "max_tokens": 2048
        }, timeout=60).json()
        
        try:
            return json.loads(resp['choices'][0]['message']['content'])
        except:
            return self._fallback_plan(goal)
    
    def _fallback_plan(self, goal: str) -> Dict:
        return {
            "goal": goal,
            "steps": [
                {"step": 1, "action": "Hedefi analiz et ve alt görevlere böl", "tool": "think", "input": "", "expected": "Alt görevler listesi"},
                {"step": 2, "action": "İlk alt görevi planla", "tool": "plan", "input": "", "expected": "Detaylı plan"},
                {"step": 3, "action": "İlk adımı uygula", "tool": "bash|python|web_search", "input": "...", "expected": "İlk çıktı"},
            ],
            "risks": ["Planlama API'si çalışmadı"],
            "fallback": "Manuel planlama yap"
        }

class ReActPlanner:
    """ReAct (Reasoning + Acting) pattern planner"""
    
    def __init__(self, api_endpoint: str):
        self.endpoint = api_endpoint
    
    def think_act_observe(self, situation: str, available_tools: list) -> Dict[str, Any]:
        """ReAct döngüsü: Düşün → Eyleme Geç → Gözlemle"""
        tools_desc = ", ".join(available_tools)
        
        prompt = f"""Sen Mirai'sin. ReAct pattern ile karar ver.

MEVCUT DURUM: {situation}
MEVCUT ARAÇLAR: {tools_desc}

JSON formatında cevap ver:
{{
  "thought": "Durumu analiz et, ne yapmalı?",
  "action": {{"tool": "araç_adı", "input": "..."}},
  "expected_observation": "Ne görmeyi bekliyorsun?"
}}

KURALLAR:
- Sadece BİR eylem seç
- Düşünce kısmında mantığını açıkla
- Eylem somut olmalı"""
        
        resp = requests.post(self.endpoint, json={
            "model": "mirai",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.5,
            "max_tokens": 1024
        }, timeout=30).json()
        
        try:
            return json.loads(resp['choices'][0]['message']['content'])
        except:
            return {
                "thought": "API başarısız, basit fallback",
                "action": {"tool": "bash", "input": "echo 'fallback'"},
                "expected_observation": "Fallback çalıştı"
            }
    
    def run_react_loop(self, goal: str, max_steps: int = 10) -> List[Dict]:
        """ReAct döngüsünü çalıştır"""
        history = []
        situation = f"Hedef: {goal}"
        
        for step in range(max_steps):
            decision = self.think_act_observe(situation, list(TOOLS.keys()))
            history.append({
                "step": step + 1,
                "thought": decision["thought"],
                "action": decision["action"],
                "expected": decision["expected_observation"]
            })
            
            # Eylem simülasyonu (gerçekte execute edilecek)
            observation = f"Simulated: {decision['action']}"
            history[-1]["observation"] = observation
            
            # Durum güncelle
            situation = f"Önceki: {decision['action']}. Gözlem: {observation}. Kalan hedef: {goal}"
            
            # Basit bitirme kontrolü
            if "tamam" in observation.lower() or "complete" in observation.lower():
                break
        
        return history

# Tool listesi (tools.py'den import edilecek)
TOOLS = ["bash", "python", "web_search", "file_write", "file_read", "file_edit", "api_call", "git"]