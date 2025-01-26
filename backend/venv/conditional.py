import yfinance as yf

class condition():
    def __init__(self, factor, arguement):
        # Initializing Governing Factor and Arguement
        self.factor = factor
        self.arguement = arguement

    def check_condition(self, row):
        data_p = row[self.factor]
        ints = ['0','1','2','3','4','5','6','7','8','9']
        int_i=1
        for i in range(len(self.arguement)):
            if self.arguement[i] in ints:
                int_i = i
                break
        bool_op = self.arguement[0:int_i]
        num = float(self.arguement[int_i:])
        if bool_op == "<=":
            if data_p <= num:
                return True
        elif bool_op == "=":
            if data_p == num:
                return True
        elif bool_op == ">=":
            if data_p >= num:
                return True
        elif bool_op == ">":
            if data_p > num:
                return True
        elif bool_op == "<":
            if data_p < num:
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
    
    def delete_condition(self, factor, arguement):
        i = 0
        while i < len(self.conditions):
            if self.conditions[i].factor == factor and self.conditions[i].arguement == arguement:
                self.conditions.pop(i)
                i -= 1
            i += 1




