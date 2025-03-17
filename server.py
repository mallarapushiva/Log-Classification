import os
import pandas as pd
from flask import Flask, request, send_file, jsonify
from classify import classify

app = Flask(__name__)

UPLOAD_FOLDER = "resources"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  

@app.route("/classify/", methods=["POST"])
def classify_logs():
    print("Ready")
    
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if not file.filename.endswith(".csv"):
        return jsonify({"error": "File must be a CSV"}), 400

    try:
        
        df = pd.read_csv(file)
        if "source" not in df.columns or "log_message" not in df.columns:
            return jsonify({"error": "CSV must contain 'source' and 'log_message' columns"}), 400

        
        df["target_label"] = classify(list(zip(df["source"], df["log_message"])))

        print("Dataframe:", df.to_dict())

        # Save the modified file
        output_file = os.path.join(UPLOAD_FOLDER, "output.csv")
        df.to_csv(output_file, index=False)
        print("File saved to output.csv")

        return send_file(output_file, mimetype="text/csv", as_attachment=True)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
