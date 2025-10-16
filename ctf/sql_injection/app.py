from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)
DB = 'sqli.db'


def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS items(id INTEGER PRIMARY KEY, name TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS secrets(id INTEGER PRIMARY KEY, secret TEXT)")
    # flag only inserted if table empty
    cur.execute("SELECT COUNT(*) FROM secrets")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO secrets(secret) VALUES('FLAG{FLAG_92_injection}')")
    # insert some sample items if table empty (optional, useful for testing)
    cur.execute("SELECT COUNT(*) FROM items")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO items(name) VALUES('apple')")
        cur.execute("INSERT INTO items(name) VALUES('banana')")
        cur.execute("INSERT INTO items(name) VALUES('orange')")
    conn.commit()
    conn.close()


@app.route('/')
def index():
    return '''<h2>Recherche d'item</h2>
<form action="/search" method="GET">
  <input name="q" placeholder="search">
  <input type="submit" value="Search">
</form>
<p>But pédagogique : trouver le secret caché.</p>
'''


@app.route('/search')
def search():
    q = request.args.get('q', '')
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    # Intentional vuln: building query via string concat
    query = "SELECT name FROM items WHERE name LIKE '%" + q + "%'"
    try:
        cur.execute(query)
        rows = cur.fetchall()
        out = '<br>'.join([r[0] for r in rows]) if rows else 'Aucun résultat.'
    except Exception as e:
        out = 'Erreur: ' + str(e)
    conn.close()
    return render_template_string('<h3>Résultats</h3><div>{{ out|safe }}</div>', out=out)


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
