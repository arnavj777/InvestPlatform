import yfinance as yf

class condition():
    def __init__(self, factor, arguement):
        # Initializing Governing Factor and Arguement
        self.factor = factor
        self.arguement = arguement

    def check_condition(self, row):
        data_p = row[self.factor]
        bool_op = self.arguement[0:2]
        num = float(self.arguement[2:])
        if bool_op == "<=":
            if data_p <= num:
                return True
        elif bool_op == "==":
            if data_p == num:
                return True
        elif bool_op == ">=":
            if data_p >= num:
                return True
        return False

class condition_manager():
    def __init__(self):
        self.conditions = []

    def check_conditions(self, row):
        for c in self.conditions:
            if not c.check_condition(row):
                return False
        return True

    def add_condition(self, factor, arguement):
        self.conditions.append(condition(factor, arguement))
        print(f'condition {factor} {arguement} added')




