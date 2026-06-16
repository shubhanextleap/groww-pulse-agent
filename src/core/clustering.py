from sentence_transformers import SentenceTransformer
import umap
import hdbscan

class ClusteringEngine:
    def __init__(self):
        print("ClusteringEngine: Loading SentenceTransformer model locally (BAAI/bge-small-en-v1.5)...")
        self.model = SentenceTransformer('BAAI/bge-small-en-v1.5')

    def cluster_reviews(self, normalized_reviews: list) -> dict:
        if not normalized_reviews:
            return {}

        print(f"ClusteringEngine: Encoding {len(normalized_reviews)} reviews into embeddings...")
        texts = [r['content'] for r in normalized_reviews]
        embeddings = self.model.encode(texts)

        # Skip clustering if we have very few reviews
        if len(texts) < 5:
            return {0: texts}

        print("ClusteringEngine: Running UMAP dimensionality reduction...")
        # Reduce dimensionality to help HDBSCAN
        n_neighbors = min(15, len(embeddings) - 1)
        umap_embeddings = umap.UMAP(
            n_neighbors=n_neighbors, 
            n_components=5, 
            metric='cosine'
        ).fit_transform(embeddings)

        print("ClusteringEngine: Running HDBSCAN clustering...")
        # HDBSCAN clusters the dense reduced embeddings
        min_cluster_size = min(5, len(embeddings))
        clusterer = hdbscan.HDBSCAN(
            min_cluster_size=min_cluster_size,
            metric='euclidean',
            cluster_selection_method='eom'
        )
        labels = clusterer.fit_predict(umap_embeddings)

        clusters = {}
        for i, label in enumerate(labels):
            # label -1 is noise, which we'll collect anyway
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(texts[i])

        print(f"ClusteringEngine: Found {len(set(labels))} clusters (including noise label -1).")
        return clusters
