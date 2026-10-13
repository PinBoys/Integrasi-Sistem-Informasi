
import os
import time
from flask import Flask, jsonify, request

app = Flask(__name__)

DATA_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data.txt"
)


def read_legacy_records():
    """Membaca data mahasiswa dari file teks."""
    records = []

    if not os.path.exists(DATA_FILE):
        return records

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        for line in f:
            clean_line = line.strip()

            if clean_line:
                fields = clean_line.split("|")

                if len(fields) == 4:
                    records.append({
                        "id": fields[0],
                        "nama": fields[1],
                        "jurusan": fields[2],
                        "status": fields[3]
                    })

    return records


def append_legacy_record(record):
    """Menambahkan data mahasiswa ke file teks."""
    line_entry = (
        f"{record['id']}|{record['nama']}|"
        f"{record['jurusan']}|{record['status']}\n"
    )

    with open(DATA_FILE, "a", encoding="utf-8") as f:
        f.write(line_entry)


@app.route("/api/v1/students", methods=["GET"])
def get_all_students():
    """Mengambil seluruh data mahasiswa dalam format JSON."""
    records = read_legacy_records()

    response_payload = {
        "metadata": {
            "service": "Legacy-Integrated API Gateway",
            "format": "JSON",
            "total_records": len(records),
            "timestamp": int(time.time())
        },
        "data": records
    }

    return jsonify(response_payload), 200


@app.route("/api/v1/students", methods=["POST"])
def create_student():
    """Menambahkan data mahasiswa baru."""
    payload = request.get_json()

    if not isinstance(payload, dict):
        return jsonify({
            "error": "Bad Request",
            "message": "Body payload JSON wajib disertakan"
        }), 400

    required_keys = ["id", "nama", "jurusan", "status"]

    missing_keys = [
        key for key in required_keys
        if key not in payload
        or not str(payload[key]).strip()
    ]

    if missing_keys:
        return jsonify({
            "error": "Unprocessable Entity",
            "message": (
                "Kunci data berikut tidak boleh kosong: "
                + ", ".join(missing_keys)
            )
        }), 422

    student_id = str(payload["id"]).strip()

    current_records = read_legacy_records()

    if any(record["id"] == student_id
           for record in current_records):
        return jsonify({
            "error": "Conflict",
            "message": (
                f"Data dengan ID {student_id} "
                "sudah ada di sistem legacy"
            )
        }), 409

    sanitized_record = {
        "id": student_id.replace("|", ""),
        "nama": str(payload["nama"]).strip().replace("|", ""),
        "jurusan": str(payload["jurusan"]).strip().replace("|", ""),
        "status": str(payload["status"]).strip().replace("|", "")
    }

    append_legacy_record(sanitized_record)

    return jsonify({
        "status": "success",
        "message": "Data berhasil disimpan ke sistem legacy",
        "created_item": sanitized_record
    }), 201


if __name__ == "__main__":
    print("API Gateway berjalan di http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
