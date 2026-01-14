#!/usr/bin/env python3
"""
AST анализатор для проверки структуры класса BankAccount
Проверяет:
1. Наличие класса BankAccount
2. Наличие методов: __init__, add, status, withdraw
3. Наличие переменных: account_number, balance в __init__
4. Вызов status() в __init__
"""

import ast
import sys

class BankAccountASTChecker:
    def __init__(self, filename):
        self.filename = filename
        self.tree = None
        self.bank_class = None
        self.findings = []
        self.points = 0
        self.max_points = 5
        
    def parse_file(self):
        """Парсит файл и находит класс BankAccount"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.tree = ast.parse(content)
            
            # Ищем класс BankAccount
            for node in ast.walk(self.tree):
                if isinstance(node, ast.ClassDef) and node.name == 'BankAccount':
                    self.bank_class = node
                    self.findings.append("✅ Класс BankAccount найден")
                    return True
            
            self.findings.append("❌ Класс BankAccount не найден")
            return False
            
        except FileNotFoundError:
            self.findings.append(f"❌ Файл {self.filename} не найден")
            return False
        except SyntaxError as e:
            self.findings.append(f"❌ Синтаксическая ошибка в файле: {e}")
            return False
    
    def check_methods(self):
        """Проверяет наличие требуемых методов"""
        if not self.bank_class:
            return
        
        methods = []
        for node in ast.walk(self.bank_class):
            if isinstance(node, ast.FunctionDef):
                methods.append(node.name)
        
        required_methods = ['__init__', 'add', 'status', 'withdraw']
        
        for method in required_methods:
            if method in methods:
                self.findings.append(f"✅ Метод {method}() найден")
                self.points += 1
            else:
                self.findings.append(f"❌ Метод {method}() отсутствует")
    
    def check_init_method(self):
        """Проверяет метод __init__ на наличие переменных и вызовов"""
        if not self.bank_class:
            return
        
        for node in ast.walk(self.bank_class):
            if isinstance(node, ast.FunctionDef) and node.name == '__init__':
                # Проверяем наличие переменных
                has_balance = False
                has_account_number = False
                has_status_call = False
                
                # Проверяем все присваивания в __init__
                for subnode in ast.walk(node):
                    # Проверка self.balance
                    if isinstance(subnode, ast.Assign):
                        for target in subnode.targets:
                            if (isinstance(target, ast.Attribute) and
                                isinstance(target.value, ast.Name) and
                                target.value.id == 'self'):
                                if target.attr == 'balance':
                                    has_balance = True
                                elif target.attr == 'account_number':
                                    has_account_number = True
                    
                    # Проверка вызова self.status()
                    if isinstance(subnode, ast.Expr):
                        if isinstance(subnode.value, ast.Call):
                            if (isinstance(subnode.value.func, ast.Attribute) and
                                isinstance(subnode.value.func.value, ast.Name) and
                                subnode.value.func.value.id == 'self' and
                                subnode.value.func.attr == 'status'):
                                has_status_call = True
                
                # Добавляем баллы за найденные элементы
                if has_balance:
                    self.findings.append("✅ Переменная self.balance найдена в __init__()")
                    self.points += 0.5
                else:
                    self.findings.append("❌ Переменная self.balance не найдена в __init__()")
                
                if has_account_number:
                    self.findings.append("✅ Переменная self.account_number найдена в __init__()")
                    self.points += 0.5
                else:
                    self.findings.append("❌ Переменная self.account_number не найдена в __init__()")
                
                if has_status_call:
                    self.findings.append("✅ Вызов self.status() найден в __init__()")
                    self.points += 1
                else:
                    self.findings.append("❌ Вызов self.status() не найден в __init__()")
                
                return
        
        self.findings.append("❌ Метод __init__() не найден")
    
    def run_checks(self):
        """Запускает все проверки"""
        if self.parse_file():
            self.check_methods()
            self.check_init_method()
        
        # Ограничиваем баллы максимумом
        if self.points > self.max_points:
            self.points = self.max_points
        
        return self.points, self.max_points, self.findings

def main():
    if len(sys.argv) != 2:
        print("Использование: python check_structure.py <filename>")
        sys.exit(1)
    
    filename = sys.argv[1]
    checker = BankAccountASTChecker(filename)
    points, max_points, findings = checker.run_checks()
    
    # Вывод результатов
    for finding in findings:
        print(finding)
    
    print(f"\nИтоговый балл: {points}/{max_points}")
    
    # Возвращаем код выхода
    sys.exit(0)

if __name__ == "__main__":
    main()
