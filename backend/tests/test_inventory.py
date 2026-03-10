import os
import json
import pytest
from pathlib import Path
from coffeemaster_agent.inventory import InventoryManager

# Setup para isolar os testes
@pytest.fixture
def test_manager(tmp_path):
    # Sobrescreve os caminhos dos arquivos para o diretório temporário
    test_inv_file = tmp_path / "inventory_test.json"
    test_hist_file = tmp_path / "history_test.json"
    
    # Injeta os caminhos no módulo (Monkeypatching manual para o teste)
    import coffeemaster_agent.inventory as inv
    old_inv = inv.INVENTORY_FILE
    old_hist = inv.HISTORY_FILE
    inv.INVENTORY_FILE = test_inv_file
    inv.HISTORY_FILE = test_hist_file
    
    manager = InventoryManager()
    
    yield manager
    
    # Restaura os caminhos originais
    inv.INVENTORY_FILE = old_inv
    inv.HISTORY_FILE = old_hist

def test_initial_inventory(test_manager):
    status = test_manager.get_status()
    assert "pó" in status
    assert "filtros" in status
    assert status["dias_restantes"] > 0

def test_update_stock_positive(test_manager):
    initial_status = test_manager.get_status()
    initial_powder = int(initial_status["pó"].replace("g", ""))
    
    res = test_manager.update_stock(powder=500, filters=10)
    
    new_status = res["inventory"]
    new_powder = int(new_status["pó"].replace("g", ""))
    
    assert new_powder == initial_powder + 500
    assert new_status["filtros"] == initial_status["filtros"] + 10
    assert res["status"] == "success"

def test_update_stock_negative(test_manager):
    test_manager.update_stock(powder=-10000, filters=-10000)
    status = test_manager.get_status()
    
    assert status["pó"] == "0g"
    assert status["filtros"] == 0

def test_gamification_points(test_manager):
    # Pega o primeiro membro da lista
    staff_name = test_manager._data["staff"][0]["name"]
    initial_points = test_manager._data["staff"][0]["points"]
    
    # Simula uma compra (deve dar 50 pontos)
    test_manager.register_purchase(staff_name, 500, 30)
    
    assert test_manager._data["staff"][0]["points"] == initial_points + 50

def test_daily_prep_consumption(test_manager):
    initial_status = test_manager.get_status()
    initial_powder = int(initial_status["pó"].replace("g", ""))
    
    config = test_manager._data["consumption_config"]
    test_manager.register_daily_prep()
    
    new_status = test_manager.get_status()
    new_powder = int(new_status["pó"].replace("g", ""))
    
    assert new_powder == initial_powder - config["daily_powder_grams"]
    assert new_status["filtros"] == initial_status["filtros"] - config["daily_filters"]

def test_history_logging(test_manager):
    import coffeemaster_agent.inventory as inv
    
    test_manager.update_stock(powder=100, filters=5, contributor="Gustavo Pupo")
    
    assert inv.HISTORY_FILE.exists()
    with open(inv.HISTORY_FILE, "r", encoding="utf-8") as f:
        history = json.load(f)
        assert len(history) > 0
        assert history[-1]["action"] == "update_stock"
        assert history[-1]["details"]["points_awarded"] == 50
