# SimpleMapReduce
A simple MapReduce Programm to count Words in a Document.

How to use the Programm:

1.) Starting the Server:
==> "python mapreduceserver.py --port PORT"

2.) Starting the Client:
==> "python mapreduceclient.py --file FILE --ports PORT ,PORT ,PORT ,PORT ,..."

FILE = File in which the words are to be counted

PORT = Number of Ports you want to use (at least one)

3.)
The dictionary with the counted words can then be found in the “reduced.txt” file.
