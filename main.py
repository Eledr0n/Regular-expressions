import csv
import re
from collections import OrderedDict

def format_phone(phone):
    """Приводит телефон к формату +7(999)999-99-99, с добавочным если есть."""
    pattern = r'(\+?[78])?[\s\-]?\(?(\d{3})\)?[\s\-]?(\d{3})[\s\-]?(\d{2})[\s\-]?(\d{2})(?:\s*(?:доб\.?)\s*(\d+))?'
    m = re.search(pattern, phone)
    if m:
        base = f"+7({m.group(2)}){m.group(3)}-{m.group(4)}-{m.group(5)}"
        if m.group(6):
            base += f" доб.{m.group(6)}"
        return base
    return phone

# Читаем исходный CSV
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

header = contacts_list[0]
data = contacts_list[1:]

cleaned_data = []

# 1 и 2: Корректировка ФИО и телефонов
for row in data:
    # Объединяем первые три поля в одну строку и разбиваем на части
    full_name = " ".join(row[:3]).strip()
    parts = full_name.split()
    lastname = parts[0] if len(parts) > 0 else ""
    firstname = parts[1] if len(parts) > 1 else ""
    surname = parts[2] if len(parts) > 2 else ""

    phone = format_phone(row[5])

    # Сохраняем очищенную строку
    cleaned_row = [
        lastname,
        firstname,
        surname,
        row[3].strip(),
        row[4].strip(),
        phone,
        row[6].strip()
    ]
    cleaned_data.append(cleaned_row)

# 3: Объединение дубликатов (по совпадению фамилии и имени)
merged = OrderedDict()
for row in cleaned_data:
    key = (row[0], row[1])  # Фамилия + Имя
    if key not in merged:
        merged[key] = {
            'last': row[0],
            'first': row[1],
            'sur': row[2],
            'org': row[3],
            'pos': row[4],
            'phone': row[5],
            'email': row[6]
        }
    else:
        entry = merged[key]
        # Заполняем только те поля, которые ещё пусты
        if not entry['sur'] and row[2]:
            entry['sur'] = row[2]
        if not entry['org'] and row[3]:
            entry['org'] = row[3]
        if not entry['pos'] and row[4]:
            entry['pos'] = row[4]
        if not entry['phone'] and row[5]:
            entry['phone'] = row[5]
        if not entry['email'] and row[6]:
            entry['email'] = row[6]

# Формируем итоговый список
final_contacts = []
for key, entry in merged.items():
    final_contacts.append([
        entry['last'],
        entry['first'],
        entry['sur'],
        entry['org'],
        entry['pos'],
        entry['phone'],
        entry['email']
    ])

# Сохраняем результат
with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, delimiter=",")
    writer.writerow(header)
    writer.writerows(final_contacts)