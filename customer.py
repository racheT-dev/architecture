from validator import CustomerValidator
import json

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

    @classmethod
    def from_json(cls, json_str: str) -> "Customer":
        """
        Создание объекта Customer из JSON-строки.
        Пример: '{"inn": "7707083893", "name": "ООО Ромашка", "address": "г. Москва", "phone": "+79991234567", "contact_person": "Иванов И.И."}'
        """
        data = json.loads(json_str)
        
        # Вызываем основной конструктор, который автоматически запустит валидацию!
        return cls(
            inn=data.get("inn", ""),
            name=data.get("name", ""),
            address=data.get("address", ""),
            phone=data.get("phone", ""),
            contact_person=data.get("contact_person", "")
        )

    @classmethod
    def from_string(cls, str_repr: str) -> "Customer":
        """
        Создание объекта Customer из строки с разделителем '|'.
        Пример: '7707083893|ООО Ромашка|г. Москва, ул. Ленина 1|+7 (999) 123-45-67|Иванов И.И.'
        """
        parts = str_repr.split("|")
        
        if len(parts) != 5:
            raise ValueError(f"Ожидается 5 полей, разделённых '|', получено {len(parts)}")
        
        # Вызываем основной конструктор, который автоматически запустит валидацию!
        return cls(
            inn=parts[0].strip(),
            name=parts[1].strip(),
            address=parts[2].strip(),
            phone=parts[3].strip(),
            contact_person=parts[4].strip()
        )