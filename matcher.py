from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



def calculateMatchScores(resumeText, jobDescription):
    if not resumeText or not jobDescription:
        return 0.0
    

    corpus = [resumeText, jobDescription]

    vectorizer = TfidfVectorizer()
    tfidfMatrix = vectorizer.fit_transform(corpus)

    #row 0 = resumes and row 1 = job description
    similarity = cosine_similarity(tfidfMatrix[0:1], tfidfMatrix[1:2])
    score = round(similarity[0][0] * 100, 2)

    return score