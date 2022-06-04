import requests
from bs4 import BeautifulSoup
import sys
import hashlib
import genanki
import pdb

def getPage(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def grabQuestionAndAnswer(soup):
    """
    Given the url of the question, parses html file and returns the html element with the question and answer
    as a list of string.

    >>> grabQuestionAndAnswer("https://www.exam4training.com/to-complete-the-sentence-select-the-appropriate-option-in-the-answer-area-107/")
    ['<p>HOTSPOT<br/> <br/>To complete the sentence, select the appropriate option in the answer area.</p>', '<p><img height="179" src="https://www.exam4training.com/wp-content/uploads/2022/02/image072-1.jpg" width="593"/></p>', '<p><button class="btn btn-common answer_view" data-target="#exam_question_1" data-toggle="collapse" type="button">View Answer</button></p>', '<p class="collapse exam_answer" id="exam_question_1" style="clear: both;"><strong>Answer: </strong><br/><img height="187" src="https://www.exam4training.com/wp-content/uploads/2022/02/image073-1.jpg" width="594"/></p>', '<p>Explanation:<br/> <br/>The Microsoft Privacy Statement explains what personal data Microsoft processes, how Microsoft processes the data, and the purpose of processing the data</p>']
    """
    div = soup.find('div', {'class': 'entry-content'})
    return [str(tag) for tag in div.findChildren('p', recursive=False)]

def separateQandA(QandA):
    frontOrBack = "front"
    front = ""
    back = ""
    for elem in QandA:
        if "View Answer" in elem:
            frontOrBack = "back"
        else:
            if frontOrBack == "front":
                front += elem
            else:
                back += elem
    return front, back

class Deck():
    def __init__(self, deck_name, tags = []):
        self.deck_name = deck_name
        self.deck = genanki.Deck(self.simple_hash(deck_name), deck_name)
        self.tags = tags
        self.model = genanki.Model(
            1607392319,
            'Simple Model',
            fields=[
                {'name': 'Question'},
                {'name': 'Answer'},
            ],
            templates=[
                {
                    'name': 'Card 1',
                    'qfmt': '{{Question}}',
                    'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
                }
            ],
        )

    def createAnkiNote(self, front, back):
        my_note = genanki.Note(
                model=self.model,
                fields=[front, back],
                tags = self.tags)
        self.deck.add_note(my_note)

    # from ankdown
    def simple_hash(self, front):
        """MD5 of text, mod 2^63. Probably not a great hash function."""
        h = hashlib.md5()
        h.update(front.encode("utf-8"))
        return int(h.hexdigest(), 16) % (1 << 63)

    def save_deck(self):
        genanki.Package(self.deck).write_to_file(self.deck_name+".apkg")
    
def checkIfThereIsANextQuestion(soup):
    result = soup.find("a",string="Next Question")
    return None if result is None else result['href']

def main():
    deck_name = sys.argv[1]
    link = sys.argv[2]

    my_deck = Deck(deck_name)
    
    while True:
        soup = getPage(link)  
        p = grabQuestionAndAnswer(soup)
        front, back = separateQandA(p)
        my_deck.createAnkiNote(front, back)

        link = checkIfThereIsANextQuestion(soup)
        if link is None:
            break

    my_deck.save_deck()

if __name__ == "__main__":
    main()

