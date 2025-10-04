class HistoryManager:
    def __init__(self):
        self.history = []
        print("Менеджер истории инициализирован")
    
    def add_record(self, expression, result):
        record = {
            'expression': expression,
            'result': result,
            'timestamp': len(self.history) + 1
        }
        self.history.append(record)
    
    def get_history(self):
        print(f"Запрошена история: {len(self.history)} записей")
        return self.history[-10:]