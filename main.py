'''https://www.youtube.com/watch?v=crUHP8Zo12k'''

from flask import Flask, render_template, url_for, request, redirect  # импортировали класс Flask  и ф-цию render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)  # Cоздаём экземпляр этого класса.
# Первый аргумент - это имя модуля или пакета приложения.
# Если вы используете единственный модуль (как в этом примере),
# вам следует использовать __name__, потому что в зависимости от того,
# запущен ли код как приложение, или был импортирован как модуль,
# это имя будет разным
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db' # Подключение к нужной базе данных
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) # Предаем объект в котором проинициализирована база данных

class Article(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id  # Когда мы будем выбирать какой либо объект на основе этого класса, то у нас будет выдаваться сам объект и плюс его id  

@app.route('/')  # Создаем ДЕКОРАТОР route(), чтобы сказать Flask, какой из URL должен запускать нашу функцию Создание еще одного декоратора позволяет отслеживатьт дополнительный URL-адрес для ф-ции ниже
@app.route('/home')
def index():  # Функция (главной страницы), которой дано имя, используемое также для генерации URL-адресов
                                          # для этой конкретной функции, возвращает сообщение,
    return render_template('index.html')  # которое мы хотим отобразить в браузере пользователя
    
@app.route('/about')  # Декоратор для передачи Flask URL побочной страницы
def about():          # Функция (Побочной страницы)
    return render_template("about.html")

'''
# Позволяет находить в URL переданные аргументы по заданным типам данных
@app.route('/user/<string:name>/<int:id>')
def user(name, id):                                # Функция (Побочной страницы)
    return "User page: " + name + '-' + str(id)
'''
@app.route('/create-article', methods=['POST', 'GET'])  
def create_article(): 
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
    
        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/')
        except:
            return 'An error occurred while adding the article'

    else:
        return render_template("create-article.html")


if __name__ == "__main__":  # Наконец, для запуска локального сервера с нашим приложением,
    app.run(debug=True)     # мы используем функцию run().
    # Благодаря конструкции if __name__ == '__main__' можно быть уверенным,
    # что сервер запустится только при непосредственном вызове скрипта из
    # интерпретатора Python, а не при его импортировании в качестве модуля.
    # debug - позволяет запускать сервер в режиме разработчика,
    # что позволяет серверу перезагружать себя при изменении кода, а также
    # при возникновении ошибок сообщит о них
