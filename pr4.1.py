import sqlite3

conn = sqlite3.connect('students.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    middle_name TEXT,
    group_name TEXT,
    grade1 REAL,
    grade2 REAL,
    grade3 REAL,
    grade4 REAL
)
''')


def input_grades(existing_grades=None):
    grades = []
    for i in range(4):
        prompt = f"Оценка {i + 1}"
        if existing_grades:
            prompt += f" ({existing_grades[i]})"
        prompt += ": "
        while True:
            val = input(prompt)
            if val == '' and existing_grades:
                grades.append(existing_grades[i])
                break
            try:
                grades.append(float(val))
                break
            except ValueError:
                print("Пожалуйста, введите число.")
    return grades


def add_student():
    first_name = input("Имя: ")
    last_name = input("Фамилия: ")
    middle_name = input("Отчество: ")
    group = input("Группа: ")
    grades = input_grades()
    cursor.execute('''
        INSERT INTO students (first_name, last_name, middle_name, group_name, grade1, grade2, grade3, grade4)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (first_name, last_name, middle_name, group, *grades))
    conn.commit()
    print("Студент добавлен.")


def view_all():
    students = cursor.execute('SELECT * FROM students').fetchall()
    if not students:
        print("Нет записей.")
        return
    for s in students:
        print(s)


def view_one():
    try:
        sid = int(input("Введите ID студента: "))
        s = cursor.execute('SELECT * FROM students WHERE id=?', (sid,)).fetchone()
        if s:
            print(s)
        else:
            print("Студент не найден.")
    except ValueError:
        print("Некорректный ввод ID.")


def edit_student():
    try:
        sid = int(input("Введите ID редактируемого студента: "))
        s = cursor.execute('SELECT * FROM students WHERE id=?', (sid,)).fetchone()
        if not s:
            print("Студент не найден.")
            return
        first_name = input(f"Имя ({s[1]}): ") or s[1]
        last_name = input(f"Фамилия ({s[2]}): ") or s[2]
        middle_name = input(f"Отчество ({s[3]}): ") or s[3]
        group = input(f"Группа ({s[4]}): ") or s[4]
        grades = input_grades(existing_grades=s[5:9])
        cursor.execute('''
            UPDATE students SET first_name=?, last_name=?, middle_name=?, group_name=?, 
            grade1=?, grade2=?, grade3=?, grade4=?
            WHERE id=?
        ''', (first_name, last_name, middle_name, group, *grades, sid))
        conn.commit()
        print("Данные обновлены.")
    except ValueError:
        print("Некорректный ввод ID.")


def delete_student():
    try:
        sid = int(input("Введите ID удаляемого студента: "))
        cursor.execute('DELETE FROM students WHERE id=?', (sid,))
        conn.commit()
        print("Студент удалён.")
    except ValueError:
        print("Некорректный ввод ID.")


def average_group():
    group = input("Введите название группы: ")
    stus = cursor.execute('SELECT * FROM students WHERE group_name=?', (group,)).fetchall()

    if not stus:
        print("Нет студентов в этой группе.")
        return

    total_scores = sum(sum(s[5:9]) for s in stus)
    total_grades_count = len(stus) * 4
    avg_score = total_scores / total_grades_count if total_grades_count else 0
    print(f"Средний балл по группе '{group}': {avg_score:.2f}")


while True:
    print("\nМеню:")
    print("1. Добавить студента")
    print("2. Посмотреть всех")
    print("3. Посмотреть по ID")
    print("4. Редактировать")
    print("5. Удалить")
    print("6. Средний по группе")
    print("0. Выход")

    choice = input("> ")

    if choice == '1':
        add_student()
    elif choice == '2':
        view_all()
    elif choice == '3':
        view_one()
    elif choice == '4':
        edit_student()
    elif choice == '5':
        delete_student()
    elif choice == '6':
        average_group()
    elif choice == '0':
        break

print("Завершение работы.")
conn.close()