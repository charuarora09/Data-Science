# Author: Charu Arora - cxa150730
import sys
import nltk
from nltk.util import ngrams
from collections import Counter
from difflib import SequenceMatcher
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import wordnet 
from itertools import product

#function words
function_words= ['A', 'ABOUT', 'ABOVE', 'AFTER', 'AGAIN', 'AGO', 'ALL', 
                'ALMOST', 'ALONG', 'ALREADY', 'ALSO', 'ALTHOUGH', 'ALWAYS', 
                'AM','AMONG', 'AN', 'AND', 'ANOTHER', 'ANY', 'ANYBODY',
                'ANYTHING','ANYWHERE', 'ARE', 'AROUND', 'AS', 'AT', 'BACK',
                'ELSE','BE', 'BEEN', 'BEFORE', 'BEING', 'BELOW', 'BENEATH',
                'BESIDE','BETWEEN', 'BEYOND', 'BILLION', 'BILLIONTH', 'BOTH',
                'EACH', 'BUT','BY', 'CAN', 'COULD', 'DID', 'DO', 'DOES', 
                'DOING', 'DONE', 'DOWN', 'DURING', 'EIGHT', 'EIGHTEEN',
                'EIGHTEENTH', 'EIGHTH', 'EIGHTIETH', 'EIGHTY', 'EITHER', 'ELEVEN',
                'ELEVENTH','ENOUGH', 'EVEN', 'EVER', 'EVERY', 'EVERYBODY',
                'EVERYONE', 'EVERYTHING','EVERYWHERE', 'EXCEPT', 'FAR', 'FEW', 
                'FEWER', 'FIFTEEN', 'FIFTEENTH','FIFTH', 'FIFTIETH', 'FIFTY', 
                'FIRST', 'FIVE', 'FOR', 'FORTIETH', 'FORTY','FOUR', 'FOURTEEN', 
                'FOURTEENTH', 'FOURTH', 'HUNDRED', 'FROM', 'GET', 'GETS', 
                'GETTING', 'GOT', 'HAD', 'HAS', 'HAVE','HAVING', 'HE' , 'HENCE',
                'HER', 'HERE', 'HERS', 'HERSELF','HIM', 'HIMSELF', 'HIS', 
                'HITHER', 'HOW', 'HOWEVER', 'NEAR','HUNDREDTH', 'I',  'IF',
                'IN', 'INTO', 'IS','IT', 'ITS', 'ITSELF', 'JUST', 'LAST', 
                'LESS', 'MANY','ME', 'MAY', 'MIGHT', 'MILLION', 'MILLIONTH', 
                'MINE', 'MORE', 'MOST','MUCH', 'MUST',  'MY', 'MYSELF', 'NEAR', 
                'NEARBY', 'NEARLY','NEITHER', 'NEVER', 'NEXT', 'NINE', 'NINETEEN',
                'NINETEENTH', 'NINETIETH','NINETY', 'NINTH', 'NO', 'NOBODY', 
                'NONE', 'NOONE', 'NOTHING', 'NOR','NOT', 'NOW', 'NOWHERE', 'OF', 
                'OFF', 'OFTEN', 'ON', 'OR', 'ONCE', 'ONE','ONLY', 'OTHER', 
                'OTHERS', 'OUGHT',  'OUR', 'OURS', 'OURSELVES',
                'OUT', 'OVER', 'QUITE', 'RATHER', 'ROUND', 'SECOND', 'SEVEN', 
                'SEVENTEEN','SEVENTEENTH', 'SEVENTH', 'SEVENTIETH', 'SEVENTY',
                'SHALL','SHE', 'SHOULD', 'SINCE', 'SIX', 
                'SIXTEEN', 'SIXTEENTH', 'SIXTH', 'SIXTIETH', 'SIXTY', 'SO', 'SOME',
                'SOMEBODY', 'SOMEONE', 'SOMETHING', 'SOMETIMES', 'SOMEWHERE', 'SOON', 
                'STILL', 'SUCH', 'TEN', 'TENTH', 'THAN', 'THAT', 'THAT', 
                'THE', 'THEIR', 'THEIRS', 'THEM', 'THEMSELVES', 'THESE', 'THEN', 
                'THENCE', 'THERE', 'THEREFORE', 'THEY', 
                'THIRD', 'THIRTEEN', 'THIRTEENTH', 'THIRTIETH', 'THIRTY', 'THIS', 
                'THITHER', 'THOSE', 'THOUGH', 'THOUSAND', 'THOUSANDTH', 'THREE', 'THRICE',
                'THROUGH', 'THUS', 'TILL', 'TO', 'TOWARDS', 'TODAY', 'TOMORROW', 'TOO', 
                'TWELFTH', 'TWELVE', 'TWENTIETH', 'TWENTY', 'TWICE', 'TWO', 'UNDER',
                'UNDERNEATH', 'UNLESS', 'UNTIL', 'UP', 'US', 'VERY', 'WHEN', 'WAS', 
                'WE',  'WERE','WHAT', 'WHENCE', 'WHERE', 'WHEREAS', 'WHICH',
                'WHILE', 'WHITHER','WHO', 'WHOM', 'WHOSE', 'WHY', 'WILL', 'WITH',
                'WITHIN', 'WITHOUT','WOULD',  'YES', 'YESTERDAY', 'YET', 'YOU', 'YOUR',
                'YOURS', 'YOURSELF', 'YOURSELVES']
                
#Reading file 1
file1 = open("orig_taska.txt").read()
#Reading file 2
file2 = open("taska_6.txt").read()

#tokenizing both the documents
tokenizer = RegexpTokenizer('\w+')

