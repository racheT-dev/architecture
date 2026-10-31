import json
import os
from typing import List, Optional
from customer import Customer
from customer_short import CustomerShort


class CustomerRepJson:
    """Репозиторий для работы с данными Customer в формате JSON (Пункт 1)."""

    def __init__(self, filepath: str = "customers.json"):
        self.filepath = filepath
        self._customers: List[Customer] = []
        self.load_all()

    def load_all(self) -> List[Customer]:
        """a. Чтение всех значений из файла."""
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Преобразуем словари обратно в объекты Customer
                self._customers = [
                    Customer(
                        inn=item["inn"],
                        name=item["name"],
                        address=item["address"],
                        phone=item["phone"],
                        contact_person=item["contact_person"]
                    ) for item in data
                ]
        else:
            self._customers = []
        return self._customers

    def save_all(self) -> None:
        """b. Запись всех значений в файл."""
        # Преобразуем объекты в словари для сериализации
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
            json.dump(data, f, ensure_ascii=False, indent=4)

    def get_by_id(self, inn: str) -> Optional[Customer]:
        """c. Получить объект по ID (в нашем случае ID = ИНН)."""
        for customer in self._customers:
            if customer.inn == inn:
                return customer
        return None

    def get_k_n_short_list(self, k: int, n: int) -> List[CustomerShort]:
        """
        d. Получить список из k объектов класса Short, начиная с n-го по счету.
        (Пагинация: n - индекс начала, k - количество).
        """
        # Берем срез списка и оборачиваем каждый элемент в CustomerShort (Адаптер)
        sliced_customers = self._customers[n : n + k]
        return [CustomerShort(c) for c in sliced_customers]

    def sort_by_field(self, field_name: str) -> None:
        """e. Сортировать элементы по выбранному полю."""
        # Проверяем, что поле существует и является строкой или числом
        if not hasattr(Customer, field_name):
            raise ValueError(f"Поле {field_name} не найдено в классе Customer")
        
        # Сортируем внутренний список
        self._customers.sort(key=lambda c: getattr(c, field_name))
        # После сортировки лучше сразу сохранить изменения
        self.save_all()

    def add(self, customer: Customer) -> None:
        """f. Добавить объект в список (проверка уникальности ID/ИНН)."""
        if self.get_by_id(customer.inn) is not None:
            raise ValueError(f"Покупатель с ИНН {customer.inn} уже существует")
        
        self._customers.append(customer)
        self.save_all()

    def replace(self, inn: str, new_customer: Customer) -> None:
        """g. Заменить элемент списка по ID."""
        for i, customer in enumerate(self._customers):
            if customer.inn == inn:
                # Проверяем, что новый ИНН либо совпадает со старым, либо тоже уникален
                if inn != new_customer.inn and self.get_by_id(new_customer.inn) is not None:
                    raise ValueError(f"Покупатель с новым ИНН {new_customer.inn} уже существует")
                
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