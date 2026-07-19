from sentence_transformers import SentenceTransformer

'''
Load the embedding model once when the application starts.
This avoids downloading/loading the model repeatedly.
'''
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def create_embedding(text: str):
    """
    Convert text into a numerical vector embedding.

    Example:
    "Refactor the PDF generator"
    ->
    [0.023, -0.041, ...]
    """

    embedding = model.encode(text)

    return embedding