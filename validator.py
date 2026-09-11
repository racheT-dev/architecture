import re


class CustomerValidator:
    """Класс со статическими методами валидации полей Customer."""

    @staticmethod
    def validate_inn(inn: str) -> str:
        """
        Валидация ИНН: только цифры, длина 10 или 12.
        """
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
        """
        Валидация наименования: минимум 2 символа, максимум 100.
        """
        if not isinstance(name, str):
            raise TypeError("Наименование должно быть строкой")
        
        cleaned = name.strip()
        
        if len(cleaned) < 2:
            raise ValueError("Наименование слишком короткое (минимум 2 символа)")
        
        if len(cleaned) > 100:
            raise ValueError("Наименование слишком длинное (максимум 100 символов)")
        
        return cleaned

    @staticmethod
    def validate_address(address: str) -> str:
        """
        Валидация адреса: минимум 5 символов, максимум 255.
        """
        if not isinstance(address, str):
            raise TypeError("Адрес должен быть строкой")
        
        cleaned = address.strip()
        
        if len(cleaned) < 5:
            raise ValueError("Адрес слишком короткий (минимум 5 символов)")
        
        if len(cleaned) > 255:
            raise ValueError("Адрес слишком длинный (максимум 255 символов)")
        
        return cleaned

    @staticmethod
    def validate_phone(phone: str) -> str:
        """
        Валидация телефона: допускаются цифры, пробелы, скобки, тире, плюс.
        Должно быть от 10 до 15 цифр.
        """
        if not isinstance(phone, str):
            raise TypeError("Телефон должен быть строкой")
        
        cleaned = phone.strip()
        
        # Проверяем допустимые символы
        if not re.match(r'^[\d\s\-\(\)\+]+$', cleaned):
            raise ValueError("Телефон содержит недопустимые символы")
        
        # Считаем только цифры
        digits_only = re.sub(r'\D', '', cleaned)
        
        if len(digits_only) < 10:
            raise ValueError("Телефон должен содержать минимум 10 цифр")
        
        if len(digits_only) > 15:
            raise ValueError("Телефон должен содержать максимум 15 цифр")
        
        return cleaned

    @staticmethod
    def validate_contact_person(contact_person: str) -> str:
        """
        Валидация контактного лица: минимум 2 символа, максимум 100.
        """
        if not isinstance(contact_person, str):
            raise TypeError("Контактное лицо должно быть строкой")
        
        cleaned = contact_person.strip()
        
        if len(cleaned) < 2:
            raise ValueError("Контактное лицо слишком короткое (минимум 2 символа)")
        
        if len(cleaned) > 100:
            raise ValueError("Контактное лицо слишком длинное (максимум 100 символов)")
        
        return cleaned