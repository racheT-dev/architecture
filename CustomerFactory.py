import json


class CustomerFactory:
    """
    Фабрика для парсинга данных.
    Автоматически определяет формат и преобразует в словарь.
    """

    @staticmethod
    def parse(data) -> dict:
        """
        Универсальный метод парсинга. Автоматически определяет формат.
        """
        # Если уже словарь — возвращаем как есть
        if isinstance(data, dict):
            return data
        
        # Если строка — пытаемся определить формат
        if isinstance(data, str):
            data = data.strip()
            
            # 1. JSON (начинается с {)
            if data.startswith('{'):
                return CustomerFactory._from_json(data)
            
            # 2. CSV (есть запятые, но нет |)
            elif ',' in data and '|' not in data:
                return CustomerFactory._from_csv(data)
            
            # 3. Строка с разделителем | (по умолчанию)
            elif '|' in data:
                return CustomerFactory._from_string(data)
            
            else:
                raise ValueError("Не удалось определить формат данных. Ожидается JSON, CSV или строка с разделителем '|'.")
        
        raise TypeError("Неподдерживаемый тип данных. Ожидается dict или str.")

    @staticmethod
    def _from_json(json_str: str) -> dict:
        return json.loads(json_str)

    @staticmethod
    def _from_csv(csv_str: str) -> dict:
        parts = csv_str.split(',')
        if len(parts) != 5:
            raise ValueError("Неверный формат CSV. Ожидается 5 полей через запятую.")
        return {
            "inn": parts[0].strip(),
            "name": parts[1].strip(),
            "address": parts[2].strip(),
            "phone": parts[3].strip(),
            "contact_person": parts[4].strip()
        }

    @staticmethod
    def _from_string(str_repr: str) -> dict:
        parts = str_repr.split('|')
        if len(parts) != 5:
            raise ValueError("Неверный формат строки. Ожидается 5 полей через '|'.")
        return {
            "inn": parts[0].strip(),
            "name": parts[1].strip(),
            "address": parts[2].strip(),
            "phone": parts[3].strip(),
            "contact_person": parts[4].strip()
        }