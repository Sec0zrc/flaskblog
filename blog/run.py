from blog import create_app
from blog.config import Config

app = create_app(config_class=Config)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
