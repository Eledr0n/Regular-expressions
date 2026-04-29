from pprint import pprint
import csv
import re


# ---------- ФУНКЦИЯ НОРМАЛИЗАЦИИ ТЕЛЕФОНА ----------
def format_phone(phone):

    pattern = re.compile(
        r"(\+7|8)\s*\(?(\d{3})\)?[\s-]*"
        r"(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})"
        r"(?:\s*\(?(доб.)\s*(\d+)\)?)?"
    )

    result = pattern.search(phone)

    if not result:
        return phone

    formatted = (
        f"+7({result.group(2)})"
        f"{result.group(3)}-{result.group(4)}-{result.group(5)}"
    )

    # добавочный номер
    if result.group(7):
        formatted += f" доб.{result.group(7)}"

    return formatted


# ---------- ЧТЕНИЕ CSV ----------
with open("phonebook_raw.csv", encoding="utf-8-sig") as f:
    rows = csv.reader(f)
    contacts_list = list(rows)

# заголовок
header = contacts_list[0]

# данные
contacts = contacts_list[1:]

processed = []


# ---------- ОБРАБОТКА КОНТАКТОВ ----------
for contact in contacts:

    # гарантируем 7 полей
    contact += [''] * (7 - len(contact))
    contact = contact[:7]

    # ---------- НОРМАЛИЗАЦИЯ ФИО ----------
    fio = " ".join(contact[:3]).split()

    lastname = fio[0] if len(fio) > 0 else ""
    firstname = fio[1] if len(fio) > 1 else ""
    surname = fio[2] if len(fio) > 2 else ""

    contact[0] = lastname
    contact[1] = firstname
    contact[2] = surname

    # ---------- НОРМАЛИЗАЦИЯ ТЕЛЕФОНА ----------
    contact[5] = format_phone(contact[5])

    processed.append(contact)


# ---------- ОБЪЕДИНЕНИЕ ДУБЛЕЙ ----------
merged = {}

for contact in processed:

    # ключ = фамилия + имя
    key = (contact[0], contact[1])

    if key not in merged:

        merged[key] = contact

    else:

        existing = merged[key]

        # заполняем только пустые поля
        for i in range(7):

            if existing[i] == "" and contact[i] != "":
                existing[i] = contact[i]


# ---------- ФИНАЛЬНЫЙ СПИСОК ----------
final_contacts = [header] + list(merged.values())


# ---------- ПРОВЕРКА ----------
print("Исходных контактов:", len(contacts))
print("После объединения:", len(final_contacts) - 1)

print("\nКлючи объединения:")
for key in merged.keys():
    print(key)

print("\nИтоговые данные:")
pprint(final_contacts)


# ---------- СОХРАНЕНИЕ CSV ----------
with open(
    "phonebook.csv",
    "w",
    encoding="utf-8-sig",
    newline=""
) as f:

    datawriter = csv.writer(f, delimiter=',')

    datawriter.writerows(final_contacts)

print("\nФайл phonebook.csv успешно сохранён.")