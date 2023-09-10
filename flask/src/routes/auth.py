from http import HTTPStatus
from os import environ
from datetime import datetime, timezone, timedelta
import jwt
from pymongo import DESCENDING
from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)
from flask_mail import Message
from flask import (
    Blueprint,
    current_app as app,
    render_template,
    request,
    jsonify,
)
from src.middlewares.validator import validate

from src.utils import constants
from src.utils import gen_otp, verify_otp
from src.validation import auth_validation

auth = Blueprint(
    "Authentication",
    __name__,
    template_folder="../templates/emails",
)


@auth.route("/")
def index():
    return render_template(
        "Password_Reset.html",
        name="Anurag",
        otp=123456,
    )


@auth.route("/register", methods=["POST"])
@validate(auth_validation.UserRegister())
def register():
    with app.app_context():
        try:
            req = request.get_json()
            user_id = 0
            last_user = app.db.user.find_one(
                {}, sort=[("id", DESCENDING)]
            )

            if last_user is not None:
                user_id = int(last_user["id"]) + 1

            name = req["name"]
            email = req["email"]
            profile = req["profile"]
            password = req["password"]

            emailExists = app.db.user.find_one(
                {"email": email}
            )

            if emailExists:
                return (
                    jsonify(
                        success=False,
                        message="Email already used.",
                    ),
                    HTTPStatus.CONFLICT,
                )

            name = req["name"]
            email = req["email"]
            profile = req["profile"]
            password = generate_password_hash(
                req["password"]
            )

            user_dict = dict(
                id=user_id,
                name=name,
                email=email,
                password=password,
                profile=profile,
                verified=True,
                created_at=str(
                    datetime.now(timezone.utc)
                ),
            )
            app.db.user.insert_one(user_dict)

            return (
                jsonify(
                    success=True,
                    message="User registered successfully.",
                ),
                201,
            )
        except Exception:
            return (
                jsonify(
                    success=False,
                    message="Something Went Wrong! Please try again.",
                ),
                500,
            )


@auth.route("/login", methods=["POST"])
@validate(auth_validation.UserLogin())
def login():
    with app.app_context():
        try:
            req = request.get_json()

            email = req["email"]
            password = req["password"]

            user_found = app.db.user.find_one(
                {"email": email},
                {
                    "id": 1,
                    "name": 1,
                    "email": 1,
                    "password": 1,
                    "verified": 1,
                    "profile": 1,
                },
            )

            if user_found is None:
                return (
                    jsonify(
                        success=False,
                        message="Account not found",
                    ),
                    404,
                )

            if check_password_hash(
                user_found["password"], password
            ):
                app.db.user.update_one(
                    {"email": email},
                    {
                        "$push": {
                            "logins": datetime.now(
                                timezone.utc
                            )
                        }
                    },
                    upsert=True,
                )
                iat = datetime.now(timezone.utc)
                jwt_body = {
                    "id": user_found["id"],
                    "email": email,
                    "iat": iat,
                    "exp": iat
                    + timedelta(days=15),
                    "iss": "Movielust",
                }
                token = jwt.encode(
                    jwt_body,
                    environ.get("SECRET"),
                )
                return (
                    jsonify(
                        success=True,
                        message="Logged In!",
                        id=user_found["id"],
                        name=user_found["name"],
                        email=email,
                        profile=user_found[
                            "profile"
                        ],
                        token=token,
                    ),
                    200,
                )

            return (
                jsonify(
                    success=False,
                    message="Invalid Password!",
                ),
                HTTPStatus.UNAUTHORIZED.value,
            )
        except:
            return (
                jsonify(
                    success=False,
                    message=HTTPStatus.INTERNAL_SERVER_ERROR.phrase,
                ),
                HTTPStatus.INTERNAL_SERVER_ERROR.value,
            )


@auth.route(
    "/verifyotp/<email>/<otp>/<otp_type>",
    methods=["GET"],
)
def verifyresetotp(email, otp, otp_type):
    try:
        isValid = verify_otp(
            email, otp, int(otp_type)
        )

        if isValid:
            return (
                jsonify(
                    success=True,
                    message="OTP Valid",
                ),
                200,
            )

        if isValid == "Error":
            raise Exception(
                "Error while verifying OTP!"
            )

        return (
            jsonify(
                success=False,
                message="Invalid OTP",
            ),
            200,
        )

    except Exception:
        return (
            jsonify(
                success=False,
                message=HTTPStatus.INTERNAL_SERVER_ERROR.phrase,
            ),
            HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )


# ------------------------Reset Password--------------------


