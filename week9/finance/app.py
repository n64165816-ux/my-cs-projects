import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # 1. Get all stocks currently owned by the user (where total shares > 0)
    rows = db.execute("""
        SELECT symbol, SUM(shares) AS total_shares
        FROM transactions
        WHERE user_id = ?
        GROUP BY symbol
        HAVING SUM(shares) > 0
    """, session["user_id"])

    # 2. Query the user's current cash balance
    user_rows = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    cash = user_rows[0]["cash"]

    # 3. Create a list to store detailed stock info and calculate global total
    portfolio = []
    total_portfolio_value = cash

    for row in rows:
        # Lookup real-time data for each stock symbol
        stock_info = lookup(row["symbol"])
        if stock_info:
            current_price = stock_info["price"]
            stock_total_value = current_price * row["total_shares"]

            # Accumulate to the grand total
            total_portfolio_value += stock_total_value

            # Append organized dictionary to our portfolio list
            portfolio.append({
                "symbol": row["symbol"].upper(),
                "name": stock_info["name"],
                "shares": row["total_shares"],
                "price": current_price,
                "total": stock_total_value
            })

    # 4. Render the homepage and pass all the calculated variables
    return render_template("index.html", portfolio=portfolio, cash=cash, total=total_portfolio_value)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # 1. Validate inputs
        if not symbol:
            return apology("must provide symbol", 400)

        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("must provide a valid positive integer for shares", 400)

        # 2. Look up the stock price
        stock = lookup(symbol)
        if stock is None:
            return apology("invalid symbol", 400)

        shares_count = int(shares)
        total_cost = stock["price"] * shares_count

        # 3. Check if user has enough cash
        # session["user_id"] contains the ID of the currently logged-in user
        user_rows = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        user_cash = user_rows[0]["cash"]

        if user_cash < total_cost:
            return apology("can't afford", 400)

        # 4. Execute transaction: update cash and log the purchase
        # Update user's cash balance
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", total_cost, session["user_id"])

        # Insert log into transactions table
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   session["user_id"], stock["symbol"], shares_count, stock["price"])

        # 5. Redirect user to home page
        return redirect("/")

    else:
        # If method is GET, check if there is a symbol passed in the URL parameters
        symbol = request.args.get("symbol", "")
        # Render the buy page, passing the symbol (it will be empty if they typed /buy manually)
        return render_template("buy.html", symbol=symbol)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # Query database for all transactions by the current user, ordered by newest first
    transactions = db.execute("""
        SELECT symbol, shares, price, timestamp
        FROM transactions
        WHERE user_id = ?
        ORDER BY timestamp DESC
    """, session["user_id"])

    # Render the history page and pass the transactions list to HTML
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        # 1. Get the symbol from the form
        symbol = request.form.get("symbol")

        # 2. Validate input
        if not symbol:
            return apology("must provide symbol", 400)

        # 3. Look up the stock price using the lookup function from helpers.py
        stock = lookup(symbol)

        # 4. If the symbol is invalid, lookup returns None
        if stock is None:
            return apology("invalid symbol", 400)

        # 5. Render the result page, passing the stock data dictionary
        return render_template("quoted.html", stock=stock)

    else:
        # If method is GET, just show the search form
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # 1. Get data from the form
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

    # 2. Validate input and handle errors
        if not username:
            return apology("must provide username", 400)

        if not password:
            return apology("must provide password", 400)

        if password != confirmation:
            return apology("passwords do not match", 400)

        # 3. Insert the new user into the Database
        try:
            # Hash the password for security before storing it
            hash_password = generate_password_hash(password)

            # Execute the INSERT query into the users table
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash_password)

        except ValueError:
            # Handle the case where the username already exists (due to the UNIQUE INDEX)
            return apology("username already exists", 400)

        # 4. Redirect the user to the login page after successful registration
        return redirect("/login")

    else:
        # If the method is GET, render the registration form page
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # 1. Validate inputs
        if not symbol:
            return apology("must provide symbol", 400)

        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("must provide a valid positive integer for shares", 400)

        shares_to_sell = int(shares)

        # 2. Check how many shares the user currently owns of this stock
        # We calculate total bought minus total sold from the transactions table
        stocks_owned = db.execute("""
            SELECT SUM(shares) AS total_shares
            FROM transactions
            WHERE user_id = ? AND symbol = ?
        """, session["user_id"], symbol.upper())

        # If user doesn't own any shares or owns fewer than they want to sell
        if not stocks_owned or stocks_owned[0]["total_shares"] is None or stocks_owned[0]["total_shares"] < shares_to_sell:
            return apology("not enough shares", 400)

        # 3. Look up current real-time stock price
        stock = lookup(symbol)
        if stock is None:
            return apology("invalid symbol", 400)

        total_earnings = stock["price"] * shares_to_sell

        # 4. Execute transaction: update cash and log the sale
        # Add earnings to user's cash
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?",
                   total_earnings, session["user_id"])

        # Insert into transactions table with a NEGATIVE number of shares for selling
        db.execute("""
            INSERT INTO transactions (user_id, symbol, shares, price)
            VALUES (?, ?, ?, ?)
        """, session["user_id"], stock["symbol"], -shares_to_sell, stock["price"])

        # 5. Redirect user to home page
        return redirect("/")

    else:
        # If method is GET, fetch all stock symbols the user currently owns to populate the dropdown
        # We group by symbol and only pick ones where the remaining shares count is > 0
        rows = db.execute("""
            SELECT symbol
            FROM transactions
            WHERE user_id = ? AND symbol != 'CASH'
            GROUP BY symbol
            HAVING SUM(shares) > 0
        """, session["user_id"])

        return render_template("sell.html", stocks=rows)


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """Allow users to change their passwords"""
    if request.method == "POST":
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirmation = request.form.get("confirmation")

        # 1. Validate inputs
        if not current_password or not new_password or not confirmation:
            return apology("must provide all fields", 400)

        if new_password != confirmation:
            return apology("new passwords do not match", 400)

        # 2. Query database for user's current password hash
        rows = db.execute("SELECT hash FROM users WHERE id = ?", session["user_id"])

        # 3. Check if current password is correct using check_password_hash
        if not check_password_hash(rows[0]["hash"], current_password):
            return apology("incorrect current password", 400)

        # 4. Hash the new password and update the database
        new_hash = generate_password_hash(new_password)
        db.execute("UPDATE users SET hash = ? WHERE id = ?", new_hash, session["user_id"])

        # 5. Redirect user to home page with a success message
        return redirect("/")

    else:
        # If method is GET, render the change password form page
        return render_template("change_password.html")


@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    """Allow users to add additional cash to their account"""
    if request.method == "POST":
        amount = request.form.get("amount")

        # 1. Validate input
        if not amount:
            return apology("must provide an amount", 400)

        try:
            amount_to_add = float(amount)
        except ValueError:
            return apology("invalid amount", 400)

        if amount_to_add <= 0:
            return apology("amount must be positive", 400)

        # 2. Update user's cash in the database
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?",
                   amount_to_add, session["user_id"])

        # 3. Log this cash addition in transactions as a deposit (Optional but good practice)
        db.execute("""
            INSERT INTO transactions (user_id, symbol, shares, price)
            VALUES (?, ?, ?, ?)
        """, session["user_id"], "DEPOSIT", 1, amount_to_add)

        # 4. Redirect user to home page
        return redirect("/")

    else:
        # If method is GET, render the add cash form page
        return render_template("add_cash.html")
