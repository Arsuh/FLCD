%{ 	 
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int currentLine = 1;
int errorFound = 0;

typedef struct {
    char token[256];
    int index;
} ST;

typedef struct {
    char token[256];
    int stCode;
}PIF;

ST st[100];
PIF pif[100];

int st_index = 0;
int pif_index = 0;

int addSt(char* symbol) {
    for(int i = 0; i < st_index; i++) {
        if(strcmp(st[i].token, symbol) == 0)
            return i;
    }

    strcpy(st[st_index].token, symbol);
    st[st_index].index = st_index;
    st_index ++;

    return st_index;
}

void addPif(char* symbol, int st) {
    strcpy(pif[pif_index].token, symbol);
    pif[pif_index].stCode = st;
    pif_index++;
}

void printSymbolTable() {
    printf("------------------ SYMBOL TABLE --------------------\n");
    for(int i = 0; i < st_index; i++) {
        printf("%s - %d\n", st[i].token, st[i].index);
    }
    printf("------------------ SYMBOL TABLE --------------------\n");
}

void printPif() {
    printf("------------------ PIF --------------------\n");
    for(int i = 0; i < pif_index; i++) {
        printf("%s - %d\n", pif[i].token, pif[i].stCode);
    }
    printf("------------------ PIF --------------------\n");
}

%} 


IDENTIFIER		[a-zA-Z][a-zA-Z0-9_]*
NUMBER_CONST	0|[+|-]?[1-9][0-9]*([.][0-9]*)?|[+|-]?0[.][0-9]*
STRING_CONST	'.*'

%%

"int"		{addPif(yytext, -1);}
"string"	{addPif(yytext, -1);}
"while"		{addPif(yytext, -1);}
"if"		{addPif(yytext, -1);}
"else"		{addPif(yytext, -1);}
"input"		{addPif(yytext, -1);}
"print"		{addPif(yytext, -1);}

"+"			{addPif(yytext, -1);}
"-"			{addPif(yytext, -1);}
"*"			{addPif(yytext, -1);}
"/"			{addPif(yytext, -1);}
"%"			{addPif(yytext, -1);}
"=="		{addPif(yytext, -1);}
"="			{addPif(yytext, -1);}
"!="		{addPif(yytext, -1);}
"<="		{addPif(yytext, -1);}
">="		{addPif(yytext, -1);}
"<"			{addPif(yytext, -1);}
">"			{addPif(yytext, -1);}
"&&"		{addPif(yytext, -1);}
"||"		{addPif(yytext, -1);}

"("			{addPif(yytext, -1);}
")"			{addPif(yytext, -1);}
"{"			{addPif(yytext, -1);}
"}"			{addPif(yytext, -1);}

{IDENTIFIER}		{int st = addSt(yytext); addPif(yytext, st);}
{NUMBER_CONST}		{int st = addSt(yytext); addPif(yytext, st);}
{STRING_CONST}		{int st = addSt(yytext); addPif(yytext, st);}

[ \t]+  	{;}
[\n]+ {currentLine++;}
. {errorFound = 1; printf("Error found at line %d\n", currentLine);}

%%

int yywrap(){}