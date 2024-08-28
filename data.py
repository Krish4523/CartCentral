import random
from datetime import datetime, timedelta

from connection import db, CC
from models import Category, Subcategory, Merchant, Customer, Product, Admin, Spec, Cart, Sale, Orders, Image

# Sample data lists
customer_names = ["John Doe", "Jane Smith", "Michael Johnson", "Emily Brown", "David Davis"]
merchant_names = ["Electro Deals", "Fashion Junction", "Book Haven", "Sports Emporium", "Beauty Essentials",
                  "Tech Galaxy", "Style Hub", "Novelty Bookstore", "Outdoor Adventures", "Glamour Palace"]
categories = [
    ("Electronics", ["Smartphones", "Laptops", "Headphones", "Cameras", "Smart Watches"]),
    ("Clothing", ["Men's Clothing", "Women's Clothing", "Kid's Clothing", "Shoes", "Accessories"]),
    ("Books", ["Fiction", "Non-Fiction", "Children's Books", "Self-Help", "Biographies"]),
    ("Sports & Outdoors", ["Fitness Equipment", "Camping Gear", "Outdoor Clothing", "Bicycles", "Sports Accessories"]),
    ("Beauty & Personal Care", ["Skincare", "Haircare", "Makeup", "Fragrances", "Personal Hygiene"]),
    ("Toys & Games", ["Action Figures", "Board Games", "Puzzles", "Educational Toys", "Outdoor Toys"]),
    ("Furniture", ["Living Room", "Bedroom", "Kitchen & Dining", "Office", "Outdoor"])
]


# Function to generate random phone numbers
def generate_phone():
    return f"{random.randint(200, 999)}{random.randint(100, 999)}{random.randint(1000, 9999)}"


# Function to generate random email addresses
def generate_email(email):
    return email.replace(" ", "").lower() + "@example.com"


# Create customers
customers = []
for name in customer_names:
    customer = Customer(name=name, username=name.lower().replace(" ", ""), password="password123",
                        address=f"{random.randint(1, 1000)} Street, City", phone=generate_phone(),
                        email=generate_email(name))
    customers.append(customer)

# Create merchants
merchants = []
for name in merchant_names:
    merchant = Merchant(name=name, username=name.lower().replace(" ", ""), password="merchant456",
                        email=generate_email(name), gstnum=f"GST{random.randint(100000000, 999999999)}")
    merchants.append(merchant)

# Create categories and subcategories
categories_entities = []
subcategories_entities = []

for cat_id, (category, subcategories) in enumerate(categories, start=1):
    cat_entity = Category(categorytype=category)
    categories_entities.append(cat_entity)

    for subcat_name in subcategories:
        subcat_entity = Subcategory(categoryname=subcat_name, parent_category=cat_entity)
        subcategories_entities.append(subcat_entity)

