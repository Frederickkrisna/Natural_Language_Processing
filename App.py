import os
import pickle
import nltk
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize, sent_tokenize

def write_file(review, review_category):
    file = open("reviews.txt", "a")
    file.write(review_category + "#" + " ".join(review) + "\n")
    file.close()
    file = open("reviews_only.txt", "a")
    file.write(" ".join(review) + "\n")
    file.close()

def check_sim(doc_index, cosine_sim, document):
    sim_score = list(enumerate(cosine_sim[doc_index]))
    sim_score = sorted(sim_score, key=lambda x: x[1], reverse=True)
    recommendation = sim_score[1:4]
    return recommendation

def view_recommendation():
    try:
        file = open("recommendation_data.pickle", "rb")
        tfidf, cosine_sim = pickle.load(file)
    except Exception as e:
        print("ERROR: " + e)
    file = open("positive.txt", "r").read()
    document = sent_tokenize(file)
    recommendation = check_sim(0, cosine_sim, document)
    counter = 0
    for rec,score in recommendation:
        counter += 1
        print(f'{counter}. {document[rec]}')
    a = input('').split(" ")[0]
    
def view_ner():
    os.system("cls")
    try:
        with open('ner_data.pickle', 'rb') as file:
            ner_data = pickle.load(file)
        print("Data loaded successfully.")
    except Exception as e:
        print(f"Error loading pickle file: {e}")
    
    print("\nExtracted Named Entities:")
    print("Smarphone_Brand: ", ner_data["smartphone_brand"])
    a = input('').split(" ")[0]

def add_review():
    select = 0
    review = ""
    review_category = ""
    while True:
        os.system("cls")
        print("1. ADD REVIEW")
        print("2. BACK")
        select = int(input(">> "))
        if select == 1:
            review = input("ENTER REVIEW: ")
            review = review.lower()
            review = word_tokenize(review)
            try:
                file = open("model.pickle", "rb")
                classifier = pickle.load(file)
                review_category = classifier.classify(FreqDist(review))
                print("REVIEW CATEGORY: " + review_category)
                file.close()
            except Exception as e:
                print("ERROR: " + e)
                a = input('').split(" ")[0]
                return
            write_file(review, review_category)
            print("REVIEW ADDED SUCCESSFULLY.")
            a = input('').split(" ")[0]
        elif select == 2:
            break
        else:
            print("INVALID INPUT. PLEASE TRY AGAIN.")
            a = input('').split(" ")[0]
            continue

def main_menu():
    select = 0
    while True:
        review = open("reviews.txt", "r").read()
        review = sent_tokenize(review)
        review_category = ""
        review_text = ""
        if len(review) > 0:
            review_text = review[-1].split("#")[1]
            review_category = review[-1].split("#")[0]
        else:
            review_text = "NO REVIEW"
            review_category = "UNKNOWN"
            
        os.system("cls")
        print("SMARTPHONE BRAND RECOMMENDATION APPLICATION BASED ON REVIEW")
        print(f"YOUR REVIEW: {review_text}")
        print(f"YOUR REVIEW CATEGORY (POSITIVE/NEGATIVE): {review_category}")
        print("1. ADD REVIEW")
        print("2. VIEW SMARTPHONE BRAND RECOMMENDATION")
        print("3. VIEW NAMED ENTITY RECOGNITION")
        print("4. EXIT")
        select = int(input(">> "))
        if select == 1:
            add_review()
        elif select == 2:
            print("VIEW SMARTPHONE BRAND RECOMMENDATION")
            view_recommendation()
        elif select == 3:
            print("VIEW NAMED ENTITY RECOGNITION")
            view_ner()
        elif select == 4:
            break
        else:
            print("INVALID INPUT. PLEASE TRY AGAIN.")
            continue

if __name__ == "__main__":
    main_menu()