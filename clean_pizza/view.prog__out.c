//Modul zum Anzeigen der Kundendaten und Bestellungen

#include "pizzaservice.h"

//Zeigt Kundendaten und Bestellungen an.
int viewUser(char *dirname) {
    FILE *fd = (FILE *) 0;
    char path[PATH_MAX], caBuffer[MAX_LEN], *cpPar = (char *) 0;
    int n = 0;
    struct dirent **namelist = (struct dirent **) 0;
    debug("%s()", __func__);

    n = scandir(dirname, &namelist, filter, alphasort);

    if (n < 0) {
        perr(ERRNO, "Can not read user dir.");
        return EXIT_FAILURE;
    } else {
        snprintf(path, sizeof(path), "%s/%s", dirname, USERDATA);
        fd = fopen(path, "r");
        if (fd == (FILE *) 0) {
            perr(ERRNO, "can't open USERDATA.");
            free(namelist);
            return EXIT_FAILURE;
        }

        debug("Reading user data from %s", path);
        while (fgets(caBuffer, MAX_LEN, fd) != (char *) 0) {
            cpPar = strtok(caBuffer, " = ");
            debug("processing line %s", cpPar);

            if (strncmp("NAME", cpPar, strlen("NAME")) == 0) {
                cpPar = strtok((char *) 0, " = ");
                debug("Value = %s", cpPar);
                if (cpPar != (char *) 0) {
                    cpPar[strlen(cpPar) - 1] = '\0';
                    fprintf(stdout, "Data of %s:\n", cpPar);
                } else {
                    perr(WARN, "Name is empty!");
                }
            } else if (strncmp("ADDRESS", cpPar, strlen("ADDRESS")) == 0) {
                cpPar = strtok((char *) 0, " = ");
                debug("Value = %s", cpPar);

                if (cpPar != (char *) 0) {
                    fprintf(stdout, "\tdelivery address: %s", cpPar);
                } else {
                    perr(WARN, "address is empty!");
                }
            } else if (strncmp("TEL", cpPar, strlen("TEL")) == 0) {
                cpPar = strtok((char *) 0, " = ");
                debug("Value = %s", cpPar);

                if (cpPar != (char *) 0) {
                    fprintf(stdout, "\tTel: %s\n", cpPar);
                } else {
                    perr(WARN, "Tel is empty!");
                }
            }

            if (cpPar == (char *) 0) break;
        }

        if (ferror(fd) != 0) {
            perr(ERRNO, "Error at reading customer data.");
            (void) fclose(fd);
            free(namelist);
            return EXIT_FAILURE;
        }

        while (n--) {
            snprintf(path, strlen(namelist[n]->d_name) + strlen(dirname) + 2, "%s/%s", dirname, namelist[n]->d_name);
            fd = fopen(path, "r");
            if (fd == (FILE *) 0) {
                perr(ERRNO, "can not open order: %s", namelist[n]->d_name);
                free(namelist);
                return EXIT_FAILURE;
            }

            while (fgets(caBuffer, MAX_LEN, fd) != (char *) 0) {
                fprintf(stdout, "%s", caBuffer);
            }
            fprintf(stdout, "----------------------------------------\n");

            if (ferror(fd) != 0) {
                perr(ERRNO, "Error at reading order data: %s", namelist[n]->d_name);
                (void) fclose(fd);
                free(namelist);
                return EXIT_FAILURE;
            }

            free(namelist[n]);
        }
        free(namelist);
    }

    return EXIT_SUCCESS;
}

//Filterfunktion um nur Bestellungen innerhalb eines Ordners aufzufinden
//Stellt fuer einen Verzeichniseintrag an Hand des Dateinamens fest, ob es eine Bestellung
//ist und somit angezeigt werden soll, oder eine andere Datei.
//Filterkriterium: Dateiname besteht nur aus Ziffern  EQUAL  >  Rechnung.
int filter(const struct dirent *content) {
    int i = 0;

    debug("%s()", __func__);

    for (i = 0; i < (int) strlen(content->d_name); i++) {
        if (!isdigit(content->d_name[i])) {
            //  Eintrag besteht nicht nur aus Ziffern
            return 0;
        }
    }
    //  Eintrag besteht nur aus Ziffern
    return 1;
}

