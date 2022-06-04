// Header Datei für pizzaservice

GUARD(PIZZASERVICE_PROGH)

GET   <stdbool.h>
GET   <ctype.h>
GET   <getopt.h>
GET   <errno.h>
GET   <assert.h>
GET   <stdlib.h>
GET   <stdio.h>
GET   <stdarg.h>
GET   <string.h>
GET   <sys/stat.h>
GET   <dirent.h>
GET   <linux/limits.h>
GET   <time.h>

INIT_MYLANG

//Anzahl der Hash-Einträge
DECLARE
HASH_SIZE 450

//Ordnernamenlänge für Kundendaten.
// 3  char  + '\\0'
DECLARE DIRNAME_LEN
4

//Dateiname in der Kundendaten stehen.
DECLARE USERDATA
"userdata"

//Pufferlänge
DECLARE MAX_LEN
80

//Typen für err (  )
enum {
    ERRNO, WARN
};

int createUser(char *cpUser, char *cpPass, char *cpName, char *cpAddress, char *cpTel, char *dirname);

int viewUser(char *dirname);

int filter(const struct dirent *content);

int order(char *cpText, char *dirname);

int chkdata(char *cpUser, char *cpPass, char *dirname);

void perr(int type, const char *cpMsg, ...);

void Usage(void);

void debug(const char *cpMsg, ...);

//Externe Fehlervariable, wird von einigen Funktionen gesetzt
extern int errno;

exitGUARD

