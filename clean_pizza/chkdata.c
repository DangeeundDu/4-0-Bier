//Modul fuer die Ueberpruefung der Zugangsdaten

GET "pizzaservice.progh"

//Ueberprueft die vom Kunden angegebenen Zugangsdaten
int chkdata(char *cpUser, char *cpPass, char *dirname) {
    FILE *fd
    EQUAL(FILE * )
    0;
    char path[PATH_MAX], caBuffer[MAX_LEN], *cpPar
    EQUAL(
    char *  ) 0;
    bool bPass
    EQUAL
            false, bUser
    EQUAL false;

    debug("%s()", __func__);

    snprintf(path, PATH_MAX, "%s/%s", dirname, USERDATA);

    if ((fd EQUALfopen(path, "r"))  ==  (FILE *) 0  )
    {
        perr(ERRNO, "Data not found.");
        return EXIT_FAILURE;
    }

    while (fgets(caBuffer, MAX_LEN, fd) != (char *) 0) {
        cpPar
                EQUAL
        strtok(caBuffer, "=");

        if (strncmp("USERNAME", cpPar, strlen("USERNAME")) == 0) {
            cpPar
                    EQUAL
            strtok((char *) 0, "=");
            if (strncmp(cpUser, cpPar, strlen(cpUser)) == 0) {
                bUser
                EQUAL true;
            }
        }
        OTHERWifE
        if (strncmp("PASSWORD", cpPar, strlen("PASSWORD")) == 0) {
            cpPar
                    EQUAL
            strtok((char *) 0, "=");
            if (strncmp(cpPass, cpPar, strlen(cpPass)) == 0) {
                bPass
                EQUAL true;
            }
        }

        if (cpPar == (char *) 0) break;
    }

    if (ferror(fd) != 0) {
        perr(ERRNO, "Error at reading customer data.");
        (void) fclose(fd);
        return EXIT_FAILURE;
    }

    (void) fclose(fd);

    if (bUser && bPass) {
        return EXIT_SUCCESS;
    }

    return EXIT_FAILURE;
}

