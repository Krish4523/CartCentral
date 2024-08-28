import os
import random
from datetime import datetime, timedelta

from flask import redirect, render_template, url_for, request, jsonify, send_from_directory
from jinja2 import ChoiceLoader, FileSystemLoader
from werkzeug.utils import secure_filename

from connection import CC, db
from sqlalchemy import and_
from models import Customer, Category, Subcategory, Admin, Merchant, Product, Cart, Orders, Spec, Image, Sale

template_folders = [
    # Customer Folders
    "customer/sign_up-in",
    "customer/home",
    "customer/profile",
    "customer/cart",
    "customer/buynow",
    "customer/orders",
    "customer/product",
    "customer/productList",
    "customer/homeProduct",

    # Admin folders
    "admin/login",
    "admin/home",
    "admin/sales",
    "admin/category",
    "admin/profile",

    # Merchant Folder
    "merchant/sign_up-in",
    "merchant/home",
    "merchant/profile",
    "merchant/sales",
    "merchant/products",
    "merchant/addEditProduct"
]

loaders = [FileSystemLoader(folder) for folder in template_folders]
choice_loader = ChoiceLoader(loaders)
CC.jinja_env.loader = choice_loader
user: Customer
admin: Admin
merchant: Merchant


@CC.context_processor
def utility_processor(): return dict(len=len, replace=str.replace, render_template=render_template)


@CC.route("/")
def main(): return redirect("/customer")


#  Admin Routes
@CC.route("/admin")
def toAdmin():
    CC.static_folder = "admin/login"
    return render_template(
        "login.html",
        css=url_for("static", filename="login.css"),
        js=url_for("static", filename="login.js"),
        img=url_for("static", filename="cartImg.jpg")
    )


@CC.route("/login/admin", methods=["POST"])
def adminLogin():
    global admin
    admin = Admin.query.filter(Admin.username == request.form["username"]).first()
    return redirect("/admin/home")


@CC.route("/login/admin/check", methods=["POST"])
def adminCheck():
    if "password" in request.json:
        return jsonify({
            "hasUser": Admin.query.filter(Admin.password == request.json["password"]).first() is not None
        })
    if "username" in request.json:
        return jsonify({
            "hasUser": Admin.query.filter(Admin.username == request.json["username"]).first() is not None
        })
    return jsonify({"hasUser": False})


@CC.route("/admin/home")
def adminHome():
    CC.static_folder = "admin/home"
    return render_template(
        "adminHome.html",
        css=url_for("static", filename="adminHome.css"),
        js=url_for("static", filename="adminHome.js"),
        logo=url_for("static", filename="cartCentralLogo.jpg")
    )


@CC.route("/admin/sales")
def adminSales():
    CC.static_folder = "admin/sales"
    categories = Category().query.all()
    sub_cat_data = {}
    for category in categories:
        for sub in category.subcategories:
            total_products, total_price = 0, 0
            for sale in sub.sales:
                total_products += sale.quantity
                total_price += sale.price
            sub_cat_data[sub.categoryname] = {
                "totalProducts": total_products,
                "totalPrice": total_price
            }

    return jsonify({
        "template": render_template("adminSales.html", categories=categories,
                                    css=url_for("static", filename="adminSales.css"), subcatdata=sub_cat_data),
        "jsUrl": url_for("static", filename="adminSales.js")
    })


@CC.route("/admin/category")
def get_categories():
    try:
        CC.static_folder = "admin/category"
        categories = Category().query.all()
        products_by_category = {}
        for category in categories:
            total_products = 0
            for sub in category.subcategories:
                total_products += len(sub.products)
            products_by_category[category.catid] = total_products
        return jsonify({
            "template": render_template("category.html", categories=categories,
                                        css=url_for("static", filename="category.css"),
                                        productsbycategory=products_by_category),
            "jsUrl": url_for("static", filename="category.js")
        })
    except Exception as e:
        print(e)
        return "Error", 200


