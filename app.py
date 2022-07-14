from flask import Flask, current_app, render_template, request
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask.views import MethodView
from flask_sqlalchemy import SQLAlchemy
from flask import Response

app = Flask(__name__)
CORS(app)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

@current_app.before_request
def basic_authentication():
    if request.method.lower() == 'options':
        return Response()

class AccountModel(db.Model):
    username = db.Column(db.String(64), primary_key=True, nullable=False)
    password = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        return f"{self.username} with password {self.password}"

class Tictactoe_score(db.Model):
    username = db.Column(db.String(64), primary_key=True, nullable=False)
    tictactoe_score_easy = db.Column(db.Integer)
    tictactoe_score_normal = db.Column(db.Integer)
    tictactoe_score_hard = db.Column(db.Integer)

    def __repr__(self):
        return f"{self.username} with password {self.tictactoe_score_easy}"

db.create_all()

account_put_args = reqparse.RequestParser()
account_put_args.add_argument("username", type=str, help="Account username", required = True)
account_put_args.add_argument("password", type=str, help="Account password", required = True)

account_tictactoe_score_put_args = reqparse.RequestParser()
account_tictactoe_score_put_args.add_argument("username", type=str, help="Account username", required = True)
account_tictactoe_score_put_args.add_argument("tictactoe_score_easy", type=int, help="Account Tictactoe Score", )
account_tictactoe_score_put_args.add_argument("tictactoe_score_normal", type=int, help="Account Tictactoe Score", )
account_tictactoe_score_put_args.add_argument("tictactoe_score_hard", type=int, help="Account Tictactoe Score", )

resource_fields = {
    'username' : fields.String,
    'password' : fields.String,
}

resource_fields_tictactoe_score = {
    'username' : fields.String,
    'tictactoe_score_easy' : fields.Integer,
    'tictactoe_score_normal' : fields.Integer,
    'tictactoe_score_hard' : fields.Integer,
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

class ScoreManager(Resource):
    @marshal_with(resource_fields_tictactoe_score)
    def get(self, account_username):
        if account_username == "all":
            result = Tictactoe_score.query.all()
        else:
            result = Tictactoe_score.query.filter_by(username=account_username).first()
        return result

    @marshal_with(resource_fields_tictactoe_score)
    def put(self, account_username):
        args = account_tictactoe_score_put_args.parse_args()
        result = Tictactoe_score.query.filter_by(username=account_username).first()
        # if result:
        #     abort(409, message="The username has already taken...")

        score = Tictactoe_score(username=args['username'], tictactoe_score_easy=args['tictactoe_score_easy'],
                                tictactoe_score_normal=args['tictactoe_score_normal'],
                                tictactoe_score_hard=args['tictactoe_score_hard'])
        if not result:
            db.session.add(score)
        else:
            if args['tictactoe_score_easy']:
                result.tictactoe_score_easy = args['tictactoe_score_easy']
            if args['tictactoe_score_normal']:
                result.tictactoe_score_normal = args['tictactoe_score_normal']
            if args['tictactoe_score_hard']:
                result.tictactoe_score_hard = args['tictactoe_score_hard'] 
        db.session.commit()
        return score, 201
    
    @marshal_with(resource_fields_tictactoe_score)
    def patch(self, account_username):
        args = account_tictactoe_score_put_args.parse_args()
        result = Tictactoe_score.query.filter_by(username=account_username).first()
        if not result:
            abort(404, message="Account doesn't exist, cannot update")

        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']

        db.session.commit()

        return result


api.add_resource(AccountManager, "/account/<string:account_username>")
api.add_resource(ScoreManager, "/tictactoe/<string:account_username>")
@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)