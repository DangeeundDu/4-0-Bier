/**
 *  Ein Programm zur einfachen Kunden- und Bestellverwaltung fuer Kleinstbetriebe
 */

/**
 * Pizzaservice: Anlegen, ansehen von Kundenkonten, Bestellungen taetigen.
 */

GET "pizzaservice.progh"

/** Programmname, z.B. fuer Usage() wichtig. */
 CONSTANT   STRING cpCommand  EQUAL  "<not yet set>" _EI

/** Debug Switch */
 LOGIC  bDebug  EQUAL  LIE _EI

/** Quiet Switch */
 LOGIC  bQuiet  EQUAL  LIE _EI

/**
 * Prueft mittels getopt uebergebene Optionen und Parameter, startet Unterprogramme
 */
NUMBER FUNCTION(main)  RB_   NUMBER  argc,  STRING POINTER argv  _RB
 CB_
	 NUMBER  c  EQUAL  -1, tmp  EQUAL  0, hash  EQUAL  -1 _EI

	 LOGIC  bc  EQUAL  LIE _EI  /* create */
	 LOGIC  bv  EQUAL  LIE _EI  /* view */
	 LOGIC  bo  EQUAL  LIE _EI  /* order */
	 LOGIC  bu  EQUAL  LIE _EI  /* username */
	 LOGIC  bp  EQUAL  LIE _EI  /* password */
	 LOGIC  bn  EQUAL  LIE _EI  /* name */
	 LOGIC  bt  EQUAL  LIE _EI  /* order text */
	 LOGIC  ba  EQUAL  LIE _EI  /* address */
	 LOGIC  bT  EQUAL  LIE _EI  /* telephone number */
	 LOGIC  bError  EQUAL  LIE _EI

	 STRING cpUser  EQUAL   RB_  STRING  _RB 0,  POINTER cpPass  EQUAL   RB_  STRING  _RB 0,  POINTER cpText  EQUAL   RB_  STRING  _RB 0 _EI
	 STRING cpTel  EQUAL   RB_  STRING  _RB 0,  POINTER cpAddress  EQUAL   RB_  STRING  _RB 0,  POINTER cpName  EQUAL   RB_  STRING  _RB 0, dirname SB_ DIRNAME_LEN _SB  _EI

	cpCommand  EQUAL  argv SB_  0  _SB  _EI

	 AS_LONG  RB_   RB_  c  EQUAL  getopt RB_  argc, argv, "-cdqvou:p:a:T:n:t:"  _RB   _RB   NOT_EQUAL  EOF  _RB
	 CB_
		 ALTERNATE  RB_  c  _RB
		 CB_
			 OPTION  'c':
				 IS  RB_  bc  EQUAL_TO  TRUTH  _RB
				 CB_
					bError  EQUAL  TRUTH _EI
					perr RB_ WARN, "'-c' may only occur once!" _RB  _EI
					 STOPHERE  _EI
				 _CB
				bc  EQUAL  TRUTH _EI
				 STOPHERE  _EI

			 OPTION  'd':
				 IS  RB_  bDebug  EQUAL_TO  TRUTH  _RB
				 CB_
					/* mehrfaches angeben von -d hat keine Wirkung */
					 STOPHERE  _EI
				 _CB
				bDebug  EQUAL  TRUTH _EI
				 STOPHERE  _EI

			 OPTION  'q':
				 IS  RB_  bQuiet  EQUAL_TO  TRUTH  _RB
				 CB_
					/* mehrfaches angeben von -q hat keine Wirkung */
					 STOPHERE  _EI
				 _CB
				bQuiet  EQUAL  TRUTH _EI
				 STOPHERE  _EI

			 OPTION  'o':
				 IS  RB_  bo  EQUAL_TO  TRUTH  _RB
				 CB_
					bError  EQUAL  TRUTH _EI
					perr RB_ WARN, "'-o' may only occur once!" _RB  _EI
					 STOPHERE  _EI
				 _CB
				bo  EQUAL  TRUTH _EI
				 STOPHERE  _EI

			 OPTION  'v':
				 IS  RB_  bv  EQUAL_TO  TRUTH  _RB
				 CB_
					bError  EQUAL  TRUTH _EI
					perr RB_ WARN, "'-v' may only occur once!" _RB  _EI
					 STOPHERE  _EI
				 _CB
				bv  EQUAL  TRUTH _EI
				 STOPHERE  _EI

			 OPTION  'a':
				 IS  RB_  ba  EQUAL_TO  TRUTH  _RB
				 CB_
					bError  EQUAL  TRUTH _EI
					perr RB_ WARN, "'-a' may only occur once!" _RB  _EI
					 STOPHERE  _EI
				 _CB
				ba  EQUAL  TRUTH _EI
				cpAddress  EQUAL  optarg _EI
				 STOPHERE  _EI

			 OPTION  'T':
				 IS  RB_  bT  EQUAL_TO  TRUTH  _RB
				 CB_
					bError  EQUAL  TRUTH _EI
					perr RB_ WARN, "'-a' may only occur once!" _RB  _EI
					bT  EQUAL  LIE _EI
					 STOPHERE  _EI
				 _CB
				bT  EQUAL  TRUTH _EI
				cpTel  EQUAL  optarg _EI
				 STOPHERE  _EI

			 OPTION  'n':
				 IS  RB_  bn  EQUAL_TO  TRUTH  _RB
				 CB_
					bError  EQUAL  TRUTH _EI
					perr RB_ WARN, "'-n' may only occur once!" _RB  _EI
					 STOPHERE  _EI
				 _CB
				bn  EQUAL  TRUTH _EI
				cpName  EQUAL  optarg _EI
				 STOPHERE  _EI

			 OPTION  'u':
				 IS  RB_  bu  EQUAL_TO  TRUTH  _RB
				 CB_
					bError  EQUAL  TRUTH _EI
					perr RB_ WARN, "'-u' may only occur once!" _RB  _EI
					 STOPHERE  _EI
				 _CB
				bu  EQUAL  TRUTH _EI
				cpUser  EQUAL  optarg _EI
				 STOPHERE  _EI

			 OPTION  'p':
				 IS  RB_  bp  EQUAL_TO  TRUTH  _RB
				 CB_
					bError  EQUAL  TRUTH _EI
					perr RB_ WARN, "'-p' may only occur once!" _RB  _EI
					 STOPHERE  _EI
				 _CB
				bp  EQUAL  TRUTH _EI
				cpPass  EQUAL  optarg _EI
				 STOPHERE  _EI

			 OPTION  't':
				 IS  RB_  bt  EQUAL_TO  TRUTH  _RB
				 CB_
					bError  EQUAL  TRUTH _EI
					perr RB_ WARN, "'-t' may only occur once!" _RB  _EI
					 STOPHERE  _EI
				 _CB
				bt  EQUAL  TRUTH _EI
				cpText  EQUAL  optarg _EI
				 STOPHERE  _EI

			 OPTION  ':':
			 OPTION  '?':
				bError  EQUAL  TRUTH _EI
				 STOPHERE  _EI

			 NOOPTION :
				Usage RB_  _RB  _EI
				 STOPHERE  _EI
		 _CB
	 _CB

	 IS  RB_  bQuiet && bDebug  _RB
	 CB_
		bQuiet  EQUAL  LIE _EI
		perr RB_ WARN, "WTF? Should be quiet '-q' and verbose '-d' at the same time?! RTFM ;)" _RB  _EI
		Usage RB_  _RB  _EI
	 _CB
	/* Debug Meldungen werden erst ab hier sicher ausgegeben wenn '-d' angegeben ist! */

	 IS  RB_  bError  EQUAL_TO  TRUTH ||
			 RB_
				! RB_ bc && !bo && bu && bp && !bt && !bv && ba && bn && bT _RB  &&
				! RB_ !bc && bo && bu && bp && bt && !bv && !ba && !bn && !bT _RB  &&
				! RB_ !bc && !bo && bu && bp && !bt && bv && !ba && !bn && !bT _RB
			 _RB
	   _RB
	 CB_
		Usage RB_  _RB  _EI
	 _CB

	debug RB_ "compiled at: %s %s", __DATE__, __TIME__ _RB  _EI
	debug RB_ "max count of customer directories: %d", HASH_SIZE _RB  _EI
	debug RB_ "calculating hash for %s.", cpUser _RB  _EI

	FLOOP RB_ tmp  EQUAL  0 _EI  tmp  SMALLER   RB_  NUMBER  _RB strlen RB_ cpUser _RB  _EI  tmp++ _RB
	 CB_
		 IS  RB_  RB_ tmp % 2 _RB   EQUAL_TO  0 _RB
		 CB_
			/* tmp is even */
			hash  EQUAL   RB_ hash +  RB_  NUMBER  _RB cpUser SB_  tmp  _SB  _RB  _EI
		 _CB
		 OTHERWISE
		 CB_
			/* tmp is odd */
			hash  EQUAL   RB_ hash -  RB_  NUMBER  _RB cpUser SB_  tmp  _SB  _RB  _EI
		 _CB
	 _CB
	hash %EQUAL HASH_SIZE _EI

	/* correct negative coset class */
	 IS  RB_ hash  SMALLER  0 _RB  hash +EQUAL  HASH_SIZE _EI

	 snprintf RB_ dirname, DIRNAME_LEN, "%03d", hash _RB  _EI

	 IS  RB_ bc _RB
	 CB_
		debug RB_ "Username: %s", cpUser _RB  _EI
		debug RB_ "Password: %s", cpPass _RB  _EI
		debug RB_ "Full Name: %s", cpName _RB  _EI
		debug RB_ "Address: %s", cpAddress _RB  _EI
		debug RB_ "Tel: %s", cpTel _RB  _EI
		debug RB_ "Customer directory (= hash): %s", dirname _RB  _EI
		 GIVEBACK  createUser RB_ cpUser, cpPass, cpName, cpAddress, cpTel, dirname _RB  _EI
	 _CB
	 OTHERWISE   IS  RB_ bv _RB
	 CB_
		debug RB_ "Username: %s", cpUser _RB  _EI
		debug RB_ "Password: %s", cpPass _RB  _EI
		debug RB_ "Customer directory (= hash): %s", dirname _RB  _EI

		 IS  RB_  chkdata RB_ cpUser, cpPass, dirname _RB   EQUAL_TO  EXIT_SUCCESS  _RB
		 CB_
			 GIVEBACK  viewUser RB_ dirname _RB  _EI
		 _CB
		 OTHERWISE
		 CB_
			perr RB_ WARN, "Username or passwort wrong!" _RB  _EI
		 _CB
	 _CB
	 OTHERWISE   IS  RB_ bo _RB
	 CB_
		debug RB_ "Username: %s", cpUser _RB  _EI
		debug RB_ "Password: %s", cpPass _RB  _EI
		debug RB_ "Customer directory (= hash) : %s", dirname _RB  _EI

		 IS  RB_  chkdata RB_ cpUser, cpPass, dirname _RB   EQUAL_TO  EXIT_SUCCESS  _RB
		 CB_
			 GIVEBACK  order RB_ cpText, dirname _RB  _EI
		 _CB
		 OTHERWISE
		 CB_
			perr RB_ WARN, "Username or passwort wrong!" _RB  _EI
		 _CB
	 _CB
	 OTHERWISE
	 CB_
		perr RB_ WARN, "WTF?! That really shouldn't happen!" _RB  _EI
		assert(0) _EI  /* WTF, That shouldn't happen! */
	 _CB

	 END  RB_  EXIT_FAILURE  _RB  _EI
 _CB

