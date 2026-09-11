import re


class CustomerValidator:
    """Класс со статическими методами валидации полей Customer."""

    @staticmethod
    def _validate_string(value: str, field_name: str, min_len: int, max_len: int) -> str:
        """
        Универсальный метод для валидации строковых полей.
        Устраняет дублирование кода (Пункт 5).
        """
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
        """Валидация ИНН: только цифры, длина 10 или 12."""
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
        """Валидация наименования: от 2 до 100 символов."""
        return CustomerValidator._validate_string(name, "Наименование", 2, 100)

    @staticmethod
    def validate_address(address: str) -> str:
        """Валидация адреса: от 5 до 255 символов."""
        return CustomerValidator._validate_string(address, "Адрес", 5, 255)

    @staticmethod
    def validate_phone(phone: str) -> str:
        """Валидация телефона: цифры, пробелы, скобки, тире, плюс. От 10 до 15 цифр."""
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
        """Валидация контактного лица: от 2 до 100 символов."""
        return CustomerValidator._validate_string(contact_person, "Контактное лицо", 2, 100)