import yaml
import os
from typing import List
from customer_rep_base import CustomerRepBase


class CustomerRepYaml(CustomerRepBase):
    """Репозиторий для работы с YAML (Пункт 2, обновлено для Пункта 3)."""

    def __init__(self, filepath: str = "customers.yaml"):
        super().__init__(filepath)

    def _load_data(self) -> List[dict]:
        if os.path.exists(self.filepath):
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                return data if data else []
        return []

    def _save_data(self, data: List[dict]) -> None:
        with open(self.filepath, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
