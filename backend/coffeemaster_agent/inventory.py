import json
import os
import threading
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

BASE_DIR = Path(__file__).parent.absolute()
INVENTORY_FILE = BASE_DIR / "inventory.json"
HISTORY_FILE = BASE_DIR / "history.json"

DEFAULT_INVENTORY = {
    "coffee_powder_grams": 1000,
    "filters_count": 40,
    "thresholds": {
        "coffee_powder_grams": 250,
        "filters_count": 5
    },
    "staff": [
        {"name": "Gustavo Pupo", "points": 0, "badge": "Elite Barista"},
        {"name": "Rafael Peroza", "points": 0, "badge": "Coffee Enthusiast"},
        {"name": "Rafael Matta", "points": 0, "badge": "Grind Master"},
        {"name": "Nat", "points": 0, "badge": "Filter Queen"},
        {"name": "Gustavo Farag", "points": 0, "badge": "Morning Starter"},
        {"name": "Guilherme", "points": 0, "badge": "Daily Brewer"},
        {"name": "Leonardo", "points": 0, "badge": "Taste Tester"},
        {"name": "Ultramari", "points": 0, "badge": "Stock Keeper"}
    ],
    "last_buyer_index": 0,
    "consumption_config": {
        "daily_powder_grams": 180,
        "daily_filters": 2
    }
}

