# Dolorem Ipsum:
## Steganography Through Random Fake Latin Generation

#### Inspired in part by _Perfectly Secure Steganography Using Minimum Entropy Coupling_: https://arxiv.org/abs/2210.14889

## Overview:

* Use mildly illegitimate behavior to mask serious infractions:  
  "I'm sorry, I've been using down time at work to do some web design on the side, and sending out sample layouts to my clients via email" "...oh by the way the lorem ipsum placeholder text in my layouts is really stego text with a hidden message -- or exfiltrated files!"
* Generate random Latin-ish text, different every time, using a valid known method and source corpus, but with a specified secret text embedded.  In this demo, the random output words are chosen such that **second** letter of each word is a vowel if the corresponding hidden bit is 0, and a consonant if it is 1.
  * In this demo the secret message is ascii and plaintext, but any binary could be encoded, including compressed or encrypted data.
  * The bandwidth of this implementation is quite low -- one bit of secret data per 64 bits or so of cover/output content -- but with a larger source corpus more refinements could be made

### Special features:

* The source data structure is precomputed, with the encoding trickery baked in, so that nothing sneaky need be done on the user's immediate machine.
* The encoding script is fairly straightforward, and makes no mention of stego or exfil, and works perfectly well as a legitimate lorem ipsum generator
* The input secret text is passed implicitly by placing a file with a given name and the desired contents in the same directory as the script.
  * The script opens a file of the same name, in append mode, and downloads the markov chain data structure file, placing it after the secret message in that file, and closes the write.
  * The script then *opens* the same file, extracts the message and the data structures into memory, then deletes the file.  On examination after the fact, no suspicious files will be present -- and if the script is run a second time, even looking at deleted files will only show a pure copy of the downloaded data structures.

## Technology

### Markov Chain Monte Carlo

In order to generate Latin-like text with verisimilitude, statistics are gathered from a valid Latin corpus, then used to generate arbitrary text with similar statistics.

* The largest single Latin corpus obtained was the Vulgate Bible, compiled in the year 382, with over 600,000 words.
https://www.biblestudyguide.org/ebooks/bibles/vul.pdf
  * All English introductions, copyright info, and chapter titles, as well as all numerals -- mostly this was chapter, verse, and page numbers -- and punctuation, were removed
  * Several proper nouns were removed which were ubiquitous and would have heavily flavored the output as Biblically sourced
  * The remaining proper nouns, as identified by initial capital letters, were simply modified by removing that initial letter.
  * Some shorter words, 1-2 letters, were removed, because their ubuiquity might have highlighted the encoding method more than was desirable.
  * Everything remaining was treated as a single long chain of words, ignoring breaks in line, verse, sentence, paragraph, page, chapter, and book.

#### Markov Chain

This series of words was digested into a data structure whereby for each consecutive set of three words, a Markov Chain (MC), the first two words were used as dictionary indexes, and the third was added to a set of words found at the indexed location.  This window was slid across the entire text, with each word taking all three roles successively, and wrapped at the end so the text was processed as a loop instead of a line.

To the above standard Markov Chain analysis was added the further modification that, at each indexed location in the data structure, **two** sets were retained, the first with words having a vowel at their second position, and the second with words having a consonant at the same place.
Also, a separate pair of sets was built, one with all the second-letter-vowel words ad one with all the second-letter-consonant words, and stored separately from the Markov Chain tree.

#### Monte Carlo

To generate text from a Markov Chain tree, the Markov Chain Monte Carlo (MCMC!) method is used:
* Select any two words found consecutively in the original corpus (trivially, use the first two words)  

* (*) Using those two words as indexes, look in the MC tree for the set of possible following words, and pick one at random.  Add that word to the output buffer

* Update the words in hand by selecting the second word and the new one to replace the former first and second.

* Repeat from (*) until the output buffer has the desired length

#### Modified Characteristic Markov Chain Monte Carlo

* In the presented algorithm (MCMCMC!!), after indexing into the data structure, two sets will be found instead of one.

* Using each consecutive bit of the hidden message in turn, select the first set on 0 and the second set on 1.

* Often, because of the corpus' innate statistics, it will not be the case that both 0 and 1 sets have candidate words. In this case, select a "next index" word from the nonempty set, but select a "next output" word from the provided separate word sets outside the MC tree.
  * This will affect the statistics of the output text, and could provide a weakness for steganalysis to exploit.
  * This weakness SHOULD be mitigated because of all the corpus processing that occurred before statistical collection, meaning the output text will diverge far from both the Vulgate Bible and Latin in general, in terms of text statistics.
  * It is possible this could be avoided by generating several permutations of the vulgate text, and ingesting all of them to build the MC tree, so that the "cache misses" are arbitrarily rare.

* Just for fun, further modifications were made to split the output into random-length sentences and comma-separated clauses.  This does not affect the stego properties of the text.

### Data-Hiding Script and Process
* Definitions/Assumptions:
  * The desired action is data exfiltration
  * The data to be stolen exists on computers at a location designated "work"
  * The actor has access to other computers at a location designated "home"
  * The Dolorem Ipsum tool is hosted on a server with full source code and usage instructions, designated "dark"
  * The second script (encoding, designated "loremipsum") and json-encoded MC data structure file are hosted on another server which appears to be a legitimate web-developer's tool, designated "dev"
* Procedure:
  1. The actor does their research on the "dark" site from home, and does not bring any code with them to work
  1. At work, the actor accesses the "dev" site, with whatever pretext behaviors like reading simplified instructions or comparing tools they deem appropriate.  Eventually, they download the "loremipsum.py" script to a local file store
  1. The actor then prepares a file, in the sample called "markov.txt", which contains their desired exfil content, in any format. (as currently written, the left-curly-brace character should be avoided)
  1. The actor executes the loremipsum.py script, which accesses the "words.json" db file from the "dev" site, and downloads it to the local file system, **APPENDING** it to the "markov.txt" file
  1. The script then reads that same file, splitting it on the first-seen left-curly-brace character.  Everything to the left is treated as the secret message, and everything to the right is MC database
  1. The MC database is then decoded and used in the MCMCMC algorithm, using consecutive bits of the secret message to select the word sets at each state, as described in the "technology" section above
  1. The script then _deletes_ the markov.txt file, ostensible to save hard drive space, deleting the source message text along with it.
  1. The actor can then use the generated _lorem ipsum_ text however they like.  One suggested method would be to create mock web site layouts, using the stego text as placeholders, then send those layouts to an external email, asking a purported client for input on the design.
  1. As an added precaution, the actor could run the script again, with an empty starting file, so hard drive analysis would show a clean copy of the db file
  1. Once home, the actor can obtain the third script from the "dark" site, and use it to extract the original message/files from the emailed placeholder text.
  1. Any later forensics investigation would uncover the "loremipsum.py" script and references to the "dev" site, which would look innocuous and function exactly as advertised.
  1. Profit!