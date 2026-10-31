import random
from typing import List, Optional
from customer import Customer
from customer_short import CustomerShort
from database_manager import DatabaseManager  # Импортируем Одиночку


class CustomerRepDB:
    """Репозиторий для работы с PostgreSQL (Пункт 4, обновлено для Пункта 5)."""

    def __init__(self):
        # ДЕЛЕГИРОВАНИЕ: Репозиторий не создает подключение сам,
        # он просит об этом класс-Одиночку.
        self.db_manager = DatabaseManager()
        self.conn = self.db_manager.get_connection()

        if self.conn:
            self.cursor = self.conn.cursor()
        else:
            self.cursor = None
            print("⚠️ Репозиторий создан, но курсор недоступен из-за ошибки БД.")

    def get_by_id(self, inn: str) -> Optional[Customer]:
        if not self.cursor:
            return None
        self.cursor.execute("SELECT * FROM customers WHERE inn = %s", (inn,))
        row = self.cursor.fetchone()
        if row:
            return Customer(
                {
                    "inn": row[0],
                    "name": row[1],
                    "address": row[2],
                    "phone": row[3],
                    "contact_person": row[4],
                }
            )
        return None

    def get_k_n_short_list(self, k: int, n: int) -> List[CustomerShort]:
        if not self.cursor:
            return []
        self.cursor.execute("SELECT * FROM customers LIMIT %s OFFSET %s", (k, n))
        rows = self.cursor.fetchall()
        return [
            CustomerShort(
                Customer(
                    {
                        "inn": r[0],
                        "name": r[1],
                        "address": r[2],
                        "phone": r[3],
                        "contact_person": r[4],
                    }
                )
            )
            for r in rows
        ]

    def _generate_new_inn(self) -> str:
        while True:
            new_inn = str(random.randint(1000000000, 9999999999))
            if not self.get_by_id(new_inn):
                return new_inn

    def add(self, customer: Customer) -> None:
        if not self.cursor:
            return
        new_inn = self._generate_new_inn()
        customer.inn = new_inn
        self.cursor.execute(
            "INSERT INTO customers (inn, name, address, phone, contact_person) VALUES (%s, %s, %s, %s, %s)",
            (
                customer.inn,
                customer.name,
                customer.address,
                customer.phone,
                customer.contact_person,
            ),
        )
        self.conn.commit()

    def replace(self, inn: str, new_customer: Customer) -> None:
        if not self.cursor:
            return
        self.cursor.execute(
            "UPDATE customers SET inn=%s, name=%s, address=%s, phone=%s, contact_person=%s WHERE inn=%s",
            (
                new_customer.inn,
                new_customer.name,
                new_customer.address,
                new_customer.phone,
                new_customer.contact_person,
                inn,
            ),
        )
        self.conn.commit()

    def delete(self, inn: str) -> None:
        if not self.cursor:
            return
        self.cursor.execute("DELETE FROM customers WHERE inn = %s", (inn,))
        self.conn.commit()

    def get_count(self) -> int:
        if not self.cursor:
            return 0
        self.cursor.execute("SELECT COUNT(*) FROM customers")
        return self.cursor.fetchone()[0]
