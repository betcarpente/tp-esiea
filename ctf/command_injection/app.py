from flask import Flask, request, render_template_string
import subprocess
import os

app = Flask(__name__)
FLAG_FILE = 'flag.txt'


@app.route('/')
def index():
    return '''<h2>Outil de diagnostic</h2>
<form action="/ping" method="GET">
  IP/host: <input name="host">
  <input type="submit" value="Ping">
</form>
<p>But pédagogique : l'interface lance une commande système avec l'entrée fournie.</p>
'''


@app.route('/ping')
def ping():
    host = request.args.get('host', '')
    # intentionally vulnerable: uses shell=True
    try:
        output = subprocess.check_output(
            f"ping -c 1 {host}",
            shell=True,
            universal_newlines=True,
            stderr=subprocess.STDOUT,
            timeout=5
        )
    except Exception as e:
        output = str(e)
    return render_template_string('<pre>{{ out }}</pre>', out=output)


@app.route('/flag')
def flag():
    try:
        with open(FLAG_FILE) as fh:
            return '<pre>Flag: ' + fh.read() + '</pre>'
    except Exception:
        return 'Flag non disponible.'


if __name__ == '__main__':
    # write flag if not present
    try:
        with open(FLAG_FILE, 'x') as fh:
            fh.write('FLAG{cmd_inject_2025}')
    except FileExistsError:
        pass

    # ensure we're listening on all interfaces
    app.run(host='0.0.0.0', port=5000)
