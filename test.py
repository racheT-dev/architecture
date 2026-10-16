from customer import Customer
from customer_short import CustomerShort

print("--- 1. Создание из JSON-строки ---")
json_data = '{"inn": "7707083893", "name": "ООО Ромашка", "address": "г. Москва, ул. Ленина 1", "phone": "+7 (999) 123-45-67", "contact_person": "Иванов И.И."}'
c1 = Customer(json_data)  # Фабрика сама поймет, что это JSON
print(c1.to_short_string())

print("\n--- 2. Создание из CSV-строки ---")
csv_data = "7707083894, ЗАО Вектор, г. СПб Невский 1, +78121112233, Сидоров С.С."
c2 = Customer(csv_data)  # Фабрика сама поймет, что это CSV
print(c2.to_short_string())

print("\n--- 3. Создание из строки с разделителем '|' ---")
str_data = "7707083895|ИП Сидоров|г. Екатеринбург, ул. Мира 5|+73431112233|Сидоров А.В."
c3 = Customer(str_data)  # Фабрика сама поймет, что это строка
print(c3.to_short_string())

print("\n--- 4. Проверка валидации (плохой ИНН) ---")
try:
    bad_c = Customer('{"inn": "123", "name": "Тест", "address": "ул. 1", "phone": "+79991234567", "contact_person": "Иван"}')
except ValueError as e:
    print(f"✅ Ошибка поймана: {e}")

print("\n--- 5. Краткая версия (Адаптер) ---")
short = CustomerShort(c1)
print("Вывод:", short)
print("Делегирование ИНН:", short.inn)