products_data = {
    "Smartphones": ["iPhone 13", "Samsung Galaxy S22", "Google Pixel 7", "OnePlus 10", "Xiaomi Mi 12"],
    "Laptops": ["MacBook Pro", "Dell XPS 15", "HP Spectre x360", "Lenovo ThinkPad X1 Carbon", "Asus ZenBook"],
    "Headphones": ["Sony WH-1000XM4", "Bose QuietComfort 45", "Apple AirPods Pro", "Sennheiser Momentum 3",
                   "Jabra Elite 85t"],
    "Smart Watches": ["Apple Watch Series 7", "Samsung Galaxy Watch 4", "Fitbit Versa 4", "Garmin Fenix 6",
                      "Huawei Watch GT 3"],
    "Men's Clothing": ["Levi's Jeans", "Nike Hoodie", "Adidas T-shirt", "Ralph Lauren Polo Shirt",
                       "Tommy Hilfiger Jacket"],
    "Women's Clothing": ["Zara Dress", "H&M Blouse", "Forever 21 Skirt", "ASOS Jeans", "Urban Outfitters Sweater"],
    "Kid's Clothing": ["Gap Kids T-shirt", "Carter's Onesie", "Old Navy Jeans", "Children's Place Dress",
                       "Hanna Andersson Pajamas"],
    "Shoes": ["Nike Air Force 1", "Adidas Ultraboost", "Vans Old Skool", "Converse Chuck Taylor", "New Balance 574"],
    "Accessories": ["Ray-Ban Sunglasses", "Gucci Belt", "Coach Wallet", "Fossil Watch", "Michael Kors Handbag"],
    "Fiction": ["Harry Potter and the Sorcerer's Stone", "To Kill a Mockingbird", "The Great Gatsby", "1984",
                "The Catcher in the Rye"],
    "Non-Fiction": ["Sapiens: A Brief History of Humankind", "The Subtle Art of Not Giving a F*ck", "Educated",
                    "Becoming", "Atomic Habits"],
    "Children's Books": ["The Very Hungry Caterpillar", "Goodnight Moon", "Where the Wild Things Are",
                         "Green Eggs and Ham", "The Giving Tree"],
    "Self-Help": ["The 7 Habits of Highly Effective People", "How to Win Friends and Influence People",
                  "The Power of Now", "Girl, Wash Your Face", "Daring Greatly"],
    "Biographies": ["Steve Jobs by Walter Isaacson", "Becoming by Michelle Obama", "Elon Musk by Ashlee Vance",
                    "Leonardo da Vinci by Walter Isaacson", "Shoe Dog by Phil Knight"],
    "Fitness Equipment": ["Dumbbell Set", "Yoga Mat", "Resistance Bands", "Jump Rope", "Exercise Ball"],
    "Camping Gear": ["Tent", "Sleeping Bag", "Portable Stove", "Camping Chair", "Headlamp"],
    "Outdoor Clothing": ["The North Face Jacket", "Patagonia Fleece", "Columbia Hiking Pants", "Arc'teryx Rain Jacket",
                         "Marmot Down Vest"],
    "Bicycles": ["Road Bike", "Mountain Bike", "Hybrid Bike", "Electric Bike", "Folding Bike"],
    "Sports Accessories": ["Basketball", "Soccer Ball", "Yoga Block", "Gymnastics Rings", "Tennis Racquet"],
    "Skincare": ["Cleanser", "Moisturizer", "Sunscreen", "Serum", "Exfoliant"],
    "Haircare": ["Shampoo", "Conditioner", "Hair Mask", "Hair Oil", "Styling Gel"],
    "Makeup": ["Foundation", "Mascara", "Lipstick", "Eyeliner", "Highlighter"],
    "Fragrances": ["Perfume", "Cologne", "Body Spray", "Aftershave", "Rollerball"],
    "Personal Hygiene": ["Toothpaste", "Toothbrush", "Deodorant", "Soap", "Floss"],
    "Action Figures": ["Marvel Legends Spider-Man", "Star Wars Black Series Darth Vader", "Transformers Optimus Prime",
                       "Pokémon Pikachu", "GI Joe Snake Eyes"],
    "Board Games": ["Settlers of Catan", "Ticket to Ride", "Codenames", "Pandemic", "Carcassonne"],
    "Puzzles": ["1000-Piece Landscape Puzzle", "3D Crystal Puzzle", "Wooden Brain Teaser", "Disney Jigsaw Puzzle",
                "Escape Room Puzzle"],
    "Educational Toys": ["LEGO Classic Brick Box", "Melissa & Doug Wooden Blocks", "VTech Alphabet Train",
                         "Fisher-Price Think & Learn Code-a-Pillar", "Osmo Genius Starter Kit"],
    "Outdoor Toys": ["Nerf N-Strike Elite", "Water Balloon Launcher", "Bubbles Machine", "Slip 'N Slide",
                     "Sidewalk Chalk"],
    "Living Room": ["Sofa", "Coffee Table", "TV Stand", "Floor Lamp", "Area Rug"],
    "Bedroom": ["Bed Frame", "Mattress", "Nightstand", "Dresser", "Table Lamp"],
    "Kitchen & Dining": ["Dining Table", "Dining Chairs", "Kitchen Island", "Bar Stools", "Dinnerware Set"],
    "Office": ["Desk", "Office Chair", "Bookshelf", "Filing Cabinet", "Desk Lamp"],
    "Outdoor": ["Patio Furniture Set", "Grill", "Outdoor Umbrella", "Fire Pit", "Hammock"]
}

