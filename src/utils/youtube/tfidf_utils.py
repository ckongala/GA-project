from flask_restful import current_app as app

from nltk import word_tokenize, pos_tag
from nltk import RegexpParser, Tree, tokenize, PorterStemmer

from math import log10


class tfidf_utils:

    def __init__(self):
        app.logger.info('Initiated tfidf_utils class')

    def pos_tag_narratives(self, text_sent_string):
        token = word_tokenize(text_sent_string)
        tags = pos_tag(token)
        grammar = r"""
        NP: {<DT|JJ|NN.*>+}
            {<IN>?<NN.*>}
        VP: {<TO>?<VB.*>+<IN>?<RB.*>?}
        CLAUSE: {<CD>?<NP><VP>+<NP>?<TO>?<NP>?<IN>?<NP>?<VP>?<NP>?<TO>?<NP>+}
        """
        a = RegexpParser(grammar)
        result = a.parse(tags)
        tfidf_string = ''
        for a in result:
            if type(a) is Tree:
                str1 = ''
                if a.label() == 'CLAUSE':
                    # This climbs into your NVN tree
                    for b in a:
                        if isinstance(b, tuple):
                            str1 += str(b[0]) + ' '
                        else:
                            for elem in b:
                                str1 += str(elem[0]) + ' '
                    str1 = str1.strip() + str('.') + str(' ')
                    tfidf_string += str1
        return tfidf_string

    def run_comprehensive(self, text, stop_words):
        # 1 Sentence Tokenize
        sentences = tokenize.sent_tokenize(text)
        total_documents = len(sentences)

        # 2 Create the Frequency matrix of the words in each sentence.
        freq_matrix = self._create_frequency_matrix(sentences, stop_words)

        # 3 Calculate TermFrequency and generate a matrix
        tf_matrix = self._create_tf_matrix(freq_matrix)

        # 4 creating table for documents per words
        count_doc_per_words = self._create_documents_per_words(freq_matrix)

        # 5 Calculate IDF and generate a matrix
        idf_matrix = self._create_idf_matrix(freq_matrix, count_doc_per_words, total_documents)

        # 6 Calculate TF-IDF and generate a matrix
        tf_idf_matrix = self._create_tf_idf_matrix(tf_matrix, idf_matrix)

        # 7 Important Algorithm: score the sentences
        sentence_scores = self._score_sentences(tf_idf_matrix)

        # 8 Find the threshold
        threshold = self._find_average_score(sentence_scores)

        # 9 Important Algorithm: Generate the narratives
        narratives = self._generate_narratives(sentences, sentence_scores, threshold)
        return narratives

    """ _create_frequency_matrix creates a matrix of sentences for a given blogpost """
    def _create_frequency_matrix(self, sentences, stop_words):
        frequency_matrix = {}
        ps = PorterStemmer()
        for sent in sentences:
            freq_table = {}
            words = word_tokenize(sent)
            for word in words:
                word = word.lower()
                word = ps.stem(word)
                if word in stop_words:
                    continue
                if word in freq_table:
                    freq_table[word] += 1
                else:
                    freq_table[word] = 1
            frequency_matrix[sent] = freq_table
        return frequency_matrix

    """ Using freq_matrix creates a TermFreq Matrix """

    def _create_tf_matrix(self, freq_matrix):
        tf_matrix = {}
        for sent, f_table in freq_matrix.items():
            tf_table = {}
            count_words_in_sentence = len(f_table)
            for word, count in f_table.items():
                tf_table[word] = count / count_words_in_sentence
            tf_matrix[sent] = tf_table
        return tf_matrix

    """ Using freq_matrix created words for document """

    def _create_documents_per_words(self, freq_matrix):
        word_per_doc_table = {}
        for sent, f_table in freq_matrix.items():
            for word, count in f_table.items():
                if word in word_per_doc_table:
                    word_per_doc_table[word] += 1
                else:
                    word_per_doc_table[word] = 1
        return word_per_doc_table

    """ this method creates Inverse Document Freq matrix """

    def _create_idf_matrix(self, freq_matrix, count_doc_per_words, total_documents):
        idf_matrix = {}
        for sent, f_table in freq_matrix.items():
            idf_table = {}
            for word in f_table.keys():
                # Considering DF only
                idf_table[word] = log10(float(count_doc_per_words[word]) / total_documents)
            idf_matrix[sent] = idf_table
        return idf_matrix

    def _create_tf_idf_matrix(self, tf_matrix, idf_matrix):
        tf_idf_matrix = {}
        for (sent1, f_table1), (sent2, f_table2) in zip(tf_matrix.items(), idf_matrix.items()):
            tf_idf_table = {}
            for (word1, value1), (word2, value2) in zip(f_table1.items(),
                                                        f_table2.items()):  # here, keys are the same in both the table
                tf_idf_table[word1] = float(value1 * value2)
            tf_idf_matrix[sent1] = tf_idf_table
        return tf_idf_matrix

    def _score_sentences(self, tf_idf_matrix):
        sentence_value = {}
        for sent, f_table in tf_idf_matrix.items():
            total_score_per_sentence = 0
            count_words_in_sentence = len(f_table)
            for word, score in f_table.items():
                total_score_per_sentence += score
            sentence_value[sent] = total_score_per_sentence / count_words_in_sentence
        return sentence_value

    def _find_average_score(self, sentence_value):
        """
        Find the average score from the sentence value dictionary
        :rtype: int
        """
        sumValues = 0
        for entry in sentence_value:
            sumValues += sentence_value[entry]

        try:
            average = (sumValues / len(sentence_value))
        except:
            average = 0
        return average

    def _generate_narratives(self, sentences, sentence_value, threshold):
        sentence_count = 0
        summary = ''
        dict_sent = {}
        for sentence in sentences:
            if sentence in sentence_value:
                dict_sent[sentence] = sentence_value[sentence]
        sentences_sorted_values = sorted(dict_sent, key=dict_sent.get, reverse=True)
        count = 0
        for r in sentences_sorted_values:
            # This is tuning parameter to display only top sentences.
            if count == 100:
                break
            count = count + 1
            summary += str(r) + " "
            sentence_count += 1
        return summary

