"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken.
"""


from flask import Flask, render_template, redirect, flash, session
import jinja2

import melons


app = Flask(__name__)

# Need to use Flask sessioning features

app.secret_key = 'akhnvofuabgubaq9ht[034tu94-t984e7tod'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.

app.jinja_env.undefined = jinja2.StrictUndefined


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melon_list = melons.get_all()
    return render_template("all_melons.html",
                           melon_list=melon_list)


@app.route("/melon/<int:melon_id>")
def show_melon(melon_id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = melons.get_by_id(melon_id)
    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/cart")
def shopping_cart():
    """Display content of shopping cart."""

    # get the list-of-ids-of-melons from the session cart
    melon_list = session['cart_items']
    melon_counts = {}
    order_total = 0

    # using set() reduces number of loops:
    for melon_id in set(melon_list):

        # grabbing the melon object based on id stored in session
        melon = melons.get_by_id(melon_id)
        qty = melon_list.count(melon_id)
        total = qty * melon.price
        order_total += total

        # creating an entry in the dictionary for each melon, with id as key
        melon_counts[melon_id] = {'melon_name': melon.common_name,
                                               'melon_price': melon.price,
                                               'qty': qty,
                                               'total_per_type': total,
                                              }

    return render_template("cart.html", melons=melon_counts, order_total=order_total)

@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Successfully added to cart'.
    """

    # - add the id of the melon they bought to the cart in the session
    session.setdefault('cart_items', []).append(id)
    melon = melons.get_by_id(id)

    #Flash a message indicating the melon was successfully added to the cart.
    flash(melon.common_name + " was added to cart")
    return redirect("/cart")


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    # TODO: Need to implement this!

    return "Oops! This needs to be implemented"


@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True)
