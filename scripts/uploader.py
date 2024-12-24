import firebase_admin
from firebase_admin import credentials, firestore
import json
import os
from datetime import datetime


def convert_firestore_data(data):
    """
    Converts Firestore data from JSON format back to Firestore format.

    Args:
        data: The Firestore data to convert. This can be a string, list, or dictionary.

    Returns:
        The converted data. Strings that are dates become datetime objects, lists and
        dictionaries are converted recursively, and other data types are returned as-is.
    """
    if isinstance(data, str):
        try:
            return datetime.fromisoformat(data)
        except ValueError:
            return data
    elif isinstance(data, list):
        return [convert_firestore_data(item) for item in data]
    elif isinstance(data, dict):
        return {key: convert_firestore_data(value) for key, value in data.items()}
    return data


def upload_collection(collection_name, db, input_file_path):
    """
    Uploads data from a JSON file to a Firestore collection.

    Args:
        collection_name (str): The name of the Firestore collection to upload to.
        db (google.cloud.firestore.Client): The Firestore database client.
        input_file_path (str): The file path where the data to be uploaded is stored.

    Returns:
        None
    """

    def recursive_upload(collection_ref, documents, depth=0):
        for doc in documents:
            doc_id = doc.pop("id", None)
            if not doc_id:
                continue
            doc_ref = collection_ref.document(doc_id)
            subcollections = {}
            doc_data = {}
            for key, value in doc.items():
                if isinstance(value, list) and all(
                    isinstance(item, dict) for item in value
                ):
                    subcollections[key] = value
                else:
                    doc_data[key] = value
            if doc_data:
                doc_ref.set(doc_data, merge=True)
            for subcol_name, subcol_docs in subcollections.items():
                recursive_upload(
                    doc_ref.collection(subcol_name), subcol_docs, depth + 1
                )

    with open(input_file_path, "r") as f:
        data = json.load(f)

    if collection_name not in data:
        collection_name = list(data.keys())[0]

    converted_data = convert_firestore_data(data.get(collection_name, []))
    if not converted_data:
        return

    collection_ref = db.collection(collection_name)
    recursive_upload(collection_ref, converted_data)


def list_json_files(directory):
    """
    Lists all JSON files in a directory.

    Args:
        directory (str): The directory to list JSON files from.

    Returns:
        A list of JSON file names.
    """
    files = [f for f in os.listdir(directory) if f.endswith(".json")]
    return files


if __name__ == "__main__":
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    json_dir = "backups"
    files = list_json_files(json_dir)

    if not files:
        print("No JSON files found in the backups directory.")
        exit(1)

    for i, file in enumerate(files):
        print(f"{i + 1}. {file}")

    try:
        choice = int(input("Select the file number to upload: ")) - 1
    except ValueError:
        print("Invalid input. Exiting.")
        exit(1)

    if 0 <= choice < len(files):
        selected_file = files[choice]
        collection_name = selected_file.replace(".json", "").split("_")[0]
        print(f"Uploading {selected_file} to Firestore collection {collection_name}...")
        upload_collection(collection_name, db, os.path.join(json_dir, selected_file))
        print(f"{collection_name} uploaded successfully from {selected_file}")
    else:
        print("Invalid selection. Exiting.")
        exit(1)
