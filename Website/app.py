import os
import papermill as pm
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for, send_file
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import pandas as pd
from helpers import apology, login_required
import time
# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.config['UPLOAD_FOLDER'] = "uploads"
db = SQL("sqlite:///data.db")

@app.route("/")
@login_required
def index():
    return render_template("about.html")
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    msg = request.args.get("msg")
    session.clear()
    if msg:
        flash(msg)

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not username:
            return apology("Must Provide Username")
        if not password:
            return apology("Must Provide Password")
        if not confirmation:
            return apology("Must Provide Confirmation")
        if password != confirmation:
            return apology("Passwords Don't Match!")
        hash = generate_password_hash(password)
        try:
            new_user = db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)
        except:
            return apology("This Username already exists. Please try another one")
        session["user_id"] = new_user
        return redirect("/")

@app.route("/about")
@login_required
def about():
    return render_template("about.html")

@app.route("/upload_csv", methods=["GET", "POST"])
@login_required
def upload_csv():
    if request.method == "GET":
        return render_template("upload_csv.html")
    else:
        if 'csvFile' not in request.files:
            return "No file part in request"

        file = request.files['csvFile']

        if file.filename == '':
            return "No file selected"

        if file:
            filename = secure_filename(file.filename)
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(upload_path)

            # Generate timestamped prediction filename
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            prediction_filename = f"predicted_{timestamp}.csv"
            prediction_path = os.path.join("predictions", prediction_filename)

            # Run clean.ipynb with input/output params
            try:
                pm.execute_notebook(
                    input_path="clean.ipynb",
                    output_path="executed_clean.ipynb",
                    parameters={
                        "input_path": upload_path,
                        "output_path": prediction_path
                    }
                )

                # Save prediction record to DB
                db.execute(
                    "INSERT INTO predictions (user_id, filename, uploaded_at) VALUES (?, ?, ?)",
                    session["user_id"], prediction_filename, datetime.now()
                )

                flash("✅ File processed successfully!")
                return redirect(url_for("predictions", file=prediction_filename))

            except Exception as e:
                flash(f"❌ Processing failed: {e}")
                return redirect(url_for("upload_csv"))

@app.route("/process")
@login_required
def process():
    msg = request.args.get("msg")
    if msg == "success":
        flash("✅ File processed successfully!")
    # Make sure the filename is in session (set during /upload_csv)
    if "uploaded_filename" not in session:
        flash("No uploaded file found. Please upload a CSV first.")
        return redirect(url_for("upload_csv"))

    # Full path to uploaded file
    try:
        pm.execute_notebook(
            input_path="clean.ipynb",
            output_path="executed_clean.ipynb",
            parameters={"input_path": f"uploads/{session['uploaded_filename']}"}
        )

        flash("✅ File processed successfully!")
        return redirect(url_for("predictions", msg="success"))

    except Exception as e:
        flash(f"❌ Processing failed: {e}")
        return redirect(url_for("upload_csv"))
    

@app.route("/predictions")
@login_required
def predictions():
    msg = request.args.get("msg")
    if msg == "success":
        flash("✅ File processed successfully!")

    # Get all prediction files for this user
    prediction_files = db.execute(
        "SELECT filename, uploaded_at FROM predictions WHERE user_id = ? ORDER BY uploaded_at DESC",
        session["user_id"]
    )

    if not prediction_files:
        flash("⚠️ You haven't uploaded any predictions yet.")
        return redirect("/upload_csv")

    # Get selected file from URL or default to most recent
    filename = request.args.get("file") or prediction_files[0]["filename"]
    file_path = os.path.join("predictions", filename)
    try:
        df = pd.read_csv(file_path)
        columns = df.columns.tolist()
        rows = df.to_dict(orient='records')
        return render_template("predictions.html", columns=columns, rows=rows, files=prediction_files, current_file=filename)


    except FileNotFoundError:
        flash("⚠️ Prediction file not found. Please upload and process a CSV first.")
        return redirect(url_for("upload_csv"))




@app.route('/download_predictions')
@login_required
def download_predictions():
    filename = request.args.get("file")
    if not filename:
        flash("❌ No prediction file specified for download.")
        return redirect(url_for("predictions"))

    file_path = os.path.join("predictions", filename)
    if not os.path.exists(file_path):
        flash("❌ File not found.")
        return redirect(url_for("predictions"))

    return send_file(file_path, as_attachment=True)



@app.route("/delete_prediction", methods=["POST"])
@login_required
def delete_prediction():
    filename = request.form.get("filename")

    if not filename:
        flash("❌ No file selected to delete.")
        return redirect(url_for("predictions"))

    # Ensure user owns the file
    row = db.execute(
        "SELECT * FROM predictions WHERE user_id = ? AND filename = ?",
        session["user_id"], filename
    )
    if not row:
        flash("❌ You don't have permission to delete this file.")
        return redirect(url_for("predictions"))

    # Delete from filesystem
    file_path = os.path.join("predictions", filename)
    if os.path.exists(file_path):
        os.remove(file_path)

    # Delete from database
    db.execute(
        "DELETE FROM predictions WHERE user_id = ? AND filename = ?",
        session["user_id"], filename
    )

    flash("🗑️ Prediction file deleted successfully.")
    return redirect(url_for("predictions"))

@app.context_processor
def inject_user():
    try:
        if "user_id" in session:
            user = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
            if user:
                return {"username": user[0]["username"]}
    except:
        pass
    return {}


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_pw():
    if request.method == "POST":
        curr_pw = request.form.get("curr_pw")
        new_pw = request.form.get("new-password")
        confirmation_new_pw = request.form.get("confirmation-new-pw")
        if not curr_pw:
            return apology("Must Provide Old Password")

        if not new_pw:
            return apology("Must Provide New Password")

        if not confirmation_new_pw:
            return apology("Must Provide Confirmation Password")

        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

        if not check_password_hash(rows[0]["hash"], curr_pw):
            return apology("Current Password is Incorrect")

        if new_pw != confirmation_new_pw:
            return apology("Passwords Do not Match!")

        hash = generate_password_hash(new_pw)

        user_id = session["user_id"]

        db.execute("UPDATE users SET hash = ? WHERE id = ?", hash, user_id)
        flash("Password Changed Successfully!")
        time.sleep(3)
        session.clear()
        return redirect("/login?msg=Password+Changed+Successfully!")
    else:
        return render_template("change_password.html")




