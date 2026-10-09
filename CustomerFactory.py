import json
from customer import Customer


class CustomerFactory:
    """
    Фабрика для создания объектов Customer из разных форматов.
    Паттерн Factory Method — выносит логику парсинга из класса Customer.
    """

    @staticmethod
    def from_json(json_str: str) -> Customer:
        """Создание Customer из JSON-строки."""
        data = json.loads(json_str)
        return Customer.from_dict(data)

    @staticmethod
    def from_string(str_repr: str) -> Customer:
        """Создание Customer из строки с разделителем '|'."""
        parts = str_repr.split("|")
        if len(parts) != 5:
            raise ValueError(f"Ожидается 5 полей, разделённых '|', получено {len(parts)}")
        
        data = {
            "inn": parts[0].strip(),
            "name": parts[1].strip(),
            "address": parts[2].strip(),
            "phone": parts[3].strip(),
            "contact_person": parts[4].strip()
        }
        return Customer.from_dict(data)