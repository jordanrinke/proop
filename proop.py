import markov, time, random
from blick import BlickLoader
from google import search
from random import randrange

b = BlickLoader(grammarType="default")
phonetics = []
phonetics.append(["th", " TH", " DH"])
phonetics.append(["sh", " SH"])
phonetics.append(["ee", " IY1"])
phonetics.append(["ai", " EY1"])
phonetics.append(["oo", " UW1", " UH1"])
phonetics.append(["ou", " AW1", " AW2", " UW2"])
phonetics.append(["oi", " OY2"])
phonetics.append(["oy", " OY1"])
phonetics.append(["oa", " OW1"])
phonetics.append(["ng", " NG"])
phonetics.append(["e", " IY2", " EH1", " EH2", " EY2", " ER1", " ER2", " ER0"])
phonetics.append(["i", " IH1", " IH2", " IH0", " AY1", " AY2"])
phonetics.append(["a", " AE1", " AE2", " AO2", " AH0"])
phonetics.append(["o", " AO1", " AA1", " AA2", " OW2", " OW0"])
phonetics.append(["u", " UW0", " UH2", " AH1", " AH2"])
phonetics.append(["p", " P"])
phonetics.append(["b", " B"])
phonetics.append(["f", " F"])
phonetics.append(["v", " V"])
phonetics.append(["m", " M"])
phonetics.append(["w", " W"])
phonetics.append(["t", " T"])
phonetics.append(["d", " D"])
phonetics.append(["s", " S"])
phonetics.append(["z", " Z", " ZH"])
phonetics.append(["n", " N"])
phonetics.append(["l", " L"])
phonetics.append(["r", " R"])
phonetics.append(["y", " Y", " IY0"])
phonetics.append(["k", " K"])
phonetics.append(["g", " G"])
phonetics.append(["j", " JH"])
phonetics.append(["h", " HH"])
phonetics.append(["c", " K", " S"])
phonetics.append(["x", " K S", " EH1 K S"])
phonetics.append(["q", " K"])

def phonetify(word):
    """Processes the generated word via the blick lib, it breaks each letter into
    the phonetic chunk that blick expects to be able to rate the word."""
    results = []
    results.append(word)
    for phon in phonetics:
        y = 0
        while y < len(results):
           if phon[0] in results[y]:
              if len(phon) > 2:
                  for x in range(2, len(phon)):
                     newresult = results[y].replace(phon[0], phon[x])
                     results.append(newresult)
              results[y]=results[y].replace(phon[0], phon[1])
           y += 1
    for x in range (0, len(results)):
        results[x] = results[x].strip()
    resultset = set(results)
    return resultset


# Load the dictionary into the markov chain
chain = markov.MarkovChain()
dictionary = "morewords"
for word in open(dictionary):
    word = word.strip()
    if word != "" and not word.endswith("'s"):
        chain.add(word.lower())

#Make a word, check if it is within set range, search google for it, save it. Up to 5000 words
words = 0
while words < 5000:
    word = "".join(chain.random_output())
    if len(word) > 4 and len(word) < 10:
        score = 100
        blickified = phonetify(word)
        for blicked in blickified:
            try:
                #sometimes this bails out, instead of tracking it down each time, this was an easy out
               thisscore = b.assessWord(blicked)
            except:
               score = 100
            if thisscore < score:
                score=thisscore
        if score > 0 and score < 18:
            try:
                first_url = search('"' + word + '"',num=10, stop=1)
                for x in range(1,10):
                    this_url = first_url.next()
                print str(score) + ',' + word + " - bad " + this_url
            except StopIteration:
		with open('proop.out', 'a') as outfile:
		    outfile.write(str(score) + ',' + word + '\n')
                print str(score) + ',' + word + " - good"
                words += 1
            time.sleep(randrange(10,120))
