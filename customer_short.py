from customer import Customer


class CustomerShort(Customer):
    """
    Класс краткой версии покупателя (Пункт 8).
    Хранит только ИНН и Наименование.
    """

    def __init__(self, inn: str, name: str):
        """
        Конструктор краткой версии. 
        Принимает только ИНН и имя, остальное передает родителю как заглушки.
        """
        super().__init__(
            inn=inn,
            name=name,
            address="Не указан",
            phone="Не указан",
            contact_person="Не указан"
        )

    def to_full_string(self) -> str:
        """
        Переопределяем полный вывод, чтобы не показывать заглушки "Не указан".
        """
        return (
            f"Покупатель (краткая карточка):\n"
            f"  ИНН: {self.inn}\n"
            f"  Наименование: {self.name}"
        )

    def to_short_string(self) -> str:
        """
        Краткий вывод (совпадает с полным в данном случае).
        """
        return f"{self.name} (ИНН: {self.inn})"