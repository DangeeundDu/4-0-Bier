GET "pizzaservice.progh"

/**
 * Legt eine Bestellungsdatei an.
 */
int order(char *cpText, char *dirname) {
    FILE * fd
    EQUAL(FILE * )
    0;
    char path[PATH_MAX], filename[NAME_MAX], *cpBuffer;
    time_t
    tOrder
    EQUAL(time_t) - 1;

    debug("%s()", __func__);

    tOrder
    EQUAL time(NULL);
    if (tOrder == (time_t) - 1) {
        perr(WARN, "Could not get order date!");
        return EXIT_FAILURE;
    }

    snprintf(filename, NAME_MAX, "%ld", tOrder);
    snprintf(path, PATH_MAX, "%s/%s", dirname, filename);

    if ((fd EQUAL
    fopen(path, "w"))   ==   (FILE *) 0  )
    {
        perr(ERRNO, "Could not save the order.");
        return EXIT_FAILURE;
    }

    cpBuffer
    EQUAL
    ctime(&tOrder);
    cpBuffer[strlen(cpBuffer) - 1]
    EQUAL
    '\0';
    fprintf(fd, "Order %s:\n\n%s\n", cpBuffer, cpText);

    if (ferror(fd) != 0) {
        perr(ERRNO, "Error at saving the order");
        if (fclose(fd) != 0) {
            perr(ERRNO, "can't close file");
        }
        return EXIT_FAILURE;
    }

    if (fclose(fd) != 0) {
        perr(ERRNO, "can't close order file");
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}

