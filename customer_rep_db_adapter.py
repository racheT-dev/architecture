from typing import List
from customer_rep_base import CustomerRepBase
from customer_rep_db import CustomerRepDB
from customer import Customer
from customer_short import CustomerShort


class CustomerRepDbAdapter(CustomerRepBase):
    """
    Адаптер для интеграции CustomerRepDB в иерархию CustomerRepBase (Пункт 6).
    Использует паттерн "Объектный Адаптер" через композицию.
    """

    def __init__(self):
        # Не вызываем super().__init__(), так как он пытается открыть файл.
        # Инициализируем поля базового класса вручную.
        self.filepath = "postgresql_db"
        self._customers: List[Customer] = []
        
        # Создаем экземпляр адаптируемого класса (Adaptee)
        self._adaptee = CustomerRepDB()

    # --- Адаптация абстрактных методов для совместимости с базовым классом ---

    def _load_data(self) -> List[dict]:
        """Адаптируем загрузку: читаем все данные из БД для синхронизации."""
        cursor = self._adaptee.cursor
        cursor.execute("SELECT * FROM customers")
        rows = cursor.fetchall()
        return [
            {"inn": r[0], "name": r[1], "address": r[2], "phone": r[3], "contact_person": r[4]}
            for r in rows
        ]

    def _save_data(self, data: List[dict]) -> None:
        """Адаптируем сохранение: массовая перезапись таблицы (для совместимости с save_all)."""
        cursor = self._adaptee.cursor
        conn = self._adaptee.conn
        cursor.execute("TRUNCATE TABLE customers")
        for item in data:
            cursor.execute(
                "INSERT INTO customers (inn, name, address, phone, contact_person) VALUES (%s, %s, %s, %s, %s)",
                (item["inn"], item["name"], item["address"], item["phone"], item["contact_person"])
            )
        conn.commit()

    # --- Переопределение методов для прямой работы с БД (оптимизация) ---
    # Чтобы не гонять всю таблицу туда-сюда, делегируем основные операции напрямую в БД.

    def get_by_id(self, inn: str) -> Customer:
        return self._adaptee.get_by_id(inn)

    def get_k_n_short_list(self, k: int, n: int) -> List[CustomerShort]:
        return self._adaptee.get_k_n_short_list(k, n)

    def add(self, customer: Customer) -> None:
        self._adaptee.add(customer)
        self._customers.append(customer) # Синхронизируем локальный список

    def replace(self, inn: str, new_customer: Customer) -> None:
        self._adaptee.replace(inn, new_customer)
        # Обновляем локальный список
        self._customers = [new_customer if c.inn == inn else c for c in self._customers]

    def delete(self, inn: str) -> None:
        self._adaptee.delete(inn)
        self._customers = [c for c in self._customers if c.inn != inn]

    def get_count(self) -> int:
        return self._adaptee.get_count()