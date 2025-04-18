import sys
import functools
import sqlite3
import json
from datetime import datetime
from typing import Union, TextIO, Callable, Optional


def trace(func: Optional[Callable] = None, *,
          handle: Union[TextIO, str, sqlite3.Connection] = sys.stdout):

    if func is None:
        return lambda func: trace(func, handle=handle)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        result = func(*args, **kwargs)


        log_entry = {
            'datetime': datetime.now().isoformat(),
            'function_name': func.__name__,
            'params': {
                'args': args,
                'kwargs': kwargs
            },
            'result': result
        }


        if isinstance(handle, str) and handle.endswith('.json'):
            try:
                with open(handle, 'a+', encoding='utf-8') as f:
                    f.seek(0)
                    try:
                        data = json.load(f)
                    except (json.JSONDecodeError, FileNotFoundError):
                        data = []
                    data.append(log_entry)
                    f.seek(0)
                    f.truncate()
                    json.dump(data, f, ensure_ascii=False, indent=2)
            except Exception as e:
                print(f"JSON write error: {e}", file=sys.stderr)

        elif isinstance(handle, sqlite3.Connection):
            try:
                cur = handle.cursor()
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        datetime TEXT,
                        function_name TEXT,
                        params TEXT,
                        result TEXT
                    )
                """)
                cur.execute(
                    """INSERT INTO logs (datetime, function_name, params, result)
                       VALUES (?, ?, ?, ?)""",
                    (
                        log_entry['datetime'],
                        log_entry['function_name'],
                        json.dumps(log_entry['params'], ensure_ascii=False),
                        json.dumps(log_entry['result'], ensure_ascii=False)
                    )
                )
                handle.commit()
            except sqlite3.Error as e:
                print(f"Database error: {e}", file=sys.stderr)

        else:
            # Запись в консоль (по умолчанию)
            handle.write(f"\n[{log_entry['datetime']}] Function {func.__name__} called:\n")
            handle.write(f"  Args: {args}\n")
            handle.write(f"  Kwargs: {kwargs}\n")
            handle.write(f"  Result: {result}\n")
            handle.flush()

        return result

    return wrapper


def show_logs(db_connection: sqlite3.Connection):
    try:
        cur = db_connection.cursor()
        cur.execute("SELECT * FROM logs")
        records = cur.fetchall()

        if not records:
            print("No logs found in database")
            return

        print("\n=== Database Logs ===")
        print(f"{'ID':<5} | {'Datetime':<25} | {'Function':<15} | {'Params':<30} | {'Result'}")
        print("-" * 100)

        for record in records:
            id, dt, func_name, params, result = record
            print(f"{id:<5} | {dt:<25} | {func_name:<15} | {params[:30]:<30} | {result[:50]}...")

    except sqlite3.Error as e:
        print(f"Error reading logs: {e}", file=sys.stderr)

@trace
def multiply_by_two(x):
    """Умножает число на 2"""
    return x * 2

@trace(handle='logs.json')
def power(x, exponent=1):
    """Возводит число в указанную степень"""
    return x ** exponent

db = sqlite3.connect(":memory:")


@trace(handle=db)
def add(a, b=0):
    """Складывает два числа"""
    return a + b

multiply_by_two(10)
power(3, exponent=2)
add(5, b=3)

show_logs(db)