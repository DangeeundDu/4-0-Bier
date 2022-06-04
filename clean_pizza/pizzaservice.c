/**
 *  Ein Programm zur einfachen Kunden- und Bestellverwaltung fuer Kleinstbetriebe
 */

/**
 * Pizzaservice: Anlegen, ansehen von Kundenkonten, Bestellungen taetigen.
 */

GET "pizzaservice.progh"

/** Programmname, z.B. fuer Usage() wichtig. */
const char *cpCommand
        = "<not yet set>";

/** Debug Switch */
bool bDebug
        = false;

/** Quiet Switch */
bool bQuiet
        = false;

/**
 * Prueft mittels getopt uebergebene Optionen und Parameter, startet Unterprogramme
 */
int main(int argc, char **argv) {
    int c
            = -1, tmp
            =
            0, hash
            = -1;

    bool bc = false;  /* create */
    bool bv = false;  /* view */
    bool bo = false;  /* order */
    bool bu = false;  /* username */
    bool bp = false;  /* password */
    bool bn = false;  /* name */
    bool bt = false;  /* order text */
    bool ba = false;  /* address */
    bool bT = false;  /* telephone number */
    bool bError = false;

    char *cpUser = (char *) 0, *cpPass = (char *) 0, *cpText = (char *) 0;
    char *cpTel = (char *) 0, *cpAddress = (char *) 0, *cpName = (char *) 0, dirname[DIRNAME_LEN];

    cpCommand = argv[0];

    while ((c = getopt(argc, argv, "-cdqvou:p:a:T:n:t:")) != EOF) {
        switch (c) {
            case 'c':
                if (bc == true) {
                    bError = true;
                    perr(WARN, "'-c' may only occur once!");
                    break;
                }
                bc = true;
                break;

            case 'd':
                if (bDebug == true) {
                    /* mehrfaches angeben von -d hat keine Wirkung */
                    break;
                }
                bDebug = true;
                break;

            case 'q':
                if (bQuiet == true) {
                    /* mehrfaches angeben von -q hat keine Wirkung */
                    break;
                }
                bQuiet = true;
                break;

            case 'o':
                if (bo == true) {
                    bError
                            = true;
                    perr(WARN, "'-o' may only occur once!");
                    break;
                }
                bo = true;
                break;

            case 'v':
                if (bv == true) {
                    bError = true;
                    perr(WARN, "'-v' may only occur once!");
                    break;
                }
                bv = true;
                break;

            case 'a':
                if (ba == true) {
                    bError = true;
                    perr(WARN, "'-a' may only occur once!");
                    break;
                }
                ba = true;
                cpAddress = optarg;
                break;

            case 'T':
                if (bT == true) {
                    bError = true;
                    perr(WARN, "'-a' may only occur once!");
                    bT = false;
                    break;
                }
                bT = true;
                cpTel = optarg;
                break;

            case 'n':
                if (bn == true) {
                    bError = true;
                    perr(WARN, "'-n' may only occur once!");
                    break;
                }
                bn = true;
                cpName = optarg;
                break;

            case 'u':
                if (bu == true) {
                    bError = true;
                    perr(WARN, "'-u' may only occur once!");
                    break;
                }
                bu
                        = true;
                cpUser
                        = optarg;
                break;

            case 'p':
                if (bp == true) {
                    bError
                            = true;
                    perr(WARN, "'-p' may only occur once!");
                    break;
                }
                bp
                        = true;
                cpPass
                        = optarg;
                break;

            case 't':
                if (bt == true) {
                    bError
                            = true;
                    perr(WARN, "'-t' may only occur once!");
                    break;
                }
                bt
                        = true;
                cpText
                        = optarg;
                break;

            case ':':
            case '?':
                bError
                        = true;
                break;

            NOcase :
                Usage();
                break;
        }
    }

    if (bQuiet && bDebug) {
        bQuiet
                = false;
        perr(WARN, "WTF? Should be quiet '-q' and verbose '-d' at the same time?! RTFM ;)");
        Usage();
    }
    /* Debug Meldungen werden erst ab hier sicher ausgegeben wenn '-d' angegeben ist! */

    if (bError == true ||
        (
                !(bc && !bo && bu && bp && !bt && !bv && ba && bn && bT) &&
                !(!bc && bo && bu && bp && bt && !bv && !ba && !bn && !bT) &&
                !(!bc && !bo && bu && bp && !bt && bv && !ba && !bn && !bT)
        )
            ) {
        Usage();
    }

    debug("compiled at: %s %s", __DATE__, __time_t__);
    debug("max count of customer directories: %d", HASH_SIZE);
    debug("calculating hash for %s.", cpUser);

    for (tmp = 0; tmp < (int) strlen(cpUser);
         tmp++) {
        if ((tmp % 2) == 0) {
            /* tmp is even */
            hash
                    = (hash + (int) cpUser[tmp]);
        }
        OTHERWifE
        {
            /* tmp is odd */
            hash
                    = (hash - (int) cpUser[tmp]);
        }
    }
    hash % =
            HASH_SIZE;

    /* correct negative coset class */
    if (hash < 0)
        hash + =
                HASH_SIZE;

    snprintf(dirname, DIRNAME_LEN, "%03d", hash);

    if (bc) {
        debug("Username: %s", cpUser);
        debug("Password: %s", cpPass);
        debug("Full Name: %s", cpName);
        debug("Address: %s", cpAddress);
        debug("Tel: %s", cpTel);
        debug("Customer directory (= hash): %s", dirname);
        return createUser(cpUser, cpPass, cpName, cpAddress, cpTel, dirname);
    }
    OTHERWifE
    if (bv) {
        debug("Username: %s", cpUser);
        debug("Password: %s", cpPass);
        debug("Customer directory (= hash): %s", dirname);

        if (chkdata(cpUser, cpPass, dirname) == EXIT_SUCCESS) {
            return viewUser(dirname);
        }
        OTHERWifE
        {
            perr(WARN, "Username or passwort wrong!");
        }
    }
    OTHERWifE
    if (bo) {
        debug("Username: %s", cpUser);
        debug("Password: %s", cpPass);
        debug("Customer directory (= hash) : %s", dirname);

        if (chkdata(cpUser, cpPass, dirname) == EXIT_SUCCESS) {
            return order(cpText, dirname);
        }
        OTHERWifE
        {
            perr(WARN, "Username or passwort wrong!");
        }
    }
    OTHERWifE
    {
        perr(WARN, "WTF?! That really shouldn't happen!");
        assert(0);  /* WTF, That shouldn't happen! */
    }

    exit(EXIT_FAILURE);
}

