import re


class CustomerValidator:
    """Класс со статическими методами валидации полей Customer."""

    @staticmethod
    def _validate_string(value: str, field_name: str, min_len: int, max_len: int) -> str:
        """Универсальный метод для валидации строковых полей (Пункт 5)."""
        if not isinstance(value, str):
            raise TypeError(f"{field_name} должен быть строкой")
        
        cleaned = value.strip()
        
        if len(cleaned) < min_len:
            raise ValueError(f"{field_name} слишком короткий (минимум {min_len} символов)")
        
        if len(cleaned) > max_len:
            raise ValueError(f"{field_name} слишком длинный (максимум {max_len} символов)")
        
        return cleaned

    @staticmethod
    def validate_inn(inn: str) -> str:
        if not isinstance(inn, str):
            raise TypeError("ИНН должен быть строкой")
        cleaned = inn.strip()
        if not cleaned.isdigit():
            raise ValueError("ИНН должен содержать только цифры")
        if len(cleaned) not in (10, 12):
            raise ValueError("ИНН должен содержать 10 или 12 цифр")
        return cleaned

    @staticmethod
    def validate_name(name: str) -> str:
        return CustomerValidator._validate_string(name, "Наименование", 2, 100)

    @staticmethod
    def validate_address(address: str) -> str:
        return CustomerValidator._validate_string(address, "Адрес", 5, 255)

    @staticmethod
    def validate_phone(phone: str) -> str:
        if not isinstance(phone, str):
            raise TypeError("Телефон должен быть строкой")
        cleaned = phone.strip()
        if not re.match(r'^[\d\s\-\(\)\+]+$', cleaned):
            raise ValueError("Телефон содержит недопустимые символы")
        digits_only = re.sub(r'\D', '', cleaned)
        if len(digits_only) < 10 or len(digits_only) > 15:
            raise ValueError("Телефон должен содержать от 10 до 15 цифр")
        return cleaned

    @staticmethod
    def validate_contact_person(contact_person: str) -> str:
        return CustomerValidator._validate_string(contact_person, "Контактное лицо", 2, 100)


class Customer:
    """Класс, представляющий покупателя (независимая сущность)."""

    def __init__(self, inn: str, name: str, address: str, phone: str, contact_person: str):
        self.inn = inn
        self.name = name
        self.address = address
        self.phone = phone
        self.contact_person = contact_person

    @classmethod
    def from_dict(cls, data: dict) -> "Customer":
        """
        Единственный метод создания объекта из универсального формата (словарь).
        Парсинг из JSON/строки/CSV вынесен в отдельные классы-фабрики (паттерн Factory).
        """
        return cls(
            inn=data["inn"],
            name=data["name"],
            address=data["address"],
            phone=data["phone"],
            contact_person=data["contact_person"]
        )

    @property
    def inn(self) -> str:
        return self._inn

    @inn.setter
    def inn(self, value: str):
        self._inn = CustomerValidator.validate_inn(value)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = CustomerValidator.validate_name(value)

    @property
    def address(self) -> str:
        return self._address

    @address.setter
    def address(self, value: str):
        self._address = CustomerValidator.validate_address(value)

    @property
    def phone(self) -> str:
        return self._phone

    @phone.setter
    def phone(self, value: str):
        self._phone = CustomerValidator.validate_phone(value)

    @property
    def contact_person(self) -> str:
        return self._contact_person

    @contact_person.setter
    def contact_person(self, value: str):
        self._contact_person = CustomerValidator.validate_contact_person(value)

    def to_full_string(self) -> str:
        return (
            f"Покупатель:\n"
            f"  ИНН: {self.inn}\n"
            f"  Наименование: {self.name}\n"
            f"  Адрес: {self.address}\n"
            f"  Телефон: {self.phone}\n"
            f"  Контактное лицо: {self.contact_person}"
        )

    def to_short_string(self) -> str:
        return f"{self.name} (ИНН: {self.inn})"

    def __str__(self) -> str:
        return self.to_full_string()

    def __repr__(self) -> str:
        return f"Customer(inn='{self.inn}', name='{self.name}')"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Customer):
            return False
        return self.inn == other.inn

    def __hash__(self) -> int:
        return hash(self.inn)