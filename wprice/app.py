from flask import Flask, render_template, Response, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.update(
    SQLALCHEMY_DATABASE_URI='sqlite:///data-price.sqlite',
    DEBUG=False,
    ITEMS_PER_PAGE=4,
)

db = SQLAlchemy(app)


class Item(db.Model):
    __tablename__ = 'PRICE_UA'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    item_url = db.Column(db.String(250))
    item_photo = db.Column(db.String(250))

    def __repr__(self):
        return self.name


@app.template_filter()
def cr2br(text):  # filter for description in template
    return text.replace('\n', '<br>')


@app.route('/')
@app.route('/<int:page>')
def index(page=1):
    items = Item.query.filter_by().paginate(page, app.config["ITEMS_PER_PAGE"])
    return render_template('index.html', items=items)


if __name__ == '__main__':
    app.run()
