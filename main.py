from flask import Flask, url_for, request, render_template, redirect, abort, make_response, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data import db_session, jobs_api, users_resource
from data.jobs import Jobs
from data.users import User
from data.departments import Department
from forms.job import JobForm
from base64 import b64encode
from io import BytesIO
from forms.login_form import LoginForm
from forms.user import RegisterForm
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "not found"}))


# для списка объектов
api.add_resource(users_resource.UsersListResource, '/api/v2/users')

# для одного объекта
api.add_resource(users_resource.UsersResource, '/api/v2/users/<int:users_id>')


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


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_jobs(id):
    form = JobForm()

    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    form.team_leader.choices = [(i.id, i.name) for i in users]
    # form.category.choices = categories
    if request.method == "GET":
        jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                          Jobs.user == current_user
                                          ).first()
        if jobs:
            form.job.data = jobs.job
            form.work_size.data = jobs.work_size
            form.team_leader.data = jobs.team_leader
            form.is_finished.data = jobs.is_finished
            if form.collaborators.data:
                form.collaborators.data = jobs.collaborators
            if form.start_date.data:
                form.start_date.data = jobs.start_date
            if form.end_date.data:
                form.end_date.data = jobs.end_date
        else:
            abort(404)
    if form.validate_on_submit():
        jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                          Jobs.user == current_user
                                          ).first()
        if jobs:
            jobs.job = form.job.data
            jobs.work_size = form.work_size.data
            jobs.team_leader = form.team_leader.data
            jobs.is_finished = form.is_finished.data
            if form.collaborators.data:
                jobs.collaborators = form.collaborators.data
            if form.start_date.data:
                jobs.start_date = form.start_date.data
            if form.end_date.data:
                jobs.end_date = form.end_date.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('jobs.html',
                           title='Редактирование работы',
                           form=form
                           )


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


@app.route('/astronaut_selection', methods=['POST', 'GET'])
def astronaut_selection():
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
                          <div class="container">
                            <div class="row">
                            <div class="col-md-6 col-md-offset-3">
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
                                        <label for="professionSelect">Какие у Вас есть профессии?</label>
                                        <div>
                                            <input type="checkbox" id="in-is" name="in-is" checked>
                                            <label for="in-is">Инженер-исследователь</label>
                                        </div>
                                        
                                            <div>
                                          <input type="checkbox" id="in-builder" name="in-builder">
                                          <label for="in-builder">Инженер-строитель</label>
                                        </div>
                                        
                                            <div>
                                          <input type="checkbox" id="pilot" name="pilot">
                                          <label for="pilot">Пилот</label>
                                        </div>
                                        
                                            <div>
                                          <input type="checkbox" id="in_provide" name="in_provide">
                                          <label for="in_provide">Инженер по жизнеобеспечению</label>
                                        </div>
                                        
                                        <div>
                                          <input type="checkbox" id="meteor" name="meteor">
                                          <label for="meteor">Метеоролог</label>
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
                                          <input type="checkbox" id="in_def" name="in_def">
                                          <label for="in_def">Инженер по радиационной защите</label>
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
                            </div>
                            </div>
                            </div>

                          </body>
                        </html>'''
    elif request.method == 'POST':
        print(request.form.get('surname'))
        print(request.form.get('name'))
        print(request.form.get('email'))
        print(request.form.get('education'))
        print(request.form.get('in-is', 'off'))
        print(request.form.get('in-builder', 'off'))
        print(request.form.get('pilot', 'off'))
        print(request.form.get('in_provide', 'off'))
        print(request.form.get('meteor', 'off'))
        print(request.form.get('climat', 'off'))
        print(request.form.get('doctor', 'off'))
        print(request.form.get('in_def', 'off'))
        print(request.form.get('exobio', 'off'))
        print(request.form.get('sex'))
        print(request.form.get('quest'))
        print(request.form.get('file'))
        print(request.form.get('accept'))
        return "<h1>Форма отправлена<h1>"


@app.route('/load_image', methods=['POST', 'GET'])
def load_image():
    if request.method == 'GET':
        return '''<!doctype html>
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
                          <div class="container">
                            <div class="row">
                            <div class="col-md-6 col-md-offset-3">
                                    <h1 align="center">Загрузка фотографии</h1>
                                    <h2 align="center">для участи в миссии</h2>
                                    <div>
                                        <form class="img_form" form method="post" enctype="multipart/form-data">
                                            <div class="form-group">
                                                <label for="photo">Приложите фотографию</label>
                                                <input type="file" class="form-control-file" id="photo" name="image">
                                            </div>
                                            <br>
                                            <button type="submit" class="btn btn-primary">Отправить</button>
                                         </form>
                                    </div>
                            </div>
                            </div>
                            </div>

                          </body>
                        </html>'''

    if request.method == 'POST':
        image = BytesIO(request.files['image'].read())
        image = image.getvalue()
        image = b64encode(image).decode('utf-8')
        return f"""<!doctype html>
                                <html lang="en">
                                  <head>
                                    <meta charset="utf-8">
                                    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                                    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">
                                    <link rel="stylesheet" type="text/css" href="static/css/style.css" />
                                    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-kenU1KFdBIe4zVF0s0G1M5b4hcpxyD9F7jL+jjXkk+Q2h455rYXK/7HAuoJl+0I4" crossorigin="anonymous"></script>
                                    <title>Загрузка фотографии</title>
                                  </head>
                                  <body>
                                                            <div class="container">
                            <div class="row">
                            <div class="col-md-6 col-md-offset-3">
                                    <h1 align="center">Загрузка фотографии</h1>
                                    <h2 align="center">для участи в миссии</h2>
                                    <div>
                                        <form class="img_form" method="post" enctype="multipart/form-data">
                                            <div class="form-group">
                                                <label for="photo">Приложите фотографию</label>
                                                <input type="file" class="form-control-file" id="photo" name="img">
                                            </div>
                                            <br>
                                            <img src="data:image/jpeg;base64,{image}"/>
                                            <br>
                                            <button type="submit" class="btn btn-primary">Отправить</button>
                                         </form>
                                    </div>
                                     </div>
                            </div>
                            </div>
                                  </body>
                                </html>"""


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
               creator=1,
               collaborators='2, 3')
    session.add(job)
    job = Jobs(team_leader=3,
               job="cleaning of residential modules 1 and 2",
               work_size=10,
               creator=1,
               collaborators='6, 3')
    session.add(job)
    session.commit()


if __name__ == '__main__':
    db_session.global_init("db/blogs.sqlite3")
    app.register_blueprint(jobs_api.blueprint)

    # user_create()
    # jobs_create()
    app.run(port=8080, host='127.0.0.1')
