import csv
from connect import get_connection


# Кесте құру
def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id         SERIAL PRIMARY KEY,
            first_name VARCHAR(50),
            last_name  VARCHAR(50),
            phone      VARCHAR(20) UNIQUE
        );
    """)
    conn.commit()
    conn.close()
    print("Таблица создана.")


# CSV ішінен қосу
def insert_from_csv():
    conn = get_connection()
    cur = conn.cursor()
    with open("contacts.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute(
                "INSERT INTO phonebook (first_name, last_name, phone) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
                (row["first_name"], row["last_name"], row["phone"])
            )
    conn.commit()
    conn.close()
    print("Контакты из CSV загружены.")


# Консольден қосу
def insert_from_console():
    first_name = input("Имя: ")
    last_name  = input("Фамилия: ")
    phone      = input("Телефон: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO phonebook (first_name, last_name, phone) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
        (first_name, last_name, phone)
    )
    conn.commit()
    conn.close()
    print("Контакт добавлен.")


# Контактіні жаңарту
def update_contact():
    old_phone = input("Телефон контакта для обновления: ")
    new_name  = input("Новое имя: ")
    new_phone = input("Новый телефон: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE phonebook SET first_name=%s, phone=%s WHERE phone=%s",
        (new_name, new_phone, old_phone)
    )
    conn.commit()
    conn.close()
    print("Контакт обновлён.")


# Контактілерді іздеу
def search_contacts():
    keyword = input("Введи имя или префикс телефона: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, first_name, last_name, phone FROM phonebook WHERE first_name ILIKE %s OR phone LIKE %s",
        (f"%{keyword}%", f"{keyword}%")
    )
    rows = cur.fetchall()
    conn.close()
    if not rows:
        print("Ничего не найдено.")
    else:
        for row in rows:
            print(f"ID:{row[0]}  {row[1]} {row[2]}  {row[3]}")


# Контактіні жою
def delete_contact():
    phone = input("Телефон контакта для удаления: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM phonebook WHERE phone=%s", (phone,))
    conn.commit()
    conn.close()
    print("Контакт удалён.")


# Негізгі мәзір
def main():
    create_table()
    while True:
        print("\n1. Загрузить из CSV")
        print("2. Добавить вручную")
        print("3. Обновить контакт")
        print("4. Найти контакт")
        print("5. Удалить контакт")
        print("0. Выход")
        choice = input("Выбор: ")

        if choice == "1":
            insert_from_csv()
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            update_contact()
        elif choice == "4":
            search_contacts()
        elif choice == "5":
            delete_contact()
        elif choice == "0":
            break

if __name__ == "__main__":
    main()