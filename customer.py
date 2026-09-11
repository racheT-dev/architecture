class Customer:
    """
    Класс, представляющий покупателя (независимая сущность).
    В качестве уникального бизнес-идентификатора используется ИНН.
    """

    def __init__(self, inn: str, name: str, address: str, phone: str, contact_person: str):
        # Инициализация через сеттеры для обеспечения инкапсуляции
        self.inn = inn
        self.name = name
        self.address = address
        self.phone = phone
        self.contact_person = contact_person

    # --- Инкапсуляция: ИНН (Главный уникальный идентификатор) ---
    @property
    def inn(self) -> str:
        return self._inn

    @inn.setter
    def inn(self, value: str):
        # Базовая проверка типа, детальная валидация будет в Пункте 4
        if not isinstance(value, str):
            raise TypeError("ИНН должен быть строкой")
        self._inn = value.strip()

    # --- Инкапсуляция: Name ---
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Наименование должно быть строкой")
        self._name = value.strip()

    # --- Инкапсуляция: Address ---
    @property
    def address(self) -> str:
        return self._address

    @address.setter
    def address(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Адрес должен быть строкой")
        self._address = value.strip()

    # --- Инкапсуляция: Phone ---
    @property
    def phone(self) -> str:
        return self._phone

    @phone.setter
    def phone(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Телефон должен быть строкой")
        self._phone = value.strip()

    # --- Инкапсуляция: Contact Person ---
    @property
    def contact_person(self) -> str:
        return self._contact_person

    @contact_person.setter
    def contact_person(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Контактное лицо должно быть строкой")
        self._contact_person = value.strip()