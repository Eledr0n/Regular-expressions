from pprint import pprint
import csv
import re

# ---------- ЧТЕНИЕ CSV ----------
with open("phonebook_raw.csv", encoding="utf-8-sig") as f:
    rows = csv.reader(f)
    contacts_list = list(rows)

header = contacts_list[0]
contacts = contacts_list[1:]

# ---------- НОРМАЛИЗАЦИЯ ФИО ----------
processed = []

for contact in contacts:

    # гарантируем 7 полей
    contact += [''] * (7 - len(contact))
    contact = contact[:7]

    # собираем ФИО
    fio = " ".join(contact[:3]).split()

    lastname = ""
    firstname = ""
    surname = ""

    if len(fio) > 0:
        lastname = fio[0]

    if len(fio) > 1:
        firstname = fio[1]

    if len(fio) > 2:
        surname = fio[2]

    contact[0] = lastname
    contact[1] = firstname
    contact[2] = surname

    # ---------- НОРМАЛИЗАЦИЯ ТЕЛЕФОНА ----------
    phone_pattern = re.compile(
        r"(\+7|8)\s*\(?(\d{3})\)?[\s-]*"
        r"(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})"
        r"(\s*\(?(доб.)\s*(\d+)\)?)?"
    )

    contact[5] = phone_pattern.sub(
        r"+7(\2)\3-\4-\5 \7\8",
        contact[5]
    ).strip()

    processed.append(contact)

# ---------- ОБЪЕДИНЕНИЕ ДУБЛЕЙ ----------
merged = {}

for contact in processed:

    key = (contact[0], contact[1])

    if key not in merged:
        merged[key] = contact

    else:
        existing = merged[key]

        for i in range(7):

            # если текущее поле пустое — заполняем
            if existing[i] == "" and contact[i] != "":
                existing[i] = contact[i]

            # если данные разные — сохраняем более длинное значение
            elif (
                existing[i] != contact[i]
                and contact[i] != ""
                and len(contact[i]) > len(existing[i])
            ):
                existing[i] = contact[i]

# ---------- ФИНАЛЬНЫЙ СПИСОК ----------
final_contacts = [header] + list(merged.values())

# проверка
print("Исходных контактов:", len(contacts))
print("После обработки:", len(final_contacts) - 1)

print("\nКлючи объединения:")
for key in merged.keys():
    print(key)

print("\nРезультат:")
pprint(final_contacts)

# ---------- СОХРАНЕНИЕ CSV ----------
with open(
    "phonebook.csv",
    "w",
    encoding="utf-8-sig",
    newline=""
) as f:

    writer = csv.writer(f)
    writer.writerows(final_contacts)