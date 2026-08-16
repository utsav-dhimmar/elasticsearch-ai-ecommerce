from sentence_transformers import SentenceTransformer
from torch import Tensor

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


# The sentences to encode


def main() -> None:
    sentences = [
        "The weather is lovely today.",
        "It's so sunny outside!",
        "He drove to the stadium.",
    ]
    embeddings: Tensor = model.encode(inputs=sentences, show_progress_bar=True)
    print(embeddings.shape)  # (3, 384)


if __name__ == "__main__":
    main()
