import PyPDF2
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def extract_important_paragraph(pdf_path):
    # Step 1: Extract text from the first 3 pages of the PDF
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for i, page in enumerate(reader.pages[:3]):
            text += page.extract_text() + "\n"
    
    # Step 2: Split text into paragraphs
    paragraphs = text.split('\n\n')
    paragraphs = [re.sub('\s+', ' ', p.strip()) for p in paragraphs if len(p.strip()) > 0]
    
    # Limit each paragraph to a maximum of 10 lines
    paragraphs = ['\n'.join(p.split('\n')[:10]) for p in paragraphs]
    
    if len(paragraphs) <= 1:
        return paragraphs[0] if paragraphs else "No meaningful content found."

    # Step 3: Create TF-IDF vectors and compute similarities
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(paragraphs)
    
    similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
    avg_similarity = np.mean(similarity_matrix, axis=1)

    # Step 4: Select the paragraph with the highest similarity to the rest
    most_important_index = np.argmax(avg_similarity)
    return paragraphs[most_important_index]

# Usage example
if __name__ == "__main__":
    pdf_path = "PATH_PDF"  # Substitute this with your PDF path
    important_paragraph = extract_important_paragraph(pdf_path)
    print("\nMost Important Paragraph:\n")
    print(important_paragraph)
