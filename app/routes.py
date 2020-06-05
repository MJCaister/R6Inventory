from flask import render_template, url_for, redirect, flash
from app import app, db
from app.models import Item, ItemType, OperatorOrg
# from app.forms import

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


@app.route('/weapons')
def weapons():
    items = Item.query.filter(Item.type.in_([8])).all()
    return render_template("list_items.html", page_title='Weapons', items=items)


@app.route('/operators')
def operators():
    items = Item.query.filter(Item.type.in_([5])).all()
    return render_template("list_items.html", page_title='Operators', items=items)


@app.route('/organisations')
def organisations():
    items = Item.query.filter(Item.type.in_([6])).all()
    return render_template("list_items.html", page_title='Organisations', items=items)


@app.route('/charms')
def charms():
    items = Item.query.filter(Item.type.in_([2])).all()
    return render_template("list_items.html", page_title='Charms', items=items)


@app.route('/headgears')
def headgears():
    items = Item.query.filter(Item.type.in_([3])).all()
    return render_template("list_items.html", page_title='Headgears', items=items)


@app.route('/uniforms')
def uniforms():
    items = Item.query.filter(Item.type.in_([4])).all()
    return render_template("list_items.html", page_title='Uniforms', items=items)


@app.route('/skins')
def skins():
    items = Item.query.filter(Item.type.in_([7])).all()
    return render_template("list_items.html", page_title='Skins', items=items)


@app.route('/weapon/<weapon>')
def weapon(weapon):
    weapon = weapon.replace("%20", " ")
    item = Item.query.filter_by(name=weapon).first_or_404()
    return render_template("weapon.html", page_title=weapon, item=item)


@app.route('/operator/<operator>')
def operator(operator):
    operator = operator.replace("%20", " ")
    item = Item.query.filter_by(name=operator).first_or_404()
    op_org = OperatorOrg.query.filter_by(operator_id=item.id).first()
    org = Item.query.filter_by(id=op_org.org_id).first()
    return render_template("operator.html", page_title=operator, item=item, org=org)


@app.route('/organisation/<organisation>')
def organisation(organisation):
    organisation = organisation.replace("%20", " ")
    item = Item.query.filter_by(name=organisation).first_or_404()
    org_ops = OperatorOrg.query.filter_by(org_id=item.id).all()
    ops_temp = []
    for op in org_ops:
        ops_temp.append(op.operator_id)
    ops = Item.query.filter(Item.id.in_(ops_temp)).all()
    return render_template("organisation.html", page_title=organisation, item=item, ops=ops)


@app.route('/charm/<charm>')
def charm(charm):
    charm = charm.replace("%20", " ")
    item = Item.query.filter_by(name=charm).first_or_404()
    return render_template("charm.html", page_title=charm, item=item)


@app.route('/headgear/<headgear>')
def headgear(headgear):
    headgear = headgear.replace("%20", " ")
    item = Item.query.filter_by(name=headgear).first_or_404()
    return render_template("headgear.html", page_title=headgear, item=item)


@app.route('/uniform/<uniform>')
def uniform(uniform):
    uniform = uniform.replace("%20", " ")
    item = Item.query.filter_by(name=uniform).first_or_404()
    return render_template("uniform.html", page_title=uniform, item=item)


@app.route('/skin/<skin>')
def skin(skin):
    skin = skin.replace("%20", " ")
    item = Item.query.filter_by(name=skin).first_or_404()
    return render_template("skin.html", page_title=skin, item=item)