/**
 *  This Function prints the correct usage of main
 */
 NOTHING  FUNCTION(Usage) RB_   NOTHING   _RB
 CB_
	 RB_  NOTHING  _RB  fprintf RB_  stderr,
					"Usage:\n"
					"Create User \t%s -c -u username -p password -a \"address\" -n \"Name\" -T \"Telephone Number\"\n"
					"Create Order\t%s -o -u username -p password -t \"Order\"\n"
					"View Orders \t%s -v -u username -p password\n"
					"Debug Switch: -d ... Prints more messages than normal (on stderr). Can not be used with -q\n"
					"Quiet Switch: -q ... Prints nothing on stderr. Can not be used with -d\n",
					cpCommand, cpCommand, cpCommand  _RB  _EI
	 RB_  NOTHING  _RB  fflush RB_ stderr _RB  _EI
	 END  RB_  EXIT_FAILURE  _RB  _EI
 _CB

/**
 *  Diese Funktion gibt eine Fehlermeldung aus, gegebenenfalls mit Aufloesung von errno.
 */
 NOTHING  FUNCTION(perr) RB_  NUMBER  type,  CONSTANT STRING cpMsg, ... _RB
 CB_
	va_list argPtr _EI

	 IS  RB_ bQuiet _RB   GIVEBACK  _EI

	debug RB_ "%s()", __func__ _RB  _EI

	va_start(argPtr, cpMsg) _EI
		 ALTERNATE  RB_ type _RB
		 CB_
			 OPTION  ERRNO:
				 RB_  NOTHING  _RB  vfprintf RB_ stderr, cpMsg, argPtr _RB  _EI
				 RB_  NOTHING  _RB  fprintf RB_ stderr, " - %s", strerror RB_ errno _RB  _RB  _EI
				 STOPHERE  _EI

			 OPTION  WARN: /* fall trough */
			 NOOPTION :
				 RB_  NOTHING  _RB  vfprintf RB_ stderr, cpMsg, argPtr _RB  _EI
				 STOPHERE  _EI
		 _CB
	va_end(argPtr) _EI
	 RB_  NOTHING  _RB  fprintf RB_ stderr, "\n" _RB  _EI
	 RB_  NOTHING  _RB  fflush RB_ stderr _RB  _EI
 _CB

/**
 * Debugging Ausgabe
 */
 NOTHING  FUNCTION(debug) RB_  CONSTANT   STRING cpMsg, ... _RB
 CB_
	va_list argPtr _EI

	 IS  RB_ !bDebug _RB   GIVEBACK  _EI

	va_start(argPtr, cpMsg)  _EI
		 RB_  NOTHING  _RB fprintf RB_ stderr, "%s - DEBUG: ", cpCommand _RB  _EI
		 RB_  NOTHING  _RB vfprintf RB_ stderr, cpMsg, argPtr _RB  _EI
		 RB_  NOTHING  _RB fprintf RB_ stderr, "\n" _RB  _EI
	va_end(argPtr) _EI
	 RB_  NOTHING  _RB  fflush RB_ stderr _RB  _EI
 _CB

