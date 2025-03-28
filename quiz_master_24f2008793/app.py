from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Subject, Chapter, Quiz, Question, Score
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()
    # Create admin user if not exists
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', is_admin=True)
        admin.set_password('admin')
        db.session.add(admin)
        db.session.commit()

@app.route('/')
def home():
    subjects = Subject.query.all()
    return render_template('home.html', subjects=subjects)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'danger')
        else:
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('home'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Admin routes
@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        return redirect(url_for('home'))
    subjects = Subject.query.all()
    return render_template('admin_dashboard.html', subjects=subjects)

@app.route('/admin/subject/add', methods=['POST'])
@login_required
def add_subject():
    if not current_user.is_admin:
        return redirect(url_for('home'))
    name = request.form['name']
    subject = Subject(name=name)
    db.session.add(subject)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/chapter/add', methods=['POST'])
@login_required
def add_chapter():
    if not current_user.is_admin:
        return redirect(url_for('home'))
    name = request.form['name']
    subject_id = request.form['subject_id']
    chapter = Chapter(name=name, subject_id=subject_id)
    db.session.add(chapter)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/quiz/add', methods=['POST'])
@login_required
def add_quiz():
    if not current_user.is_admin:
        return redirect(url_for('home'))
    title = request.form['title']
    chapter_id = request.form['chapter_id']
    quiz = Quiz(title=title, chapter_id=chapter_id)
    db.session.add(quiz)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/question/add', methods=['POST'])
@login_required
def add_question():
    if not current_user.is_admin:
        return redirect(url_for('home'))
    text = request.form['text']
    options = request.form.getlist('options[]')
    correct_answer = request.form['correct_answer']
    quiz_id = request.form['quiz_id']
    question = Question(
        text=text,
        options=options,
        correct_answer=correct_answer,
        quiz_id=quiz_id
    )
    db.session.add(question)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/subject/<int:subject_id>/edit', methods=['POST'])
@login_required
def edit_subject(subject_id):
    if not current_user.is_admin:
        return redirect(url_for('home'))
    subject = Subject.query.get_or_404(subject_id)
    subject.name = request.form['name']
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/subject/<int:subject_id>/delete', methods=['POST'])
@login_required
def delete_subject(subject_id):
    if not current_user.is_admin:
        return redirect(url_for('home'))
    subject = Subject.query.get_or_404(subject_id)
    db.session.delete(subject)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/chapter/<int:chapter_id>/edit', methods=['POST'])
@login_required
def edit_chapter(chapter_id):
    if not current_user.is_admin:
        return redirect(url_for('home'))
    chapter = Chapter.query.get_or_404(chapter_id)
    chapter.name = request.form['name']
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/chapter/<int:chapter_id>/delete', methods=['POST'])
@login_required
def delete_chapter(chapter_id):
    if not current_user.is_admin:
        return redirect(url_for('home'))
    chapter = Chapter.query.get_or_404(chapter_id)
    db.session.delete(chapter)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/quiz/<int:quiz_id>/edit', methods=['POST'])
@login_required
def edit_quiz(quiz_id):
    if not current_user.is_admin:
        return redirect(url_for('home'))
    quiz = Quiz.query.get_or_404(quiz_id)
    quiz.title = request.form['title']
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/quiz/<int:quiz_id>/delete', methods=['POST'])
@login_required
def delete_quiz(quiz_id):
    if not current_user.is_admin:
        return redirect(url_for('home'))
    quiz = Quiz.query.get_or_404(quiz_id)
    db.session.delete(quiz)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/question/<int:question_id>/edit', methods=['POST'])
@login_required
def edit_question(question_id):
    if not current_user.is_admin:
        return redirect(url_for('home'))
    question = Question.query.get_or_404(question_id)
    question.text = request.form['text']
    question.options = request.form.getlist('options[]')
    question.correct_answer = request.form['correct_answer']
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/question/<int:question_id>/delete', methods=['POST'])
@login_required
def delete_question(question_id):
    if not current_user.is_admin:
        return redirect(url_for('home'))
    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('admin'))
    text = request.form['text']
    options = request.form.getlist('options[]')
    correct_answer = request.form['correct_answer']
    quiz_id = request.form['quiz_id']
    question = Question(
        text=text,
        options=options,
        correct_answer=correct_answer,
        quiz_id=quiz_id
    )
    db.session.add(question)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/quiz/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    if request.method == 'POST':
        score = 0
        for question in quiz.questions:
            answer = request.form.get(f'question_{question.id}')
            if answer == question.correct_answer:
                score += 1
        score_entry = Score(
            user_id=current_user.id,
            quiz_id=quiz_id,
            score=score
        )
        db.session.add(score_entry)
        db.session.commit()
        flash(f'You scored {score} out of {len(quiz.questions)}!', 'success')
        return redirect(url_for('scores'))
    return render_template('quiz.html', quiz=quiz)

@app.route('/scores')
@login_required
def scores():
    if current_user.is_admin:
        users = User.query.all()
        return render_template('scores.html', users=users)
    else:
        user_scores = Score.query.filter_by(user_id=current_user.id).all()
        return render_template('scores.html', scores=user_scores)

@app.route('/admin/score/<int:score_id>/delete', methods=['POST'])
@login_required
def delete_score(score_id):
    if not current_user.is_admin:
        return redirect(url_for('home'))
    score = Score.query.get_or_404(score_id)
    db.session.delete(score)
    db.session.commit()
    return redirect(url_for('scores'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
