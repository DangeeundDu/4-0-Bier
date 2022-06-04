/**
 *  Ein Programm zur einfachen Kunden- und Bestellverwaltung fuer Kleinstbetriebe
 */

/**
 * Pizzaservice: Anlegen, ansehen von Kundenkonten, Bestellungen taetigen.
 */

GET "pizzaservice.progh"

/** Programmname, z.B. fuer Usage() wichtig. */
 const   char * cpCommand  EQUAL  "<not yet set>" ;

/** Debug Switch */
 bool  bDebug  EQUAL  false ;

/** Quiet Switch */
 bool  bQuiet  EQUAL  false ;

/**
 * Prueft mittels getopt uebergebene Optionen und Parameter, startet Unterprogramme
 */
int FUNCTION(main)  (   int  argc,  char * * argv  )
 {
	 int  c  EQUAL  -1, tmp  EQUAL  0, hash  EQUAL  -1 ;

	 bool  bc  EQUAL  false ;  /* create */
	 bool  bv  EQUAL  false ;  /* view */
	 bool  bo  EQUAL  false ;  /* order */
	 bool  bu  EQUAL  false ;  /* username */
	 bool  bp  EQUAL  false ;  /* password */
	 bool  bn  EQUAL  false ;  /* name */
	 bool  bt  EQUAL  false ;  /* order text */
	 bool  ba  EQUAL  false ;  /* address */
	 bool  bT  EQUAL  false ;  /* telephone number */
	 bool  bError  EQUAL  false ;

	 char * cpUser  EQUAL   (  char *  ) 0,  * cpPass  EQUAL   (  char *  ) 0,  * cpText  EQUAL   (  char *  ) 0 ;
	 char * cpTel  EQUAL   (  char *  ) 0,  * cpAddress  EQUAL   (  char *  ) 0,  * cpName  EQUAL   (  char *  ) 0, dirname [ DIRNAME_LEN ]  ;

	cpCommand  EQUAL  argv [  0  ]  ;

	 while  (   (  c  EQUAL  getopt (  argc, argv, "-cdqvou:p:a:T:n:t:"  )   )   !=  EOF  )
	 {
		 switch  (  c  )
		 {
			 case  'c':
				 if  (  bc  ==  true  )
				 {
					bError  EQUAL  true ;
					perr ( WARN, "'-c' may only occur once!" )  ;
					 break  ;
				 }
				bc  EQUAL  true ;
				 break  ;

			 case  'd':
				 if  (  bDebug  ==  true  )
				 {
					/* mehrfaches angeben von -d hat keine Wirkung */
					 break  ;
				 }
				bDebug  EQUAL  true ;
				 break  ;

			 case  'q':
				 if  (  bQuiet  ==  true  )
				 {
					/* mehrfaches angeben von -q hat keine Wirkung */
					 break  ;
				 }
				bQuiet  EQUAL  true ;
				 break  ;

			 case  'o':
				 if  (  bo  ==  true  )
				 {
					bError  EQUAL  true ;
					perr ( WARN, "'-o' may only occur once!" )  ;
					 break  ;
				 }
				bo  EQUAL  true ;
				 break  ;

			 case  'v':
				 if  (  bv  ==  true  )
				 {
					bError  EQUAL  true ;
					perr ( WARN, "'-v' may only occur once!" )  ;
					 break  ;
				 }
				bv  EQUAL  true ;
				 break  ;

			 case  'a':
				 if  (  ba  ==  true  )
				 {
					bError  EQUAL  true ;
					perr ( WARN, "'-a' may only occur once!" )  ;
					 break  ;
				 }
				ba  EQUAL  true ;
				cpAddress  EQUAL  optarg ;
				 break  ;

			 case  'T':
				 if  (  bT  ==  true  )
				 {
					bError  EQUAL  true ;
					perr ( WARN, "'-a' may only occur once!" )  ;
					bT  EQUAL  false ;
					 break  ;
				 }
				bT  EQUAL  true ;
				cpTel  EQUAL  optarg ;
				 break  ;

			 case  'n':
				 if  (  bn  ==  true  )
				 {
					bError  EQUAL  true ;
					perr ( WARN, "'-n' may only occur once!" )  ;
					 break  ;
				 }
				bn  EQUAL  true ;
				cpName  EQUAL  optarg ;
				 break  ;

			 case  'u':
				 if  (  bu  ==  true  )
				 {
					bError  EQUAL  true ;
					perr ( WARN, "'-u' may only occur once!" )  ;
					 break  ;
				 }
				bu  EQUAL  true ;
				cpUser  EQUAL  optarg ;
				 break  ;

			 case  'p':
				 if  (  bp  ==  true  )
				 {
					bError  EQUAL  true ;
					perr ( WARN, "'-p' may only occur once!" )  ;
					 break  ;
				 }
				bp  EQUAL  true ;
				cpPass  EQUAL  optarg ;
				 break  ;

			 case  't':
				 if  (  bt  ==  true  )
				 {
					bError  EQUAL  true ;
					perr ( WARN, "'-t' may only occur once!" )  ;
					 break  ;
				 }
				bt  EQUAL  true ;
				cpText  EQUAL  optarg ;
				 break  ;

			 case  ':':
			 case  '?':
				bError  EQUAL  true ;
				 break  ;

			 NOcase :
				Usage (  )  ;
				 break  ;
		 }
	 }

	 if  (  bQuiet && bDebug  )
	 {
		bQuiet  EQUAL  false ;
		perr ( WARN, "WTF? Should be quiet '-q' and verbose '-d' at the same time?! RTFM ;)" )  ;
		Usage (  )  ;
	 }
	/* Debug Meldungen werden erst ab hier sicher ausgegeben wenn '-d' angegeben ist! */

	 if  (  bError  ==  true ||
			 (
				! ( bc && !bo && bu && bp && !bt && !bv && ba && bn && bT )  &&
				! ( !bc && bo && bu && bp && bt && !bv && !ba && !bn && !bT )  &&
				! ( !bc && !bo && bu && bp && !bt && bv && !ba && !bn && !bT )
			 )
	   )
	 {
		Usage (  )  ;
	 }

	debug ( "compiled at: %s %s", __DATE__, __time_t__ )  ;
	debug ( "max count of customer directories: %d", HASH_SIZE )  ;
	debug ( "calculating hash for %s.", cpUser )  ;

	for ( tmp  EQUAL  0 ;  tmp  <   (  int  ) strlen ( cpUser )  ;  tmp++ )
	 {
		 if  (  ( tmp % 2 )   ==  0 )
		 {
			/* tmp is even */
			hash  EQUAL   ( hash +  (  int  ) cpUser [  tmp  ]  )  ;
		 }
		 OTHERWifE
		 {
			/* tmp is odd */
			hash  EQUAL   ( hash -  (  int  ) cpUser [  tmp  ]  )  ;
		 }
	 }
	hash %EQUAL HASH_SIZE ;

	/* correct negative coset class */
	 if  ( hash  <  0 )  hash +EQUAL  HASH_SIZE ;

	 snprintf ( dirname, DIRNAME_LEN, "%03d", hash )  ;

	 if  ( bc )
	 {
		debug ( "Username: %s", cpUser )  ;
		debug ( "Password: %s", cpPass )  ;
		debug ( "Full Name: %s", cpName )  ;
		debug ( "Address: %s", cpAddress )  ;
		debug ( "Tel: %s", cpTel )  ;
		debug ( "Customer directory (= hash): %s", dirname )  ;
		 return  createUser ( cpUser, cpPass, cpName, cpAddress, cpTel, dirname )  ;
	 }
	 OTHERWifE   if  ( bv )
	 {
		debug ( "Username: %s", cpUser )  ;
		debug ( "Password: %s", cpPass )  ;
		debug ( "Customer directory (= hash): %s", dirname )  ;

		 if  (  chkdata ( cpUser, cpPass, dirname )   ==  EXIT_SUCCESS  )
		 {
			 return  viewUser ( dirname )  ;
		 }
		 OTHERWifE
		 {
			perr ( WARN, "Username or passwort wrong!" )  ;
		 }
	 }
	 OTHERWifE   if  ( bo )
	 {
		debug ( "Username: %s", cpUser )  ;
		debug ( "Password: %s", cpPass )  ;
		debug ( "Customer directory (= hash) : %s", dirname )  ;

		 if  (  chkdata ( cpUser, cpPass, dirname )   ==  EXIT_SUCCESS  )
		 {
			 return  order ( cpText, dirname )  ;
		 }
		 OTHERWifE
		 {
			perr ( WARN, "Username or passwort wrong!" )  ;
		 }
	 }
	 OTHERWifE
	 {
		perr ( WARN, "WTF?! That really shouldn't happen!" )  ;
		assert(0) ;  /* WTF, That shouldn't happen! */
	 }

	 exit  (  EXIT_FAILURE  )  ;
 }