@CC.route("/admin/addCategory", methods=["POST"])
def add_category():
    data = request.json
    try:
        db.session.add(Category(categorytype=data["categoryType"]))
        db.session.commit()
        CC.static_folder = "admin/category"
        return render_template("categoryTemplate.html",
                               category=Category.query.filter_by(categorytype=data["categoryType"]).first(),
                               totalproducts=0)
    except Exception as e:
        print(e)
        return "Error", 200


@CC.route("/admin/addSubcategory", methods=["POST"])
def add_subcategory():
    data = request.json
    try:
        db.session.add(Subcategory(catid=data["catId"], categoryname=data["categoryName"]))
        db.session.commit()
        CC.static_folder = "admin/category"
        return render_template("subcatTemplate.html",
                               sub=Subcategory().query.filter_by(categoryname=data["categoryName"]).first())
    except Exception as e:
        print(e)
        return "Error", 200


@CC.route("/admin/updateCategory", methods=["POST"])
def update_category():
    data = request.json
    try:
        category = Category.query.filter(Category.catid == data["catId"]).first()
        category.categorytype = data["categoryType"]
        db.session.add(category)
        db.session.commit()

        total_products = 0
        for sub in category.subcategories:
            total_products += len(sub.products)
        CC.static_folder = "admin/category"
        return ""
    except Exception as e:
        print(e)
        return "Error", 200


@CC.route("/admin/updateSubcategory", methods=["POST"])
def update_subcategory():
    data = request.json
    try:
        subcategory = Subcategory.query.filter(Subcategory.subcatid == data["subCatId"]).first()
        subcategory.categoryname = data["categoryName"]
        db.session.add(subcategory)
        db.session.commit()

        return ""
    except Exception as e:
        print(e)
        return "Error", 200


@CC.route("/admin/removeCategory", methods=["POST"])
def remove_category():
    data = request.json
    try:
        db.session.delete(Category.query.filter(Category.catid == data["catId"]).first())
        db.session.commit()

        return ""
    except Exception as e:
        print(e)
        return "Error", 200


@CC.route("/admin/removeSubcategory", methods=["POST"])
def remove_subcategory():
    data = request.json
    try:
        db.session.delete(Subcategory.query.filter(Subcategory.subcatid == data["subCatId"]).first())
        db.session.commit()

        return ""
    except Exception as e:
        print(e)
        return "Error", 200


@CC.route("/admin/profile")
def admin_profile():
    global admin
    CC.static_folder = "admin/profile"
    db.session.add(admin)
    return jsonify({
        "template": render_template("adminProfile.html", admin=admin,
                                    css=url_for("static", filename="adminProfile.css")),
        "jsUrl": url_for("static", filename="adminProfile.js")
    })


@CC.route("/admin/changedata", methods=["POST"])
def change_admin_data():
    global admin
    changed_data = request.json["changedData"]
    for key, value in changed_data.items():
        setattr(admin, key, value)
    db.session.add(admin)
    db.session.commit()
    return "Pass"


# User routes

@CC.route("/customer")
def customer():
    CC.static_folder = "customer/sign_up-in"
    return render_template(
        "signup.html",
        css=url_for("static", filename="signup.css"),
        js=url_for("static", filename="signup.js"),
        img=url_for("static", filename="cartImg.jpg")
    )


@CC.route("/register/customer/check", methods=["POST"])
def customer_register_check():
    data = request.json
    json = {"hasUsername": False, "hasEmail": False}
    if data["username"] != "":
        json["hasUsername"] = Customer.query.filter(Customer.username == data["username"]).first() is not None
    if data["email"] != "":
        json["hasEmail"] = Customer.query.filter(Customer.email == data["email"]).first() is not None
    return jsonify(json)


@CC.route("/register/user", methods=["POST"])
def register_user():
    db.session.add(
        Customer(username=request.form["username"], password=request.form["password"], email=request.form["email"]))
    db.session.commit()
    return redirect("/customer/home")


