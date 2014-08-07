# -*- coding: iso-8859-1 -*-
# This file contains the lists of error messages used by xmlproc

import string

# The interface to the outside world

# Todo:
# - 3047 needed in Swedish, Norwegian and French
# - 2024 ditto
# - 2025 ditto
# - 2004 must be retranslated

error_lists={}  # The hash of errors

def add_error_list(language,list):
    error_lists[string.lower(language)]=list

def get_error_list(language):
    return error_lists[string.lower(language)]

def get_language_list():
    return error_lists.keys()

# Errors in English

english={

    # --- Warnings: 1000-1999
    1000: "Undeclared namespace prefix '%s'",
    1002: "Unsupported encoding '%s'",
    1003: "Obsolete namespace syntax",
    1005: "Unsupported character number '%d' in character reference",
    1006: "Element '%s' has attribute list, but no element declaration",
    1007: "Attribute '%s' defined more than once",
    1008: "Ambiguous content model",

    # --- Namespace warnings
    1900: "Namespace prefix names cannot contain ':'s.",
    1901: "Namespace URI cannot be empty",
    1902: "Namespace prefix not declared",
    1903: "Attribute names not unique after namespace processing",

    # --- Validity errors: 2000-2999
    2000: "Actual value of attribute '%s' does not match fixed value",
    2001: "Element '%s' not allowed here",
    2002: "Document root element '%s' does not match declared root element",
    2003: "Element '%s' not declared",
    2004: "Element '%s' ended before required elements found (%s)",
    2005: "Character data not allowed in the content of this element",
    2006: "Attribute '%s' not declared",
    2007: "ID '%s' appears more than once in document",
    2008: "Only unparsed entities allowed as the values of ENTITY attributes",
    2009: "Notation '%s' not declared",
    2010: "Required attribute '%s' not present",
    2011: "IDREF referred to non-existent ID '%s'",
    2012: "Element '%s' declared more than once",
    2013: "Only one ID attribute allowed on each element type",
    2014: "ID attributes cannot be #FIXED or defaulted",
    2015: "xml:space must be declared an enumeration type",
    2016: "xml:space must have exactly one or both of the values 'default' and 'preserve'",
    2017: "'%s' is not an allowed value for the '%s' attribute",
    2018: "Value of '%s' attribute must be a valid name",
    2019: "Value of '%s' attribute not a valid name token",
    2020: "Value of '%s' attribute not a valid name token sequence",
    2021: "Token '%s' in the value of the '%s' attribute is not a valid name",
    2022: "Notation attribute '%s' uses undeclared notation '%s'",
    2023: "Unparsed entity '%s' uses undeclared notation '%s'",
    2024: "Cannot resolve relative URI '%s' when document URI unknown",
    2025: "Element '%s' missing before element '%s'",

    # --- Well-formedness errors: 3000-3999
    # From xmlutils
    3000: "Couldn't open resource '%s'",
    3001: "Construct started, but never completed",
    3002: "Whitespace expected here",
    3003: "Didn't match '%s'",   ## FIXME: This must be redone
    3004: "One of %s or '%s' expected",
    3005: "'%s' expected",
    3047: "encoding '%s' conflicts with autodetected encoding",
    3048: "character set conversion problem: %s",

    # From xmlproc.XMLCommonParser
    3006: "SYSTEM or PUBLIC expected",
    3007: "Text declaration must appear first in entity",
    3008: "XML declaration must appear first in document",
    3009: "Multiple text declarations in a single entity",
    3010: "Multiple XML declarations in a single document",
    3011: "XML version missing on XML declaration",
    3012: "Standalone declaration on text declaration not allowed",
    3045: "Processing instruction target names beginning with 'xml' are reserved",
    3046: "Unsupported XML version",

    # From xmlproc.XMLProcessor
    3013: "Illegal construct",
    3014: "Premature document end, element '%s' not closed",
    3015: "Premature document end, no root element",
    3016: "Attribute '%s' occurs twice",
    3017: "Elements not allowed outside root element",
    3018: "Illegal character number '%d' in character reference",
    3019: "Entity recursion detected",
    3020: "External entity references not allowed in attribute values",
    3021: "Undeclared entity '%s'",
    3022: "'<' not allowed in attribute values",
    3023: "End tag for '%s' seen, but '%s' expected",
    3024: "Element '%s' not open",
    3025: "']]>' must not occur in character data",
    3027: "Not a valid character number",
    3028: "Character references not allowed outside root element",
    3029: "Character data not allowed outside root element",
    3030: "Entity references not allowed outside root element",
    3031: "References to unparsed entities not allowed in element content",
    3032: "Multiple document type declarations",
    3033: "Document type declaration not allowed inside root element",
    3034: "Premature end of internal DTD subset",
    3042: "Element crossed entity boundary",

    # From xmlproc.DTDParser
    3035: "Parameter entities cannot be unparsed",
    3036: "Parameter entity references not allowed in internal subset declarations",
    3037: "External entity references not allowed in entity replacement text",
    3038: "Unknown parameter entity '%s'",
    3039: "Expected type or alternative list",
    3040: "Choice and sequence lists cannot be mixed",
    3041: "Conditional sections not allowed in internal subset",
    3043: "Conditional section not closed",
    3044: "Token '%s' defined more than once",
    # next: 3049

    # From regular expressions that were not matched
    3900: "Not a valid name",
    3901: "Not a valid version number (%s)",
    3902: "Not a valid encoding name",
    3903: "Not a valid comment",
    3905: "Not a valid hexadecimal number",
    3906: "Not a valid number",
    3907: "Not a valid parameter reference",
    3908: "Not a valid attribute type",
    3909: "Not a valid attribute default definition",
    3910: "Not a valid enumerated attribute value",
    3911: "Not a valid standalone declaration",

    # --- Internal errors: 4000-4999
    4000: "Internal error: Entity stack broken",
    4001: "Internal error: Entity reference expected.",
    4002: "Internal error: Unknown error number %d.",
    4003: "Internal error: External PE references not allowed in declarations",

    # --- XCatalog errors: 5000-5099
    5000: "Uknown XCatalog element: %s.",
    5001: "Required XCatalog attribute %s on %s missing.",

    # --- SOCatalog errors: 5100-5199
    5100: "Invalid or unsupported construct: %s.",
    }

