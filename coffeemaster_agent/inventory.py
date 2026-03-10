import json
import os
from typing import Dict, Any, List, Optional
from pathlib import Path

BASE_DIR = Path(__file__).parent.absolute()
INVENTORY_FILE = BASE_DIR / "inventory.json"

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

    def calculate_days_left(self) -> Dict[str, int]:
        data = self._data
        powder_days = data["coffee_powder_grams"] // data["consumption_config"]["daily_powder_grams"]
        filter_days = data["filters_count"] // data["consumption_config"]["daily_filters"]
        return {
            "pó": int(powder_days),
            "filtros": int(filter_days),
            "minimo": int(min(powder_days, filter_days))
        }

    def get_status(self) -> Dict[str, Any]:
        days_left = self.calculate_days_left()
        return {
            "pó": f"{self._data['coffee_powder_grams']}g",
            "filtros": self._data["filters_count"],
            "dias_restantes": days_left["minimo"],
            "proximo_comprador": self._data["staff"][self._data["last_buyer_index"]]["name"],
            "ranking": sorted(self._data["staff"], key=lambda x: x["points"], reverse=True)
        }

    def check_alerts(self) -> List[str]:
        alerts = []
        if self._data["coffee_powder_grams"] < self._data["thresholds"]["coffee_powder_grams"]:
            alerts.append("ALERTA: CAFÉ CRÍTICO!")
        if self._data["filters_count"] < self._data["thresholds"]["filters_count"]:
            alerts.append("ALERTA: FILTROS CRÍTICOS!")
        return alerts

    def update_stock(self, powder: int = 0, filters: int = 0, contributor: str = None) -> Dict[str, Any]:
        self._data["coffee_powder_grams"] = max(0, self._data["coffee_powder_grams"] + powder)
        self._data["filters_count"] = max(0, self._data["filters_count"] + filters)
        
        # Gamificação: Adiciona pontos se houver um contribuidor
        if contributor:
            for member in self._data["staff"]:
                if member["name"].lower() in contributor.lower():
                    member["points"] += 10
                    break

        self._save(self._data)
        return {
            "status": "success",
            "inventory": self.get_status(),
            "alerts": self.check_alerts()
        }

    def register_daily_prep(self, contributor: str = None) -> Dict[str, Any]:
        config = self._data["consumption_config"]
        # Se não informou o nome, o próximo da lista ganha os pontos
        if not contributor:
            contributor = self._data["staff"][self._data["last_buyer_index"]]["name"]
            
        return self.update_stock(
            powder=-config["daily_powder_grams"], 
            filters=-config["daily_filters"],
            contributor=contributor
        )

    def register_purchase(self, staff_name: str, powder: int, filters: int) -> Dict[str, Any]:
        # Compra dá mais pontos (+50)
        for member in self._data["staff"]:
            if staff_name.lower() in member["name"].lower():
                member["points"] += 50
                break
                
        res = self.update_stock(powder=powder, filters=filters)
        self._data["last_buyer_index"] = (self._data["last_buyer_index"] + 1) % len(self._data["staff"])
        self._save(self._data)
        return res

# Instância Singleton para uso em todo o app
manager = InventoryManager()

# Funções de compatibilidade (Wrapper para o Agente e API)
def get_inventory(): return manager.get_status()
def update_stock(powder: int = 0, filters: int = 0): return manager.update_stock(powder, filters)
def register_daily_prep(): return manager.register_daily_prep()
def register_purchase(staff_name: str, powder: int, filters: int): return manager.register_purchase(powder, filters)
def get_next_buyer(): return {"proximo_comprador": manager.get_status()["proximo_comprador"]}