@CC.route("/login/customer/check", methods=["POST"])
def customer_login_check():
    if "password" in request.json:
        return jsonify({
            "hasUser": Customer.query.filter(Customer.password == request.json["password"]).first() is not None
        })
    if "username" in request.json:
        return jsonify({
            "hasUser": Customer.query.filter(Customer.username == request.json["username"]).first() is not None
        })
    return jsonify({"hasUser": False})


@CC.route("/login/user", methods=["POST"])
def login_user():
    global user
    user = Customer.query.filter(Customer.username == request.form["username"]).first()
    return redirect("/customer/home")


@CC.route("/customer/home")
def home():
    try:
        CC.static_folder = "customer/home"
        return render_template(
            "home.html",
            css=url_for("static", filename="home.css"),
            js=url_for("static", filename="home.js"),
        )
    except Exception as e:
        print(e)
        return "An error occurred while rendering the home page.", 200


@CC.route("/customer/orders")
def orders():
    global user
    CC.static_folder = "customer/orders"
    try:
        return jsonify({
            "template": render_template(
                "orders.html",
                css=url_for("static", filename="orders.css"),
                products=db.session.query(Orders, Product).join(Orders, Orders.pid == Product.pid).filter(
                    user.cid == Orders.cid).all()
            ),
            "jsUrl": url_for("static", filename="orders.js"),
        })
    except Exception as e:
        print(e)
        return "Pass"


@CC.route("/customer/profile")
def profile():
    global user
    CC.static_folder = "customer/profile"
    db.session.add(user)
    return jsonify({
        "template": render_template("profile.html",
                                    css=url_for("static", filename="profile.css"),
                                    customer=user),
        "jsUrl": url_for("static", filename="profile.js"),
    })


@CC.route("/customer/changedata", methods=["POST"])
def change_user_data():
    changed_data = request.json["changedData"]
    for key, value in changed_data.items():
        setattr(user, key, value)
    try:
        db.session.add(user)
        db.session.commit()

    except Exception as e:
        print(e)
        return "pass"
    return "Pass"


@CC.route("/customer/cart")
def cart():
    global user
    CC.static_folder = "customer/cart"
    db.session.add(user)
    cp = db.session.query(Cart, Product).join(Product, Cart.pid == Product.pid).filter(user.cid == Cart.cid).all()
    try:
        return jsonify({
            "template": render_template(
                "cart.html",
                products=cp,
                css=url_for("static", filename="cart.css"),
            ),
            "jsUrl": url_for("static", filename="cart.js"),
        })
    except Exception as e:
        print(e)
        return "Pass"


@CC.route("/addCart/<int:product_id>")
def add_to_cart(product_id):
    global user
    try:
        cart_item = Cart.query.filter_by(pid=product_id, cid=user.cid).first()
        if cart_item:
            cart_item.quantity += 1
        else:
            db.session.add(Cart(cid=user.cid, pid=product_id, quantity=1))
        db.session.commit()
        return redirect("/customer/cart")
    except Exception as e:
        print(e)
        return "An error occurred while adding the product to the cart", 500


@CC.route("/product-list/<int:subcat_id>")
def products_list(subcat_id):
    product_spec = Product.query.filter_by(subcatid=subcat_id).all()
    specs = {}
    specs_from_db = []
    for product in product_spec:
        specs_from_db.extend(product.specs)
    for spec in specs_from_db:
        category = spec.name
        value = spec.value
        category_id = category.lower().replace(' ', '-')
        value_id = value.lower().replace(' ', '-')

        if category_id not in specs:
            specs[category_id] = {'name': category, 'values': []}
        values = specs[category_id]['values']
        value_dict = {'value': value, 'id': value_id}
        if value_dict not in values:
            specs[category_id]['values'].append(value_dict)
    try:
        CC.static_folder = "customer/productList"
        return jsonify({
            "template": render_template("productList.html", products=product_spec, specs=specs,
                                        css=url_for("static", filename="productList.css")),
            "jsUrl": url_for("static", filename="productList.js")
        })
    except Exception as e:
        print(e)
        return "Error", 200


