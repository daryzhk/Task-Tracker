import sqlite3
from datetime import datetime
connect = sqlite3.connect("tasks.db")
connect.row_factory = sqlite3.Row
cursor = connect.cursor()

#создание таблицы
cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
status TEXT,
priority TEXT,
deadline DATE,
created_at DATE
)
''')
connect.commit()

#создание задачи
def add_task():
    name = input("\nНазвание: ")
    while True:
        print("\nСтатусы:")
        print("1. новая")
        print("2. в работе")
        print("3. завершена")
        status_choice = input("Выберите статус: ")
        if status_choice == "1":
            status = "новая"
            break
        elif status_choice == "2":
            status = "в работе"
            break
        elif status_choice == "3":
            status = "завершена"
            break
        else:
            print("Неверный выбор")
    while True:
        print("\nПриоритет:")
        print("1. низкий")
        print("2. средний")
        print("3. высокий")
        priority_choice = input("Выберите приоритет: ")
        if priority_choice == "1":
            priority = "низкий"
            break
        elif priority_choice == "2":
            priority = "средний"
            break
        elif priority_choice == "3":
            priority = "высокий"
            break
        else:
            print("Неверный выбор")
    while True:
        deadline = input("\nДедлайн (DD.MM.YYYY): ")
        try:
            deadline_check = datetime.strptime(deadline, "%d.%m.%Y").date()
            today = datetime.now().date()
            if deadline_check < today:
                print("Дедлайн не может быть в прошлом.")
            else:
                break
        except ValueError:
            print("Неверный формат даты")

    created_at = datetime.now().strftime("%d.%m.%Y")

    cursor.execute('''
        INSERT INTO tasks (name, status, priority, deadline, created_at)
        VALUES (?, ?, ?, ?, ?)
        ''', (name, status, priority, deadline, created_at))
    connect.commit()
    print("\nЗадача успешно добавлена.")

#вывод задач
def show_tasks():
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    if not tasks:
        print("\nЗадач нет")
        return
    today = datetime.now().date()
    for task in tasks:
        task_id = task["id"]
        name = task["name"]
        status = task["status"]
        priority = task["priority"]
        deadline = task["deadline"]
        created_at = task["created_at"]
        
        #проверка дедлайна
        try:
            deadline_date = datetime.strptime(deadline, "%d.%m.%Y").date()
            if deadline_date < today and status != "завершена":
                deadline_display = f"{deadline} !!!истёк срок дедлайна"
            else:
                deadline_display = deadline
        except:
            deadline_display = deadline

        print(f"\nID: {task_id}")
        print(f"Название: {name}")
        print(f"Статус: {status}")
        print(f"Приоритет: {priority}")
        print(f"Дедлайн: {deadline_display}")
        print(f"Дата создания: {created_at}")
        print("_" * 10 )

#редактирование задач 
def update_task():
    cursor.execute('SELECT id, name from tasks')
    tasks = cursor.fetchall()
    if not tasks:
        print("Нет задач")
        return
    
    print("\nЗадачи")
    for task in tasks:
            print(f"{task[0]} - {task[1]}")
    while True:
        task_id = input("\nВведите айди задачи, которую хотите отредактировать: ")
        if not task_id.isdigit():
            print("\nНужно ввести число")
            continue
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        task = cursor.fetchone()
        if task is None:
            print("\nЗадача с таким айди не найдена")
            continue
        break
    actual_id = task["id"]
    actual_name = task["name"]
    actual_status = task["status"]
    actual_priority = task["priority"]
    actual_deadline = task["deadline"]
    
    print(f"Вы выбрали задачу под номером {actual_id} с названием «{actual_name}»")
    new_name = input("\nВведите новое название (Enter - оставить без изменений)")
    if new_name == "":
        new_name = actual_name
    
    print(f"Текущий статус задачи: {actual_status}")
    print("1. новая")
    print("2. в работе")
    print("3. завершена")
    while True:
        new_status = input("\nВыберите новый статус, введя нужную цифру (Enter - оставить без изменений): ")
        if new_status == "":
            new_status = actual_status
            break
        elif new_status == "1":
            new_status = "новая"
            break
        elif new_status == "2":
            new_status = "в работе"
            break
        elif new_status == "3":
            new_status = "завершена"
            break
        else:
            print("Неверный выбор")
    
    print(f"Текущий приоритет задачи: {actual_priority}")
    print("1. низкий")
    print("2. средний")
    print("3. высокий")
    while True:
        new_priority = input("\nВыберите новый приоритет, введя нужную цифру (Enter - оставить без изменений): ")
        if new_priority == "":
            new_priority = actual_priority
            break
        elif new_priority == "1":
            new_priority = "низкий"
            break
        elif new_priority == "2":
            new_priority = "средний"
            break
        elif new_priority == "3":
            new_priority = "высокий"
            break
        else:
            print("Неверный выбор")
    
    print(f"Текущий дедлайн: {actual_deadline}")
    while True:
        new_deadline = input("\nУстановите новые сроки дедлайна в формате «DD.MM.YYYY» (Enter - оставить без изменений): ")
        if new_deadline == "":
            new_deadline = actual_deadline
            break
        try:
            deadline_check = datetime.strptime(new_deadline, "%d.%m.%Y").date()
            today = datetime.now().date()
            if deadline_check < today:
                print("Дедлайн не может быть в прошлом.")
            else:
                break
        except ValueError:
            print("Неверный формат даты")
    cursor.execute('''
        UPDATE tasks
        SET name = ?, status = ?, priority = ?, deadline = ? WHERE id = ?
        ''', (new_name, new_status, new_priority, new_deadline, actual_id))
    connect.commit()
    print("\nЗадача успешно обновлена.")

#удаление задач 
def delete_task():
    cursor.execute('SELECT id, name from tasks')
    tasks = cursor.fetchall()
    if not tasks:
        print("Нет задач")
        return
    print("\nЗадачи")
    for task in tasks:
            print(f"{task[0]} - {task[1]}")
    while True:
        task_id = input("\nВведите айди задачи, которую хотите удалить (Enter - если передумали): ")
        if task_id == "":
            print("\nВы передумали удалять задачу.")
            return
        elif not task_id.isdigit():
            print("\nНужно ввести число")
            continue
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        task = cursor.fetchone()
        if task is None:
            print("\nЗадача с таким айди не найдена")
            continue
        confrim_delete = input("\nТочно хотите удалить? (y/n): ")
        if confrim_delete.lower() != "y":
            continue
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        connect.commit()
        print("\nЗадача успешно удалена")
        break

#статистика
def statistics():
    cursor.execute('SELECT * from tasks')
    tasks = cursor.fetchall()
    if not tasks:
        print("\nЗадач нет, статистика недоступна")
        return
    
    all_tasks = len(tasks)
    active = 0
    completed = 0
    deadline_missed = 0
    
    today = datetime.now().date()
    for task in tasks:
        status = task["status"]
        deadline = task["deadline"]
        if status == "завершена":
            completed += 1
        else:
            active += 1
        deadline_date = datetime.strptime(deadline, "%d.%m.%Y").date()
        if deadline_date < today and status != "завершена":
            deadline_missed += 1
    completed_percent = round((completed / all_tasks) * 100, 2)

    print("\nСтатистика")
    print(f"Общее количество задач: {all_tasks}")
    print(f"Активные: {active}")
    print(f"Завершено: {completed}")
    print(f"Просрочено: {deadline_missed}")
    print(f"Процент выполненных задач: {completed_percent}%")

#меню
while True:
    print("\nМеню")
    print("1. Добавить задачу")
    print("2. Вывод задач")
    print("3. Отредактировать задачу")
    print("4. Удалить задачу")
    print("5. Статистика")
    print("6. Выход")
    choice = input("\nВыберите, что хотите сделать: ")
    if choice == "1":
        add_task()
    elif choice == "2":
        show_tasks()
    elif choice == "3":
        update_task()
    elif choice == "4":
        delete_task()
    elif choice == "5":
        statistics()
    elif choice == "6":
        print("Завершение работы")
        break
    else:
        print("Неверный выбор!")
connect.close()