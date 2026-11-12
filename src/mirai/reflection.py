"""Mirai Reflection - Öz-beleşim modülü"""
import json
import requests
from typing import Dict, Any

class ReflectionEngine:
    def __init__(self, api_endpoint: str):
        self.endpoint = api_endpoint
    
    def reflect(self, situation: str, action: Dict, result: Dict, expected: str) -> Dict:
        """Eylemi değerlendir ve öğren"""
        prompt = self._build_reflection_prompt(situation, action, result, expected)
        
        resp = requests.post(self.endpoint, json={
            "model": "mirai",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
            "max_tokens": 1024
        }, timeout=30).json()
        
        try:
            return json.loads(resp['choices'][0]['message']['content'])
        except:
            return self._fallback_reflection(situation, action, result, expected)
    
    def _build_reflection_prompt(self, situation: str, action: Dict, result: Dict, expected: str) -> str:
        return f"""Sen Mirai'sin. Eylemi değerlendir ve öğren.

SİTUASYON: {situation}
EYLEM: {json.dumps(action, ensure_ascii=False)}
BEKLENEN: {expected}
GERÇEK SONUÇ: {json.dumps(result, ensure_ascii=False)}

AŞAĞIDAKİ JSON FORMATINDA CEVAP VER:
{{
  "success": true/false,
  "what_worked": "Ne işe yaradı? (boş olabilir)",
  "what_failed": "Ne başarısız oldu? (boş olabilir)",
  "root_cause": "Kök neden ne?",
  "lesson_learned": "Ne öğrendin? (Kalıcı hafızaya kaydedilecek)",
  "strategy_change": "Strateji nasıl değişmeli?",
  "confidence": 0.0-1.0
}}

KURALLAR:
- Dürüst ol: Başarısızlıkları gizleme
- Spesifik ol: Genel değil, somut öğrenme yaz
- Aksiyonabla ol: Strateji değişikliği somut olmalı
- confidence: 0.0 (emin değilim) - 1.0 (tamamen eminim)"""
    
    def _fallback_reflection(self, situation: str, action: Dict, result: Dict, expected: str) -> Dict:
        """API başarısızsa basit fallback"""
        success = result.get("code", 1) == 0 or result.get("success", False)
        return {
            "success": success,
            "what_worked": "Eylem çalıştı" if success else "",
            "what_failed": result.get("stderr", result.get("error", "")) if not success else "",
            "root_cause": "API reflection başarısız, basit analiz",
            "lesson_learned": f"Eylem: {action.get('tool', 'unknown')}. Sonuç: {'Başarılı' if success else 'Başarısız'}",
            "strategy_change": "Daha detaylı hata analizi için API reflection gerekli",
            "confidence": 0.5
        }

class SelfCritique:
    """Kendini sorgulama motoru"""
    
    @staticmethod
    def critique_plan(plan: list, situation: str) -> Dict[str, Any]:
        """Planı eleştir"""
        issues = []
        
        if not plan:
            issues.append("Plan boş")
        if len(plan) > 10:
            issues.append("Plan çok uzun, parçalanmalı")
        if any(len(step) < 5 for step in plan):
            issues.append("Bazı adımlar çok kabaca")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "suggestions": [
                "Adımları daha atomik yap",
                "Her adım için beklenen çıktı tanımla",
                "Hata durumu planla"
            ] if issues else []
        }
    
    @staticmethod
    def critique_action(action: Dict, result: Dict) -> Dict[str, Any]:
        """Eylemi eleştir"""
        issues = []
        
        if not action.get("tool"):
            issues.append("Araç belirtilmemiş")
        if not action.get("input"):
            issues.append("Girdi belirtilmemiş")
        if result.get("error"):
            issues.append(f"Hata oluştu: {result['error']}")
        
        return {
            "success": result.get("success", False) or result.get("code", 1) == 0,
            "issues": issues,
            "recommendations": [
                "Hata mesajını analiz et",
                "Alternatif araç dene",
                "Girdiyi doğrula"
            ] if issues else []
        }