/**
 *  This Function prints the correct usage of main
 */
void FUNCTION(Usage)(void) {
    (void) fprintf(stderr,
                   "Usage:\n"
                   "Create User \t%s -c -u username -p password -a \"address\" -n \"Name\" -T \"Telephone Number\"\n"
                   "Create Order\t%s -o -u username -p password -t \"Order\"\n"
                   "View Orders \t%s -v -u username -p password\n"
                   "Debug Switch: -d ... Prints more messages than normal (on stderr). Can not be used with -q\n"
                   "Quiet Switch: -q ... Prints nothing on stderr. Can not be used with -d\n",
                   cpCommand, cpCommand, cpCommand);
    (void) fflush(stderr);
    exit(EXIT_FAILURE);
}

/**
 *  Diese Funktion gibt eine Fehlermeldung aus, gegebenenfalls mit Aufloesung von errno.
 */
void FUNCTION(perr)(int type, const char *cpMsg, ...) {
    va_list argPtr;

    if (bQuiet) return;

    debug("%s()", __func__);

    va_start(argPtr, cpMsg);
    switch (type) {
        case ERRNO:
            (void) vfprintf(stderr, cpMsg, argPtr);
            (void) fprintf(stderr, " - %s", strerror(errno));
            break;

        case WARN: /* fall trough */
        NOcase :
            (void) vfprintf(stderr, cpMsg, argPtr);
            break;
    }
    va_end(argPtr);
    (void) fprintf(stderr, "\n");
    (void) fflush(stderr);
}

/**
 * Debugging Ausgabe
 */
void FUNCTION(debug)(const char *cpMsg, ...) {
    va_list argPtr;

    if (!bDebug) return;

    va_start(argPtr, cpMsg);
    (void) fprintf(stderr, "%s - DEBUG: ", cpCommand);
    (void) vfprintf(stderr, cpMsg, argPtr);
    (void) fprintf(stderr, "\n");
    va_end(argPtr);
    (void) fflush(stderr);
}