# Errors in Norwegian
norsk = english.copy()
norsk.update({

    # --- Warnings: 1000-1999
    1000: "Navneroms-prefikset '%s' er ikke deklarert",
    1002: "Tegn-kodingen '%s' er ikke støttet",
    1003: "Denne navnerom-syntaksen er foreldet",
    1005: "Tegn nummer '%d' i tegn-referansen er ikke støttet",
    1006: "Element '%s' har attributt-liste, men er ikke deklarert",
    1007: "Attributt '%s' deklarert flere ganger",
    1008: "Tvetydig innholds-modell",

    # --- Namespace warnings: 1900-1999
    1900: "Navnerommets prefiks-navn kan ikke inneholde kolon",
    1901: "Navnerommets URI kan ikke være tomt",
    1902: "Navnerommets prefiks er ikke deklarert",
    1903: "Attributt-navn ikke unike etter navneroms-prosessering",

    # --- Validity errors: 2000-2999
    2000: "Faktisk verdi til attributtet '%s' er ikke lik #FIXED-verdien",
    2001: "Elementet '%s' er ikke tillatt her",
    2002: "Dokumentets rot-element '%s' er ikke det samme som det deklarerte",
    2003: "Element-typen '%s' er ikke deklarert",
    2004: "Elementet '%s' avsluttet, men innholdet ikke ferdig",
    2005: "Tekst-data er ikke tillatt i dette elementets innhold",
    2006: "Attributtet '%s' er ikke deklarert",
    2007: "ID-en '%s' brukt mer enn en gang",
    2008: "Bare uparserte entiteter er tillatt som verdier til ENTITY-attributter",
    2009: "Notasjonen '%s' er ikke deklarert",
    2010: "Påkrevd attributt '%s' mangler",
    2011: "IDREF viste til ikke-eksisterende ID '%s'",
    2012: "Elementet '%s' deklarert mer enn en gang",
    2013: "Bare ett ID-attributt er tillatt pr element-type",
    2014: "ID-attributter kan ikke være #FIXED eller ha standard-verdier",
    2015: "xml:space må deklareres som en oppramstype",
    2016: "xml:space må ha en eller begge av verdiene 'default' og 'preserve'",
    2017: "'%s' er ikke en gyldig verdi for '%s'-attributtet",
    2018: "Verdien til '%s'-attributtet må være et gyldig navn",
    2019: "Verdien til '%s'-attributtet er ikke et gyldig NMTOKEN",
    2020: "Verdien til '%s'-attributtet er ikke et gyldig NMTOKENS",
    2021: "Symbolet '%s' i verdien til '%s'-attributtet er ikke et gyldig navn",
    2022: "Notasjons-attributtet '%s' bruker en notasjon '%s' som ikke er deklarert",
    2023: "Uparsert entitet '%s' bruker en notasjon '%s' som ikke er deklarert",

    # --- Well-formedness errors: 3000-3999
    # From xmlutils
    3000: "Kunne ikke åpne '%s'",
    3001: "For tidlig slutt på entiteten",
    3002: "Blanke forventet her",
    3003: "Matchet ikke '%s'",   ## FIXME: This must be redone
    3004: "En av %s eller '%s' forventet",
    3005: "'%s' forventet",

    # From xmlproc.XMLCommonParser
    3006: "SYSTEM eller PUBLIC forventet",
    3007: "Tekst-deklarasjonen må stå først i entiteten",
    3008: "XML-deklarasjonen må stå først i dokumentet",
    3009: "Flere tekst-deklarasjoner i samme entitet",
    3010: "Flere tekst-deklarasjoner i samme dokument",
    3011: "XML-versjonen mangler på XML-deklarasjonen",
    3012: "'Standalone'-deklarasjon på tekst-deklarasjon ikke tillatt",

    # From xmlproc.XMLProcessor
    3013: "Syntaksfeil",
    3014: "Dokumentet slutter for tidlig, elementet '%s' er ikke lukket",
    3015: "Dokumentet slutter for tidlig, rot-elementet mangler",
    3016: "Attributtet '%s' gjentatt",
    3017: "Kun ett rot-element er tillatt",
    3018: "Ulovlig tegn nummer '%d' i tegn-referanse",
    3019: "Entitets-rekursjon oppdaget",
    3020: "Eksterne entitets-referanser ikke tillatt i attributt-verdier",
    3021: "Entiteten '%s' er ikke deklarert",
    3022: "'<' er ikke tillatt i attributt-verdier",
    3023: "Slutt-tagg for '%s', men '%s' forventet",
    3024: "Elementet '%s' lukket, men ikke åpent",
    3025: "']]>' ikke tillatt i tekst-data",
    3027: "Ikke et gyldig tegn-nummer",
    3028: "Tegn-referanser ikke tillatt utenfor rot-elementet",
    3029: "Tekst-data ikke tillatt utenfor rot-elementet",
    3030: "Entitets-referanser ikke tillatt utenfor rot-elementet",
    3031: "Referanser til uparserte entiteter er ikke tillatt i element-innhold",
    3032: "Mer enn en dokument-type-deklarasjon",
    3033: "Dokument-type-deklarasjon kun tillatt før rot-elementet",
    3034: "Det interne DTD-subsettet slutter for tidlig",
    3042: "Element krysset entitets-grense",
    3045: "Processing instruction navn som begynner med 'xml' er reservert",
    3046: "Denne XML-versjonen er ikke støttet",

    # From xmlproc.DTDParser
    3035: "Parameter-entiteter kan ikke være uparserte",
    3036: "Parameter-entitets-referanser ikke tillatt inne i deklarasjoner i det interne DTD-subsettet",
    3037: "Eksterne entitets-referanser ikke tillatt i entitetsdeklarasjoner",
    3038: "Parameter-entiteten '%s' ikke deklarert",
    3039: "Forventet attributt-type eller liste av alternativer",
    3040: "Valg- og sekvens-lister kan ikke blandes",
    3041: "'Conditional sections' er ikke tillatt i det interne DTD-subsettet",
    3043: "'Conditional section' ikke lukket",
    3044: "Symbolet '%s' er definert mer enn en gang",

    # From regular expressions that were not matched
    3900: "Ikke et gyldig navn",
    3901: "Ikke et gyldig versjonsnummer (%s)",
    3902: "Ikke et gyldig tegnkodings-navn",
    3903: "Ikke en gyldig kommentar",
    3905: "Ikke et gyldig heksadesimalt tall",
    3906: "Ikke et gyldig tall",
    3907: "Ikke en gyldig parameter-entitets-referanse",
    3908: "Ikke en gyldig attributt-type",
    3909: "Ikke en gyldig attributt-standard-verdi",
    3910: "Ikke en gyldig verdi for opprams-attributter",
    3911: "Ikke en gyldig verdi for 'standalone'",

    # --- Internal errors: 4000-4999
    4000: "Intern feil: Entitets-stakken korrupt.",
    4001: "Intern feil: Entitets-referanse forventet.",
    4002: "Intern feil: Ukjent feilmelding %d.",
    4003: "Intern feil: Eksterne parameter-entiteter ikke tillatt i deklarasjoner",
    # --- XCatalog errors: 5000-5099
    5000: "Ukjent XCatalog-element: %s.",
    5001: "Påkrevd XCatalog-attributt %s på %s mangler.",

    # --- SOCatalog errors: 5100-5199
    5100: "Ugyldig eller ikke støttet konstruksjon: %s.",
    })

