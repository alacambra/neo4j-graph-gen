from flask import Flask
import entityloader;

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/clear')
def clear():
    entityloader.clear_all()
    return 'all clean'

@app.route('/channel/<int:total_items>')
def loadChannel(total_items):
    entityloader.create_channel(total_items)
    return 'channel built'

# @app.route('/channel/')
# def loadChannelDefault():
#     entityloader.create_channel(10)
#     return 'channel built'

if __name__ == '__main__':
    app.run()
