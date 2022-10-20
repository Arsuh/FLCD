# Documentation - FLCD Compiler

## Symbol table
The symbol table (unique for identifiers and constants) is implemented as a hashtable. The data structure initalizes a fixed size array and implements the search and add operations. The hash function used computes the sum of the ascii codes of each character in the key and takes the reminder of the division by the number of elements for the index. For the collision resolution simple linked lists are used.
