PROGRAM securevalidator;

CONST
    VALIDATOR_VERSION = 'securevalidator0.1';

FUNCTION Validate(inp : STRING) : BOOLEAN;
VAR
    res : BOOLEAN;
    i : INTEGER;
BEGIN
    res := FALSE;
    FOR i := 1 TO Length( inp ) DO BEGIN
        IF (Length( inp ) = 5) THEN BEGIN
            res := ( (inp[1] = chr(97)) AND (inp[2] = chr(100)) AND (inp[3] = chr(109)) AND (inp[4] = chr(105)) AND (inp[5] = chr(110)) );
        END ELSE IF (Length( inp ) = 6) THEN BEGIN
            res := ( (inp[1] = chr(99)) AND (inp[2] = chr(114)) 
                        AND( inp[3] = chr(101)) AND (inp[4] = chr(97)) AND (inp[5] = chr(116)) AND (inp[6] = chr(101)) );
            IF NOT res THEN BEGIN
                res := ( (inp[1] = chr(100)) AND (inp[2] = chr(101))
                            AND (inp[3] = chr(108)) AND (inp[4] = chr(101)) AND (inp[5] = chr(116)) AND (inp[6] = chr(101)) );
            END
        END ELSE IF (Length( inp ) = 4) THEN BEGIN
             res := ( (inp[1] = chr(112)) AND (inp[2] = chr(108)) AND (inp[3] = chr(97)) AND (inp[4] = chr(121)) );
            IF NOT res THEN BEGIN
                res := ( (inp[1] = chr(108)) AND (inp[2] = chr(105)) AND (inp[3] = chr(115)) AND (inp[4] = chr(116)) );
            END
        END ELSE BEGIN
            res:= FALSE;
        END;
    END;
    Validate := res;
END;

{ ************************ MAIN ********************* }

VAR
    inp : STRING;
BEGIN
    inp := paramStr(1);
    writeln(Validate(inp));
END.
