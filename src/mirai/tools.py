"""Mirai Tools - Araçlar modülü"""
import subprocess
import requests
import json
from pathlib import Path
from typing import Dict, Any, Optional
import time

class ToolError(Exception):
    """Araç çalıştırma hatası"""
    pass

def run_bash(command: str, timeout: int = 120) -> Dict[str, Any]:
    """Bash komutu çalıştır"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=timeout
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "code": result.returncode,
            "success": result.returncode == 0
        }
    except subprocess.TimeoutExpired:
        return {"error": f"Timeout after {timeout}s", "success": False}
    except Exception as e:
        return {"error": str(e), "success": False}

def run_python(code: str, timeout: int = 120) -> Dict[str, Any]:
    """Python kodu çalıştır"""
    try:
        result = subprocess.run(
            ["python", "-c", code],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "code": result.returncode,
            "success": result.returncode == 0
        }
    except subprocess.TimeoutExpired:
        return {"error": f"Timeout after {timeout}s", "success": False}
    except Exception as e:
        return {"error": str(e), "success": False}

def web_search(query: str, max_results: int = 5) -> Dict[str, Any]:
    """Web araması yap (placeholder - gerçek API entegrasyonu gerekli)"""
    # Gerçek implementasyon için: SerpAPI, Google Custom Search, Brave Search API vb.
    return {
        "results": f"Web search placeholder for: {query}",
        "success": True,
        "note": "Gerçek API entegrasyonu gerekli: SerpAPI, Brave Search, Google CSE"
    }

def file_write(path: str, content: str) -> Dict[str, Any]:
    """Dosya yaz"""
    try:
        Path(path).write_text(content, encoding='utf-8')
        return {"ok": True, "path": path}
    except Exception as e:
        return {"error": str(e), "success": False}

def file_read(path: str) -> Dict[str, Any]:
    """Dosya oku"""
    try:
        content = Path(path).read_text(encoding='utf-8')
        return {"content": content, "success": True}
    except Exception as e:
        return {"error": str(e), "success": False}

def file_edit(path: str, old_text: str, new_text: str) -> Dict[str, Any]:
    """Dosya düzenle"""
    try:
        content = Path(path).read_text(encoding='utf-8')
        if old_text not in content:
            return {"error": "Eski metin bulunamadı", "success": False}
        content = content.replace(old_text, new_text)
        Path(path).write_text(content, encoding='utf-8')
        return {"ok": True, "path": path}
    except Exception as e:
        return {"error": str(e), "success": False}

def api_call(method: str, url: str, json_data: dict = None, headers: dict = None, timeout: int = 30) -> Dict[str, Any]:
    """API çağrısı yap"""
    try:
        default_headers = {"Content-Type": "application/json"}
        if headers:
            default_headers.update(headers)
            
        response = requests.request(
            method=method.upper(),
            url=url,
            json=json_data,
            headers=default_headers,
            timeout=30
        )
        
        content_type = response.headers.get('content-type', '')
        if 'application/json' in content_type:
            data = response.json()
        else:
            data = response.text
            
        return {
            "status": response.status_code,
            "data": data,
            "success": 200 <= response.status_code < 300
        }
    except Exception as e:
        return {"error": str(e), "success": False}

def git_command(command: str, repo_path: str = ".") -> Dict[str, Any]:
    """Git komutu çalıştır"""
    full_command = f"cd {repo_path} && git {command}"
    return run_bash(full_command)

# Tool registry
TOOLS = {
    "bash": run_bash,
    "python": run_python,
    "web_search": web_search,
    "file_write": file_write,
    "file_read": file_read,
    "file_edit": file_edit,
    "api_call": api_call,
    "git": git_command,
}

def get_tool(name: str):
    """Araç getir"""
    return TOOLS.get(name)

def list_tools() -> list:
    """Mevcut araçları listele"""
    return list(TOOLS.keys())