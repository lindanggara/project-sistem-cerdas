from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer


class TopicModel:
    def __init__(self, n_topics: int = 5):
        self.n_topics = n_topics
        self.vectorizer = TfidfVectorizer(
            max_df=0.95, min_df=2, max_features=5000
        )
        self.nmf = NMF(n_components=n_topics, random_state=42, init="nndsvd")

    def fit_transform(self, texts):
        if len(texts) < self.n_topics:
            return {"distribution": {}, "keywords": {}}

        X = self.vectorizer.fit_transform(texts)
        W = self.nmf.fit_transform(X)
        H = self.nmf.components_

        feature_names = self.vectorizer.get_feature_names_out()
        keywords = {}
        for topic_idx, topic in enumerate(H):
            top_idx = topic.argsort()[-10:][::-1]
            keywords[f"topic_{topic_idx}"] = [feature_names[i] for i in top_idx]

        dominant = W.argmax(axis=1).tolist()
        distribution = {f"topic_{i}": dominant.count(i) for i in range(self.n_topics)}

        return {"distribution": distribution, "keywords": keywords}
