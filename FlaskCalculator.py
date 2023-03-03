from flask import Flask, render_template, request
import math
import datetime

app = Flask(__name__)

class Calculator:
    def __init__(self):
        self.result = "0"
        self.counter = 0

    def calculate(self, key):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.counter >= 5:
            return "You have reached the maximum number of calculations."
        if key == "=":
            try:
                result = eval(self.result)
                self.result = str(result)
            except:
                self.result = "Error"
        elif key == "C":
            self.result = "0"
        elif key == "pi":
            self.result += str(math.pi)
        elif key in ["sin", "cos", "tan", "log"]:
            try:
                if key == "sin":
                    result = math.sin(float(self.result))
                elif key == "cos":
                    result = math.cos(float(self.result))
                elif key == "tan":
                    result = math.tan(float(self.result))
                elif key == "log":
                    result = math.log(float(self.result))
                self.result = str(result)
            except:
                self.result = "Error"
        else:
            if self.result == "0":
                self.result = key
            else:
                self.result += key

        with open("calculations.log", "a") as f:
            f.write(f"{timestamp} - {self.result}\n")

        # Increment counter and check if user is locked out
        self.counter += 1
        if self.counter >= 5:
            return "You have reached the maximum number of calculations."

        return self.result

    def show_log(self):
        with open("calculations.log", "r") as f:
            log_text = f.read()
        return log_text

calculator = Calculator()

@app.route('/')
def index():
    return render_template('calculator.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    key = request.form['key']
    result = calculator.calculate(key)
    return result

@app.route('/log')
def log():
    log_text = calculator.show_log()
    return render_template('log.html', log_text=log_text)

if __name__ == '__main__':
    app.run(debug=True)
