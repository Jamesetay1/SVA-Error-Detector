<h1>Subject Verb Agreement Error Detection</h1>
This is a program designed to detect subject verb agreement errors.<br>
The program specifically targets errors commonly found in the English Placement Test for Non-Native English speakers (EPT)
<h3> Background </h3>
This program was the final group project for <b>LING 520: Computational Analysis of English at Iowa State University, Fall 2020</b>
The associated research paper for this program is available here: https://github.com/Jamesetay1/520/blob/master/SVA/docs/research_paper.pdf <br>

<br />
Program written by me (James Taylor, jamesetay1@gmail.com)<br>
Corpus Research and Derivation of Rules by:<br>
Ella Alhudithi (ella@iastate.edu) <br>
Thomas Elliott (thomase@iastate.edu) <br>
Sondoss Elnegahy (sondoss@iastate.edu) <br>

<h3>How it works</h3>
After reading in a file that contains the sentences in question, coreNLP Python library Stanza is used to
tokenize, tag, and dependency parse on a sentence by sentence basis.<br>
<br />
After this is done we iterate through each sentence object and
build a 'forward' dependency list. Each word object
already contains the id of it's governor, so this information
is simply reconstructed in a format that's easier to use.<br>
<br />
For Example, coreNLP parses "He walked through the door ." to the following dependencies:<br>
word.text = He, word.head = 2 (walked)<br>
word.text = walked, word.head = 0 (ROOT)<br>
word.text = through, word.head = 5 (door)<br>
word.text = the, word.head = 5 (door)<br>
word.text = door, word.head = 2 (walked)<br>
word.text = ., word.head = 2 (walked)<br>
<br />
Resulting in a forwards dependency list of word objects:<br>    
[ [] , [word.text = "he", word.text = "door", word.text =  "."], [], [], [word.text = "through", word.text = "the"] ]<br>
<em> Note that this list is populated with word objects, not just their text. 
Also note that the root never appears (because it can only be a governor, and is never a dependent) </em>  
<h3> Relationships and Rules </h3>
Once we have completed our forward dependency list, we go through the sentence again
and look for special relationships to test. We test against an agreement dictionary, which is determined
by the matrix below:  
![mtx](https://raw.githubusercontent.com/Jamesetay1/520/master/SVA/docs/agreement_matrix.png)
<br>  
<br />
The relationships we are currently looking for are:<br>    
<b>1: Main Verb --nsubj--> Noun:</b>     
<em>If the word is a verb AND it has a nsubj forward dependency AND it does <b>NOT</b> have any aux forward dependency</em><br>
<br />
<b>2: Aux <--aux-- Main Verb --nsubj--> Noun:</b>  
<em>If the word is a verb AND it has a nsubj forward dependency AND it <b>DOES</b> have any aux forward dependency</em><br> 
<br />
<b>3A: Noun <--nsubj-- Subject Predicate --cop--> Verb:</b>  
<em>If the word has a copular forward dependency AND an nsubj forward dependency</em><br>
<b>3B: 3A + Subject Predicate --aux--> Aux:</b>  
<em>If the word has a copular forward dependency AND an nsubj forward dependency AND an aux nsubj forward depdency</em><br> 
<br />  
<h3>Example</h3> 
Given the sentence: I am happy that he have been a friend since we met last September.<br>
<br />
<b>The program will recognize three subject-verb relationships in this sentence:</b><br>  
I am happy (Relationship 3A)<br>  
he have been a friend (Relationship 3B)<br>  
we met (Relationship 1)<br>  
<br />
When we check these against our error matrix we find:<br>  
Correct: I (PRP) <--nsubj-- am (VBP)<br>
Incorrect: he (PRP) <--nsubj-- have (VBP)<br>
Correct: we (PRP) <--nsubj-- met (VBD)<br>
<br />
<h3> Limitations </h3>

One more permanent limitation of this program surrounds the uncertainty of if there is a mismatch in number between
subject and verb or if it is truly a compound noun. coreNLP will mark instances like "The man park his car"
as: Man: NN, park: NN, as to say that the noun is 'man park'. Of course this is actually meant to be, 
"The man parks his car", but the agreement in number between subject and verb was incorrect. This case is
currently counted as incorrect IF the head noun of the compound is the root of the sentence.  

<h3> Future Additions </h3>

Future additions of SVA errors should be easy to add with the current framework
Additionally, it would be ideal to have a GUI for this program in addition to what is already there.
