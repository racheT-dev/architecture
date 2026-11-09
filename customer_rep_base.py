import os
import random
from abc import ABC, abstractmethod
from typing import List, Optional
from customer import Customer
from customer_short import CustomerShort


class CustomerRepBase(ABC):
    """Абстрактный базовый класс репозитория (Пункт 3)."""

    def __init__(self, filepath: str):
        self.filepath = filepath
        self._customers: List[Customer] = []
        
        # Определяем формат по расширению
        if filepath.endswith('.json'):
            self._format = 'json'
        elif filepath.endswith('.yaml') or filepath.endswith('.yml'):
            self._format = 'yaml'
        else:
            raise ValueError(f"Неподдерживаемый формат: {filepath}. Используйте .json или .yaml")
        
        self.load_all()

    # --- Работа с форматами (вся логика здесь) ---

    def _load_data(self) -> List[dict]:
        if not os.path.exists(self.filepath):
            return []
        
        if self._format == 'json':
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        elif self._format == 'yaml':
            import yaml
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                return data if data else []
        
    def _save_data(self, data: List[dict]) -> None:
        if self._format == 'json':
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        elif self._format == 'yaml':
            import yaml
            with open(self.filepath, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, allow_unicode=True, default_flow_style=False)

    # --- Общая бизнес-логика (работает только со списком в памяти) ---

    def load_all(self) -> List[Customer]:
        """a. Чтение всех значений."""
        raw_data = self._load_data()
        self._customers = [Customer(item) for item in raw_data] if raw_data else []
        return self._customers

    def save_all(self) -> None:
        """b. Запись всех значений."""
        data = [
            {
                "inn": c.inn,
                "name": c.name,
                "address": c.address,
                "phone": c.phone,
                "contact_person": c.contact_person,
            }
            for c in self._customers
        ]
        self._save_data(data)

    def get_by_id(self, inn: str) -> Optional[Customer]:
        """c. Получить объект по ID."""
        for customer in self._customers:
            if customer.inn == inn:
                return customer
        return None

    def get_k_n_short_list(self, k: int, n: int) -> List[CustomerShort]:
        """d. Получить список k по счету n объектов класса short."""
        return [CustomerShort(c) for c in self._customers[n : n + k]]

    def sort_by_field(self, field_name: str) -> None:
        """e. Сортировать элементы по выбранному полю."""
        if not hasattr(Customer, field_name):
            raise ValueError(f"Поле {field_name} не найдено")
        self._customers.sort(key=lambda c: getattr(c, field_name))
        self.save_all()

    def _generate_new_inn(self) -> str:
        """Вспомогательный метод для генерации уникального ИНН."""
        while True:
            new_inn = str(random.randint(1000000000, 9999999999))
            if not self.get_by_id(new_inn):
                return new_inn

    def add(self, customer: Customer) -> None:
        """f. Добавить объект (сформировать новый ID)."""
        customer.inn = self._generate_new_inn()
        self._customers.append(customer)
        self.save_all()

    def replace(self, inn: str, new_customer: Customer) -> None:
        """g. Заменить элемент списка по ID."""
        for i, customer in enumerate(self._customers):
            if customer.inn == inn:
                if customer.inn != new_customer.inn:
                    new_customer.inn = self._generate_new_inn()
                self._customers[i] = new_customer
                self.save_all()
                return
        raise ValueError(f"Покупатель с ИНН {inn} не найден")

    def delete(self, inn: str) -> None:
        """h. Удалить элемент списка по ID."""
        for i, customer in enumerate(self._customers):
            if customer.inn == inn:
                del self._customers[i]
                self.save_all()
                return
        raise ValueError(f"Покупатель с ИНН {inn} не найден")

    def get_count(self) -> int:
        """i. Получить количество элементов."""
        return len(self._customers)