# Errors in Swedish
# Contributed by Marus Brisenfeldt, <marcusb@infotek.no>

svenska = english.copy()
svenska.update({

    # --- Warnings: 1000-1999
    1000: "Namnrymds-prefixet '%s' är inte deklarerat",
    1002: "Systemet stöder inte teckenuppsättningen '%s'",
    1003: "Denna namnrymds-syntax är förlegad",
    1005: "Teckennummer '%d' i teckenreferansen stöds inte",
    1006: "Ett attribut måste deklareras för elementet '%s'",
    1007: "Attributet '%s' är deklarerat flera gånger",
    1008: "Tvetydig innhållsmodell",

    # --- Namespace warnings: 1900-1999
    1900: "Namnrymdens prefixnamn kan inte innehålla kolon",
    1901: "Namnrymdens URI får inte vara tom (måste deklareras)",
    1902: "Namnrymdsprefixet är inte deklarerat",
    1903: "Attribut-namn inte unika efter namnrymds-prosessering",

    # --- Validity errors: 2000-2999
    2000: "Attributet '%s' faktiska värde är inte likt #FIXED-värdet",
    2001: "Elementet '%s' tillåts inte här",
    2002: "Dokumentets rot-element '%s' är inte det samma som deklarerat",
    2003: "Elementtypen '%s' är inte deklarerad",
    2004: "Elementet '%s' är avslutat, men innhållet är inte fullständigt",
    2005: "Textdata (PCDATA) är inte tillåtet som innehåll i elementet",
    2006: "Attributet '%s' är inte deklarerat",
    2007: "ID't '%s' används mer än en gång",
    2008: "Endast icke 'parsade' entiteter är tillåtna som värden till ENTITY-attribut",
    2009: "Notationen '%s' är inte deklarerad",
    2010: "Erfordligt attribut '%s' saknas",
    2011: "IDREF hänvisar till ett icke existerande ID ('%s')",
    2012: "Elementet '%s' har deklarerats mer än en gång",
    2013: "Endast ett ID-attribut er tillåtet per elementtyp",
    2014: "ID-attribut kan inte vara '#FIXED' eller ha ett standardvärde",
    2015: "xml:space måste deklareras som en listtyp",
    2016: "xml:space måste ha en eller båda av värdena 'default' och 'preserve'",
    2017: "'%s' är inte ett giltigt värde på attributet '%s'",
    2018: "Värdet på attributet '%s' måste vara ett giltigt namn",
    2019: "Värdet på attributet '%s' är inte ett giltigt NMTOKEN",
    2020: "Värdet på attributet '%s' är inte ett giltigt NMTOKENS",
    2021: "Symbolen '%s' i värdet på attributet '%s' är inte ett giltigt namn",
    2022: "Notations-attributet '%s' använder en notation ('%s') som inte är deklarerad",
    2023: "Icke 'parsad' entitet använder en notation ('%s') som inte är deklarerad",

    # --- Well-formedness errors: 3000-3999
    # From xmlutils
    3000: "Systemet kunde inte öppna '%s'",
    3001: "Entitet påbörjad, men inte avslutad",
    3002: "Mellanslag förväntat här",
    3003: "Matchar inte '%s'",   ## FIXME: This must be redone
    3004: "Antingen %s eller '%s' förväntad",
    3005: "'%s' förväntad",

    # From xmlproc.XMLCommonParser
    3006: "Antingen SYSTEM eller PUBLIC förväntad",
    3007: "Textdeklarationen måste stå först i entiteten",
    3008: "XML-deklarationen måste stå först i dokumentet",
    3009: "Flera textdeklarationer i samma entitet",
    3010: "Flera textdeklarationer i samma dokument",
    3011: "XML-version saknas i XML-deklarationen",
    3012: "'Standalone'-deklaration i textdeklarationen är inte tillåtet",

    # From xmlproc.XMLProcessor
    3013: "Syntaxfel",
    3014: "För tidigt dokumentslut, elementet '%s' är inte stängt",
    3015: "För tidigt dokumentslut, rotelement saknas",
    3016: "Attributet '%s' använt två gånger",
    3017: "Endast ett rotelement är tillåtet",
    3018: "Olovlig teckennummer ('%d') i teckenreferansen",
    3019: "Entitets-upprepning upptäckt",
    3020: "Externa entitets-referanser är inte tillåtna i attributvärden",
    3021: "Entiteten '%s' är inte deklarerad",
    3022: "'<' er inte tillåtet i attributvärdet",
    3023: "Sluttagg för '%s' istället för förväntad '%s'",
    3024: "Finner elementet '%s' sluttagg, men inte dess starttagg",
    3025: "']]>' inte tillåtet i textdata",
    3027: "Inget giltigt teckennummer",
    3028: "Teckenreferanser är inte tillåtna utanför rotelementet",
    3029: "Textdata är inte tillåtet utanför rotelementet",
    3030: "Entitetsreferanser är inte tillåtna utanför rotelementet",
    3031: "Referanser till icke 'parsade' entiteter tillåts inte i elementinnhållet",
    3032: "Multipla dokumenttypsdeklarationer",
    3033: "Dokumenttypsdeklarationer tillåts inte i rotelementet",
    3034: "Det interna DTD-subsettet avslutas för tidigt",
    3042: "Element överskrider entitetsgräns",

    # From xmlproc.DTDParser
    3035: "Parameterentiteter kan inte vara 'oparsade'",
    3036: "Parameterentitetsreferanser tillåts inte inne i deklarationer i det interna DTD-subsettet",
    3037: "Externa entitetsreferanser tillåts inte i entitetsdeklarationer",
    3038: "Parameterentiteten '%s' är inte deklarerad",
    3039: "Förväntat attributtyp eller lista av alternativ",
    3040: "Val- och sekvenslistor kan inte blandas",
    3041: "'Villkorssektioner' är inte tillåtna i den interna DTD-delmängden (subsetet)",
    3043: "'Villkorssektionen' är inte stängd",
    3044: "Symbolen '%s' har definerats mer än en gång",
    3045: "Processinstruktionsnamn som börjar med 'xml' är reserverade",
    3046: "Systemet stöder inte använd XML-versjon",

    # From regular expressions that were not matched
    3900: "Inget giltigt namn",
    3901: "Inget giltigt versionsnummer",
    3902: "Inget giltigt teckenkodsnamn",
    3903: "Ingen giltig kommentar",
    3905: "Inget giltigt hexadecimalt tal",
    3906: "Inget giltigt tal",
    3907: "Ingen giltig parameterentitetsreferans",
    3908: "Ingen giltig attributtyp",
    3909: "Inge giltigt attributstandardvärde",
    3910: "Ikke en gyldig attributt-standard-verdi",
    3911: "Ikke en gyldig verdi for 'standalone'",

    # --- Internal errors: 4000-4999
    4000: "Internt fel: Entitetsstacken korrupt.",
    4001: "Internt fel: Entitetsreferans förväntad.",
    4002: "Internt fel: Okänt felmeddelande %d.",
    4003: "Internt fel: Externa parameterentiteter tillåts inte i deklarationer.",
    # --- XCatalog errors: 5000-5099
    5000: "Okänt XCatalog-element: %s.",
    5001: "Nödvändigt XCatalog-attribut %s på %s saknas.",

    # --- SOCatalog errors: 5100-5199
    5100: "Konstruktionen: %s är ogiltig eller saknar stöd.",
    })

