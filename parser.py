from adapt.entity_tagger import EntityTagger
from adapt.tools.text.tokenizer import EnglishTokenizer
from adapt.tools.text.trie import Trie
from adapt.intent import IntentBuilder
from adapt.parser import Parser
from adapt.engine import IntentDeterminationEngine

import json, sys

tokenizer = EnglishTokenizer()
trie = Trie()
tagger = EntityTagger(trie, tokenizer)
parser = Parser(tokenizer, tagger)

engine = IntentDeterminationEngine()

def get_keywords(filename):
    entities = []
    with open(filename, "r") as f:
        for line in f:
            entities.append(line.replace('\n', ''))
    return entities

#COnstatnts
#Greeting Entities
GREETING_KEYWORD = 'GreetingKeyword'
GOODBYE_KEYWORD = 'GoodbyeKeyword'
ACADEMY_KETWORD = 'AcademyKeyword'
DEPARTMENT_KEYWORD = 'DepartmentKeyword'
SEMESTER_KEYWORD = 'SemesterKeyword'
SUBJECT_KEYWORD = 'SubjectKeyword'

greeting_keywords = get_keywords('train_greetings.txt')

for gk in greeting_keywords:
    engine.register_entity(gk, GREETING_KEYWORD)

#goodbyw keywors
goodbye_keywords = get_keywords('goodbye.txt')

for gk in goodbye_keywords:
    engine.register_entity(gk, GOODBYE_KEYWORD)

#Academy keywords
academy_keywords = get_keywords('academy.txt')

for gk in academy_keywords:
    engine.register_entity(gk, ACADEMY_KETWORD)

#department keywords
department_keywords = get_keywords('departments.txt')

for gk in department_keywords:
    engine.register_entity(gk, DEPARTMENT_KEYWORD)



#semester_keywors

semester_keywords = get_keywords('semesters.txt')

for gk in semester_keywords:
    engine.register_entity(gk, SEMESTER_KEYWORD)


#subjects keywords
subject_keywords = get_keywords('subjects.txt')

for gk in subject_keywords:
    engine.register_entity(gk, SUBJECT_KEYWORD)


greeting_intent = IntentBuilder("GreetingIntent")\
                    .require(GREETING_KEYWORD)\
                    .build()

goodbye_intent = IntentBuilder("GoodbyeIntent")\
                    .require(GOODBYE_KEYWORD)\
                    .build()

academy_intent = IntentBuilder("AcademyIntent")\
                    .require(ACADEMY_KETWORD)\
                    .build()

department_intent = IntentBuilder("DepartmentIntent")\
                    .require(DEPARTMENT_KEYWORD)\
                    .build()

semester_intent = IntentBuilder("SemesterIntent")\
                    .require(SEMESTER_KEYWORD)\
                    .build()

subject_intent = IntentBuilder("SubjectIntent")\
                    .require(SUBJECT_KEYWORD)\
                    .build()

engine.register_intent_parser(greeting_intent)
engine.register_intent_parser(goodbye_intent)
engine.register_intent_parser(academy_intent)
engine.register_intent_parser(department_intent)
engine.register_intent_parser(semester_intent)
engine.register_intent_parser(subject_intent)

def parse_text(text):
    for intent in engine.determine_intent(text):
        if intent and intent.get('confidence') > 0:
            return json.dumps(intent, indent=4)

print parse_text("Hello")