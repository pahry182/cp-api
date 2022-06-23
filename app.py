from flask import Flask, render_template
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class AccountModel(db.Model):
    username = db.Column(db.String(64), primary_key=True, nullable=False)
    password = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        return f"{self.username} with password {self.password}"

#db.create_all()

account_put_args = reqparse.RequestParser()
account_put_args.add_argument("username", type=str, help="Account username", required = True)
account_put_args.add_argument("password", type=str, help="Account password", required = True)

resource_fields = {
    'username' : fields.String,
    'password' : fields.String,
}

class AccountManager(Resource):
    @marshal_with(resource_fields)
    def get(self, account_username):
        result = AccountModel.query.filter_by(username=account_username).first()
        return result

    @marshal_with(resource_fields)
    def post(self, account_username):
        args = account_put_args.parse_args()
        result = AccountModel.query.filter_by(username=account_username).first()
        if result:
            abort(409, message="The username has already taken...")

        account = AccountModel(username=args['username'], password=args['password'])
        db.session.add(account)
        db.session.commit()
        return account, 201

api.add_resource(AccountManager, "/account/<string:account_username>")
@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)