import yaml
import os
import random
from typing import List, Optional
from customer import Customer
from customer_short import CustomerShort


class CustomerRepYaml:
    """Репозиторий для работы с данными Customer в формате YAML (Пункт 2)."""

    def __init__(self, filepath: str = "customers.yaml"):
        self.filepath = filepath
        self._customers: List[Customer] = []
        self.load_all()

    def _generate_new_inn(self) -> str:
        """Вспомогательный метод для генерации уникального ИНН (10 цифр)."""
        while True:
            new_inn = str(random.randint(1000000000, 9999999999))
            if not self.get_by_id(new_inn):
                return new_inn

    def load_all(self) -> List[Customer]:
        """a. Чтение всех значений из файла."""
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                # Если файл пустой, yaml вернет None
                if data is None:
                    self._customers = []
                else:
                    self._customers = [Customer(item) for item in data]
        else:
            self._customers = []
        return self._customers

    def save_all(self) -> None:
        """b. Запись всех значений в файл."""
        data = [
            {
                "inn": c.inn,
                "name": c.name,
                "address": c.address,
                "phone": c.phone,
                "contact_person": c.contact_person
            } for c in self._customers
        ]
        with open(self.filepath, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)

    def get_by_id(self, inn: str) -> Optional[Customer]:
        """c. Получить объект по ID (ИНН)."""
        for customer in self._customers:
            if customer.inn == inn:
                return customer
        return None

    def get_k_n_short_list(self, k: int, n: int) -> List[CustomerShort]:
        """d. Получить список из k объектов класса Short, начиная с n-го."""
        sliced_customers = self._customers[n : n + k]
        return [CustomerShort(c) for c in sliced_customers]

    def sort_by_field(self, field_name: str) -> None:
        """e. Сортировать элементы по выбранному полю."""
        if not hasattr(Customer, field_name):
            raise ValueError(f"Поле {field_name} не найдено в классе Customer")
        self._customers.sort(key=lambda c: getattr(c, field_name))
        self.save_all()

    def add(self, customer: Customer) -> None:
        """f. Добавить объект в список (при добавлении сформировать новый ID)."""
        new_inn = self._generate_new_inn()
        customer.inn = new_inn
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
        raise ValueError(f"Покупатель с ИНН {inn} не найден для замены")

    def delete(self, inn: str) -> None:
        """h. Удалить элемент списка по ID."""
        for i, customer in enumerate(self._customers):
            if customer.inn == inn:
                del self._customers[i]
                self.save_all()
                return
        raise ValueError(f"Покупатель с ИНН {inn} не найден для удаления")

    def get_count(self) -> int:
        """i. Получить количество элементов."""
        return len(self._customers)