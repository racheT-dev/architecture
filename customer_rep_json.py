import json
import os
from typing import List
from customer_rep_base import CustomerRepBase


class CustomerRepJson(CustomerRepBase):
    """Репозиторий для работы с JSON (Пункт 1, обновлено для Пункта 3)."""

    def __init__(self, filepath: str = "customers.json"):
        super().__init__(filepath)

    def _load_data(self) -> List[dict]:
        if os.path.exists(self.filepath):
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def _save_data(self, data: List[dict]) -> None:
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
