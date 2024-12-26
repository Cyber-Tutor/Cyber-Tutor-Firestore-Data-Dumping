import firebase_admin
from firebase_admin import credentials, firestore
import json
from google.cloud.firestore_v1.base_document import DocumentSnapshot
from google.cloud.firestore_v1.types import Document
from datetime import datetime
import os


def convert_firestore_data(data):
    """
    Converts Firestore data into a format that can be easily saved as JSON.

    Args:
        data: The Firestore data to convert. This can be a datetime object,
              DocumentSnapshot, Document, list, or dictionary.

    Returns:
        The converted data. Datetime objects become strings, DocumentSnapshot and
        Document objects become dictionaries, lists and dictionaries are converted
        recursively, and other data types are returned as-is.
    """
    if isinstance(data, datetime):
        return data.isoformat()
    elif isinstance(data, DocumentSnapshot):
        return convert_firestore_data(data.to_dict())
    elif isinstance(data, Document):
        return convert_firestore_data(data.to_dict())
    elif isinstance(data, list):
        return [convert_firestore_data(item) for item in data]
    elif isinstance(data, dict):
        return {key: convert_firestore_data(value) for key, value in data.items()}
    return data


def download_collection(collection_name, db, output_file_path):
    """
    Downloads a Firestore collection and its subcollections recursively and saves it to a JSON file.
    Args:
        collection_name (str): The name of the Firestore collection to download.
        db (google.cloud.firestore.Client): The Firestore database client.
        output_file_path (str): The file path where the downloaded data will be saved.
    Returns:
        None
    """

    def recursive_download(collection_ref):
        data = []
        for doc in collection_ref.stream():
            doc_dict = doc.to_dict()
            doc_dict["id"] = doc.id
            subcollections = doc.reference.collections()
            for subcol in subcollections:
                doc_dict[subcol.id] = recursive_download(subcol)
            data.append(doc_dict)
        return data

    collection_ref = db.collection(collection_name)
    collection_data = recursive_download(collection_ref)

    converted_data = convert_firestore_data(collection_data)

    with open(output_file_path, "w") as f:
        json.dump({collection_name: converted_data}, f, indent=4)


def list_collections(db):
    """
    Lists all collections in the Firestore database.

    Args:
        db (google.cloud.firestore.Client): The Firestore database client.

    Returns:
        A list of collection names.
    """
    collections = db.collections()
    return [col.id for col in collections]


if __name__ == "__main__":
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    collections = list_collections(db)
    print("Available collections:")
    for i, collection in enumerate(collections):
        print(f"{i + 1}. {collection}")

    choice = int(input("Select the collection number to download: ")) - 1
    selected_collection = collections[choice]

    print(f"Downloading {selected_collection}...")

    base_output_file_path = os.path.join("backups", f"{selected_collection}_1.json")
    output_file_path = base_output_file_path
    counter = 1

    while os.path.exists(output_file_path):
        counter += 1
        output_file_path = os.path.join(
            "backups", f"{selected_collection}_{counter}.json"
        )

    download_collection(selected_collection, db, output_file_path)
    print(f"{selected_collection} downloaded successfully to {output_file_path}")