/**
 *  This Function prints the correct usage of main
 */
 void  FUNCTION(Usage) (   void   )
 {
	 (  void  )  fprintf (  stderr,
					"Usage:\n"
					"Create User \t%s -c -u username -p password -a \"address\" -n \"Name\" -T \"Telephone Number\"\n"
					"Create Order\t%s -o -u username -p password -t \"Order\"\n"
					"View Orders \t%s -v -u username -p password\n"
					"Debug Switch: -d ... Prints more messages than normal (on stderr). Can not be used with -q\n"
					"Quiet Switch: -q ... Prints nothing on stderr. Can not be used with -d\n",
					cpCommand, cpCommand, cpCommand  )  ;
	 (  void  )  fflush ( stderr )  ;
	 exit  (  EXIT_FAILURE  )  ;
 }

/**
 *  Diese Funktion gibt eine Fehlermeldung aus, gegebenenfalls mit Aufloesung von errno.
 */
 void  FUNCTION(perr) (  int  type,  const char * cpMsg, ... )
 {
	va_list argPtr ;

	 if  ( bQuiet )   return  ;

	debug ( "%s()", __func__ )  ;

	va_start(argPtr, cpMsg) ;
		 switch  ( type )
		 {
			 case  ERRNO:
				 (  void  )  vfprintf ( stderr, cpMsg, argPtr )  ;
				 (  void  )  fprintf ( stderr, " - %s", strerror ( errno )  )  ;
				 break  ;

			 case  WARN: /* fall trough */
			 NOcase :
				 (  void  )  vfprintf ( stderr, cpMsg, argPtr )  ;
				 break  ;
		 }
	va_end(argPtr) ;
	 (  void  )  fprintf ( stderr, "\n" )  ;
	 (  void  )  fflush ( stderr )  ;
 }

/**
 * Debugging Ausgabe
 */
 void  FUNCTION(debug) (  const   char * cpMsg, ... )
 {
	va_list argPtr ;

	 if  ( !bDebug )   return  ;

	va_start(argPtr, cpMsg)  ;
		 (  void  ) fprintf ( stderr, "%s - DEBUG: ", cpCommand )  ;
		 (  void  ) vfprintf ( stderr, cpMsg, argPtr )  ;
		 (  void  ) fprintf ( stderr, "\n" )  ;
	va_end(argPtr) ;
	 (  void  )  fflush ( stderr )  ;
 }

