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
    print("Кесте құрылды.")


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
    print("CSV контактілері жүктелді.")


# Консольден қосу
def insert_from_console():
    first_name = input("Аты: ")
    last_name  = input("Тегі: ")
    phone      = input("Телефон: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO phonebook (first_name, last_name, phone) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
        (first_name, last_name, phone)
    )
    conn.commit()
    conn.close()
    print("Контакт қосылды.")


# Контактіні жаңарту
def update_contact():
    old_phone = input("Жаңартылатын контактінің телефоны: ")
    new_name  = input("Жаңа аты: ")
    new_phone = input("Жаңа телефон: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE phonebook SET first_name=%s, phone=%s WHERE phone=%s",
        (new_name, new_phone, old_phone)
    )
    conn.commit()
    conn.close()
    print("Контакт жаңартылды.")


# Контактілерді іздеу
def search_contacts():
    keyword = input("Атын немесе телефон префиксін енгіз: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, first_name, last_name, phone FROM phonebook WHERE first_name ILIKE %s OR phone LIKE %s",
        (f"%{keyword}%", f"{keyword}%")
    )
    rows = cur.fetchall()
    conn.close()
    if not rows:
        print("Ештеңе табылмады.")
    else:
        for row in rows:
            print(f"ID:{row[0]}  {row[1]} {row[2]}  {row[3]}")


# Контактіні жою
def delete_contact():
    phone = input("Жойылатын контактінің телефоны: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM phonebook WHERE phone=%s", (phone,))
    conn.commit()
    conn.close()
    print("Контакт жойылды.")


# Негізгі мәзір
def main():
    create_table()
    while True:
        print("\n1. CSV-тен жүктеу")
        print("2. Қолмен қосу")
        print("3. Контактіні жаңарту")
        print("4. Контактіні іздеу")
        print("5. Контактіні жою")
        print("0. Шығу")
        choice = input("Таңдау: ")

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