from flask import Flask, render_template
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class AccountModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        return f"{self.username} with ID {self.id} and password {self.password}"

#db.create_all()

account_put_args = reqparse.RequestParser()
account_put_args.add_argument("username", type=str, help="Account username", required = True)
account_put_args.add_argument("password", type=str, help="Account password", required = True)

resource_fields = {
    'id' : fields.Integer,
    'username' : fields.String,
    'password' : fields.String,
}

class AccountManager(Resource):
    @marshal_with(resource_fields)
    def get(self, account_id):
        result = AccountModel.query.filter_by(id=account_id).first()
        return result

    @marshal_with(resource_fields)
    def put(self, account_id):
        args = account_put_args.parse_args()
        result = AccountModel.query.filter_by(id=account_id).first()
        if result:
            abort(409, message="Account id taken...")

        account = AccountModel(id=account_id, username=args['username'], password=args['password'])
        db.session.add(account)
        db.session.commit()
        return account, 201

api.add_resource(AccountManager, "/account/<int:account_id>")
@app.route('/')
def index():
    return render_template("index.html")

# if __name__ == '__main__':
#     app.run(debug=True)