# Errors in French
# Contributed by Alexandre Fayolle, Logilab. Alexandre.Fayolle@logilab.fr

french = english.copy()
french.update({
    # Les termes français utilisés sont tirés de l'ouvrage
    # XML, Langage et applications, Alain Michard, Eyrolles
    # ISBN 2-212-09052-8

    # --- Warnings: 1000-1999
    1000: "Préfixe de domaine nominal non déclaré '%s'",
    1002: "Encodage non supporté '%s'",
    1003: "Syntaxe de domaine nominal obsolète",
    1005: "Caractère numéro '%d' non supporté dans la référence de caractère",
    1006: "L'élément '%s' a une liste d'attributs mais pas de déclaration d'élément",
    1007: "L'attribute '%s' est défini plus d'une fois",
    1008: "Modèle de contenu ambigu",

    # --- Namespace warnings
    1900: "Les préfixes de domaines nominaux ne peuvent contenir le caractère ':'",
    1901: "L'URI du domaine nominal ne doit pas être vide",
    1902: "Le préfixe du domaine nominal n'est pas déclaré",
    1903: "Le nom d'attribut n'est pas unique après traitement des domaines nominaux",

    # --- Validity errors: 2000-2999
    2000: "La valeur de l'attribut '%s' ne correspond pas à la valeur imposée",
    2001: "L'élément '%s' ne peut figurer à cet endroit",
    2002: "L'élément racine du document '%s' ne correspond pas à la racine déclarée",
    2003: "L'élément '%s' n'a pas été déclaré",
    2004: "L'élément '%s' est terminé, mais il n'est pas complet",
    2005: "Les données ne sont pas autorisées comme contenu de cet élément",
    2006: "L'attribut '%s' n'a pas été déclaré",
    2007: "L'ID '%s' apparaît plusieurs fois dans le document",
    2008: "Seules les entités non XML sont permises dans les attributs ENTITY",
    2009: "La notation '%s' n'a pas été déclarée",
    2010: "L'attribut requis '%s' est absent",
    2011: "L'attribut IDREF point sur un ID inexistant '%s'",
    2012: "L'élément '%s' est déclaré plus d'une fois",
    2013: "Un seul attribut ID par type d'élément",
    2014: "Les attributs ID nepeuvent être #FIXED ou avoir de valeur par défaut",
    2015: "xml:space doit être de type énumération",
    2016: "xml:space doit avoir comme valeurs possibles 'default' et 'preserve'",
    2017: "'%s' n'est pas une valeur autorisée pour l'attribut '%s'",
    2018: "La valeur de l'attribut '%s' doit être un nom valide",
    2019: "La valeur de l'attribut '%s' n'est pas un identifiant de nom valide",
    2020: "La valeur de l'attribut '%s' n'est pas une liste d'identifiants de noms valides",
    2021: "L'identifiant '%s' dans la valeur de l'attribut '%s' n'est pas valide",
    2022: "L'attribut notation '%s' utilise la notation non déclarée '%s'",
    2023: "L'entité non XML '%s' utilise la notation non déclarée '%s'",

    # --- Well-formedness errors: 3000-3999
    # From xmlutils
    3000: "Impossible d'ouvrir la ressource '%s'",
    3001: "Construction commencée mais jamais achevée",
    3002: "Caractères d'espacement attendus à cet endroit",
    3003: "Impossible de faire correspondre '%s'",   ## FIXME: This must be redone
    3004: "'%s' ou '%s' était attendu",
    3005: "'%s' état attendu",

    # From xmlproc.XMLCommonParser
    3006: "SYSTEM ou PUBLIC était attendu",
    3007: "La déclaration de texte doit apparaître en premier dans une entité",
    3008: "La déclaration XML doit apparaître en premier dans un document",
    3009: "Plusieurs déclarations de texte dans une seule entité",
    3010: "Plusieurs déclarations XML dans le document",
    3011: "Il manque la versin d'XML dans la déclaratino XML",
    3012: "Une déclaration indépendante de texte sont interdites",
    3045: "Les noms de cibles d'instruction de traitement commençant par 'xml' sont réservés",
    3046: "Version de XML non supportée",

    # From xmlproc.XMLProcessor
    3013: "Construction illégale",
    3014: "Fin de document prématurée, l'élément '%s' n'est pas fermé",
    3015: "Fin de document prématurée, pas d'élément racine",
    3016: "L'attribut '%s' apparâit deux fois",
    3017: "Les éléments ne peuvent apparaître à l'extérieur de l'élément racine",
    3018: "Caractère numéro '%d' non supporté dans la référence de caractère",
    3019: "Une entité récursive a été détectée",
    3020: "Les références à des entités externes sont interdites dans les valeurs d'attributs",
    3021: "L'entité '%s' n'a pas été déclarée",
    3022: "'<' est interdit dans les valeurs d'attributs",
    3023: "La balise de fin pour '%s' a été vue, alors que '%s' était attendu",
    3024: "L'élément'%s' n'a pas été ouvert",
    3025: "']]>' ne doit pas apparaître dans les sections littérales",
    3027: "Numéro de caractère invalide",
    3028: "Les références de caractères sont interdites en dehors de l'élément racine",
    3029: "Les sections littérales sont interdites en dehors de l'élément racine",
    3030: "Les références à des entités sont interdites en dehors de l'élément racine",
    3031: "Les références à des entités non XML sont interdites dans un élément",
    3032: "Il y a de multiples déclaratinos de type de document",
    3033: "La déclaration de type de document est interdite dans l'élément racine",
    3034: "Fin prématurée de la DTD interne",
    3042: "Un élément chevauche les limites d'une entité",

    # From xmlproc.DTDParser
    3035: "Les entités paramètres ne peuvent pas être déréférencées",
    3036: "Les références à des entités paramètres sont interdites dans la DTD interne",
    3037: "Les références à des entités externes sont interdites dans le texte de remplacement",
    3038: "L'entité paramètre '%s' est inconnue",
    3039: "Un type une liste de valeurs possibles est attendu",
    3040: "Les liste de choix et les listes de séquences ne peuvent être mélangées",
    3041: "Les sections conditionnelles sont interdites dans la DTD interne",
    3043: "La section conditionnelle n'est pas fermée",
    3044: "Le marqueur '%s' est défini plusieurs fois",
    # next: 3047

    # From regular expressions that were not matched
    3900: "Nom invalide",
    3901: "Numéro de version invalide (%s)",
    3902: "Nom d'encodage invalide",
    3903: "Commentaire invalide",
    3905: "Nombre hexadécimal invalide",
    3906: "Nombre invalide",
    3907: "Référence à un paramètre invalide",
    3908: "Type d'attribut invalide",
    3909: "Définitionde valeur par défaut d'attribut invalide",
    3910: "Valeur d'attribut énuméré invalide",
    3911: "Déclaration autonome invalide",

    # --- Internal errors: 4000-4999
    4000: "Erreur interne : pile dentités cassée",
    4001: "Erreur interne : référence à une entité attendue.",
    4002: "Erreur interne : numéro d'erreur inconnu.",
    4003: "Erreur interne : référence à un PE externe interdite dans la déclaration",

    # --- XCatalog errors: 5000-5099
    5000: "L'élément de XCatalog est inconnu : %s.",
    5001: "L'attribut de XCatalog  %s requis sur %s est manquant.",

    # --- SOCatalog errors: 5100-5199
    5100: "Construction invalide ou non supportée : %s.",
    })

