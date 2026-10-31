import psycopg2
import random
from typing import List, Optional
from customer import Customer
from customer_short import CustomerShort


class CustomerRepDB:
    """Репозиторий для работы с PostgreSQL (Пункт 4). Только сырые SQL-запросы."""

    def __init__(self, dbname: str = "architecture_lab", user: str = "postgres", 
                 password: str = "password", host: str = "localhost", port: str = "5432"):
        # Подключение к БД (в Пункте 5 мы вынесем это в Одиночку)
        self.conn = psycopg2.connect(
            dbname=dbname, user=user, password=password, host=host, port=port
        )
        self.cursor = self.conn.cursor()

    def get_by_id(self, inn: str) -> Optional[Customer]:
        """a. Получить объект по ID."""
        self.cursor.execute("SELECT * FROM customers WHERE inn = %s", (inn,))
        row = self.cursor.fetchone()
        if row:
            # Передаем словарь в конструктор Customer
            return Customer({
                "inn": row[0], "name": row[1], "address": row[2], 
                "phone": row[3], "contact_person": row[4]
            })
        return None

    def get_k_n_short_list(self, k: int, n: int) -> List[CustomerShort]:
        """b. Получить список k по счету n объектов класса short (пагинация)."""
        self.cursor.execute("SELECT * FROM customers LIMIT %s OFFSET %s", (k, n))
        rows = self.cursor.fetchall()
        
        result = []
        for row in rows:
            cust = Customer({
                "inn": row[0], "name": row[1], "address": row[2], 
                "phone": row[3], "contact_person": row[4]
            })
            result.append(CustomerShort(cust))
        return result

    def _generate_new_inn(self) -> str:
        """Генерация уникального ИНН."""
        while True:
            new_inn = str(random.randint(1000000000, 9999999999))
            if not self.get_by_id(new_inn):
                return new_inn

    def add(self, customer: Customer) -> None:
        """c. Добавить объект (сформировать новый ID)."""
        new_inn = self._generate_new_inn()
        customer.inn = new_inn  # Присваиваем через сеттер
        
        self.cursor.execute(
            "INSERT INTO customers (inn, name, address, phone, contact_person) VALUES (%s, %s, %s, %s, %s)",
            (customer.inn, customer.name, customer.address, customer.phone, customer.contact_person)
        )
        self.conn.commit()

    def replace(self, inn: str, new_customer: Customer) -> None:
        """d. Заменить элемент списка по ID."""
        # Если ИНН не менялся, просто обновляем остальные поля
        # Если менялся, обновляем и его
        self.cursor.execute(
            "UPDATE customers SET inn=%s, name=%s, address=%s, phone=%s, contact_person=%s WHERE inn=%s",
            (new_customer.inn, new_customer.name, new_customer.address, new_customer.phone, new_customer.contact_person, inn)
        )
        self.conn.commit()

    def delete(self, inn: str) -> None:
        """e. Удалить элемент списка по ID."""
        self.cursor.execute("DELETE FROM customers WHERE inn = %s", (inn,))
        self.conn.commit()

    def get_count(self) -> int:
        """f. Получить количество элементов."""
        self.cursor.execute("SELECT COUNT(*) FROM customers")
        return self.cursor.fetchone()[0]