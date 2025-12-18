from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_similarity(job_desc, resume_text):
    emb1 = model.encode(job_desc)
    emb2 = model.encode(resume_text)
    return util.cos_sim(emb1, emb2)[0][0].item()
