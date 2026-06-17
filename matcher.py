from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, ENGLISH_STOP_WORDS
from sklearn.metrics.pairwise import cosine_similarity
import spacy, re

nlp = spacy.load("en_core_web_sm")

customStopWords = list(ENGLISH_STOP_WORDS) + [
    "bonus", "candidate", "ideal", "looking", "required",
    "strong", "familiar", "familiarity", "plus", "like",
    "worked", "libraries", "processing", "experience",
    "skills", "looking", "engineer", "intern", "actions",
    "qualify", "daily", "utilize", "leverage", "ensure",
    "support", "assist", "help", "manage", "maintain", 
    "perform", "execute", "handle", "oversee", "contribute",
    "position", "responsibilities", "qualifications", "requirements",
    "duties", "tasks", "work", "job", "career", "company", "team",
    "member", "environment", "culture", "using", "alongside", "participate",
    "real", "world", "person", "multi", "additionally", "fundamental", "proven",
    "portfolio", "possess", "include", "write", "logs", "audit", "managing"
]

def lemmatization(text):

    #cleaning
    text = re.sub(r'([.!?,()\-])', r' \1 ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    doc = nlp(text)

    lemmas = [token.lemma_.lower() for token in doc if not token.is_punct and not token.is_space]

    return " ".join(lemmas)




def calculateMatchScores(resumeText, jobDescription):

    resumeText = lemmatization(resumeText)
    jobDescription = lemmatization(jobDescription)

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

    resumeText = lemmatization(resumeText)
    jobDescription = lemmatization(jobDescription)

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




