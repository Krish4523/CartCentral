from connection import db


class Customer(db.Model):
    __tablename__ = 'customer'
    cid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    address = db.Column(db.Text, nullable=True)
    phone = db.Column(db.Numeric, nullable=True)
    email = db.Column(db.String(200), nullable=False, unique=True)


class Merchant(db.Model):
    __tablename__ = 'merchant'
    mid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    address = db.Column(db.Text, default=None)
    phone = db.Column(db.BigInteger, default=None)
    email = db.Column(db.String(200), nullable=False, unique=True)
    gstnum = db.Column(db.String(200), nullable=False)


class Category(db.Model):
    __tablename__ = 'categories'
    catid = db.Column(db.Integer, primary_key=True)
    categorytype = db.Column(db.String(200), nullable=False)
    addingdate = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    lastupdated = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(),
                            onupdate=db.func.current_timestamp())
    subcategories = db.relationship('Subcategory', backref='parent_category', lazy=True)


class Subcategory(db.Model):
    __tablename__ = 'subcategories'
    subcatid = db.Column(db.Integer, primary_key=True)
    catid = db.Column(db.Integer, db.ForeignKey('categories.catid'), nullable=False)
    categoryname = db.Column(db.String(200), nullable=False)
    addingdate = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    lastupdated = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(),
                            onupdate=db.func.current_timestamp())
    products = db.relationship("Product", backref="products", lazy=True)
    sales = db.relationship("Sale", backref="subcategory", lazy=True)


class Product(db.Model):
    __tablename__ = 'product'
    pid = db.Column(db.Integer, primary_key=True)
    subcatid = db.Column(db.Integer, db.ForeignKey('subcategories.subcatid'))
    mid = db.Column(db.Integer, db.ForeignKey('merchant.mid'))
    price = db.Column(db.Numeric, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    addingdate = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    lastupdated = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    primaryimg = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    images = db.relationship("Image", backref="product", lazy=True)
    specs = db.relationship("Spec", backref="product", lazy=True)
    sales = db.relationship("Sale", backref="product", lazy=True)


class Image(db.Model):
    __tablename__ = 'images'
    imgid = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer, db.ForeignKey('product.pid'))
    imgurl = db.Column(db.Text, nullable=False)


class Spec(db.Model):
    __tablename__ = 'specs'
    sid = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer, db.ForeignKey('product.pid'))
    name = db.Column(db.String(200), nullable=False)
    value = db.Column(db.String(200), nullable=False)


class Sale(db.Model):
    __tablename__ = 'sales'
    saleid = db.Column(db.Integer, primary_key=True)
    mid = db.Column(db.Integer, db.ForeignKey('merchant.mid'))
    pid = db.Column(db.Integer, db.ForeignKey('product.pid'))
    subcatid = db.Column(db.Integer, db.ForeignKey('subcategories.subcatid'))
    price = db.Column(db.Numeric, nullable=False)
    quantity = db.Column(db.Numeric, nullable=False)
    deliverydate = db.Column(db.TIMESTAMP, nullable=True)


class Cart(db.Model):
    __tablename__ = 'cart'
    cid = db.Column(db.Integer, db.ForeignKey('customer.cid'), primary_key=True)
    pid = db.Column(db.Integer, db.ForeignKey('product.pid'), primary_key=True)
    quantity = db.Column(db.Integer)
    products = db.relationship("Product", backref="cartProducts")


class Orders(db.Model):
    __tablename__ = 'orders'
    oid = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer, db.ForeignKey('product.pid'), nullable=False)
    cid = db.Column(db.Integer, db.ForeignKey('customer.cid'), nullable=False)
    quantity = db.Column(db.Numeric, nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    status = db.Column(db.String(200))
    deliveryaddress = db.Column(db.Text, nullable=False)
    orderdate = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    deliverydate = db.Column(db.TIMESTAMP, nullable=True)


class Admin(db.Model):
    __tablename__ = 'admin'
    aid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), default=None)
    username = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.BigInteger, default=None)
    email = db.Column(db.String(200), nullable=False, unique=True)
