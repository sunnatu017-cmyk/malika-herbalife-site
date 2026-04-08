from flask import Flask, render_template_string, request, redirect, session
from functools import wraps
import sqlite3

app = Flask(__name__)
app.secret_key = 'malika_super_secure_2026'
DB = 'malika_site.db'

ADMIN_USER = 'Malika@'
ADMIN_PASS = '4321'


def db(query, params=(), fetch=False):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall() if fetch else None
    conn.commit()
    conn.close()
    return rows


def init_db():
    db("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        description TEXT,
        usage_text TEXT,
        image TEXT,
        price TEXT DEFAULT ''
    )
    """)

    db("""
    CREATE TABLE IF NOT EXISTS videos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        video_url TEXT
    )
    """)

    db("""
    CREATE TABLE IF NOT EXISTS announcements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        text TEXT
    )
    """)

    db("""
    CREATE TABLE IF NOT EXISTS settings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        phone TEXT,
        telegram TEXT
    )
    """)

    settings = db("SELECT * FROM settings", fetch=True)
    if not settings:
        db(
            "INSERT INTO settings (phone, telegram) VALUES (?, ?)",
            ("+998990993259", "@Malikaa_19_03")
        )


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect("/login")
        return f(*args, **kwargs)
    return wrapper


HOME_HTML = """
<!DOCTYPE html>
<html lang="uz">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Herbalife Malika</title>

<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Arial;background:#fff;color:#111}

.navbar{
display:flex;
justify-content:space-between;
align-items:center;
padding:20px 40px;
background:white;
box-shadow:0 2px 10px rgba(0,0,0,.06);
position:sticky;
top:0;
z-index:1000;
}

.logo{
font-size:28px;
font-weight:bold;
color:#0a8f2f;
}

.hero{
height:100vh;
background:linear-gradient(rgba(0,0,0,.35),rgba(0,0,0,.35)),
url('https://images.unsplash.com/photo-1490645935967-10de6ba17061?q=80&w=1800')
center/cover;
display:flex;
justify-content:center;
align-items:center;
text-align:center;
color:white;
}

.hero h1{
font-size:72px;
}

.section-title{
font-size:48px;
padding:50px 50px 20px;
}

.product-slider{
display:flex;
flex-wrap:wrap;
gap:25px;
padding:20px 50px 40px;
overflow-x:auto;
overflow-y:auto;
scroll-behavior:smooth;
}

.card{
width:320px;
cursor:pointer;
transition:.6s;
}

.card img{
width:100%;
height:360px;
object-fit:cover;
border-radius:28px;
transition:.7s;
box-shadow:0 18px 45px rgba(0,0,0,.12);
}

.card:hover img{
transform:scale(1.08) translateX(10px) translateY(-10px);
}

.card h2{
text-align:center;
margin-top:15px;
font-size:28px;
}

.video-grid{
display:grid;
grid-template-columns:repeat(auto-fit,minmax(320px,1fr));
gap:30px;
padding:20px 50px 50px;
}

.modal{
display:none;
position:fixed;
top:0;
left:0;
width:100%;
height:100%;
background:rgba(0,0,0,.75);
z-index:9999;
justify-content:center;
align-items:center;
}

.modal-box{
background:white;
padding:30px;
border-radius:24px;
width:90%;
max-width:650px;
position:relative;
}

.modal-box img{
width:100%;
height:320px;
object-fit:cover;
border-radius:18px;
margin-bottom:20px;
}

.close-btn{
position:absolute;
right:20px;
top:10px;
font-size:36px;
cursor:pointer;
}

.footer{
background:#111;
color:white;
text-align:center;
padding:60px 20px;
margin-top:40px;
font-size:22px;
}

.footer a{
display:block;
margin-top:12px;
color:white;
text-decoration:none;
}

.footer a:hover{
color:#0a8f2f;
}
</style>
</head>
<body>

<div class="navbar">
<div class="logo">Herbalife</div>
<a href="/login">Admin</a>
</div>

<div class="hero">
<div>
<h1>Herbalife Malika</h1>
<p>Sog'lom hayot sari ishonchli qadam</p>
</div>
</div>

{% if announcements %}
<div style="padding:30px 50px">
{% for a in announcements %}
<div style="background:#fff3cd;padding:20px;border-radius:18px;margin-bottom:15px;">
<h2>{{a[1]}}</h2>
<p>{{a[2]}}</p>
</div>
{% endfor %}
</div>
{% endif %}

<h2 class="section-title">Premium Mahsulotlar</h2>

<div class="product-slider">
{% for p in products %}
<div class="card"
onclick="openModal('{{p[1]}}','{{p[2]}}','{{p[3]}}','{{p[4]}}','{{p[5]}}')">
<img src="{{p[4]}}">
<h2>{{p[1]}}</h2>
</div>
{% endfor %}
</div>

<h2 class="section-title">Videolar</h2>

<div class="video-grid">
{% for v in videos %}
<div>
<iframe width="100%" height="250" src="{{v[2]}}" allowfullscreen></iframe>
<h3 style="margin-top:10px">{{v[1]}}</h3>
</div>
{% endfor %}
</div>

<div id="productModal" class="modal">
<div class="modal-box">
<span class="close-btn" onclick="closeModal()">&times;</span>
<img id="modalImage" src="">
<h2 id="modalName"></h2>
<p id="modalDesc"></p>
<p id="modalUsage"></p>
<p id="modalPrice" style="font-size:24px;color:green;font-weight:bold"></p>
</div>
</div>

