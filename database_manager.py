import psycopg2


class DatabaseManager:
    """
    Класс-Одиночка (Singleton) для управления подключением к БД (Пункт 5).
    Гарантирует, что существует только одно активное соединение с базой данных.
    """

    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        # Если экземпляр еще не создан, создаем его
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(
        self,
        dbname: str = "architecture_lab",
        user: str = "postgres",
        password: str = "password",
        host: str = "localhost",
        port: str = "5432",
    ):
        # Инициализируем подключение только один раз
        if not self._initialized:
            try:
                self._connection = psycopg2.connect(
                    dbname=dbname, user=user, password=password, host=host, port=port
                )
                self._initialized = True
                print("✅ Подключение к БД успешно установлено (Singleton).")
            except Exception as e:
                print(f"❌ Ошибка подключения к БД: {e}")
                self._connection = None

    def get_connection(self):
        """Возвращает текущее соединение."""
        # В реальном проекте тут можно добавить проверку на разрыв связи
        return self._connection

    def close(self):
        """Метод для корректного закрытия соединения."""
        if self._connection and not self._connection.closed:
            self._connection.close()
            print("🛑 Подключение к БД закрыто.")
