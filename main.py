import csv
import re



def format_phone(phone):

    phone_pattern = re.compile(
        r"(\+7|8)\s*"
        r"\(?(\d{3})\)?[\s-]*"
        r"(\d{3})[\s-]*"
        r"(\d{2})[\s-]*"
        r"(\d{2})"
        r"(?:\s*\(?(доб.)\s*(\d+)\)?)?"
    )

    result = phone_pattern.search(phone)

    # если телефон не подошёл под шаблон
    if not result:
        return phone

    formatted_phone = (
        f"+7({result.group(2)})"
        f"{result.group(3)}-"
        f"{result.group(4)}-"
        f"{result.group(5)}"
    )

    # добавочный номер
    if result.group(7):
        formatted_phone += f" доб.{result.group(7)}"

    return formatted_phone


with open("phonebook_raw.csv", encoding="utf-8-sig") as f:

    reader = csv.reader(f)

    contacts_list = list(reader)



header = contacts_list[0]

raw_contacts = contacts_list[1:]



normalized_contacts = []

for contact in raw_contacts:

    # гарантируем ровно 7 полей
    contact += [''] * (7 - len(contact))
    contact = contact[:7]

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

    contact[5] = format_phone(contact[5])

    normalized_contacts.append(contact)


merged_contacts = {}

for contact in normalized_contacts:

    # ключ = фамилия + имя
    key = (contact[0], contact[1])

    # если контакт новый
    if key not in merged_contacts:

        merged_contacts[key] = contact

    # если дубль найден
    else:

        existing_contact = merged_contacts[key]

        # объединяем поля
        for i in range(7):

            # если поле пустое — заполняем
            if existing_contact[i] == "" and contact[i] != "":

                existing_contact[i] = contact[i]


final_contacts = [header] + list(merged_contacts.values())


with open(
    "phonebook.csv",
    "w",
    encoding="utf-8-sig",
    newline=""
) as f:

    writer = csv.writer(f, delimiter=",")

    writer.writerows(final_contacts)


print("\nФайл phonebook.csv успешно создан.")