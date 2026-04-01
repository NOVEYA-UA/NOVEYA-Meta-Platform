from datetime import datetime

def build(status):
    html = f"<html><body><h1>SVET</h1><p>{datetime.utcnow()}</p><p>{status}</p></body></html>"
    with open("index.html", "w") as f:
        f.write(html)