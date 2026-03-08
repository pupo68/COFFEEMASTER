import json
import os

INVENTORY_FILE = "inventory.json"

DEFAULT_INVENTORY = {
    "coffee_powder_grams": 0,
    "filters_count": 0,
    "thresholds": {
        "coffee_powder_grams": 250,
        "filters_count": 5
    },
    "staff_list": [
        "Gustavo Pupo", "Rafael Peroza", "Rafael Matta", "Nat",
        "Gustavo Farag", "Guilherme", "Leonardo", "Ultramari"
    ],
    "last_buyer_index": 0,
    "consumption_config": {
        "daily_powder_grams": 180,
        "daily_filters": 2
    }
}

def load_inventory():
    if not os.path.exists(INVENTORY_FILE):
        save_inventory(DEFAULT_INVENTORY)
        return DEFAULT_INVENTORY
    with open(INVENTORY_FILE, "r") as f:
        return json.load(f)

def save_inventory(data):
    with open(INVENTORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

def check_alerts(data):
    alerts = []
    if data["coffee_powder_grams"] < data["thresholds"]["coffee_powder_grams"]:
        alerts.append("ALERTA: Café baixo!")
    if data["filters_count"] < data["thresholds"]["filters_count"]:
        alerts.append("ALERTA: Filtros baixos!")
    return alerts

def update_stock(powder: int = 0, filters: int = 0):
    """Atualiza o estoque. Valores negativos subtraem."""
    data = load_inventory()
    data["coffee_powder_grams"] += powder
    data["filters_count"] += filters
    
    # Garantir que não seja negativo
    data["coffee_powder_grams"] = max(0, data["coffee_powder_grams"])
    data["filters_count"] = max(0, data["filters_count"])
    
    save_inventory(data)
    alerts = check_alerts(data)
    
    return {
        "status": "success",
        "inventory": {
            "pó": f"{data['coffee_powder_grams']}g",
            "filtros": data["filters_count"]
        },
        "alerts": alerts
    }

def register_daily_prep():
    """Abatimento automático das 2 garrafas diárias (3L totais)."""
    data = load_inventory()
    config = data["consumption_config"]
    
    return update_stock(
        powder=-config["daily_powder_grams"], 
        filters=-config["daily_filters"]
    )

def get_next_buyer():
    """Informa quem é o próximo comprador da lista."""
    data = load_inventory()
    idx = data["last_buyer_index"]
    return {"proximo_comprador": data["staff_list"][idx]}

def register_purchase(staff_name: str, powder: int, filters: int):
    """Registra compra, atualiza estoque e rotaciona comprador."""
    data = load_inventory()
    
    # Atualiza estoque primeiro
    res = update_stock(powder=powder, filters=filters)
    
    # Rotaciona o comprador (modulo lista)
    data = load_inventory() # Recarrega para ter estoque atualizado
    data["last_buyer_index"] = (data["last_buyer_index"] + 1) % len(data["staff_list"])
    save_inventory(data)
    
    res["mensagem"] = f"Compra registrada por {staff_name}."
    res["proximo_comprador"] = data["staff_list"][data["last_buyer_index"]]
    return res

def get_inventory():
    data = load_inventory()
    return {
        "pó": f"{data['coffee_powder_grams']}g",
        "filtros": data["filters_count"],
        "proximo_comprador": data["staff_list"][data["last_buyer_index"]]
    }