# Errors in Spanish
# Contributed by Ricardo Javier Cardenes (ricardo@conysis.com)

spanish = {

    # --- Warnings: 1000-1999
    1000: "Prefijo de espacio de nombres sin declarar '%s'",
    1002: "Codificación no soportada '%s'",
    1003: "Sintaxis de espacio de nombres obsoleta",
    1005: "Caracter número '%d' no soportado en la referencia a caracter",
    1006: "El elemento '%s' tiene lista de atributos, pero no declaración de elemento",
    1007: "El atributo '%s' está definido más de una vez",
    1008: "Modelo de contenido ambiguo",

    # --- Namespace warnings
    1900: "Los prefijos de espacio de nombres no pueden contener ':'.",
    1901: "Las URI de los espacios de nombre no pueden estar vacías",
    1902: "Prefijo de espacio de nombres sin declarar",
    1903: "Nombres de atributo repetidos después de procesar el espacio de nombres",

    # --- Validity errors: 2000-2999
    2000: "El valor real del atributo '%s' no se corresponde al valor fijado",
    2001: "No se permite aquí el elemento '%s'",
    2002: "El elemento '%s' raíz del documento no es el mismo que se declaró",
    2003: "El elemento '%s' no está declarado",
    2004: "El elemento '%s' termina antes de encontrar los elementos requeridos (%s)",
    2005: "No se permite texto en el contenido de este elemento",
    2006: "El atributo '%s' no ha sido declarado",
    2007: "El ID '%s' aparece más de una vez en el documento",
    2008: "Sólo se permiten entidades sin analizar como valores de los atributos ENTITY",
    2009: "No está declarada la notación '%s'",
    2010: "No está presente el atributo '%s' necesario",
    2011: "IDREF referida a un ID '%s', que no existe",
    2012: "El elemento '%s' está declarado más de una vez",
    2013: "Sólo se permite un atributo ID por cada tipo de elemento",
    2014: "Los atributos ID no pueden ser #FIXED ni tener valor por defecto",
    2015: "xml:space debe ser declarado como tipo enumerado",
    2016: "xml:space debe tener exactamente los valores 'default' y 'preserve'",
    2017: "'%s' no es un tipo válido para el atributo '%s'",
    2018: "El valor del atributo '%s' debe ser un nombre válido",
    2019: "El valor del atributo '%s' no es un NMTOKEN válido",
    2020: "El valor del atributo '%s' no es un NMTOKENS válido",
    2021: "El símbolo '%s' en el valor del atributo '%s' no es un nombre válido",
    2022: "El atributo de notación '%s' usa la notación '%s', que no está declarada",
    2023: "La entidad sin analizar '%s' usa la notación '%s', que no está declarada",
    2024: "No se puede resolver la URI relativa '%s' si se desconoce la URI del documento",
    2025: "No se encuentra el elemento '%s' antes del '%s'",

    # --- Well-formedness errors: 3000-3999
    # From xmlutils
    3000: "No pude abrir el recurso '%s'",
    3001: "Se empezó la construcción, pero no se pudo completar",
    3002: "Aquí se esperaba un espacio en blanco",
    3003: "'%s' no se corresponde",   ## FIXME: This must be redone
    3004: "Se esperaba %s o '%s'",
    3005: "Se esperaba '%s'",
    3047: "La codificación '%s' es conflictiva con la autodetectada",
    3048: "Problema de conversión de conjunto de caracteres: %s",

    # From xmlproc.XMLCommonParser
    3006: "Se esperaba SYSTEM o PUBLIC",
    3007: "La declaración de texto debe aparecer la primera en la entidad",
    3008: "La declaración XML debe aparecer la primera en el documento",
    3009: "Varias declaraciones de texto en la misma entidad",
    3010: "Múltiples declaraciones XML en el mismo documento",
    3011: "Falta la versión en la declaración XML",
    3012: "No se permite una declaración 'standalone' en una declaración de texto",
    3045: "Los nombres de PI que comienzan por 'xml' están reservados",
    3046: "Versión XML no soportada",
    
    # From xmlproc.XMLProcessor
    3013: "Construcción ilegal",
    3014: "El documento acabó prematuramente. No se cerró el elemento '%s'",
    3015: "Fin prematuro del documento. No hay elemento raíz",
    3016: "El atributo '%s' está duplicado",
    3017: "No se permiten elementos fuera del raíz",
    3018: "Caracter ilegal número '%d' en la referencia a caracter",
    3019: "Detectada recursividad de entidades",
    3020: "No se permiten referencias a entidades externas en los valores de los atributos",
    3021: "Entidad '%s' sin declarar",
    3022: "No se permite '<' en los valores de atributos",
    3023: "Se encontró la etiqueta de fin de '%s', pero se esperaba '%s'",
    3024: "Element '%s' not open",
    3025: "No debe aparecer ']]>' dentro de datos de texto",
    3027: "No es un número de caracter válido",
    3028: "No se permite la referencia a caracteres fuera del elemento raíz",
    3029: "No se admite texto fuera del elemento raíz",
    3030: "No se admiten referencias a entidades fuera del elemento raíz",
    3031: "No se admiten referencias a entidades sin analizar en el contenido de un elemento",
    3032: "Múltiples declaraciones de tipo de documento",
    3033: "No se admite una declaración de tipo de documento dentro del elemento raíz",
    3034: "Fin prematuro de un subconjunto interno de DTD",
    3042: "Un elemento cruza los límites de la entidad",

    # From xmlproc.DTDParser
    3035: "Las entidades paramétricas no pueden ser de tipo 'unparsed'",
    3036: "No se permiten referencias a entidades paramétricas en un subconjunto interno de declaraciones",
    3037: "No se permiten referencias a entidades externas en texto de reemplazo de entidades",
    3038: "Entidad paramétrica desconocida '%s'",
    3039: "Se esperaba un tipo o una lista de alternativas",
    3040: "No se puede mezclar listas secuenciales con alternativas",
    3041: "No se admiten secciones condicionales en subconjuntos internos",
    3043: "Sección condicional sin cerrar",
    3044: "Se definió el símbolo '%s' más de una vez",
    # next: 3049
    
    # From regular expressions that were not matched
    3900: "No es un nombre válido",
    3901: "No es un número de versión válido (%s)",
    3902: "No es un nombre de codificación válido",
    3903: "No es un comentario válido",
    3905: "No es un número hexadecimal válido",
    3906: "No es un número válido",
    3907: "No es una referencia a parámetro válida",
    3908: "No es un tipo de atributo válido",
    3909: "No es una definición de atributo por defecto válida",
    3910: "No es un valor de atributo enumerado válido",
    3911: "No es una declaración 'standalone' válida",
    
    # --- Internal errors: 4000-4999
    4000: "Error interno: Pila de la entidad corrupta",
    4001: "Error interno: Se esperaba una referencia a entidad.",
    4002: "Error interno: Número de error desconocido.",
    4003: "Error interno: No se admiten refrencias PE externas en las declaraciones",

    # --- XCatalog errors: 5000-5099
    5000: "Elemento XCatalog desconocido: %s.",
    5001: "Falta el atributo XCatalog %s necesario en %s.",
     
    # --- SOCatalog errors: 5100-5199
    5100: "Construcción inválida o no soportada: %s.",
    }

# Updating the error hash

add_error_list("en", english)
add_error_list("no", norsk)
add_error_list("sv", svenska)
add_error_list("fr", french)
add_error_list("es", spanish)

# Checking

def _test():
    def compare(l1, l2):
        for key in l1:
            if not key in l2:
                print "l1:", key

        for key in l2:
            if not key in l1:
                print "l2:", key

    en = english.keys()
    no = norsk.keys()
    sv = svenska.keys()
    fr = french.keys()
    es = spanish.keys()

    en.sort()
    no.sort()
    sv.sort()
    fr.sort()
    es.sort()

    print "en == no"
    compare(en, no)

    print "en == sv"
    compare(en, sv)

    print "en == fr"
    compare(en, fr)

    print "en == es"
    compare(en, es)

if __name__ == "__main__":
    _test()
