//Modul zum Anlegen eines neuen Kunden

GET  "pizzaservice.progh"

//Legt einen neuen Kundenordner an und speichert die Daten
int createUser(char *cpUser, char *cpPass, char *cpName, char *cpAddress, char *cpTel, char *dirname) {
    FILE * fDat
    EQUAL(FILE * )
    0;
    char path[DIRNAME_LEN + sizeof(USERDATA)];

    debug("%s()", __func__);

    snprintf(path, sizeof(path), "%s/%s", dirname, USERDATA);

    if (mkdir(dirname, S_IRWXU) != 0) {
        perr(ERRNO, "possible problem with user dir: %s", dirname);
    }

    if ((fDat EQUAL
    fopen(path, "a+"))   ==   (FILE *) 0  )
    {
        perr(ERRNO, "can not find password file: %s", USERDATA);
        return EXIT_FAILURE;
    }

    fprintf(fDat, "USERNAME=%s\n"
                  "PASSWORD=%s\n"
                  "NAME=%s\n"
                  "ADDRESS=%s\n"
                  "TEL=%s\n", cpUser, cpPass, cpName, cpAddress, cpTel);

    fflush(fDat);
    if (fclose(fDat) != 0) {
        perr(ERRNO, "can't close password file: %s", USERDATA);
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}

