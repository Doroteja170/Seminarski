import os
import random
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
db_folder = os.path.join(basedir, "db")
os.makedirs(db_folder, exist_ok=True)


db_path = os.path.join(db_folder, "followers.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"connect_args": {"check_same_thread": False}}

db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    followers = db.Column(db.Integer, nullable=False)


items = {
    "Instagram, Social media platform": 690_000_000,
    "Cristiano Ronaldo, Footballer": 660_000_000,
    "Lionel Messi, Footballer": 505_000_000,
    "Selena Gomez, Musician and actress": 419_000_000,
    "Kylie Jenner, Media personality": 393_000_000,
    "Dwayne Johnson, Actor and wrestler": 393_000_000,
    "Ariana Grande, Musician and actress": 375_000_000,
    "Kim Kardashian, Media personality": 356_000_000,
    "Beyoncé, Musician and actress": 311_000_000,
    "Khloé Kardashian, Media personality": 302_000_000,
    "Nike, Sportswear multinational": 300_000_000,
    "Justin Bieber, Musician": 294_000_000,
    "Kendall Jenner, Media personality": 287_000_000,
    "Taylor Swift, Musician": 281_000_000,
    "National Geographic, Magazine": 278_000_000,
    "Virat Kohli, Cricketer": 273_000_000,
    "Jennifer Lopez, Musician and actress": 248_000_000,
    "Neymar, Footballer": 230_000_000,
    "Nicki Minaj, Musician": 225_000_000,
    "Kourtney Kardashian, Media personality": 218_000_000,
    "Miley Cyrus, Musician and actress": 212_000_000,
    "Katy Perry, Musician": 204_000_000,
    "Zendaya, Actress and singer": 178_000_000,
    "Kevin Hart, Comedian and actor": 177_000_000,
    "Real Madrid CF, Football club": 176_000_000,
    "Cardi B, Musician and actress": 163_000_000,
    "LeBron James, Basketball player": 159_000_000,
    "Demi Lovato, Musician and actress": 153_000_000,
    "Rihanna, Musician": 149_000_000,
    "Chris Brown, Musician": 144_000_000,
    "Drake, Musician": 142_000_000,
    "FC Barcelona, Football club": 141_000_000,
    "Ellen DeGeneres, Comedian and television host": 136_000_000,
    "Billie Eilish, Musician": 124_000_000,
    "Kylian Mbappé, Footballer": 124_000_000,
    "UEFA Champions League, Club football competition": 121_000_000,
    "Gal Gadot, Actress": 108_000_000,
    "Lisa, Musician": 106_000_000,
    "Vin Diesel, Actor": 103_000_000,
    "NASA, Space agency": 96_400_000,
    "NBA, Professional basketball league": 90_700_000,
    "Snoop Dogg, Musician": 88_300_000,
    "David Beckham, Former footballer": 88_100_000,
    "Dua Lipa, Musician": 87_600_000,
    "Jennie, Musician": 87_300_000
}


with app.app_context():
    db.create_all()
    if Item.query.count() == 0:
        for name, followers in items.items():
            db.session.add(Item(name=name, followers=followers))
        db.session.commit()


@app.route("/pair", methods=["GET"])
def get_pair():
    all_items = Item.query.all()
    if len(all_items) < 2:
        return jsonify({"error": "Not enough items"}), 400
    choices = random.sample(all_items, 2)
    return jsonify({
        "A": {"name": choices[0].name, "followers": choices[0].followers},
        "B": {"name": choices[1].name, "followers": choices[1].followers}  
    })

@app.route("/guess", methods=["POST"])
def check_guess():
    data = request.get_json()
    choice = data.get("choice")
    A_name = data.get("A")
    B_name = data.get("B")

    if not A_name or not B_name:
        return jsonify({"correct": False, "error": "Missing pair"}), 400

    A = Item.query.filter_by(name=A_name).first()
    B = Item.query.filter_by(name=B_name).first()

    if not A or not B:
        return jsonify({"correct": False, "error": "Item not found"}), 400

    if B.followers > A.followers:
        correct = choice == "higher"
    elif B.followers < A.followers:
        correct = choice == "lower"
    else:
        correct = False

    return jsonify({"correct": correct})

@app.route('/health')
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
