import nltk
import re
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

# Ensure NLTK resources are downloaded
nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    # Clean text
    text = re.sub(r'\[[0-9]*\]', '', text)
    text = re.sub(r'\s+', ' ', text)
    
    sentences = sent_tokenize(text)
    stopwords_list = set(stopwords.words('english'))
    word_frequencies = {}
    
    for word in word_tokenize(text.lower()):
        if word not in stopwords_list and word.isalnum():
            word_frequencies[word] = word_frequencies.get(word, 0) + 1
                
    max_frequency = max(word_frequencies.values())
    word_frequencies = {word: freq / max_frequency for word, freq in word_frequencies.items()}
    
    sentence_scores = {}
    for sent in sentences:
        for word in word_tokenize(sent.lower()):
            if word in word_frequencies:
                if len(sent.split(' ')) < 30:
                    sentence_scores[sent] = sentence_scores.get(sent, 0) + word_frequencies[word]

    return sentence_scores, sentences

def enhance_summary(sentences, top_sentences):
    # Reorder top sentences for better flow
    sentence_indices = {sent: sentences.index(sent) for sent in top_sentences}
    ordered_sentences = sorted(top_sentences, key=lambda x: sentence_indices[x])
    
    # Add smooth transitions and context hints
    enhanced_summary = []
    for i, sentence in enumerate(ordered_sentences):
        if i > 0:
            enhanced_summary.append("Additionally, ")
        enhanced_summary.append(sentence.strip())
    
    return ' '.join(enhanced_summary)

def generate_summary(text, num_sentences=3):
    sentence_scores, sentences = preprocess_text(text)
    sorted_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
    top_sentences = [sentence[0] for sentence in sorted_sentences[:num_sentences]]
    
    # Enhance the naturalness of the summary
    summary = enhance_summary(sentences, top_sentences)
    return summary
