import nltk
import re
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

# Download NLTK resources if not already downloaded
nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    # Remove special characters and digits
    text = re.sub(r'\[[0-9]*\]', '', text)
    text = re.sub(r'\s+', ' ', text)
    
    # Tokenize sentences
    sentences = sent_tokenize(text)
    
    # Remove stopwords
    stopwords_list = set(stopwords.words('english'))
    word_frequencies = {}
    
    for word in word_tokenize(text.lower()):
        if word not in stopwords_list:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
                
    maximum_frequency = max(word_frequencies.values())
    
    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequency)
        
    sentence_scores = {}
    
    for sent in sentences:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]

    return sentence_scores

def generate_summary(text, num_sentences=3):
    # Preprocess the text and get sentence scores
    sentence_scores = preprocess_text(text)
    
    # Convert sentences into a list
    sentences = sent_tokenize(text)
    
    # Select top sentences based on scores
    sorted_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
    top_sentences = [sentence[0] for sentence in sorted_sentences[:num_sentences]]
    
    # Join top sentences to create the summary
    summary = ' '.join(top_sentences)
    
    return summary
