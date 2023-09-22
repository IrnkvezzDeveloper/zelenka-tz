import click # импорт модуля для организации CLI
import sqlite3 # импорт модуля для взаимодействия с базой данных

# Инициализация подключения и получение курсора базы данных
conn = sqlite3.connect("keep.db")
cur = conn.cursor()


def create_tables():
    """Создание таблиц в базе данных при их отсутсвии
    """
    cur.execute(
        "CREATE TABLE keep (id INTEGER PRIMARY KEY AUTOINCREMENT, name_keep TEXT, desc_keep TEXT);"
    )
    conn.commit()


@click.group()
def start_cli():
    """Метод для запуска группы команд и проверки бд
    """
    cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    )
    tables = cur.fetchall()
    if not tables:
        create_tables()


@start_cli.command('create', help='Создание заметки')
@click.option('_title', '--title')
@click.option('_body', '--body')
def create_new_note(_title: str, _body: str) -> any:
    """Создание новой заметки и занесение ее в базу данных

    Args:
        title (str): Название заметки
        body (str): Контент в заметке
    """
    if _title is None or _body is None:
        raise click.UsageError("Аргументы не указаны")
    cur.execute(
        "INSERT INTO keep (name_keep, desc_keep) VALUES (?,?)", 
        (_title, _body)
    )
    conn.commit()
    click.echo('Новая заметка создана')
        


@start_cli.command('list', help='Показать заметки')
def list_all_note():
    """Показ всех созданных заметок
    """
    cur.execute("SELECT * FROM keep")
    rows = cur.fetchall()
    if len(rows) == 0:
        click.echo("Заметок не найдено")
        return
    for row in rows:
        click.echo(
            f"[{row[0]}] {row[1]}: {row[2]}"
        )


@start_cli.command('search', help='Поиск заметки')
@click.argument("_keyword")
def search_title_note(_keyword):
    """Поиск записки по его названию

    Args:
        keyword (str): слово которое есть в названии заметки
    """
    if _keyword is None:
        raise click.UsageError("Аргументы не указаны")
    cur.execute(f"SELECT * FROM keep WHERE name_keep LIKE '%{_keyword}%'")
    rows = cur.fetchall()
    if len(rows) == 0:
        click.echo("Заметок не найдено")
        return
    for row in rows:
        click.echo(
            f"[{row[0]}] {row[1]}: {row[2]}"
        )


@start_cli.command('delete', help='Удаление заметки')
@click.argument('_id')
def delete_note(_id):
    """Удаление заметки

    Args:
        id (int): Удаление заметки из базы данных
    """
    if _id is None:
        raise click.UsageError("Аргументы не указаны")
    cur.execute("DELETE FROM keep WHERE id =?", (_id,))
    conn.commit()
    click.echo('Действие было выполнено')


if __name__ == '__main__':
    start_cli()