class InventoryManager:
    def __init__(self):
        self._lock = threading.Lock()
        self._data: Dict[str, Any] = self._load()

    def _load(self) -> Dict[str, Any]:
        if not INVENTORY_FILE.exists():
            self._save(DEFAULT_INVENTORY)
            return DEFAULT_INVENTORY
        try:
            with open(INVENTORY_FILE, "r", encoding="utf-8") as f:
                content = f.read()
                if not content.strip():
                    return DEFAULT_INVENTORY
                data = json.loads(content)
                
                # Migração: Converte estrutura antiga para v2
                if "staff_list" in data and "staff" not in data:
                    data["staff"] = [{"name": name, "points": 0, "badge": "Elite Barista"} for name in data["staff_list"]]
                    del data["staff_list"]
                    self._save(data)
                
                return data
        except (json.JSONDecodeError, IOError):
            return DEFAULT_INVENTORY

    def _save(self, data: Dict[str, Any]) -> None:
        with open(INVENTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def _log_history(self, action: str, details: Dict[str, Any]) -> None:
        history = []
        if HISTORY_FILE.exists():
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    history = json.load(f)
            except (json.JSONDecodeError, IOError):
                history = []
        
        history.append({
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details
        })
        
        # Mantém apenas os últimos 100 registros para economizar espaço
        history = history[-100:]
        
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=4, ensure_ascii=False)

    def calculate_days_left(self) -> Dict[str, int]:
        with self._lock:
            data = self._data
            powder_days = data["coffee_powder_grams"] // data["consumption_config"]["daily_powder_grams"]
            filter_days = data["filters_count"] // data["consumption_config"]["daily_filters"]
            return {
                "pó": int(powder_days),
                "filtros": int(filter_days),
                "minimo": int(min(powder_days, filter_days))
            }

    def get_status(self) -> Dict[str, Any]:
        with self._lock:
            days_left = self._calculate_days_left_unlocked()
            return {
                "pó": f"{self._data['coffee_powder_grams']}g",
                "filtros": self._data["filters_count"],
                "dias_restantes": days_left["minimo"],
                "proximo_comprador": self._data["staff"][self._data["last_buyer_index"]]["name"],
                "ranking": sorted(self._data["staff"], key=lambda x: x["points"], reverse=True)
            }

    def _calculate_days_left_unlocked(self) -> Dict[str, int]:
        data = self._data
        powder_days = data["coffee_powder_grams"] // data["consumption_config"]["daily_powder_grams"]
        filter_days = data["filters_count"] // data["consumption_config"]["daily_filters"]
        return {
            "pó": int(powder_days),
            "filtros": int(filter_days),
            "minimo": int(min(powder_days, filter_days))
        }

    def check_alerts(self) -> List[str]:
        with self._lock:
            alerts = []
            if self._data["coffee_powder_grams"] < self._data["thresholds"]["coffee_powder_grams"]:
                alerts.append("ALERTA: CAFÉ CRÍTICO!")
            if self._data["filters_count"] < self._data["thresholds"]["filters_count"]:
                alerts.append("ALERTA: FILTROS CRÍTICOS!")
            return alerts

    def update_stock(self, powder: int = 0, filters: int = 0, contributor: str = None) -> Dict[str, Any]:
        with self._lock:
            # Validação básica
            if not isinstance(powder, int) or not isinstance(filters, int):
                raise ValueError("Valores de estoque devem ser inteiros.")

            self._data["coffee_powder_grams"] = max(0, self._data["coffee_powder_grams"] + powder)
            self._data["filters_count"] = max(0, self._data["filters_count"] + filters)
            
            points_awarded = 0
            # Gamificação: Adiciona pontos se houver um contribuidor
            if contributor:
                for member in self._data["staff"]:
                    if member["name"].lower() in contributor.lower():
                        points_awarded = 10 if (powder < 0 or filters < 0) else 50
                        member["points"] += points_awarded
                        break

            self._save(self._data)
            self._log_history("update_stock", {
                "powder": powder,
                "filters": filters,
                "contributor": contributor,
                "points_awarded": points_awarded
            })
            
            status = self._get_status_unlocked()
            alerts = self._check_alerts_unlocked()
            
        return {
            "status": "success",
            "inventory": status,
            "alerts": alerts
        }

    def _get_status_unlocked(self) -> Dict[str, Any]:
        days_left = self._calculate_days_left_unlocked()
        return {
            "pó": f"{self._data['coffee_powder_grams']}g",
            "filtros": self._data["filters_count"],
            "dias_restantes": days_left["minimo"],
            "proximo_comprador": self._data["staff"][self._data["last_buyer_index"]]["name"],
            "ranking": sorted(self._data["staff"], key=lambda x: x["points"], reverse=True)
        }

    def _check_alerts_unlocked(self) -> List[str]:
        alerts = []
        if self._data["coffee_powder_grams"] < self._data["thresholds"]["coffee_powder_grams"]:
            alerts.append("ALERTA: CAFÉ CRÍTICO!")
        if self._data["filters_count"] < self._data["thresholds"]["filters_count"]:
            alerts.append("ALERTA: FILTROS CRÍTICOS!")
        return alerts

    def register_daily_prep(self, contributor: str = None) -> Dict[str, Any]:
        config = self._data["consumption_config"]
        # Se não informou o nome, o próximo da lista ganha os pontos
        if not contributor:
            with self._lock:
                contributor = self._data["staff"][self._data["last_buyer_index"]]["name"]
            
        return self.update_stock(
            powder=-config["daily_powder_grams"], 
            filters=-config["daily_filters"],
            contributor=contributor
        )

    def register_purchase(self, staff_name: str, powder: int, filters: int) -> Dict[str, Any]:
        res = self.update_stock(powder=powder, filters=filters, contributor=staff_name)
        with self._lock:
            self._data["last_buyer_index"] = (self._data["last_buyer_index"] + 1) % len(self._data["staff"])
            self._save(self._data)
        return res

# Instância Singleton para uso em todo o app
manager = InventoryManager()

# Funções de compatibilidade (Wrapper para o Agente e API)
def get_inventory(): return manager.get_status()
def update_stock(powder: int = 0, filters: int = 0): return manager.update_stock(powder, filters)
def register_daily_prep(): return manager.register_daily_prep()
def register_purchase(staff_name: str, powder: int, filters: int): return manager.register_purchase(staff_name, powder, filters)
def get_next_buyer(): return {"proximo_comprador": manager.get_status()["proximo_comprador"]}

