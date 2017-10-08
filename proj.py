#
#Final Project
#FINAL VERSION
#Anton Njavro (njavro@bu.edu)
#
#And
#
#Alexander Vardanyan (avard@bu.edu)
#
import math

def clean_text(txt):
        """This function takes
           a string of text txt
           as a parameter and
           returns a list containing
           the words in txt after it
           has been 'cleaned'"""
        cleaned_txt = txt.replace('!', ' ').replace('.',' ').replace('?',' ').replace(',',' ').replace(':', ' ').replace('-', ' ').replace("'",'').replace('(','').replace(')','').lower()
        return cleaned_txt

def stem(s):
    """This function should returns the stem of s"""
    if s[-3:] == 'ing' and len(s) >= 5:
        rest = s[:-3]
        if rest[-1] == rest[-2]:
            return rest[:-1]
        else:
            return rest
    elif s[-3:] == 'ies' and len(s) >= 6:
        rest = s[:-3]
        return rest + 'y'
    elif s[-3:] == 'est' and len(s) >= 5:
        return s[:-3]
    elif s[-2:] == 'ed' and len(s) >= 4:
        return s[:-2]
    elif s[-1:] == 's':
        return s[:-1]
    elif s[-3:] == 'ied':
        rest = s[:-3]
        return rest + 'y'
    elif s[-3:] == 'ary':
        return s[:-3]
    elif s[-2:] == 'ly':
        return s [:-2]
    else:
        return s

def sample_file_read(filename):
    """A function that demonstrates how to read a
       Python dictionary from a file.
    """
    f = open(filename, 'r')    # Open for reading.
    d_str = f.read()           # Read in a string that represents a dict.
    f.close()

    d = dict(eval(d_str))      # Convert the string to a dictionary.

    print("Inside the newly-read dictionary, d, we have:")
    print(d)


def sample_file_write(filename):
    """A function that demonstrates how to write a
       Python dictionary to an easily-readable file.
    """
    d = {'test': 1, 'foo': 42}   # Create a sample dictionary.
    f = open(filename, 'w')      # Open file for writing.
    f.write(str(d))              # Writes the dictionary to the file.
    f.close()                    # Close the file.

def compare_dictionaries(d1, d2):
    """This fucntion should take two
       feature dictionaries d1 and d2 as
       inputs, and it should compute and
       return their log similarity score
    """
    score = 0
    total = sum(d1.values())
    for item in d2:
        if item in d1:
            score += math.log(d1[item]/total)*d2[item]
        else:
            score += math.log(0.5/total)*d2[item]
    return score