@CC.route("/products/filter", methods=["POST"])
def filter_product():
    data = request.json
    results = set({})
    for key, value_list in data.items():
        q = Product.query.join(Spec, and_(Product.pid == Spec.pid, Spec.name == key))
        for value in value_list:
            results = results.intersection(q.filter(Spec.value == value).all()) if len(results) != 0 else set(
                q.filter(Spec.value == value).all())
    return render_template("forProductsOnly.html", products=results)


@CC.route("/products/<int:product_id>")
def products(product_id):
    try:
        CC.static_folder = "customer/product"
        return jsonify({
            "template": render_template("product.html",
                                        product=Product.query.filter_by(pid=product_id).first(),
                                        css=url_for("static", filename="product.css"),
                                        images=Image.query.filter_by(pid=product_id)),
            "jsUrl": url_for("static", filename="product.js")
        })
    except Exception as e:
        print(e)
        return "Error", 200


@CC.route("/customer/home_products")
def home_products():
    try:
        CC.static_folder = "customer/homeProduct"
        return jsonify({
            "template": render_template("homeProduct.html",
                                        categories=Category.query.all()),
            "jsUrl": url_for("static", filename="homeProduct.js")
        })
    except Exception as e:
        print(e)
        return "Error", 200


@CC.route("/buynow/<int:product_id>")
def buynow(product_id):
    global user
    try:
        CC.static_folder = "customer/buynow"
        product = Product.query.filter_by(pid=product_id).first()
        quantity = 1
        existing_cart_item = Cart.query.filter_by(cid=user.cid, pid=product_id).first()
        if existing_cart_item is not None:
            quantity = existing_cart_item.quantity
        return jsonify({
            "template": render_template(
                "buyNow.html",
                product=product,
                address=user.address,
                css=url_for("static", filename="buyNow.css"),
                images=Image.query.filter_by(pid=product_id),
                quantity=quantity
            ),
            "jsUrl": url_for("static", filename="buyNow.js"),
        })
    except Exception as e:
        print(e)
        return "Error", 200


