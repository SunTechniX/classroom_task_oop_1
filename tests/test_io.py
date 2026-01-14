#!/usr/bin/env python3
"""
Тестовый скрипт для BankAccount
Используется в GitHub Classroom
"""

import sys

def check_io():
    import os
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    # Импортируем класс из файла студента
    try:
        from task import BankAccount
    except ImportError:
        # При ошибке импорта просто выходим
        # autograding-io-grader сам обработает это как ошибку
        return

    # Читаем входные данные
    data = sys.stdin.read().strip().split()
    # data = [input(), input()]
    if len(data) != 2:
        return
    
    try:
        # Преобразуем в числа
        initial_balance = int(data[0])
        operation = int(data[1])
        
        # Создаем счет
        account = BankAccount("test_account", initial_balance)
        
        # Выполняем операцию
        if operation >= 0:
            account.add(operation)
        else:
            account.withdraw(-operation)
        
        # Выводим итоговый баланс
        account.status()
        
    except (ValueError, TypeError):
        # Неправильные типы данных
        pass
    except Exception:
        # Любая другая ошибка
        pass

if __name__ == "__main__":
    check_io()
