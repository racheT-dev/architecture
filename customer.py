from validator import CustomerValidator


class Customer:
    """Класс, представляющий покупателя (независимая сущность)."""

    def __init__(self, inn: str, name: str, address: str, phone: str, contact_person: str):
        """
        Конструктор класса Customer.
        Все поля валидируются через CustomerValidator.
        Если данные невалидны, объект НЕ будет создан (выбросится ValueError).
        """
        # Валидация и присваивание через сеттеры
        self.inn = inn
        self.name = name
        self.address = address
        self.phone = phone
        self.contact_person = contact_person

    # --- Инкапсуляция: INN ---
    @property
    def inn(self) -> str:
        return self._inn

    @inn.setter
    def inn(self, value: str):
        self._inn = CustomerValidator.validate_inn(value)

    # --- Инкапсуляция: Name ---
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = CustomerValidator.validate_name(value)

    # --- Инкапсуляция: Address ---
    @property
    def address(self) -> str:
        return self._address

    @address.setter
    def address(self, value: str):
        self._address = CustomerValidator.validate_address(value)

    # --- Инкапсуляция: Phone ---
    @property
    def phone(self) -> str:
        return self._phone

    @phone.setter
    def phone(self, value: str):
        self._phone = CustomerValidator.validate_phone(value)

    # --- Инкапсуляция: Contact Person ---
    @property
    def contact_person(self) -> str:
        return self._contact_person

    @contact_person.setter
    def contact_person(self, value: str):
        self._contact_person = CustomerValidator.validate_contact_person(value)