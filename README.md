# Documentation - FLCD Compiler

## Symbol table
The symbol table (unique for identifiers and constants) is implemented as a hashtable. The data structure initalizes a fixed size array and implements the search and add operations. The hash function used computes the sum of the ascii codes of each character in the key and takes the reminder of the division by the number of elements for the index. For the collision resolution simple linked lists are used.

## Parser
The parser splits the source code by every delimiter and constructs one symbol table for identifiers and constants.

## PIF Generation
The program internal form is represented as a linked list. The parses splits all tokens and looks for any lexical errors. If everything is fine the files ST.out and PIF.out are generated, otherwise an exception is thrown.

## Finite Automata
The FA class reads the data of the input file and generates a finite automata. The check function is used in order to verify if the given string is valid.

### FA.in file - EBNF
```
LETTER = "a" | "b" | ... | "z"
SYMBOL = "+" | "-" | "*" | "/" | "_" | "(" | ")" | "<" | ">" | "{" | "}"

FA = STATES"\n"ALPHABET"\n"INITIAL_STATE"\n"FINAL_STATE"\n"TRANSITIONS

STATES = "states = " LETTER " " {LETTER " "}
ALPHABET = "alphabet = " (LETTER | SYMBOL) " " {(LETTER | SYMBOL) " "}
FINAL_STATES = "final_states = " LETTER " " {LETTER " "}
TRANSITIONS = LETTER " " LETTER " " (LETTER | SYMBOL) "\n" {LETTER " " LETTER " " (LETTER | SYMBOL) "\n"}
```