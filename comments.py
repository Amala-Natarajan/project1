from sentence_transformers import SentenceTransformer, util
import itertools

# Load comments from file
with open("d:/IIT Diploma/Tools in Data Science/Project 1/comments.txt", "r", encoding="utf-8") as f:
    comments = [line.strip() for line in f.readlines() if line.strip()]

# Load pre-trained sentence embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Compute embeddings for all comments
embeddings = model.encode(comments, convert_to_tensor=True)

# Find the most similar pair using cosine similarity
max_sim = -1
best_pair = None

for i, j in itertools.combinations(range(len(comments)), 2):
    sim = util.pytorch_cos_sim(embeddings[i], embeddings[j]).item()
    if sim > max_sim:
        max_sim = sim
        best_pair = (comments[i], comments[j])

# Write the most similar comments to output file
if best_pair:
    with open("d:/IIT Diploma/Tools in Data Science/Project 1/comments-similar.txt", "w", encoding="utf-8") as f:
        f.write(best_pair[0] + "\n" + best_pair[1])

print("Most similar comments saved to d:/IIT Diploma/Tools in Data Science/Project 1/comments-similar.txt")