class TextModel:
    """This class models body of text and files"""

    def __init__(self, model_name):
        """Initializator for class TextModel"""
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.punctiations = {}

    def __repr__(self):
        """Return a string representation of the TextModel."""
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        s += '  number of different stems: ' + str(len(self.stems)) + '\n'
        s += '  number of different sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'
        s += '  number of different punctiations: ' + str(len(self.punctiations)) + '\n'
        return s

    def add_string(self, s):
        """This function adds
           a string of text s
           to the model by augmenting
           the feature dictionaries defined
           in the constructor
        """
        word_list = clean_text(s).split()

        for w in word_list:
            if w not in self.words:
                self.words.update({w:1})
            elif w in self.words:
                self.words[w] += 1
            if len(w) not in self.word_lengths:
                self.word_lengths.update({len(w): 1})
            elif len(w) in self.word_lengths:
                self.word_lengths[len(w)] += 1

        #Splits text into sentences and puts them into list
        sentences = s.replace('?', '.').replace('!', '.')
        sentences = sentences.split('.')[0:-1]
        #Update for sentence lengths in format {Length of sentence: number of those sentences}
        for g in sentences:
            if len(g.split()) not in self.sentence_lengths:
                self.sentence_lengths.update({len(g.split()): 1})
            elif len(g.split()) in self.sentence_lengths:
                self.sentence_lengths[len(g.split())] += 1
        #Updates stem dictionard returned in format {stem: occurances of stem}
        for w in word_list:
            if stem(w) not in self.stems:
                self.stems.update({stem(w): 1})
            elif stem(w) in self.stems:
                self.stems[stem(w)] += 1
        #Adds dict self.punctiations with number of occurances of punctiations in form {punctiation: number of occurances}
        for w in s:
                if w == '.' and '.' not in self.punctiations:
                    self.punctiations.update({'.': 1})
                elif w == '.' and '.' in self.punctiations:
                    self.punctiations['.'] += 1
                if w == ',' and ',' not in self.punctiations:
                    self.punctiations.update({',': 1})
                elif w == ',' and ',' in self.punctiations:
                    self.punctiations[','] += 1
                if w == '?' and '?' not in self.punctiations:
                    self.punctiations.update({'?': 1})
                elif w == '?' and '?' in self.punctiations:
                    self.punctiations['?'] += 1
                if w == '!' and '!' not in self.punctiations:
                    self.punctiations.update({'!': 1})
                elif w == '!' and '!' in self.punctiations:
                    self.punctiations['!'] += 1
                if w == ':' and ':' not in self.punctiations:
                    self.punctiations.update({':': 1})
                elif w == ':' and ':' in self.punctiations:
                    self.punctiations[':'] += 1

    def similarity_scores(self, other):
        """This method returns a list of log similarity
           scores measuring the similarity of 2 dict.
        """
        score_list = []
        word_score = round(compare_dictionaries(other.words, self.words), 3)
        word_lengths_score = round(compare_dictionaries(other.word_lengths, self.word_lengths),3)
        stems_score = round(compare_dictionaries(other.stems, self.stems),3)
        sentence_lengths_score = round(compare_dictionaries(other.sentence_lengths, self.sentence_lengths),3)
        punctiations_score = round(compare_dictionaries(other.punctiations, self.punctiations),3)

        score_list = [word_score, word_lengths_score, stems_score, sentence_lengths_score, punctiations_score]
        return score_list

    def classify(self, source1, source2):
        """This method compares the called TextModel
           object (self) to two other “source” TextModel
           objects
        """
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        print('scores for ', source1.name, ':', scores1)
        print('scores for ', source2.name, ':', scores2)
        weighted_sum1 = 10*scores1[0] + 7*scores1[3] + 5*scores1[4] + 3*scores1[1] + scores1[2]
        weighted_sum2 = 10*scores2[0] + 7*scores2[3] + 5*scores2[4] + 3*scores2[1] + scores2[2]

        if weighted_sum1 > weighted_sum2:
            print(self.name, ' is more likely to have come from ', source1.name,'\n')
        else:
            print(self.name, ' is more likely to have come from ', source2.name,'\n')




    def add_file(self, filename):
        """This function adds all
           of the text in the file
           identified by filename
           to the model. It should
           not explicitly return a value
        """

        f = open(filename, 'r', encoding='utf8', errors='ignore')
        s = ''
        for line in f:
            line = line[:-1]
            s += clean_text(line)
        self.add_string(s)




    def save_model(self):
        """This function saves
           the TextModel object
           self by writing its various
           feature dictionaries to files.
        """

        filename_words = self.name + '_' + 'words'
        filename_words_length = self.name + '_' + 'words_length'
        filename_stems = self.name + '_' + 'stems'
        filename_sentence_lengths = self.name + '_' + 'sentence_lengths'
        filename_punctiations = self.name + '_' + 'punctiations'

        f1 = open(filename_words, 'w')
        f1.write(str(self.words))
        f1.close()

        f2 = open(filename_words_length, 'w')
        f2.write(str(self.word_lengths))
        f2.close()

        f3 = open(filename_stems, 'w')
        f3.write(str(self.stems))
        f3.close()

        f4 = open(filename_sentence_lengths, 'w')
        f4.write(str(self.sentence_lengths))
        f4.close()

        f5 = open(filename_punctiations, 'w')
        f5.write(str(self.punctiations))
        f5.close()




    def read_model(self):
        """This function reads the
           stored dictionaries for the
           called TextModel object from
           their files and assigns them
           to the attributes of the called
           TextModel
        """
        filename_words = self.name + '_' + 'words'
        filename_words_length = self.name + '_' + 'words_length'
        filename_stems = self.name + '_' + 'stems'
        filename_sentence_lengths = self.name + '_' + 'sentence_lengths'
        filename_punctiations = self.name + '_' + 'punctiations'

        f1 = open(filename_words,'r')
        d1_str = f1.read()
        f1.close()
        self.words = dict(eval(d1_str))

        f2 = open(filename_words_length,'r')
        d2_str = f2.read()
        f2.close()
        self.word_lengths = dict(eval(d2_str))

        f3 = open(filename_stems, 'r')
        d3_str = f3.read()
        f3.close()
        self.stems = dict(eval(d3_str))

        f4 = open(filename_sentence_lengths, 'r')
        d4_str = f4.read()
        f4.close()
        self.sentence_lengths = dict(eval(d4_str))

        f5 = open(filename_punctiations, 'r')
        d5_str = f5.read()
        f5.close()
        self.punctiations = dict(eval(d5_str))




def test():
    """ your docstring goes here """
    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')

    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')

    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)





# Copy and paste the following function into finalproject.py
# at the bottom of the file, *outside* of the TextModel class.
def run_tests():
    """This function tests our models"""
    #main
    source1 = TextModel('Lord Of The Rings')
    source1.add_file('lord_of_the_rings_source_text.txt')

    source2 = TextModel('Harry Potter')
    source2.add_file('harry_potter_source_text.txt')

    new1 = TextModel('Hunger Games')
    new1.add_file('hunger_games_source_text.txt')
    new1.classify(source1, source2)

    new2 = TextModel('Lord Of The Rings Test')
    new2.add_file('lord_of_the_rings_test_source_text.txt')
    new2.classify(source1, source2)

    new3 = TextModel('Harry Potter Test')
    new3.add_file('harry_potter_test_source_text.txt')
    new3.classify(source1, source2)

    new4 = TextModel('Winds Of Winter')
    new4.add_file('winds_of_winter_source_text.txt')
    new4.classify(source1, source2)