ftokens1 = nltk.word_tokenize(file1.lower())
ftokens2 = nltk.word_tokenize(file2.lower())

#counting unigrams
file1_unigram = Counter(ngrams(ftokens1,1))
file2_unigram = Counter(ngrams(ftokens2,1))



print "Total number of words in original file: "+ str(len(ftokens1)) 
print "Total number of unique words in original file: "+ str(len(file1_unigram)) + "\n"
print "Total number of words in copied file: "+ str(len(ftokens2)) 
print "Total number of unique words in copied file: "+ str(len(file2_unigram)) + "\n"

ftokens1 = tokenizer.tokenize(file1.lower())
ftokens2 = tokenizer.tokenize(file2.lower())


stop = set(function_words)

#converting strings into a form that is present in WordNet
for i in range(1,len(ftokens1)):
		if wordnet.morphy(ftokens1[i]):
			ftokens1[i]=str(wordnet.morphy(ftokens1[i]))

for i in range(1,len(ftokens2)):
		if wordnet.morphy(ftokens2[i]):
			ftokens2[i]=str(wordnet.morphy(ftokens2[i]))
			
# removing functional words
ftokens1 = set(ftokens1) - stop
ftokens2 = set(ftokens2) - stop

#calculating bigrams, trigram, etc..
file1_bigram = list(ngrams(ftokens1,2))
file1_trigram = list(ngrams(ftokens1,3))
file1_4gram = list(ngrams(ftokens1,4))
file1_5gram = list(ngrams(ftokens1,5))

file2_bigram = list(ngrams(ftokens2,2))
file2_trigram = list(ngrams(ftokens2,3))
file2_4gram = list(ngrams(ftokens2,4))
file2_5gram = list(ngrams(ftokens2,5))

common_5gram =list(set(file1_5gram).intersection(file2_5gram))
common_5gram_percent = (len(common_5gram)/float(min(len(file1_5gram), len(file2_5gram))))*100

#checking for similarity
if (common_5gram_percent>70):
	print "True Copy prediction! \nPercentage  Similarity "+ str(common_5gram_percent)
else:
	common_4gram =list(set(file1_4gram).intersection(file2_4gram))
	common_4gram_percent = (len(common_4gram)/float(min(len(file1_4gram), len(file2_4gram))))*100
	if (common_4gram_percent>70):
		print "Close to a True Copy prediction! \nPercentage Similarity "+ str(common_4gram_percent)
	else:
		common_trigram =list(set(file1_trigram).intersection(file2_trigram))
		common_trigram_percent = (len(common_trigram)/float(min(len(file1_trigram), len(file2_trigram))))*100
		if (common_trigram_percent>70):
			print "Few words written together from the document have been copied exactly. Rearranging of words in sentence predicted! \nPercentage Similarity "+ str(common_trigram_percent)
		else:
			#if not that similar:
			#checking a sentence from one document with each
			#sentence in second document to find similar sentences within a document
			#and calculating similarity based on number of matched sentences
			seq = SequenceMatcher(None, file2, file1)
			r_seq=seq.ratio()*100
			print "Percentage Similar: "+ str(r_seq)

			#applying nlp pre-processing techniques
			
			#splitting into words
			sent1=filter(None, file1.split('.'))
			sent2=filter(None, file2.split('.'))
			
			total = 0
			percent =0
			for s2 in sent2:
				f2=s2
				#remove punctuations from sentence and form tokens
				tokens2 = tokenizer.tokenize(f2.lower())
				file2_len= len(tokens2)
				#lemmatize tokens of sentence
				for i in range(1,len(tokens2)):
					if wordnet.morphy(tokens2[i]):
						tokens2[i]=str(wordnet.morphy(tokens2[i]))
			
				#ignoring function words
				file2set = set(tokens2) - stop

				for s1 in sent1:

					f1=s1
					#remove punctuations from second sentence and form tokens
					tokens1 = tokenizer.tokenize(f1.lower())
					file1_len= len(tokens1)

					#lemmatize tokens of second sentence
					for i in range(1,len(tokens1)):
						if wordnet.morphy(tokens1[i]):
							tokens1[i]=str(wordnet.morphy(tokens1[i]))
					
					#removing functional words
					file1set = set(tokens1) - stop
					file1list = list(file1set)
					
					#comparing common words between a sentence from each document
					common =set(tokens1).intersection(set(tokens2))
					file2set= set(tokens2)-common
					file1set= set(tokens1)-common

					file1_new_len= len(file1set)
					file2_new_len= len(file2set)
					
					count= 0
					for word1 in file2set:
						for word2 in file1set:
							allsyns1 = set(wordnet.synsets(word1))
							allsyns2 = set(wordnet.synsets(word2))
							if allsyns1 and allsyns2:
								best = max((wordnet.wup_similarity(s1, s2) or 0, s1, s2) for s1, s2 in product(allsyns1, allsyns2))
								if(best[0]==1):
									count=count+1
									
					if file2_len:
						doc_sim=(file2_len-file2_new_len+count)/float(file2_len)*100
						if(doc_sim>60):
							percent=percent+doc_sim
							total=total+1
							print "Statement:\n" +str(f2) + "\nSimilar to Statement:\n"+str(f1) +"\nSimilarity Percent : " + str(doc_sim) + "\n"
							break;
			print "Total Number of Sentences in copied document: " + str(len(sent2))	
			print "Total Number of similar sentences: " + str(total)			
			print  "\n" + str(total/float(len(sent2))*100) + " Percent of the sentences from the copied document are similar with the original document."
			print  "Percentage Similarity: "+  str(percent/float(len(sent2))) 


