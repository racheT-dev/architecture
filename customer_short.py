from customer import Customer


class CustomerShort:
    """
    Класс краткой версии покупателя (Пункт 8-9).
    
    Использует паттерн Adapter (Адаптер) через композицию:
    - НЕ наследует Customer (нарушало бы принцип подстановки Лисков)
    - Содержит ссылку на объект Customer
    - Предоставляет упрощенный интерфейс только к нужным полям
    """

    def __init__(self, customer: Customer):
        """
        Конструктор принимает объект Customer (композиция).
        """
        if not isinstance(customer, Customer):
            raise TypeError("CustomerShort требует объект типа Customer")
        self._customer = customer

    @property
    def inn(self) -> str:
        """Делегируем получение ИНН объекту Customer."""
        return self._customer.inn

    @property
    def name(self) -> str:
        """Делегируем получение наименования объекту Customer."""
        return self._customer.name

    def to_full_string(self) -> str:
        """Краткая полная версия (только ИНН и имя)."""
        return (
            f"Покупатель (краткая карточка):\n"
            f"  ИНН: {self.inn}\n"
            f"  Наименование: {self.name}"
        )

    def to_short_string(self) -> str:
        """Краткая версия."""
        return f"{self.name} (ИНН: {self.inn})"

    def __str__(self) -> str:
        return self.to_short_string()

    def __repr__(self) -> str:
        return f"CustomerShort(inn='{self.inn}', name='{self.name}')"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CustomerShort):
            return False
        return self.inn == other.inn

    def __hash__(self) -> int:
        return hash(self.inn)