@auth.route("/resetotp", methods=["POST"])
@validate(auth_validation.ResetOTP())
def send_otp():
    with app.app_context():
        try:
            req = request.get_json()

            email = req["email"]

            user_exists = app.db.user.find_one(
                {"email": email},
                {"_id": 0, "id": 1, "name": 1},
            )

            if user_exists is None:
                return (
                    jsonify(
                        success=False,
                        message="Email Does not Exist.",
                    ),
                    404,
                )

            otp = gen_otp()

            app.db.otp.delete_many(
                {"email": email}
            )

            data = dict(
                email=email,
                otp=otp,
                type=constants.OTP_TYPES[1],
                exp=datetime.now(timezone.utc)
                + timedelta(minutes=11),
            )

            app.db.otp.insert_one(data)

            msg = Message(
                "Movielust Password Reset",
                recipients=[email],
            )

            msg.html = render_template(
                "Password_Reset.html",
                name=user_exists["name"],
                otp=otp,
            )

            app.mail.send(msg)

            return (
                jsonify(
                    success=True,
                    message="OTP sent.",
                ),
                200,
            )

        except Exception:
            return (
                jsonify(
                    success=False,
                    message=HTTPStatus.INTERNAL_SERVER_ERROR.phrase,
                ),
                HTTPStatus.INTERNAL_SERVER_ERROR.value,
            )


@auth.route("/verifyemailotp", methods=["POST"])
@validate(auth_validation.VerifyEmailOTP())
def sende_mail_verify_otp():
    try:
        req = request.get_json()

        email = req["email"]
        name = req["name"]
        otp = gen_otp()
        app.db.otp.delete_many({"email": email})
        data = dict(
            email=email,
            otp=otp,
            type=constants.OTP_TYPES[0],
            exp=datetime.now(timezone.utc)
            + timedelta(minutes=11),
        )
        app.db.otp.insert_one(data)
        msg = Message(
            "Movielust Email Verification",
            recipients=[email],
        )
        msg.html = render_template(
            "Verify_Email.html",
            name=name,
            otp=otp,
        )
        app.mail.send(msg)
        return (
            jsonify(
                success=True, message="OTP sent."
            ),
            200,
        )

    except Exception as err:
        print(err)
        return (
            jsonify(
                success=False,
                message=HTTPStatus.INTERNAL_SERVER_ERROR.phrase,
            ),
            HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )


@auth.route("/resetpass", methods=["POST"])
@validate(auth_validation.ResetPassword())
def resetpass():
    with app.app_context():
        try:
            req = request.get_json()

            otp_valid = verify_otp(
                req["email"], req["otp"], 1
            )

            if not otp_valid:
                return (
                    jsonify(
                        success=False,
                        message="Request Expired try again!",
                    ),
                    200,
                )

            password = req["password"]

            if len(password) < 6:
                return (
                    jsonify(
                        success=False,
                        message="Password too short",
                    ),
                    200,
                )

            app.db.otp.delete_many(
                {"email": req["email"]}
            )

            password_hash = (
                generate_password_hash(password)
            )

            app.db.user.update_one(
                {"email": req["email"]},
                {
                    "$set": {
                        "password": password_hash
                    }
                },
            )

            return (
                jsonify(
                    success=True,
                    message="Password Updated.",
                ),
                200,
            )
        except Exception:
            return (
                jsonify(
                    success=False,
                    message=HTTPStatus.INTERNAL_SERVER_ERROR.phrase,
                ),
                HTTPStatus.INTERNAL_SERVER_ERROR.value,
            )


@auth.route("/admin/login", methods=["POST"])
@validate(auth_validation.AdminAuth())
def admin_login():
    try:
        req = request.get_json()

        userName = req["userName"]
        password = req["password"]

        admin = app.db.admin.find_one(
            {"userName": userName}
        )

        if admin is None:
            return jsonify(success=False), 404

        if password != admin["password"]:
            return (
                jsonify(
                    success=False,
                    message="Incorrect Password!",
                ),
                401,
            )

        iat = datetime.now(timezone.utc)
        jwt_body = {
            "userName": userName,
            "iat": iat,
            "exp": iat + timedelta(minutes=30),
            "iss": "Movielust",
        }

        token = jwt.encode(
            jwt_body, environ.get("ADMIN_SECRET")
        )

        return (
            jsonify(
                success=True,
                message="Logged In!",
                token=token,
                name=admin["name"],
                avatar=admin["avatar"],
            ),
            200,
        )
    except Exception as e:
        print(e)
        return (
            jsonify(
                success=False,
                message=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            ),
            500,
        )
