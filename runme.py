# coding: utf8
from app import create_app
app = create_app()
if __name__ == '__main__':

    app.jinja_env.auto_reload = True
    print(app.url_map)
    app.run()
