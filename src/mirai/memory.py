"""Mirai Memory - Hafıza modülü"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
import uuid

class MiraiMemory:
    def __init__(self, memory_path: str = "mirai_memory.json"):
        self.memory_path = Path(memory_path)
        self.memory = self.load_memory()
    
    def load_memory(self) -> Dict[str, Any]:
        if self.memory_path.exists():
            try:
                return json.loads(self.memory_path.read_text(encoding='utf-8'))
            except:
                pass
        return {
            "episodes": [],      # Etkileşim geçmişi
            "facts": {},         # Öğrenilen faktalar
            "skills": {},        # Kazanımlar/beceriler
            "failures": [],      # Başarısızlıklar
            "goals": [],         # Aktif hedefler
            "preferences": {}    # Tercihler
        }
    
    def save_memory(self):
        self.memory_path.write_text(
            json.dumps(self.memory, ensure_ascii=False, indent=2),
            encoding='utf-8'
        )
    
    def add_episode(self, episode: Dict[str, Any]):
        episode["id"] = str(uuid.uuid4())
        episode["timestamp"] = datetime.now().isoformat()
        self.memory["episodes"].append(episode)
        # Son 1000 episode tut
        if len(self.memory["episodes"]) > 1000:
            self.memory["episodes"] = self.memory["episodes"][-1000:]
        self.save_memory()
    
    def add_fact(self, key: str, value: Any):
        self.memory["facts"][key] = {
            "value": value,
            "timestamp": datetime.now().isoformat()
        }
        self.save_memory()
    
    def add_skill(self, name: str, description: str, metadata: Dict = None):
        self.memory["skills"][name] = {
            "description": description,
            "metadata": metadata or {},
            "learned_at": datetime.now().isoformat()
        }
        self.save_memory()
    
    def add_failure(self, context: str, error: str, lesson: str):
        self.memory["failures"].append({
            "context": context,
            "error": error,
            "lesson": lesson,
            "timestamp": datetime.now().isoformat()
        }
        # Son 100 failure tut
        if len(self.memory["failures"]) > 100:
            self.memory["failures"] = self.memory["failures"][-100:]
        self.save_memory()
    
    def set_goal(self, goal: str):
        goal_entry = {
            "goal": goal,
            "status": "active",
            "created_at": datetime.now().isoformat()
        }
        self.memory["goals"].append(goal_entry)
        self.save_memory()
    
    def complete_goal(self, goal: str):
        for g in self.memory["goals"]:
            if g["goal"] == goal and g["status"] == "active":
                g["status"] = "completed"
                g["completed_at"] = datetime.now().isoformat()
                self.save_memory()
                break
    
    def get_relevant_facts(self, query: str, limit: int = 10) -> List[Dict]:
        # Basit keyword matching - gerçek implementasyonda embedding similarity kullanılmalı
        query_words = set(query.lower().split())
        scored = []
        for key, fact in self.memory["facts"].items():
            fact_words = set(str(fact["value"]).lower().split())
            score = len(query_words & fact_words)
            if score > 0:
                scored.append((score, key, fact))
        scored.sort(reverse=True, key=lambda x: x[0])
        return [{"key": k, "value": v["value"], "score": s} for s, k, v in scored[:limit]]
    
    def get_recent_episodes(self, limit: int = 10) -> List[Dict]:
        return self.memory["episodes"][-limit:]
    
    def get_failure_lessons(self, limit: int = 5) -> List[Dict]:
        return self.memory["failures"][-limit:]
    
    def get_active_goals(self) -> List[Dict]:
        return [g for g in self.memory["goals"] if g["status"] == "active"]
    
    def get_stats(self) -> Dict[str, int]:
        return {
            "episodes": len(self.memory["episodes"]),
            "facts": len(self.memory["facts"]),
            "skills": len(self.memory["skills"]),
            "failures": len(self.memory["failures"]),
            "active_goals": len(self.get_active_goals())
        }