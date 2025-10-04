import sys
import os
import time
import socket

sys.path.append('/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/site-packages')

USE_CALCULATOR = 1
USE_HISTORY = 1
USE_WEB_INTERFACE = 1

try:
    from flask import Flask, render_template, request, jsonify
    FLASK_AVAILABLE = True
    print("Flask импортирован")
    
    app = Flask(__name__)
    
except ImportError as e:
    FLASK_AVAILABLE = False
    print(f"Flask недоступен: {e}")
    app = None

from modules.calculator import Calculator
from modules.history import HistoryManager

calculator = Calculator()
history = HistoryManager()

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def kill_port(port):
    try:
        import subprocess
        result = subprocess.run(['lsof', '-ti', f':{port}'], capture_output=True, text=True)
        if result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                subprocess.run(['kill', '-9', pid])
            print(f"Освобожден порт {port} (PID: {', '.join(pids)})")
            time.sleep(1)
    except Exception as e:
        print(f"Не удалось освободить порт: {e}")

def create_system():
    print(f"Создаем систему: Веб={USE_WEB_INTERFACE}, Калькулятор={USE_CALCULATOR}, История={USE_HISTORY}")
    
    calc = calculator if USE_CALCULATOR else None
    hist = history if USE_HISTORY else None
    
    return calc, hist

def terminal_calculator():
    calc, hist = create_system()
    
    print("\n" + "="*50)
    print("КАЛЬКУЛЯТОР - ТЕРМИНАЛЬНЫЙ РЕЖИМ")
    print("="*50)
    print("Команды:")
    print("  выражение - вычислить (например: 2+2*3)")
    print("  history  - показать историю")
    print("  config   - изменить настройки")
    print("  exit     - выход")
    print("="*50)
    
    while True:
        try:
            command = input("\nВведите команду: ").strip()
            
            if command.lower() == 'exit':
                break
            elif command.lower() == 'history':
                if hist:
                    history_data = hist.get_history()
                    if history_data:
                        print("\nИстория операций:")
                        for record in history_data:
                            print(f"  {record['expression']} = {record['result']}")
                    else:
                        print("История пуста")
                else:
                    print("История отключена")
            elif command.lower() == 'config':
                change_config_terminal()
            elif command:
                if not calc:
                    print("Калькулятор отключен")
                    continue
                
                try:
                    result = calc.evaluate(command)
                    print(f"Результат: {result}")
                    
                    if hist:
                        hist.add_record(command, result)
                        
                except Exception as e:
                    print(f"Ошибка: {e}")
                    
        except KeyboardInterrupt:
            print("\nВыход...")
            break
        except EOFError:
            break

def change_config_terminal():
    """Изменение конфигурации в терминале"""
    global USE_CALCULATOR, USE_HISTORY, USE_WEB_INTERFACE
    
    print(f"\nТекущая конфигурация:")
    print(f"1. Веб-интерфейс: {'ВКЛ' if USE_WEB_INTERFACE else 'ВЫКЛ'}")
    print(f"2. Калькулятор: {'ВКЛ' if USE_CALCULATOR else 'ВЫКЛ'}")
    print(f"3. История: {'ВКЛ' if USE_HISTORY else 'ВЫКЛ'}")
    
    try:
        choice = input("Какой параметр изменить? (1-3): ").strip()
        if choice == '1':
            old_value = USE_WEB_INTERFACE
            USE_WEB_INTERFACE = 1 - USE_WEB_INTERFACE
            print(f"Веб-интерфейс: {'ВКЛ' if USE_WEB_INTERFACE else 'ВЫКЛ'}")
            
            if USE_WEB_INTERFACE and not old_value:
                print("Освобождаем порт 5000...")
                kill_port(5000)
                
        elif choice == '2':
            USE_CALCULATOR = 1 - USE_CALCULATOR
            print(f"Калькулятор: {'ВКЛ' if USE_CALCULATOR else 'ВЫКЛ'}")
        elif choice == '3':
            USE_HISTORY = 1 - USE_HISTORY
            print(f"История: {'ВКЛ' if USE_HISTORY else 'ВЫКЛ'}")
        else:
            print("Неверный выбор")
    except:
        print("Ошибка ввода")

