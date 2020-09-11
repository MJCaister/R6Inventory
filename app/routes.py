from flask import render_template, url_for, redirect, flash, request, abort
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.email import send_password_reset_email, send_profile_information_changed_email
from app.forms import (LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm, ChangeProfileInformationForm, UploadNewItemForm)
from app.models import Item, OperatorOrg, User, OperatorItem, UserItem, ItemType


# charm = Item.query.filter(Item.type.in_([2])).all()
# headgear = Item.query.filter(Item.type.in_([3])).all()
# uniform = Item.query.filter(Item.type.in_([4])).all()
# operator = Item.query.filter(Item.type.in_([5])).all()
# org = Item.query.filter(Item.type.in_([6])).all()
# skin = Item.query.filter(Item.type.in_([7])).all()
# weapon = Item.query.filter(Item.type.in_([8])).all()


@app.route('/')
def home():
    return render_template('home.html', page_title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Checks if user is logged in and redirects them to the url endpoint home
    if current_user.is_authenticated:
        flash("User {} already logged in".format(current_user.username))
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        # Queries the User table for the entered username
        user = User.query.filter_by(username=form.username.data).first()
        # If the username does not exist or the entered password is incorrect
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # Calls the flask-login function to log the user in
        login_user(user, remember=form.remember_me.data)
        # Checks if the next page argument was parsed into url otherwise redirects home
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        flash("Logged in user {}".format(form.username.data))
        return redirect(next_page)
    # Parses page title to the render templater along with the form
    return render_template('login.html', page_title='Log In', form=form)


@app.route('/logout')
def logout():
    try:
        flash("Successfully logged out user {}".format(current_user.username))
        logout_user()
    # AttributeError is called by flask-login when it tries to logout an anonymous user
    except AttributeError:
        flash("Not logged in")
    return redirect(url_for('home'))


@app.route('/reset_password_request', methods=["GET", "POST"])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('If the account exists you will receive an email for the instructions on how to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           page_title='Password Reset', form=form)


# Route takes in the token as a variable
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    # Checks if the token is valid
    user = User.verify_reset_password_token(token)
    if not user:
        flash("Invalid or expired token")
        return redirect(url_for('login'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        # Updates the User class in session using a dictionary
        db.session.query(User).filter_by(id=user.id).update({User.password: user.password})
        db.session.commit()
        flash('Your password has been reset')
        return redirect(url_for('login'))
    return render_template("reset_password.html", form=form, page_title='Reset password')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        # Calls the function to hash the users entered password and sets it in the user class
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Registered new user '{}'".format(form.username.data))
        return redirect(url_for('login'))
    return render_template('register.html', page_title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    # Checks if user exists, otherwise returns a 404 error to the user
    user = User.query.filter_by(username=username).first_or_404()

    # Requests all item that the user has in their inventory by the item_type's id
    operators_inventory = UserItem.query.filter_by(user_id=user.id, item_type=5).all()
    # Temporarily stores the ids of these item in a list to be queried
    operators_temp = []
    for op in operators_inventory:
        operators_temp.append(op.item_id)
    # Queries the Item table to get the item information for each added item by the list of item ids
    operators = Item.query.filter(Item.id.in_(operators_temp)).all()

    skins_inventory = UserItem.query.filter_by(user_id=user.id, item_type=7).all()
    skins_temp = []
    for skin in skins_inventory:
        skins_temp.append(skin.item_id)
    skins = Item.query.filter(Item.id.in_(skins_temp)).all()

    headgear_inventory = UserItem.query.filter_by(user_id=user.id, item_type=3).all()
    headgear_temp = []
    for headgear in headgear_inventory:
        headgear_temp.append(headgear.item_id)
    headgear = Item.query.filter(Item.id.in_(headgear_temp)).all()

    uniforms_inventory = UserItem.query.filter_by(user_id=user.id, item_type=4).all()
    uniforms_temp = []
    for uniform in uniforms_inventory:
        uniforms_temp.append(uniform.item_id)
    uniforms = Item.query.filter(Item.id.in_(uniforms_temp)).all()

    charms_inventory = UserItem.query.filter_by(user_id=user.id, item_type=2).all()
    charms_temp = []
    for charm in charms_inventory:
        charms_temp.append(charm.item_id)
    charms = Item.query.filter(Item.id.in_(charms_temp)).all()

    return render_template('user.html', user=user, page_title=username, operators=operators, skins=skins, headgear=headgear, uniforms=uniforms, charms=charms)


@app.route('/user/<username>/settings', methods=["GET", "POST"])
@login_required
def user_settings(username):
    # Returns forbidden if currently logged in user is not the same as the requested one
    if current_user.username != username:
        abort(403)
    form = ChangeProfileInformationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first_or_404()
        if form.username.data != '':
            user.set_username(form.username.data)
            db.session.query(User).filter_by(id=user.id).update({User.username: user.username})
            send_profile_information_changed_email(user)
        if form.email.data != '':
            # Saves old email to email both the new and old email to inform of possible stolen accounts
            new_email = user.email
            user.set_email(form.email.data)
            db.session.query(User).filter_by(id=user.id).update({User.email: user.email})
            send_profile_information_changed_email(user, new_email)
        if form.username.data == '' and form.email.data == '':
            flash("No data was entered")
            return redirect(url_for('user_settings', username=username))
        db.session.commit()
        flash("Profile information has been changed")
        return redirect(url_for('home'))
    return render_template('user_settings.html', form=form, page_title=username + "'s settings")


@app.route('/new_item', methods=['POST'])
@login_required
def new_item():
    form = UploadNewItemForm()
    if form.validate_on_submit():
        # Do stuff
        print()
    return render_template("new_item.html", form=form, page_title='New Item')


@app.route('/add_to_inventory/<item_name>')
@login_required
def add_to_inventory(item_name):
    item_types_allowed = [2, 3, 4, 5, 7]
    item = Item.query.filter_by(name=item_name).first_or_404()
    item_type = ItemType.query.filter_by(id=item.type).first()
    if item.type not in item_types_allowed:
        flash("Invalid item")
        return redirect("/{}/{}".format(item_type.name, item.name))
    # Checks if item already in the users inventory
    in_inventory = UserItem.query.filter_by(user_id=current_user.id, item_id=item.id).first()
    if in_inventory is None:
        # Creates the new entry into the UserItem table to add the item to the users inventory
        item_to_add = UserItem(user_id=current_user.id, item_id=item.id, item_type=item.type)
        db.session.add(item_to_add)
        db.session.commit()
        flash("Successfully added new item to your inventory")
        # Returns to the items page for 'seamless' adding of item
        return redirect("/{}/{}".format(item_type.name, item.name))
    else:
        flash("Item is already in your inventory")
        return redirect("/{}/{}".format(item_type.name, item.name))


@app.route('/remove_from_inventory/<item_name>')
@login_required
def remove_from_inventory(item_name):
    item_types_allowed = [2, 3, 4, 5, 7]
    item = Item.query.filter_by(name=item_name).first_or_404()
    item_type = ItemType.query.filter_by(id=item.type).first()
    if item.type not in item_types_allowed:
        flash("Invalid item")
        return redirect("/{}/{}".format(item_type.name, item.name))
    in_inventory = UserItem.query.filter_by(user_id=current_user.id, item_id=item.id).first()
    if in_inventory is not None:
        db.session.query(UserItem).filter_by(user_id=current_user.id, item_id=item.id).delete()
        db.session.commit()
        flash("Successfully removed item from your inventory")
        return redirect("/{}/{}".format(item_type.name, item.name))
    else:
        flash("Item is not in your inventory")
        return redirect("/{}/{}".format(item_type.name, item.name))


@app.route('/weapons')
def weapons():
    items = Item.query.filter(Item.type.in_([8])).all()
    return render_template("list_items.html", page_title='Weapons',
                           items=items)


@app.route('/operators')
def operators():
    items = Item.query.filter(Item.type.in_([5])).all()
    return render_template("list_items.html", page_title='Operators',
                           items=items)


@app.route('/organisations')
def organisations():
    items = Item.query.filter(Item.type.in_([6])).all()
    return render_template("list_items.html", page_title='Organisations',
                           items=items)


@app.route('/charms')
def charms():
    items = Item.query.filter(Item.type.in_([2])).all()
    return render_template("list_items.html", page_title='Charms', items=items)


@app.route('/headgears')
def headgears():
    items = Item.query.filter(Item.type.in_([3])).all()
    return render_template("list_items.html", page_title='Headgears',
                           items=items)


@app.route('/uniforms')
def uniforms():
    items = Item.query.filter(Item.type.in_([4])).all()
    return render_template("list_items.html", page_title='Uniforms',
                           items=items)


@app.route('/skins')
def skins():
    flash("Support for universal skins will be added in the future")
    items = Item.query.filter(Item.type.in_([7])).all()
    return render_template("list_items.html", page_title='Skins', items=items)


@app.route('/weapon/<weapon>')
def weapon(weapon):
    # Replaces literal unicode spaces with spaces to be queried
    weapon = weapon.replace("%20", " ")
    item = Item.query.filter_by(name=weapon).first_or_404()

    item_ops = OperatorItem.query.filter_by(item_id=item.id).all()
    ops_temp = []
    for op in item_ops:
        ops_temp.append(op.operator_id)
    ops = Item.query.filter(Item.id.in_(ops_temp)).all()
    return render_template("weapon.html", page_title=weapon, item=item, ops=ops)


@app.route('/operator/<operator>')
def operator(operator):
    operator = operator.replace("%20", " ")
    item = Item.query.filter_by(name=operator).first_or_404()

    # Gets the organisation that the operator belongs to
    op_org = OperatorOrg.query.filter_by(operator_id=item.id).first()
    org = Item.query.filter_by(id=op_org.org_id).first()

    # Gets the weapons that the operator has
    op_items = OperatorItem.query.filter_by(operator_id=item.id).all()
    opitems_temp = []
    for i in op_items:
        opitems_temp.append(i.item_id)
    items = Item.query.filter(Item.id.in_(opitems_temp)).all()

    # Checks if user is logged in
    if current_user.is_authenticated:
        # If logged in user has added operator to their inventory returns True to be handled in jinja templating
        in_inventory_check = UserItem.query.filter_by(user_id=current_user.id, item_id=item.id).first()
        if in_inventory_check is not None:
            in_inventory = True
            return render_template("operator.html", page_title=operator, item=item, org=org, items=items, in_inventory=in_inventory)
        else:
            in_inventory = False
            return render_template("operator.html", page_title=operator, item=item, org=org, items=items, in_inventory=in_inventory)
    return render_template("operator.html", page_title=operator, item=item, org=org, items=items)


@app.route('/organisation/<organisation>')
def organisation(organisation):
    organisation = organisation.replace("%20", " ")
    item = Item.query.filter_by(name=organisation).first_or_404()
    org_ops = OperatorOrg.query.filter_by(org_id=item.id).all()
    ops_temp = []
    for op in org_ops:
        ops_temp.append(op.operator_id)
    ops = Item.query.filter(Item.id.in_(ops_temp)).all()
    return render_template("organisation.html", page_title=organisation,
                           item=item, ops=ops)


@app.route('/charm/<charm>')
def charm(charm):
    charm = charm.replace("%20", " ")
    item = Item.query.filter_by(name=charm).first_or_404()

    if current_user.is_authenticated:
        in_inventory_check = UserItem.query.filter_by(user_id=current_user.id, item_id=item.id).first()
        if in_inventory_check is not None:
            in_inventory = True
            return render_template("charm.html", page_title=charm, item=item, in_inventory=in_inventory)
        else:
            in_inventory = False
            return render_template("charm.html", page_title=charm, item=item, in_inventory=in_inventory)
    return render_template("charm.html", page_title=charm, item=item)


@app.route('/headgear/<headgear>')
def headgear(headgear):
    headgear = headgear.replace("%20", " ")
    item = Item.query.filter_by(name=headgear).first_or_404()

    if current_user.is_authenticated:
        in_inventory_check = UserItem.query.filter_by(user_id=current_user.id, item_id=item.id).first()
        if in_inventory_check is not None:
            in_inventory = True
            return render_template("headgear.html", page_title=headgear, item=item, in_inventory=in_inventory)
        else:
            in_inventory = False
            return render_template("headgear.html", page_title=headgear, item=item, in_inventory=in_inventory)
    return render_template("headgear.html", page_title=headgear, item=item)


@app.route('/uniform/<uniform>')
def uniform(uniform):
    uniform = uniform.replace("%20", " ")
    item = Item.query.filter_by(name=uniform).first_or_404()

    if current_user.is_authenticated:
        in_inventory_check = UserItem.query.filter_by(user_id=current_user.id, item_id=item.id).first()
        if in_inventory_check is not None:
            in_inventory = True
            return render_template("uniform.html", page_title=uniform, item=item, in_inventory=in_inventory)
        else:
            in_inventory = False
            return render_template("uniform.html", page_title=uniform, item=item, in_inventory=in_inventory)
    return render_template("uniform.html", page_title=uniform, item=item)


@app.route('/skin/<skin>')
def skin(skin):
    skin = skin.replace("%20", " ")
    item = Item.query.filter_by(name=skin).first_or_404()

    if current_user.is_authenticated:
        in_inventory_check = UserItem.query.filter_by(user_id=current_user.id, item_id=item.id).first()
        if in_inventory_check is not None:
            in_inventory = True
            return render_template("skin.html", page_title=skin, item=item, in_inventory=in_inventory)
        else:
            in_inventory = False
            return render_template("skin.html", page_title=skin, item=item, in_inventory=in_inventory)
    return render_template("skin.html", page_title=skin, item=item)


# Error handlers to handle errors the user encounters nicely
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403
