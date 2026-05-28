from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, ENGLISH_STOP_WORDS
from sklearn.metrics.pairwise import cosine_similarity


customStopWords = list(ENGLISH_STOP_WORDS) + [
    "bonus", "candidate", "ideal", "looking", "required",
    "strong", "familiar", "familiarity", "plus", "like",
    "worked", "libraries", "processing", "experience",
    "skills", "looking", "engineer", "intern"
]



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


def extractKeywords(resumeText, jobDescription):

    corpus = [resumeText, jobDescription]

    vectorizer = TfidfVectorizer(stop_words=customStopWords, min_df=1)
    tfidfMatrix = vectorizer.fit_transform(corpus)

    vocab = vectorizer.get_feature_names_out()
    tfidfMatrix_array = tfidfMatrix.toarray()

    matched = []
    missing = []

    for i, word in enumerate(vocab):

        if (tfidfMatrix_array[1][i] > 0):

            if(tfidfMatrix_array[0][i] > 0):
                matched.append(word)

            else:
                missing.append(word)

    return matched, missing