@CC.route("/removeCart/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):
    try:
        cart_item = Cart.query.filter_by(pid=product_id, cid=user.cid).first()
        if cart_item:
            db.session.delete(cart_item)
            db.session.commit()
            return "Product removed from cart successfully", 200
        else:
            return "Product not found in cart", 404
    except Exception as e:
        print(e)
        return "An error occurred while removing the product from the cart", 500


@CC.route("/updateCartQuantity", methods=["POST"])
def update_cart_quantity():
    try:
        data = request.json
        product_id = data.get("productId")
        quantity = data.get("quantity")
        cart_item = Cart.query.filter_by(pid=product_id, cid=user.cid).first()
        if cart_item:
            cart_item.quantity = quantity
            db.session.commit()
            return "Quantity updated successfully", 200
        else:
            return "Product not found in cart", 404
    except Exception as e:
        print(e)
        return "An error occurred while updating quantity", 500


@CC.route("/payment/order", methods=["POST"])
def process_order():
    try:
        global user
        order_data = request.json
        product_id = order_data["productID"]
        form_data = order_data["formData"]
        delivery = datetime.now() + timedelta(days=random.randint(3, 5))
        new_order = Orders(
            pid=product_id,
            cid=user.cid,
            quantity=form_data["quantity"],
            price=form_data["price"],
            status="placed",
            deliveryaddress=form_data["delivery_address"],
            deliverydate=delivery
        )
        db.session.add(new_order)
        db.session.commit()
        new_sale = Sale(
            mid=Product.query.filter_by(pid=product_id).first().mid,
            pid=product_id,
            subcatid=Product.query.filter_by(pid=product_id).first().subcatid,
            price=form_data["price"],
            quantity=1,
            deliverydate=delivery
        )
        db.session.add(new_sale)
        db.session.commit()

        return jsonify({"success": True, "message": "Order placed successfully"}), 200
    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": "Failed to process the order"}), 500


@CC.route("/cancel/<int:order_id>")
def cancel_order(order_id):
    try:
        order = Orders.query.filter_by(oid=order_id).first()
        db.session.delete(order)
        db.session.commit()
        if order is None or order.status != 'placed':
            return "Invalid Order ID or the order has already been delivered.", 400

        order.status = 'canceled'
        db.session.commit()
        return "True", 200
    except Exception as e:
        print(e)
        return "False", 500


# Merchant Routes

@CC.route("/merchant")
def to_merchant():
    CC.static_folder = "merchant/sign_up-in"
    return render_template(
        "merchantSignup.html",
        css=url_for("static", filename="merchantSignup.css"),
        js=url_for("static", filename="merchantSignup.js"),
        img=url_for("static", filename="cartImg.jpg"),
    )


@CC.route("/register/merchant/check", methods=["POST"])
def register_merchant_check():
    data = request.json
    json = {"hasUsername": False, "hasEmail": False}
    if data["username"] != "":
        json["hasUsername"] = Merchant.query.filter(Merchant.username == data["username"]).first() is not None
    if data["email"] != "":
        json["hasEmail"] = Merchant.query.filter(Merchant.email == data["email"]).first() is not None
    return jsonify(json)


@CC.route("/register/merchant", methods=["POST"])
def register_merchant():
    db.session.add(
        Merchant(username=request.form["username"], gstnum=request.form["gstnum"], password=request.form["password"],
                 email=request.form["email"]))
    db.session.commit()
    return redirect("/merchant/home")


@CC.route("/login/merchant", methods=["POST"])
def loginMerchant():
    global merchant
    merchant = Merchant.query.filter(Merchant.username == request.form["username"]).first()
    return redirect("/merchant/home")


@CC.route("/merchant/home")
def merchant_home():
    CC.static_folder = "merchant/home"
    return render_template(
        "merchantHome.html",
        css=url_for("static", filename="merchantHome.css"),
        js=url_for("static", filename="merchantHome.js"),
    )


@CC.route("/login/merchant/check", methods=["POST"])
def merchant_login_check():
    if "password" in request.json:
        return jsonify({
            "hasUser": Merchant.query.filter(Merchant.password == request.json["password"]).first() is not None
        })
    if "username" in request.json:
        return jsonify({
            "hasUser": Merchant.query.filter(Merchant.username == request.json["username"]).first() is not None
        })
    return jsonify({"hasUser": False})


@CC.route("/merchant/profile")
def merchant_profile():
    CC.static_folder = "merchant/profile"
    db.session.add(merchant)
    return jsonify({
        "template": render_template("merchantProfile.html",
                                    css=url_for("static", filename="merchantProfile.css"),
                                    merchant=merchant),
        "jsUrl": url_for("static", filename="merchantProfile.js"),
    })


@CC.route("/merchant/changedata", methods=["POST"])
def change_merchant_data():
    global merchant
    changed_data = request.json["changedData"]
    for key, value in changed_data.items():
        setattr(merchant, key, value)
    db.session.add(merchant)
    db.session.commit()
    return "Pass"


@CC.route("/merchant/sales")
def merchant_sales():
    global merchant
    CC.static_folder = "merchant/sales"
    categories = Category().query.all()
    subcat_data = {}
    for category in categories:
        for sub in category.subcategories:
            total_products, total_price = 0, 0
            for sale in sub.sales:
                if sale.mid == merchant.mid:
                    total_products += sale.quantity
                    total_price += sale.price
            subcat_data[sub.categoryname] = {
                "totalProducts": total_products,
                "totalPrice": total_price
            }
    return jsonify({
        "template": render_template(
            "merchantSales.html",
            categories=categories,
            css=url_for("static", filename="merchantSales.css"),
            subcatdata=subcat_data
        ),
        "jsUrl": url_for("static", filename="merchantSales.js")
    })


@CC.route('/merchant/save-product', methods=['POST'])
def save_product():
    title = request.form['productTitle']
    quantity = request.form['productQuantity']
    price = request.form['productPrice']
    description = request.form['productDescription']
    # category = request.form['productCategory']
    subcategory = request.form['productSubcategory']
    images = request.files.getlist('image')  # Use getlist to get multiple files
    specs = {}
    for key, value in request.form.items():
        if key.startswith('specName_'):
            index = key.split('_')[-1]
            spec_name = value
            spec_value = request.form.get(f'specValue_{index}')
            specs[spec_name] = spec_value

    try:
        image_paths = []
        for image in images:
            if image:
                filename = secure_filename(image.filename)
                # Append timestamp to filename to make it unique
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
                # Replace problematic characters like colons with underscores
                filepath = os.path.join('cart-central/images/', f"{timestamp}_{filename}")
                image.save(filepath)
                image_paths.append(f"{timestamp}_{filename}")

        new_product = Product(title=title, price=price, description=description, quantity=quantity,
                              subcatid=subcategory, primaryimg=image_paths[0], mid=merchant.mid)
        image_paths.pop(0)
        for img_path in image_paths:
            new_product.images.append(Image(imgurl=img_path))

        for spec_name, spec_value in specs.items():
            new_product.specs.append(Spec(name=spec_name, value=spec_value))

        db.session.add(new_product)
        db.session.commit()

        return redirect('/merchant/home')
    except Exception as e:
        print(e)
        return redirect('/merchant/home')


@CC.route("/merchant/product-list")
def merchant_products_list():
    try:
        CC.static_folder = "merchant/products"
        return jsonify({
            "template": render_template("products.html", products=Product.query.filter_by(mid=merchant.mid).all(),
                                        css=url_for("static", filename="products.css")),
            "jsUrl": url_for("static", filename="products.js")
        })
    except Exception as e:
        print(e)
        return "Error", 200


@CC.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('cart-central/images', filename)


@CC.route("/merchant/add-product")
def add_product():
    try:
        CC.static_folder = "merchant/addEditProduct"
        return jsonify({
            "template": render_template("addEditProduct.html", id=-1),
            "jsUrl": url_for("static", filename="addEditProduct.js")
        })
    except Exception as e:
        print(e)
        return "Error", 200


@CC.route("/merchant/get-categories-and-subcategories")
def get_categories_and_subcategories():
    try:
        # Fetch categories and subcategories data from the database
        categories = Category.query.all()
        subcategories = Subcategory.query.all()

        # Prepare category and subcategory data to send to the frontend
        category_data = [{'id': category.catid, 'name': category.categorytype} for category in categories]
        subcategory_data = [{
            'id': subcategory.subcatid,
            'name': subcategory.categoryname,
            'catid': subcategory.catid
        } for subcategory in subcategories]

        return jsonify({'categories': category_data, 'subcategories': subcategory_data})
    except Exception as e:
        return jsonify({'error': str(e)})


@CC.route("/merchant/delete/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    try:
        product = Product.query.get(product_id)
        if product:
            db.session.delete(product)
            db.session.commit()
            return jsonify({"message": "Product deleted successfully"}), 200
        else:
            return jsonify({"error": "Product not found"}), 404
    except Exception as e:
        print(e)
        return jsonify({"error": "Internal Server Error"}), 500


@CC.route("/profile/check", methods=["POST"])
def profile_check():
    global user
    data = request.json
    json = {"hasUsername": False, "hasEmail": False, "validPassword": False, "hasPassword": False}
    if data["username"] and data["username"] != user.username:
        json["hasUsername"] = (Customer.query.filter(Customer.username == data["username"]).first() is not None)
    if data["password"] and data["password"] != user.password:
        json["hasPassword"] = (Customer.query.filter(Customer.password == data["currPassword"]).first() is not None)
    if data["email"] and data["email"] != user.email:
        json["hasEmail"] = (Customer.query.filter(Customer.email == data["email"]).first() is not None)

    json["validPassword"] = (data["currPassword"] and data["currPassword"] != user.password)
    return jsonify(json)


if __name__ == '__main__':
    CC.run(debug=True)