# Generate products for each subcategory
products = []
count = 1
for subcatid, (subcategory, product_list) in enumerate(products_data.items(), start=1):
    for product_name in product_list:
        product = Product(
            subcatid=subcatid,
            # Assuming you have a method to generate random merchant IDs
            mid=random.randint(1, 5),
            price=random.randint(1000, 2000000),  # Adjust price range as needed
            title=product_name,
            description=f"Description for {product_name}",
            primaryimg="image_" + str(count) + ".jpg",
            quantity=random.randint(1, 100),  # Random quantity in stock
        )
        count += 1
        products.append(product)

admin1 = Admin(username="admin", password="admin123", email="admin@example.com")

# Assuming you have defined the Spec class

# Sample specs data
specs_data = {
    "Smartphones": {
        "Display Size": ["6.1 inches", "6.2 inches", "6.4 inches", "6.5 inches", "6.7 inches"],
        "RAM": ["6 GB", "8 GB", "12 GB", "16 GB"],
        "Storage": ["128 GB", "256 GB", "512 GB", "1 TB"],
        "Battery Capacity": ["4000 mAh", "4500 mAh", "5000 mAh", "5500 mAh"],
        "Camera Resolution": ["12 MP", "16 MP", "20 MP", "24 MP"],
        "Processor": ["Snapdragon 888", "Exynos 2200", "Apple A15 Bionic", "Kirin 9000"],
    },
    "Laptops": {
        "Screen Size": ["13.3 inches", "14 inches", "15.6 inches", "16 inches", "17.3 inches"],
        "RAM": ["8 GB", "16 GB", "32 GB", "64 GB"],
        "Storage": ["256 GB SSD", "512 GB SSD", "1 TB SSD", "2 TB SSD", "4 TB SSD"],
        "Processor": ["Intel Core i5", "Intel Core i7", "AMD Ryzen 5", "AMD Ryzen 7"],
        "Graphics Card": ["NVIDIA GeForce GTX 1650", "NVIDIA GeForce RTX 3060", "AMD Radeon RX 6700M"],
        "Battery Life": ["Up to 8 hours", "Up to 10 hours", "Up to 12 hours", "Up to 15 hours"],
    },
    "Headphones": {
        "Driver Size": ["40 mm", "50 mm", "30 mm", "35 mm"],
        "Frequency Response": ["20 Hz - 20 kHz", "10 Hz - 40 kHz", "15 Hz - 25 kHz"],
        "Impedance": ["32 ohms", "64 ohms", "16 ohms", "80 ohms"],
        "Sensitivity": ["100 dB", "105 dB", "110 dB", "115 dB"],
        "Connectivity": ["Bluetooth 5.0", "Bluetooth 5.2", "Wired", "Wireless"],
    },
    "Cameras": {
        "Resolution": ["24 MP", "30 MP", "40 MP", "50 MP"],
        "Sensor Type": ["APS-C", "Full Frame", "Micro Four Thirds"],
        "Lens Mount": ["Canon EF", "Nikon F", "Sony E", "Micro Four Thirds"],
        "ISO Range": ["100-6400", "100-12800", "100-25600", "100-51200"],
        "Video Recording": ["4K at 30 fps", "4K at 60 fps", "1080p at 120 fps", "1080p at 240 fps"],
    },
    "Smart Watches": {
        "Display Type": ["AMOLED", "LCD", "Transflective"],
        "Battery Life": ["Up to 7 days", "Up to 10 days", "Up to 14 days"],
        "Water Resistance": ["IP68", "5 ATM", "10 ATM"],
        "Sensors": ["Heart Rate Monitor", "GPS", "Accelerometer", "Gyroscope"],
        "Compatibility": ["iOS", "Android", "Both"],
    },
    "Men's Clothing": {
        "Material": ["Cotton", "Polyester", "Linen", "Wool"],
        "Fit": ["Slim Fit", "Regular Fit", "Relaxed Fit"],
        "Size": ["S", "M", "L", "XL"],
        "Color": ["Black", "Blue", "White", "Gray"],
        "Style": ["T-shirt", "Polo Shirt", "Button-Down Shirt", "Hoodie"],
    },
    "Women's Clothing": {
        "Material": ["Cotton", "Polyester", "Silk", "Lace"],
        "Fit": ["Slim Fit", "Regular Fit", "Loose Fit"],
        "Size": ["XS", "S", "M", "L"],
        "Color": ["Red", "Pink", "Yellow", "Green"],
        "Style": ["Dress", "Blouse", "Skirt", "Jeans"],
    },
    "Kid's Clothing": {
        "Material": ["Cotton", "Polyester", "Organic Cotton", "Fleece"],
        "Fit": ["Slim Fit", "Regular Fit", "Loose Fit"],
        "Size": ["2T", "3T", "4T", "5T"],
        "Color": ["Blue", "Pink", "Yellow", "Green"],
        "Style": ["T-shirt", "Dress", "Leggings", "Jacket"],
    },
    "Shoes": {
        "Material": ["Leather", "Canvas", "Synthetic", "Mesh"],
        "Type": ["Sneakers", "Boots", "Sandals", "Flats"],
        "Size": ["US 6", "US 7", "US 8", "US 9"],
        "Color": ["Black", "Brown", "White", "Blue"],
        "Closure": ["Lace-up", "Slip-on", "Velcro"],
    },
    "Accessories": {
        "Material": ["Leather", "Metal", "Fabric", "Plastic"],
        "Type": ["Wallet", "Watch", "Belt", "Hat"],
        "Color": ["Black", "Brown", "Silver", "Gold"],
        "Size": ["Small", "Medium", "Large"],
        "Style": ["Casual", "Formal", "Sporty"],
    },
    "Fiction": {
        "Genre": ["Fantasy", "Mystery", "Science Fiction", "Romance"],
        "Pages": ["200 pages", "300 pages", "400 pages", "500 pages"],
        "Language": ["English", "Spanish", "French", "German"],
        "Format": ["Hardcover", "Paperback", "E-book"],
        "Author": ["J.K. Rowling", "Stephen King", "George R.R. Martin", "J.R.R. Tolkien"],
    },
    "Non-Fiction": {
        "Topic": ["Self-Help", "Business", "Biography", "History"],
        "Pages": ["200 pages", "300 pages", "400 pages", "500 pages"],
        "Language": ["English", "Spanish", "French", "German"],
        "Format": ["Hardcover", "Paperback", "E-book"],
        "Author": ["Malcolm Gladwell", "Stephen Covey", "Michelle Obama", "Bill Gates"],
    },
    "Children's Books": {
        "Age Range": ["0-2 years", "3-5 years", "6-8 years", "9-12 years"],
        "Pages": ["10 pages", "20 pages", "30 pages", "40 pages"],
        "Language": ["English", "Spanish", "French", "German"],
        "Illustrations": ["Colorful", "Black and White", "Hand-drawn"],
        "Author": ["Dr. Seuss", "Eric Carle", "Roald Dahl", "Mo Willems"],
    },
    "Self-Help": {
        "Topic": ["Motivation", "Productivity", "Mindfulness", "Relationships"],
        "Pages": ["200 pages", "300 pages", "400 pages", "500 pages"],
        "Language": ["English", "Spanish", "French", "German"],
        "Format": ["Hardcover", "Paperback", "E-book"],
        "Author": ["Brené Brown", "Tim Ferriss", "Tony Robbins", "Mark Manson"],
    },
    "Biographies": {
        "Subject": ["Leaders", "Artists", "Inventors", "Politicians"],
        "Pages": ["200 pages", "300 pages", "400 pages", "500 pages"],
        "Language": ["English", "Spanish", "French", "German"],
        "Format": ["Hardcover", "Paperback", "E-book"],
        "Author": ["Walter Isaacson", "David McCullough", "Ron Chernow", "Doris Kearns Goodwin"],
    },
    "Fitness Equipment": {
        "Type": ["Treadmill", "Exercise Bike", "Elliptical Trainer", "Rowing Machine"],
        "Resistance Levels": ["5 levels", "10 levels", "15 levels", "20 levels"],
        "Weight Capacity": ["250 lbs", "300 lbs", "350 lbs", "400 lbs"],
        "Display": ["LCD", "LED", "Touchscreen"],
        "Features": ["Heart Rate Monitor", "Bluetooth Connectivity", "Foldable Design"],
    },
    "Camping Gear": {
        "Type": ["Tent", "Sleeping Bag", "Backpack", "Camp Stove"],
        "Capacity": ["1 person", "2 person", "4 person", "6 person"],
        "Season Rating": ["3-season", "4-season"],
        "Material": ["Nylon", "Polyester", "Down"],
        "Features": ["Waterproof", "Windproof", "Breathable"],
    },
    "Outdoor Clothing": {
        "Material": ["Nylon", "Polyester", "Merino Wool", "Gore-Tex"],
        "Activity": ["Hiking", "Camping", "Running", "Cycling"],
        "Weather Protection": ["Waterproof", "Windproof", "Insulated"],
        "Fit": ["Slim Fit", "Regular Fit", "Relaxed Fit"],
        "Color": ["Black", "Gray", "Green", "Blue"],
    },
    "Bicycles": {
        "Type": ["Road Bike", "Mountain Bike", "Hybrid Bike", "Electric Bike"],
        "Frame Material": ["Aluminum", "Carbon Fiber", "Steel"],
        "Wheel Size": ["26 inches", "27.5 inches", "29 inches"],
        "Gears": ["Single Speed", "7 Speed", "21 Speed", "24 Speed"],
        "Suspension": ["Hardtail", "Full Suspension"],
    },
    "Sports Accessories": {
        "Type": ["Gloves", "Helmets", "Knee Pads", "Elbow Pads"],
        "Material": ["Polyester", "Neoprene", "Leather", "Foam"],
        "Size": ["Small", "Medium", "Large", "Extra Large"],
        "Color": ["Black", "Red", "Blue", "Green"],
        "Usage": ["Cycling", "Skating", "Skiing", "Football"],
    },
    "Skincare": {
        "Skin Type": ["Dry", "Oily", "Combination", "Sensitive"],
        "Product Type": ["Cleanser", "Moisturizer", "Serum", "Sunscreen"],
        "Ingredients": ["Hyaluronic Acid", "Vitamin C", "Retinol", "Salicylic Acid"],
        "Scent": ["Fragrance-Free", "Citrus", "Floral", "Herbal"],
        "Packaging": ["Bottle", "Tube", "Jar", "Pump"],
    },
    "Haircare": {
        "Hair Type": ["Straight", "Wavy", "Curly", "Coily"],
        "Product Type": ["Shampoo", "Conditioner", "Hair Oil", "Hair Mask"],
        "Ingredients": ["Argan Oil", "Coconut Oil", "Keratin", "Shea Butter"],
        "Scent": ["Fruity", "Floral", "Minty", "Woody"],
        "Packaging": ["Bottle", "Tube", "Jar", "Spray"],
    },
    "Makeup": {
        "Product Type": ["Foundation", "Concealer", "Lipstick", "Eyeshadow"],
        "Finish": ["Matte", "Dewy", "Satin", "Shimmer"],
        "Shade": ["Fair", "Light", "Medium", "Deep"],
        "Formula": ["Liquid", "Cream", "Powder", "Stick"],
        "Packaging": ["Bottle", "Tube", "Palette", "Compact"],
    },
    "Fragrances": {
        "Fragrance Type": ["Eau de Parfum", "Eau de Toilette", "Cologne", "Perfume Oil"],
        "Notes": ["Citrus", "Floral", "Woody", "Spicy"],
        "Longevity": ["Long-lasting", "Moderate", "Short-lived"],
        "Occasion": ["Everyday", "Evening", "Special Occasion"],
        "Bottle Size": ["50 ml", "100 ml", "200 ml", "250 ml"],
    },
    "Personal Hygiene": {
        "Product Type": ["Soap", "Body Wash", "Deodorant", "Hand Sanitizer"],
        "Scent": ["Fresh", "Clean", "Citrus", "Floral"],
        "Ingredients": ["Glycerin", "Tea Tree Oil", "Aloe Vera", "Shea Butter"],
        "Packaging": ["Bar", "Bottle", "Spray", "Pump"],
    },
    "Action Figures": {
        "Character": ["Superhero", "Villain", "Anime", "Movie Character"],
        "Height": ["6 inches", "8 inches", "12 inches", "18 inches"],
        "Material": ["Plastic", "Vinyl", "Resin", "Metal"],
        "Articulation": ["Fixed Pose", "Limited Articulation", "Fully Articulated"],
        "Accessories": ["Weapons", "Props", "Interchangeable Parts"],
    },
    "Board Games": {
        "Genre": ["Strategy", "Party", "Cooperative", "Family"],
        "Player Count": ["2 players", "3-4 players", "5-6 players", "7+ players"],
        "Play Time": ["30 minutes", "1 hour", "2 hours", "3+ hours"],
        "Age Range": ["Kids", "Family", "Teenagers", "Adults"],
        "Components": ["Board", "Cards", "Dice", "Tokens"],
    },
    "Puzzles": {
        "Puzzle Type": ["Jigsaw", "Logic", "3D", "Wooden"],
        "Difficulty": ["Easy", "Medium", "Hard", "Expert"],
        "Number of Pieces": ["100 pieces", "500 pieces", "1000 pieces", "2000 pieces"],
        "Theme": ["Landscapes", "Animals", "Cities", "Art"],
        "Size": ["Small", "Medium", "Large"],
    },
    "Educational Toys": {
        "Age Range": ["0-2 years", "3-5 years", "6-8 years", "9-12 years"],
        "Subject": ["STEM", "Language", "Mathematics", "Science"],
        "Skill Development": ["Problem Solving", "Creativity", "Critical Thinking"],
        "Material": ["Wood", "Plastic", "Fabric", "Cardboard"],
        "Interactive Features": ["Lights", "Sounds", "Buttons", "Movement"],
    },
    "Outdoor Toys": {
        "Type": ["Swing Set", "Trampoline", "Sand and Water Table", "Playhouse"],
        "Age Range": ["Toddler", "Preschool", "Elementary", "Tween"],
        "Material": ["Plastic", "Metal", "Wood"],
        "Assembly Required": ["Yes", "No"],
        "Safety Features": ["Safety Net", "Soft Edges", "Secure Anchoring"],
    },
    "Living Room": {
        "Furniture Type": ["Sofa", "Coffee Table", "TV Stand", "Bookshelf"],
        "Material": ["Wood", "Metal", "Glass", "Fabric"],
        "Color": ["Neutral", "Bold", "Monochrome", "Patterned"],
        "Style": ["Modern", "Traditional", "Contemporary", "Rustic"],
        "Dimensions": ["Small", "Medium", "Large"],
    },
    "Bedroom": {
        "Furniture Type": ["Bed", "Dresser", "Nightstand", "Wardrobe"],
        "Material": ["Wood", "Metal", "Upholstered", "Wicker"],
        "Color": ["White", "Brown", "Black", "Gray"],
        "Style": ["Modern", "Traditional", "Contemporary", "Vintage"],
        "Size": ["Twin", "Full", "Queen", "King"],
    },
    "Kitchen & Dining": {
        "Furniture Type": ["Dining Table", "Chairs", "Bar Stools", "Kitchen Island"],
        "Material": ["Wood", "Metal", "Glass", "Marble"],
        "Color": ["White", "Black", "Brown", "Silver"],
        "Style": ["Farmhouse", "Industrial", "Mid-Century Modern", "Contemporary"],
        "Seating Capacity": ["2 seats", "4 seats", "6 seats", "8+ seats"],
    },
    "Office": {
        "Furniture Type": ["Desk", "Office Chair", "Bookcase", "Filing Cabinet"],
        "Material": ["Wood", "Metal", "Glass", "Composite"],
        "Color": ["White", "Brown", "Black", "Gray"],
        "Style": ["Modern", "Traditional", "Contemporary", "Industrial"],
        "Size": ["Small", "Medium", "Large"],
    },
    "Outdoor": {
        "Furniture Type": ["Patio Set", "Outdoor Sofa", "Fire Pit", "Hammock"],
        "Material": ["Wicker", "Metal", "Wood", "Resin"],
        "Color": ["Beige", "Brown", "Gray", "Blue"],
        "Style": ["Modern", "Traditional", "Contemporary", "Rustic"],
        "Weather Resistance": ["Weatherproof", "Waterproof", "UV Resistant"],
    },
}

