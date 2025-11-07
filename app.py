from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import os


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)

    @app.get("/health")
    def health():
        return jsonify(status="ok")

    @app.get("/api/list")
    def list_files():
        base = os.path.join(os.getcwd(), "data")
        files = []
        if os.path.isdir(base):
            for name in os.listdir(base):
                if name.lower().endswith(".xlsx") and os.path.isfile(os.path.join(base, name)):
                    files.append(os.path.join("data", name))
        return jsonify(files=files)

    @app.get("/api/preview")
    def preview():
        path = request.args.get("file")
        rows = int(request.args.get("rows", 5))
        sheet = request.args.get("sheet", 0)
        if not path:
            data_dir = os.path.join(os.getcwd(), "data")
            if os.path.isdir(data_dir):
                for name in os.listdir(data_dir):
                    if name.lower().endswith(".xlsx") and os.path.isfile(os.path.join(data_dir, name)):
                        path = os.path.join(data_dir, name)
                        break
            if not path:
                for name in os.listdir("."):
                    if name.lower().endswith(".xlsx") and os.path.isfile(name):
                        path = name
                        break
        if not path:
            return jsonify(error="No file provided and no .xlsx found in cwd"), 400
        try:
            df = pd.read_excel(path, sheet_name=sheet)
        except Exception as e:
            return jsonify(error=str(e)), 400
        head = df.head(rows)
        return jsonify(
            file=os.path.abspath(path),
            shape=list(df.shape),
            columns=list(head.columns),
            rows=head.fillna("").astype(str).values.tolist(),
        )

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=True)
