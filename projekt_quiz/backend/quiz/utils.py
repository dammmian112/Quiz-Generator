import nltk
import logging
import re
import random

logger = logging.getLogger(__name__)

# Pobieranie wymaganych danych NLTK
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    logger.info("Pobieranie danych NLTK punkt...")
    nltk.download('punkt', quiet=True)

def clean_text(text):
    """
    Czyści tekst z niepotrzebnych znaków i formatowania.
    """
    # Usuwamy nawiasy i ich zawartość
    text = re.sub(r'\([^)]*\)', '', text)
    # Usuwamy znaki specjalne, greckie litery i ich opisy
    text = re.sub(r'[α-ωΑ-Ω]|ῆ\s*ge|ά\s*grapho', '', text)
    # Usuwamy wielokrotne spacje
    text = re.sub(r'\s+', ' ', text)
    # Usuwamy spacje na początku i końcu
    text = text.strip()
    # Usuwamy "według" i podobne słowa z początku
    text = re.sub(r'^(według|definicja według|zgodnie z)\s+', '', text, flags=re.IGNORECASE)
    return text

def shorten_text(text, max_words=12):
    """
    Skraca tekst do określonej liczby słów.
    """
    words = text.split()
    if len(words) > max_words:
        return ' '.join(words[:max_words]) + '...'
    return text

def split_into_sentences(text):
    """
    Dzieli tekst na zdania.
    """
    # Czyścimy tekst
    text = clean_text(text)
    
    # Dzielimy na zdania
    sentences = re.split(r'[.!?]+', text)
    
    # Usuwamy puste zdania i białe znaki
    sentences = [s.strip() for s in sentences if s.strip()]
    
    return sentences

def generate_false_answers(correct_answer, topic):
    """
    Generuje fałszywe odpowiedzi na podstawie poprawnej odpowiedzi.
    """
    # Skracamy odpowiedź
    correct_answer = shorten_text(correct_answer)
    topic = topic.lower()
    
    false_answers = []
    
    # Generujemy przeciwne stwierdzenie
    if "jest" in correct_answer.lower():
        false_answers.append(correct_answer.replace("jest", "nie jest"))
    elif "są" in correct_answer.lower():
        false_answers.append(correct_answer.replace("są", "nie są"))
    elif "umożliwiają" in correct_answer.lower():
        false_answers.append(correct_answer.replace("umożliwiają", "nie umożliwiają"))
    else:
        false_answers.append(f"To niepoprawna definicja {topic}")
    
    # Generujemy kreatywne fałszywe odpowiedzi
    if "roślina" in correct_answer.lower() or "rośliny" in correct_answer.lower():
        false_answers.append(f"To zwierzęta, nie rośliny")
        false_answers.append(f"To grzyby, nie rośliny")
    elif "zwierzęta" in correct_answer.lower():
        false_answers.append(f"To rośliny, nie zwierzęta")
        false_answers.append(f"To grzyby, nie zwierzęta")
    elif "nauka" in correct_answer.lower():
        false_answers.append(f"To dziedzina sztuki, nie nauki")
    elif "badanie" in correct_answer.lower():
        false_answers.append(f"To tylko teoretyczne rozważania")
    elif "sztuka" in correct_answer.lower():
        false_answers.append(f"To technika, nie sztuka")
    else:
        false_answers.append(f"To inna dziedzina wiedzy")
    
    # Dodajemy trzecią odpowiedź
    false_answers.append(f"Żadne z powyższych")
    
    return false_answers[:3]

def create_question_from_sentence(sentence):
    """
    Tworzy pytanie ze zdania.
    """
    # Czyścimy zdanie
    sentence = clean_text(sentence)
    
    # Jeśli zdanie jest za krótkie lub zawiera niepożądane elementy, pomijamy je
    if len(sentence.split()) < 5 or any(word in sentence.lower() for word in ['np', 'np.', 'etc', 'itp', 'itp.', 'tj', 'tj.']):
        return None
    
    words = sentence.split()
    
    # Tworzymy pytanie na podstawie struktury zdania
    if 'jest' in words:
        idx = words.index('jest')
        if idx > 0 and idx < len(words) - 1:
            subject = ' '.join(words[:idx])
            subject = shorten_text(subject, 5)
            
            question = f"Co jest prawdą o {subject}?"
            correct_answer = shorten_text(sentence)
            false_answers = generate_false_answers(correct_answer, subject)
            
            all_answers = [correct_answer] + false_answers
            random.shuffle(all_answers)
            
            return {
                'question': question,
                'answers': all_answers,
                'correctAnswerIndex': all_answers.index(correct_answer)
            }
            
    elif 'to' in words:
        idx = words.index('to')
        if idx > 0 and idx < len(words) - 1:
            subject = ' '.join(words[:idx])
            subject = shorten_text(subject, 5)
            
            question = f"Co to jest {subject}?"
            correct_answer = shorten_text(sentence)
            false_answers = generate_false_answers(correct_answer, subject)
            
            all_answers = [correct_answer] + false_answers
            random.shuffle(all_answers)
            
            return {
                'question': question,
                'answers': all_answers,
                'correctAnswerIndex': all_answers.index(correct_answer)
            }
    
    # Dla pozostałych zdań tworzymy pytanie o prawdziwość
    question = "Które z tych stwierdzeń jest prawdziwe?"
    correct_answer = shorten_text(sentence)
    false_answers = generate_false_answers(correct_answer, words[0])
    
    all_answers = [correct_answer] + false_answers
    random.shuffle(all_answers)
    
    return {
        'question': question,
        'answers': all_answers,
        'correctAnswerIndex': all_answers.index(correct_answer)
    }

def generate_quiz(article_content):
    """
    Generator quizu tworzący pytania z odpowiedziami.
    """
    try:
        # Dzielimy tekst na zdania
        sentences = split_into_sentences(article_content)
        
        # Tworzymy pytania ze zdań
        questions = []
        for sentence in sentences:
            question_data = create_question_from_sentence(sentence)
            if question_data:
                questions.append(question_data)
        
        # Wybieramy najlepsze pytania (maksymalnie 5)
        num_questions = min(5, len(questions))
        selected_questions = random.sample(questions, num_questions)
        
        return selected_questions
        
    except Exception as e:
        logger.error(f"Błąd podczas generowania quizu: {str(e)}")
        raise
