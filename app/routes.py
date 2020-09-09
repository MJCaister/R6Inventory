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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', page_title='Log In', form=form)


@app.route('/logout')
def logout():
    try:
        flash("Successfully logged out user {}".format(current_user.username))
        logout_user()
    except AttributeError:
        flash("User already logged out")
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
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           page_title='Password Reset', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Registered new user '{}'".format(form.username.data))
        return redirect(url_for('login'))
    return render_template('register.html', page_title='Register', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('home'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.query(User).filter_by(id=user.id).update({User.password: user.password})
        db.session.commit()
        flash('Your password has been reset')
        return redirect(url_for('login'))
    return render_template("reset_password.html", form=form, page_title='Reset password')


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user, page_title=username)


@app.route('/user/<username>/settings', methods=["GET", "POST"])
@login_required
def user_settings(username):
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
    item = Item.query.filter_by(name=item_name).first()
    item_type = ItemType.query.filter_by(id=item.type).first()
    in_inventory = UserItem.query.filter_by(user_id=current_user.id, item_id=item.id).first()
    if in_inventory is None:
        item_to_add = UserItem(user_id=current_user.id, item_id=item.id, item_type=item.type)
        db.session.add(item_to_add)
        db.session.commit()
        flash("Successfully added new item to your inventory")
        return redirect("/{}/{}".format(item_type.name, item.name))
    else:
        flash("Item is already in your inventory")
        return redirect("/{}/{}".format(item_type.name, item.name))


@app.route('/remove_from_inventory/<item_name>')
@login_required
def remove_from_inventory(item_name):
    item = Item.query.filter_by(name=item_name).first()
    item_type = ItemType.query.filter_by(id=item.type).first()
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
    flash("Support for charms will be added in the future")
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

    op_org = OperatorOrg.query.filter_by(operator_id=item.id).first()
    org = Item.query.filter_by(id=op_org.org_id).first()

    op_items = OperatorItem.query.filter_by(operator_id=item.id).all()
    opitems_temp = []
    for i in op_items:
        opitems_temp.append(i.item_id)
    items = Item.query.filter(Item.id.in_(opitems_temp)).all()

    in_inventory_check = UserItem.query.filter_by(user_id=current_user.id, item_id=item.id).first()
    if in_inventory_check is not None:
        in_inventory = True
        return render_template("operator.html", page_title=operator, item=item, org=org, items=items, in_inventory=in_inventory)
    else:
        in_inventory = False
        return render_template("operator.html", page_title=operator, item=item, org=org, items=items, in_inventory=in_inventory)


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
    in_inventory_check = UserItem.query.filter_by(user_id=current_user.id, item_id=item.id).first()
    if in_inventory_check is not None:
        in_inventory = True
        return render_template("operator.html", page_title=operator, item=item, org=org, items=items, in_inventory=in_inventory)
    else:
        in_inventory = False
        return render_template("operator.html", page_title=operator, item=item, org=org, items=items, in_inventory=in_inventory)
    return render_template("charm.html", page_title=charm, item=item)


@app.route('/headgear/<headgear>')
def headgear(headgear):
    headgear = headgear.replace("%20", " ")
    item = Item.query.filter_by(name=headgear).first_or_404()
    in_inventory_check = UserItem.query.filter_by(user_id=current_user.id, item_id=item.id).first()
    if in_inventory_check is not None:
        in_inventory = True
        return render_template("operator.html", page_title=operator, item=item, org=org, items=items, in_inventory=in_inventory)
    else:
        in_inventory = False
        return render_template("operator.html", page_title=operator, item=item, org=org, items=items, in_inventory=in_inventory)
    return render_template("headgear.html", page_title=headgear, item=item)


@app.route('/uniform/<uniform>')
def uniform(uniform):
    uniform = uniform.replace("%20", " ")
    item = Item.query.filter_by(name=uniform).first_or_404()
    in_inventory_check = UserItem.query.filter_by(user_id=current_user.id, item_id=item.id).first()
    if in_inventory_check is not None:
        in_inventory = True
        return render_template("operator.html", page_title=operator, item=item, org=org, items=items, in_inventory=in_inventory)
    else:
        in_inventory = False
        return render_template("operator.html", page_title=operator, item=item, org=org, items=items, in_inventory=in_inventory)
    return render_template("uniform.html", page_title=uniform, item=item)


@app.route('/skin/<skin>')
def skin(skin):
    skin = skin.replace("%20", " ")
    item = Item.query.filter_by(name=skin).first_or_404()
    in_inventory_check = UserItem.query.filter_by(user_id=current_user.id, item_id=item.id).first()
    if in_inventory_check is not None:
        in_inventory = True
        return render_template("operator.html", page_title=operator, item=item, org=org, items=items, in_inventory=in_inventory)
    else:
        in_inventory = False
        return render_template("operator.html", page_title=operator, item=item, org=org, items=items, in_inventory=in_inventory)
    return render_template("skin.html", page_title=skin, item=item)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403