if FLASK_AVAILABLE:
    @app.route('/')
    def index():
        calc, hist = create_system()
        
        history_data = []
        if hist:
            history_data = hist.get_history()
        
        return render_template('index.html', 
                            calculator_enabled=USE_CALCULATOR,
                            history_enabled=USE_HISTORY,
                            history=history_data)

    @app.route('/calculate', methods=['POST'])
    def calculate():
        calc, hist = create_system()
        
        expression = request.json.get('expression', '')
        
        if not calc:
            return jsonify({'result': 'Калькулятор отключен', 'expression': expression})
        
        try:
            result = calc.evaluate(expression)
            
            if hist:
                hist.add_record(expression, result)
            
            return jsonify({'result': result, 'expression': expression})
        
        except Exception as e:
            return jsonify({'error': str(e)})

    @app.route('/history')
    def get_history():
        _, hist = create_system()
        
        if not hist:
            return jsonify({'history': [], 'enabled': False})
        
        history_data = hist.get_history()
        return jsonify({'history': history_data, 'enabled': True})

    @app.route('/config', methods=['POST'])
    def change_config_web():
        global USE_CALCULATOR, USE_HISTORY, USE_WEB_INTERFACE
        
        config = request.json
        if 'calculator' in config:
            USE_CALCULATOR = config['calculator']
        if 'history' in config:
            USE_HISTORY = config['history']
        if 'web' in config:
            old_value = USE_WEB_INTERFACE
            USE_WEB_INTERFACE = config['web']
            
            if USE_WEB_INTERFACE and not old_value:
                print("Освобождаем порт 5000...")
                kill_port(5000)
        
        return jsonify({
            'calculator': USE_CALCULATOR,
            'history': USE_HISTORY,
            'web': USE_WEB_INTERFACE
        })

    @app.route('/test/top-down')
    def test_top_down():
        global USE_CALCULATOR, USE_HISTORY
        
        steps = [
            (0, 0, "1. Только интерфейс"),
            (1, 0, "2. Интерфейс + Калькулятор"),
            (1, 1, "3. Полная система")
        ]
        
        results = []
        
        for calc, hist, desc in steps:
            USE_CALCULATOR, USE_HISTORY = calc, hist
            calc_obj, hist_obj = create_system()
            
            test_result = f"{desc}: "
            if calc_obj:
                result = calc_obj.evaluate("2 + 2")
                test_result += f"2+2={result}"
            else:
                test_result += "калькулятор отключен"
            
            if hist_obj:
                test_result += f", записей в истории: {len(hist_obj.get_history())}"
            
            results.append(test_result)
        
        return jsonify({'steps': results})

    @app.route('/test/bottom-up')
    def test_bottom_up():
        global USE_CALCULATOR, USE_HISTORY
        
        steps = [
            (0, 1, "1. Только история"),
            (1, 1, "2. История + Калькулятор"),
            (1, 1, "3. Полная система")
        ]
        
        results = []
        
        for calc, hist, desc in steps:
            USE_CALCULATOR, USE_HISTORY = calc, hist
            calc_obj, hist_obj = create_system()
            
            test_result = f"{desc}: "
            
            if hist_obj:
                hist_obj.add_record("test", "test_result")
                test_result += f"записей в истории: {len(hist_obj.get_history())}"
            
            if calc_obj:
                result = calc_obj.evaluate("3 * 3")
                test_result += f", 3*3={result}"
            
            results.append(test_result)
        
        return jsonify({'steps': results})

def main():
    if USE_WEB_INTERFACE and FLASK_AVAILABLE:
        if is_port_in_use(5000):
            print("Порт 5000 занят, освобождаем...")
            kill_port(5000)
            time.sleep(2)
        
        print("Запуск в режиме ВЕБ-ИНТЕРФЕЙСА...")
        print("Откройте: http://localhost:5000")
        try:
            app.run(debug=True, port=5000, use_reloader=False)
        except OSError as e:
            if "Address already in use" in str(e):
                print("Не удалось запустить сервер: порт 5000 занят")
                print("Попробуйте освободить порт вручную:")
                print("   lsof -ti:5000 | xargs kill -9")
                print("Или запустите программу заново")
            else:
                raise e
    else:
        if not FLASK_AVAILABLE:
            print("Flask недоступен, запуск в ТЕРМИНАЛЬНОМ режиме")
        else:
            print("Веб-интерфейс отключен, запуск в ТЕРМИНАЛЬНОМ режиме")
        terminal_calculator()

if __name__ == '__main__':
    main()