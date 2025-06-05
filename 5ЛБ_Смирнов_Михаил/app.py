from flask import Flask
from controllers import index_controller, update_controller

app = Flask(__name__)

@app.route('/')
def index():
    return index_controller()

@app.route('/update', methods=['GET', 'POST'])
def update():
    return update_controller()

if __name__ == '__main__':
    app.run(debug=True) 