<div class="footer">
<h2>Herbalife Malika</h2>
<a href="tel:{{settings[1]}}">📞 {{settings[1]}}</a>
<a href="https://t.me/{{settings[2].replace('@','')}}" target="_blank">📩 {{settings[2]}}</a>
</div>

<script>
function openModal(name, desc, usage, image, price){
document.getElementById('productModal').style.display='flex';
document.getElementById('modalName').innerText=name;
document.getElementById('modalDesc').innerText=desc;
document.getElementById('modalUsage').innerText=usage;
document.getElementById('modalImage').src=image;
document.getElementById('modalPrice').innerText=price ? 'Narxi: ' + price : '';
}

function closeModal(){
document.getElementById('productModal').style.display='none';
}
</script>

</body>
</html>
"""


ADMIN_HTML = """
<!DOCTYPE html>
<html>
<body style="font-family:Arial">

<div style="width:250px;height:100vh;position:fixed;background:#111;color:white;padding:30px">
<h2>Admin Panel</h2>
<a href="/logout" style="color:white">Chiqish</a>
</div>

<div style="margin-left:270px;padding:40px">

<h2>Mahsulot qo'shish</h2>
<form method="post">
<input name="name" placeholder="Nomi"><br><br>
<input name="description" placeholder="Tavsif"><br><br>
<input name="usage_text" placeholder="Qo'llanish"><br><br>
<input name="image" placeholder="Rasm URL"><br><br>
<input name="price" placeholder="Narx"><br><br>
<button>Qo'shish</button>
</form>

<hr>

<h2>Video qo'shish</h2>
<form method="post" action="/add_video">
<input name="title" placeholder="Video nomi"><br><br>
<input name="video_url" placeholder="YouTube embed link"><br><br>
<button>Qo'shish</button>
</form>

<hr>

<h2>E'lon qo'shish</h2>
<form method="post" action="/add_announcement">
<input name="title" placeholder="Sarlavha"><br><br>
<textarea name="text"></textarea><br><br>
<button>Qo'shish</button>
</form>

<hr>

<h2>Telefon va Telegram</h2>
<form method="post" action="/update_settings">
<input name="phone" placeholder="Telefon raqam"><br><br>
<input name="telegram" placeholder="@telegram"><br><br>
<button>Saqlash</button>
</form>

<hr>

<h2>Mahsulotlar</h2>
{% for p in products %}
<p>{{p[1]}} | {{p[5]}} | <a href="/delete_product/{{p[0]}}">O'chirish</a></p>
{% endfor %}

<h2>Videolar</h2>
{% for v in videos %}
<p>{{v[1]}} | <a href="/delete_video/{{v[0]}}">O'chirish</a></p>
{% endfor %}

<h2>E'lonlar</h2>
{% for a in announcements %}
<p>{{a[1]}} | <a href="/delete_announcement/{{a[0]}}">O'chirish</a></p>
{% endfor %}

</div>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(
        HOME_HTML,
        products=db("SELECT * FROM products", fetch=True),
        videos=db("SELECT * FROM videos", fetch=True),
        announcements=db("SELECT * FROM announcements", fetch=True),
        settings=db("SELECT * FROM settings LIMIT 1", fetch=True)[0]
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == ADMIN_USER and request.form["password"] == ADMIN_PASS:
            session["admin_logged_in"] = True
            return redirect("/admin")

    return """
    <form method="post" style="max-width:400px;margin:100px auto">
    <input name="username" placeholder="Login"><br><br>
    <input type="password" name="password" placeholder="Parol"><br><br>
    <button>Kirish</button>
    </form>
    """


@app.route("/admin", methods=["GET", "POST"])
@admin_required
def admin():
    if request.method == "POST":
        db(
            "INSERT INTO products (name,description,usage_text,image,price) VALUES (?,?,?,?,?)",
            (
                request.form["name"],
                request.form["description"],
                request.form["usage_text"],
                request.form["image"],
                request.form["price"]
            )
        )
        return redirect("/admin")

    return render_template_string(
        ADMIN_HTML,
        products=db("SELECT * FROM products", fetch=True),
        videos=db("SELECT * FROM videos", fetch=True),
        announcements=db("SELECT * FROM announcements", fetch=True)
    )


@app.route("/add_video", methods=["POST"])
@admin_required
def add_video():
    db("INSERT INTO videos (title, video_url) VALUES (?,?)",
       (request.form["title"], request.form["video_url"]))
    return redirect("/admin")


@app.route("/add_announcement", methods=["POST"])
@admin_required
def add_announcement():
    db("INSERT INTO announcements (title, text) VALUES (?,?)",
       (request.form["title"], request.form["text"]))
    return redirect("/admin")


@app.route("/update_settings", methods=["POST"])
@admin_required
def update_settings():
    db(
        "UPDATE settings SET phone=?, telegram=? WHERE id=1",
        (request.form["phone"], request.form["telegram"])
    )
    return redirect("/admin")


@app.route("/delete_product/<int:id>")
@admin_required
def delete_product(id):
    db("DELETE FROM products WHERE id=?", (id,))
    return redirect("/admin")


@app.route("/delete_video/<int:id>")
@admin_required
def delete_video(id):
    db("DELETE FROM videos WHERE id=?", (id,))
    return redirect("/admin")


@app.route("/delete_announcement/<int:id>")
@admin_required
def delete_announcement(id):
    db("DELETE FROM announcements WHERE id=?", (id,))
    return redirect("/admin")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)