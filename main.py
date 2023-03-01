from flask import Flask, url_for, request, render_template, redirect
from flask_login import LoginManager, login_user, login_required, logout_user

from data import db_session
from data.jobs import Jobs
from data.users import User
from data.departments import Department
from forms.job import JobForm

from forms.login_form import LoginForm
from forms.user import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@login_required
@app.route('/addjob', methods=['GET', 'POST'])
def addjob():
    form = JobForm()
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    form.team_leader.choices = [(i.id, i.name) for i in users]
    if form.validate_on_submit():
        job = Jobs(
            job=form.job.data,
            work_size=form.work_size.data,
            team_leader=form.team_leader.data,
            is_finished=form.is_finished.data)
        if form.collaborators.data:
            job.collaborators = form.collaborators.data
        if form.start_date.data:
            job.start_date = form.start_date.data
        if form.end_date.data:
            job.end_date = form.end_date.data

        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('jobs.html', title='Добавление работы', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            surname=form.surname.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data

        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/')
@app.route('/index/')
def index(title="Журнал работ"):
    session = db_session.create_session()
    jobs = session.query(Jobs).all()

    return render_template('index.html', title=title, jobs=jobs)


@app.route('/training/<prof>')
def training(prof):
    return render_template('training.html', prof=prof, title='Тренировки в полёте')


@app.route('/answer')
@app.route('/auto_snswer')
def answer():
    param = {"title": "Автоматический ответ",
             "surname": "Watny",
             "name": "Mark",
             "education": "выше среднего",
             "profession": "штурман марсохода",
             "sex": "male",
             "motivation": "Всегда мечтал застрять на Марсе!",
             "ready": "True"}
    return render_template("auto_answer.html", **param)


@app.route('/list_prof/')
@app.route('/list_prof/<prof>')
def list_prof(prof='ol'):
    professions = ['инженер-исследователь', 'пилот', 'строитель', 'экзобиолог', 'врач',
                   'инженер по терраформированию', 'климатолог',
                   'специалист по радиационной защите', 'астрогеолог', 'гляциолог',
                   'инженер жизнеобеспечения', 'метеоролог', 'оператор марсохода', 'киберинженер',
                   'штурман', 'пилот дронов']
    return render_template('list_prof.html', prof=prof, title='Список', professions=professions)


@app.route('/promotion')
def promotion():
    a = ["Человечество вырастает из детства.</p>",
         "Человечеству мала одна планета.</p>",
         "Мы сделаем обитаемыми безжизненные пока планеты.</p>",
         "И начнем с Марса!</p>",
         "Присоединяйся!</p>"]
    return f"""<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <title>Рекламная кампания</title>
                  </head>
                  <body>
                    <h2>{'<p>'.join(a)}</h2>
                  </body>
                </html>"""


@app.route('/image_mars')
def image_mars():
    return f"""<!doctype html>
                    <html lang="en">
                      <head>
                        <meta charset="utf-8">
                        <title>Привет, Марс!</title>
                      </head>
                      <body>
                        <h1>Жди нас, Марс!</h1>
                        <img src="{url_for('static', filename='img/mars.png')}" 
                            alt="здесь должна была быть картинка, но не нашлась">
                        <p>Вот она какая, красная планета.</p>
                      </body>
                    </html>"""


@app.route('/promotion_image')
def promotion_image():
    return f"""<!doctype html>
                    <html lang="en">
                      <head>
                        <meta charset="utf-8">
                        <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                        <link rel="stylesheet"
                        href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                        integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                        crossorigin="anonymous">
                        <title>Реклама с картинкой</title>
                      </head>
                      <body>
                        <h1>Жди нас, Марс!</h1>
                        <img src="{url_for('static', filename='img/mars.png')}" 
                            width="300" height="300" 
                            alt="здесь должна была быть картинка, но не нашлась">
                        <div class="alert alert-secondary" role="alert">Человечество вырастает из детства.</div>
                        <div class="alert alert-success" role="alert">Человечеству мала одна планета.</div>
                        <div class="alert alert-secondary" role="alert">Мы сделаем обитаемыми безжизненные пока планеты.</div>
                        <div class="alert alert-warning" role="alert">И начнем с Марса!</div>
                        <div class="alert alert-danger" role="alert">Присоединяйся!</div>
                      </body>
                    </html>"""


@app.route('/form_sample', methods=['POST', 'GET'])
def form_sample():
    if request.method == 'GET':
        return f'''<!doctype html>
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                            <link rel="stylesheet"
                            href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                            integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                            crossorigin="anonymous">
                            <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                            <title>Отбор астронавтов</title>
                          </head>
                          <body>
                            <h1 align="center">Анкета претендента</h1>
                            <h2 align="center">на участие в миссии</h2>
                            <div>
                                <form class="login_form" method="post">
                                    <input type="text" class="form-control" id="email" aria-describedby="emailHelp" placeholder="Введите фамилию" name="surname">
                                    <input type="text" class="form-control" id="password" placeholder="Введите имя" name="name">
                                    <p></p>
                                    <input type="email" class="form-control" id="email" aria-describedby="emailHelp" placeholder="Введите адрес почты" name="email">
                                    <div class="form-group">
                                        <label for="educationSelect">Какое у Вас образование</label>
                                        <select class="form-control" id="educationSelect" name="education">
                                          <option>Начальное</option>
                                          <option>Основное</option>
                                          <option>Среднее</option>
                                          <option>Среднее профессиональное</option>
                                          <option>Высшее</option>
                                        </select>
                                    </div>
                                    <div class="form-group">
                                        <label for="professionSelect">Какие у Вас профессии</label>
                                        <div>
                                            <input type="checkbox" id="in-is" name="in-is" checked>
                                            <label for="in-is">Инженер-исследователь</label>
                                        </div>

                                        <div>
                                          <input type="checkbox" id="pilot" name="pilot">
                                          <label for="pilot">Пилот</label>
                                        </div>

                                        <div>
                                          <input type="checkbox" id="climat" name="climat">
                                          <label for="climat">Климатолог</label>
                                        </div>

                                        <div>
                                          <input type="checkbox" id="doctor" name="doctor">
                                          <label for="doctor">Врач</label>
                                        </div>

                                        <div>
                                          <input type="checkbox" id="builder" name="builder">
                                          <label for="builder">Строитель</label>
                                        </div>

                                        <div>
                                          <input type="checkbox" id="exobio" name="exobio">
                                          <label for="exobio">Экзобиолог</label>
                                        </div>
                                    </div>
                                    <div class="form-group">
                                        <label for="form-check">Укажите пол</label>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="sex" id="male" value="male" checked>
                                          <label class="form-check-label" for="male">
                                            Мужской
                                          </label>
                                        </div>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="sex" id="female" value="female">
                                          <label class="form-check-label" for="female">
                                            Женский
                                          </label>
                                        </div>
                                    </div>
                                    <div class="form-group">
                                        <label for="quest">Почему вы хотите принять участие в миссии?</label>
                                        <textarea class="form-control" id="quest" rows="3" name="quest"></textarea>
                                    </div>
                                    <div class="form-group">
                                        <label for="photo">Приложите фотографию</label>
                                        <input type="file" class="form-control-file" id="photo" name="file">
                                    </div>

                                    <div class="form-group form-check">
                                        <input type="checkbox" class="form-check-input" id="acceptRules" name="accept">
                                        <label class="form-check-label" for="acceptRules">Готовы ли остаться на Марсе?</label>
                                    </div>
                                    <button type="submit" class="btn btn-primary">Записаться</button>
                                </form>
                            </div>
                          </body>
                        </html>'''
    elif request.method == 'POST':
        print(request.form.get('surname'))
        print(request.form.get('name'))
        print(request.form.get('email'))
        print(request.form.get('education'))
        print(request.form.get('in-is', 'off'))
        print(request.form.get('pilot', 'off'))
        print(request.form.get('climat', 'off'))
        print(request.form.get('doctor', 'off'))
        print(request.form.get('builder', 'off'))
        print(request.form.get('exobio', 'off'))
        print(request.form.get('sex'))
        print(request.form.get('quest'))
        print(request.form.get('file'))
        print(request.form.get('accept'))
        return "<h1>Форма отправлена<h1>"


def user_create():
    session = db_session.create_session()
    user = User(surname="Scott",
                name="Ridley",
                age="21",
                position="captain",
                speciality="research engineer",
                address="module_1",
                email="scott_chief@mars.org")
    session.add(user)
    user = User(surname="Harry",
                name="Potter",
                age="14",
                position="mag",
                speciality="engineer",
                address="module_1",
                email="Harry@mars.org")
    session.add(user)
    user = User(surname="John",
                name="DSD",
                age="67",
                position="doctor",
                speciality="med",
                address="module_2",
                email="med@mars.org")
    session.add(user)
    user = User(surname="Somebody",
                name="Bds",
                age="67",
                position="Something",
                speciality="some",
                address="module_5",
                email="some@mars.org")
    session.add(user)
    session.commit()


def jobs_create():
    session = db_session.create_session()
    job = Jobs(team_leader=1,
               job="deployment of residential modules 1 and 2",
               work_size=15,
               collaborators='2, 3')
    session.add(job)
    job = Jobs(team_leader=3,
               job="cleaning of residential modules 1 and 2",
               work_size=10,
               collaborators='6, 3')
    session.add(job)
    session.commit()


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    # user_create()
    # jobs_create()
    app.run(port=8080, host='127.0.0.1')