# Get a list of customer IDs from 1 to 5
customer_ids = list(range(1, 6))

# Get a list of product IDs from 1 to 170
product_ids = list(range(1, 171))

# Define the number of products to add to each cart (between 2 and 4)
min_products_per_cart = 2
max_products_per_cart = 4

order_statuses = ['Placed', 'Shipped']
num_orders = 50
num_sales = 50
# Generate carts for each customer

# Add data to the session
if __name__ == '__main__':
    with CC.app_context():
        db.create_all()
        db.session.add_all(customers)
        db.session.add_all(merchants)
        db.session.add_all(categories_entities)
        db.session.add_all(subcategories_entities)
        db.session.add_all(products)
        db.session.add(admin1)
        for product in Product.query.all():
            subcategory = Subcategory.query.filter_by(subcatid=product.subcatid).first().categoryname
            if subcategory in specs_data:
                product_specs = []
                num_specs = random.randint(2, 6)
                available_specs = specs_data[subcategory]
                specs_keys = list(available_specs.keys())
                # Shuffle the specs keys to randomize selection
                random.shuffle(specs_keys)
                for spec_name in specs_keys[:num_specs]:
                    spec_value = random.choice(available_specs[spec_name])
                    product_spec = Spec(pid=product.pid, name=spec_name, value=spec_value)
                    product_specs.append(product_spec)
                db.session.add_all(product_specs)
        for customer_id in customer_ids:
            num_products = random.randint(min_products_per_cart, max_products_per_cart)
            cart_product_ids = random.sample(product_ids, num_products)
            cart = Cart(cid=customer_id)

            for product_id in cart_product_ids:
                product = Product.query.filter_by(pid=product_id).first()
                print("Product ID:", product_id, "Product:", product)

                quantity = random.randint(1, 5)

                if product:
                    cart_item = Cart(cid=customer_id, pid=product_id, quantity=quantity)
                    db.session.add(cart_item)

            db.session.commit()
        for _ in range(num_orders):
            # Choose a random product ID
            product_id = random.choice(product_ids)

            # Choose a random customer ID
            customer_id = random.choice(customer_ids)

            # Retrieve the product information
            product = Product.query.filter_by(pid=product_id).first()
            if product:
                # Generate a random quantity for the order
                quantity = random.randint(1, 5)

                # Generate a random price for the order (assuming a fixed price for simplicity)
                price = random.randint(10, 100)

                # Generate a random delivery date (within 3 to 5 days)
                delivery_date = datetime.now() + timedelta(days=random.randint(3, 5))

                # Choose a random order status
                status = random.choice(order_statuses)

                # Create a new order
                order = Orders(pid=product_id, cid=customer_id, quantity=quantity, price=price,
                               status=status, deliveryaddress="Customer Address",
                               orderdate=datetime.now(), deliverydate=delivery_date)

                db.session.add(order)

        # Commit changes to the database
        db.session.commit()

        # Generate random sales data
        # Define the number of sales to generate
        num_sales = 50

        # Generate random sales data
        for _ in range(num_sales):
            # Choose a random product ID
            product_id = random.choice(product_ids)

            # Retrieve the product information
            product = Product.query.filter_by(pid=product_id).first()
            if product:
                merchant_id = product.mid
                subcategory_id = product.subcatid  # Retrieve subcategory ID from the product

                # Generate a random quantity for the sale
                quantity = random.randint(1, 5)

                # Generate a random price for the sale (assuming a fixed price for simplicity)
                price = random.randint(10, 100)

                # Generate a random delivery date (within the next month)
                delivery_date = datetime.now() + timedelta(days=3)

                # Create a new sale
                sale = Sale(mid=merchant_id, pid=product_id, subcatid=subcategory_id, quantity=quantity, price=price,
                            deliverydate=delivery_date)

                # Add the sale to the database
                db.session.add(sale)

        image_filenames = [f"image_{i}.jpg" for i in
                           range(1, 201)]  # Assuming you have 200 image files named image_1.jpg to image_200.jpg

        # Generate image URLs and fill the Image table
        for product_id in range(1, 171):
            # Choose a random number of images for each product (between 2 and 4)
            num_images = random.randint(2, 5)

            # Choose random image filenames for the product
            product_images = random.sample(image_filenames, num_images)

            # Generate image URLs for the product
            for img_filename in product_images:
                # Construct the image URL based on the image filename
                img_url = img_filename  # Adjust the path to your image directory

                # Create a new Image object and add it to the database
                image = Image(pid=product_id, imgurl=img_url)
                db.session.add(image)
        db.session.commit()
