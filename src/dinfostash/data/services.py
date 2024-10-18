from google.cloud.firestore_v1 import DocumentReference, DocumentSnapshot

from .constants import users_collection


def read_all_resume(user_id: str) -> list[str]:
    docs: list[DocumentSnapshot] = (
        users_collection.document(user_id).collection("resume").get()
    )
    return [doc.id for doc in docs]


def read_resume(user_id: str, resume_name: str) -> dict:
    doc: DocumentSnapshot = (
        users_collection.document(user_id)
        .collection("resume")
        .document(resume_name)
        .get()
    )

    if not doc.exists:
        raise KeyError(f"Resume with name {resume_name} not found")

    data = doc.to_dict()
    if not data:
        raise ValueError(f"Resume with name {resume_name} has no data")
    return data


def save_resume(user_id: str, resume_name: str, resume_data: dict):
    doc_ref: DocumentReference = (
        users_collection.document(user_id).collection("resume").document(resume_name)
    )
    doc: DocumentSnapshot = doc_ref.get()

    if doc.exists:
        raise KeyError(f"Resume with name {resume_name} already exists")

    doc_ref.set(resume_data)

    return doc_ref.get().to_dict()


def remove_resume(user_id: str, resume_name: str) -> str:
    doc_ref: DocumentReference = (
        users_collection.document(user_id).collection("resume").document(resume_name)
    )
    doc: DocumentSnapshot = doc_ref.get()

    if not doc.exists:
        raise KeyError(f"Resume with name {resume_name} not found")

    return str(doc_ref.delete())


def update_resume(user_id: str, resume_name: str, resume_data: dict):
    doc_ref: DocumentReference = (
        users_collection.document(user_id).collection("resume").document(resume_name)
    )
    doc: DocumentSnapshot = doc_ref.get()

    if not doc.exists:
        raise KeyError(f"Resume with name {resume_name} not found")

    doc_ref.update(resume_data)
    return doc_ref.get().to_dict()
