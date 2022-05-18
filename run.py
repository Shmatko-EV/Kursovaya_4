from project.config import DevelopmentConfig
from project.server import create_app

# Создание приложения с помощью функции, находящейся в сервере.
app = create_app(DevelopmentConfig)


# @app.shell_context_processor
# def shell():
#     return {
#         "db": db,
#         "Genre": Genre,
#     }

if __name__ == '__main__':
    app.run(host="localhost", port=10001, debug=True)
