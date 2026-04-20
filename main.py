import csv
import re
from pprint import pprint

def normalize_fio(row):
    full_name = ' '.join(row[:3]).strip()
    parts = full_name.split()
    if len(parts) == 3:
        lastname, firstname, surname = parts
    elif len(parts) == 2:
        lastname, firstname = parts
        surname = ''
    elif len(parts) == 1:
        lastname = parts[0]
        firstname = surname = ''
    else:
        lastname = firstname = surname = ''
    return [lastname, firstname, surname] + row[3:]

def normalize_phone(phone):
    if not phone:
        return ''
    pattern = r'(8|\+7|7)?\s*\(?(\d{3})\)?\s*[-]?(\d{3})[-]?(\d{2})[-]?(\d{2})(\s*\(?(доб\.?|доб|ext\.?|extension)?\s*(\d+)\)?)?'
    match = re.search(pattern, phone, re.IGNORECASE)
    if match:
        country = match.group(1)
        if country in ('8', '7'):
            country = '+7'
        elif country != '+7':
            country = '+7'
        code = match.group(2)
        part1 = match.group(3)
        part2 = match.group(4)
        part3 = match.group(5)
        extension = match.group(8)
        formatted = f"{country}({code}){part1}-{part2}-{part3}"
        if extension:
            formatted += f" доб.{extension}"
        return formatted
    return phone

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

if not contacts_list:
    print("Файл пуст")
    exit()

print("Исходные данные:")
pprint(contacts_list)
print("\n" + "="*70 + "\n")

header = contacts_list[0]
data = contacts_list[1:]

processed = []
deleted_count = 0
for row in data:
    row = normalize_fio(row)
    row[5] = normalize_phone(row[5])
    if not row[0] and not row[1]:
        deleted_count += 1
        continue
    processed.append(row)

contacts_dict = {}
for row in processed:
    key = (row[0].lower(), row[1].lower())
    if key not in contacts_dict:
        contacts_dict[key] = row[:]
    else:
        existing = contacts_dict[key]
        for i in range(len(row)):
            if row[i] and not existing[i]:
                existing[i] = row[i]

result = [header] + list(contacts_dict.values())

print("Результат после обработки (дубликаты объединены, записи без ФИО удалены):")
pprint(result)

if deleted_count:
    print(f"\nУдалено записей без ФИО: {deleted_count}")

with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerows(result)

print("\nГотово! Результат сохранён в phonebook.csv")