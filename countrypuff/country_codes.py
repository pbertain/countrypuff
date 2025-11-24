"""
Country code mappings between ISO 3166-1 alpha-2 and CIA Factbook GEC codes.

This module provides comprehensive mappings to convert between standard ISO country codes
and the GEC (formerly FIPS) codes used by the CIA World Factbook.
"""

from typing import Dict, Optional, List, Tuple


class CountryCodeMapper:
    """
    Maps between ISO 3166-1 alpha-2 codes and CIA Factbook GEC codes.
    
    The CIA World Factbook uses GEC (Geopolitical Entities and Codes) which
    are different from the standard ISO 3166-1 alpha-2 codes.
    """
    
    # Comprehensive mapping: ISO 3166-1 alpha-2 -> GEC code
    ISO_TO_GEC = {
        # A
        'AD': 'an',  # Andorra
        'AE': 'ae',  # United Arab Emirates
        'AF': 'af',  # Afghanistan
        'AG': 'ac',  # Antigua and Barbuda
        'AI': 'av',  # Anguilla
        'AL': 'al',  # Albania
        'AM': 'am',  # Armenia
        'AO': 'ao',  # Angola
        'AQ': 'ay',  # Antarctica
        'AR': 'ar',  # Argentina
        'AS': 'aq',  # American Samoa
        'AT': 'au',  # Austria
        'AU': 'as',  # Australia
        'AW': 'aa',  # Aruba
        'AX': 'ax',  # Åland Islands (Akrotiri in CIA)
        'AZ': 'aj',  # Azerbaijan
        
        # B
        'BA': 'bk',  # Bosnia and Herzegovina
        'BB': 'bb',  # Barbados
        'BD': 'bg',  # Bangladesh
        'BE': 'be',  # Belgium
        'BF': 'uv',  # Burkina Faso
        'BG': 'bu',  # Bulgaria
        'BH': 'ba',  # Bahrain
        'BI': 'by',  # Burundi
        'BJ': 'bn',  # Benin
        'BL': 'tb',  # Saint Barthélemy
        'BM': 'bd',  # Bermuda
        'BN': 'bx',  # Brunei
        'BO': 'bl',  # Bolivia
        'BQ': 'bq',  # Bonaire, Sint Eustatius and Saba (Navassa Island in CIA)
        'BR': 'br',  # Brazil
        'BS': 'bf',  # Bahamas
        'BT': 'bt',  # Bhutan
        'BV': 'bv',  # Bouvet Island
        'BW': 'bc',  # Botswana
        'BY': 'bo',  # Belarus
        'BZ': 'bh',  # Belize
        
        # C
        'CA': 'ca',  # Canada
        'CC': 'ck',  # Cocos (Keeling) Islands
        'CD': 'cg',  # Congo, Democratic Republic
        'CF': 'ct',  # Central African Republic
        'CG': 'cf',  # Congo
        'CH': 'sz',  # Switzerland
        'CI': 'iv',  # Côte d'Ivoire
        'CK': 'cw',  # Cook Islands
        'CL': 'ci',  # Chile
        'CM': 'cm',  # Cameroon
        'CN': 'ch',  # China
        'CO': 'co',  # Colombia
        'CR': 'cs',  # Costa Rica
        'CU': 'cu',  # Cuba
        'CV': 'cv',  # Cape Verde
        'CW': 'uc',  # Curaçao
        'CX': 'kt',  # Christmas Island
        'CY': 'cy',  # Cyprus
        'CZ': 'ez',  # Czech Republic
        
        # D
        'DE': 'gm',  # Germany
        'DJ': 'dj',  # Djibouti
        'DK': 'da',  # Denmark
        'DM': 'do',  # Dominica
        'DO': 'dr',  # Dominican Republic
        'DZ': 'ag',  # Algeria
        
        # E
        'EC': 'ec',  # Ecuador
        'EE': 'en',  # Estonia
        'EG': 'eg',  # Egypt
        'EH': 'wi',  # Western Sahara (removed from CIA in 2020)
        'ER': 'er',  # Eritrea
        'ES': 'sp',  # Spain
        'ET': 'et',  # Ethiopia
        'EU': 'ee',  # European Union
        
        # F
        'FI': 'fi',  # Finland
        'FJ': 'fj',  # Fiji
        'FK': 'fk',  # Falkland Islands
        'FM': 'fm',  # Micronesia
        'FO': 'fo',  # Faroe Islands
        'FR': 'fr',  # France
        
        # G
        'GA': 'gb',  # Gabon
        'GB': 'uk',  # United Kingdom
        'GD': 'gj',  # Grenada
        'GE': 'gg',  # Georgia
        'GF': 'fg',  # French Guiana
        'GG': 'gk',  # Guernsey
        'GH': 'gh',  # Ghana
        'GI': 'gi',  # Gibraltar
        'GL': 'gl',  # Greenland
        'GM': 'ga',  # Gambia
        'GN': 'gv',  # Guinea
        'GP': 'gp',  # Guadeloupe
        'GQ': 'ek',  # Equatorial Guinea
        'GR': 'gr',  # Greece
        'GS': 'sx',  # South Georgia and the South Sandwich Islands
        'GT': 'gt',  # Guatemala
        'GU': 'gq',  # Guam
        'GW': 'pu',  # Guinea-Bissau
        'GY': 'gy',  # Guyana
        
        # H
        'HK': 'hk',  # Hong Kong
        'HM': 'hm',  # Heard Island and McDonald Islands
        'HN': 'ho',  # Honduras
        'HR': 'hr',  # Croatia
        'HT': 'ha',  # Haiti
        'HU': 'hu',  # Hungary
        
        # I
        'ID': 'id',  # Indonesia
        'IE': 'ei',  # Ireland
        'IL': 'is',  # Israel
        'IM': 'im',  # Isle of Man
        'IN': 'in',  # India
        'IO': 'io',  # British Indian Ocean Territory
        'IQ': 'iz',  # Iraq
        'IR': 'ir',  # Iran
        'IS': 'ic',  # Iceland
        'IT': 'it',  # Italy
        
        # J
        'JE': 'je',  # Jersey
        'JM': 'jm',  # Jamaica
        'JO': 'jo',  # Jordan
        'JP': 'ja',  # Japan
        
        # K
        'KE': 'ke',  # Kenya
        'KG': 'kg',  # Kyrgyzstan
        'KH': 'cb',  # Cambodia
        'KI': 'kr',  # Kiribati
        'KM': 'cn',  # Comoros
        'KN': 'sc',  # Saint Kitts and Nevis
        'KP': 'kn',  # North Korea
        'KR': 'ks',  # South Korea
        'KW': 'ku',  # Kuwait
        'KY': 'cj',  # Cayman Islands
        'KZ': 'kz',  # Kazakhstan
        
        # L
        'LA': 'la',  # Laos
        'LB': 'le',  # Lebanon
        'LC': 'st',  # Saint Lucia
        'LI': 'ls',  # Liechtenstein
        'LK': 'ce',  # Sri Lanka
        'LR': 'li',  # Liberia
        'LS': 'lt',  # Lesotho
        'LT': 'lh',  # Lithuania
        'LU': 'lu',  # Luxembourg
        'LV': 'lg',  # Latvia
        'LY': 'ly',  # Libya
        
        # M
        'MA': 'mo',  # Morocco
        'MC': 'mn',  # Monaco
        'MD': 'md',  # Moldova
        'ME': 'mj',  # Montenegro
        'MF': 'rn',  # Saint Martin
        'MG': 'ma',  # Madagascar
        'MH': 'rm',  # Marshall Islands
        'MK': 'mk',  # North Macedonia
        'ML': 'ml',  # Mali
        'MM': 'bm',  # Myanmar (Burma)
        'MN': 'mg',  # Mongolia
        'MO': 'mc',  # Macao
        'MP': 'cq',  # Northern Mariana Islands
        'MQ': 'mb',  # Martinique
        'MR': 'mr',  # Mauritania
        'MS': 'mh',  # Montserrat
        'MT': 'mt',  # Malta
        'MU': 'mp',  # Mauritius
        'MV': 'mv',  # Maldives
        'MW': 'mi',  # Malawi
        'MX': 'mx',  # Mexico
        'MY': 'my',  # Malaysia
        'MZ': 'mz',  # Mozambique
        
        # N
        'NA': 'wa',  # Namibia
        'NC': 'nc',  # New Caledonia
        'NE': 'ng',  # Niger
        'NF': 'nf',  # Norfolk Island
        'NG': 'ni',  # Nigeria
        'NI': 'nu',  # Nicaragua
        'NL': 'nl',  # Netherlands
        'NO': 'no',  # Norway
        'NP': 'np',  # Nepal
        'NR': 'nr',  # Nauru
        'NU': 'ne',  # Niue
        'NZ': 'nz',  # New Zealand
        
        # O
        'OM': 'mu',  # Oman
        
        # P
        'PA': 'pm',  # Panama
        'PE': 'pe',  # Peru
        'PF': 'fp',  # French Polynesia
        'PG': 'pp',  # Papua New Guinea
        'PH': 'rp',  # Philippines
        'PK': 'pk',  # Pakistan
        'PL': 'pl',  # Poland
        'PM': 'sb',  # Saint Pierre and Miquelon
        'PN': 'pc',  # Pitcairn
        'PR': 'rq',  # Puerto Rico
        'PS': 'gz',  # Palestine (Gaza Strip)
        'PT': 'po',  # Portugal
        'PW': 'ps',  # Palau
        'PY': 'pa',  # Paraguay
        
        # Q
        'QA': 'qa',  # Qatar
        
        # R
        'RE': 're',  # Réunion
        'RO': 'ro',  # Romania
        'RS': 'ri',  # Serbia
        'RU': 'rs',  # Russia
        'RW': 'rw',  # Rwanda
        
        # S
        'SA': 'sa',  # Saudi Arabia
        'SB': 'bp',  # Solomon Islands
        'SC': 'se',  # Seychelles
        'SD': 'su',  # Sudan
        'SE': 'sw',  # Sweden
        'SG': 'sn',  # Singapore
        'SH': 'sh',  # Saint Helena
        'SI': 'si',  # Slovenia
        'SJ': 'sv',  # Svalbard and Jan Mayen
        'SK': 'lo',  # Slovakia
        'SL': 'sl',  # Sierra Leone
        'SM': 'sm',  # San Marino
        'SN': 'sg',  # Senegal
        'SO': 'so',  # Somalia
        'SR': 'ns',  # Suriname
        'SS': 'od',  # South Sudan
        'ST': 'tp',  # São Tomé and Príncipe
        'SV': 'es',  # El Salvador
        'SX': 'nn',  # Sint Maarten
        'SY': 'sy',  # Syria
        'SZ': 'wz',  # Eswatini (Swaziland)
        
        # T
        'TC': 'tk',  # Turks and Caicos Islands
        'TD': 'cd',  # Chad
        'TF': 'fs',  # French Southern Territories
        'TG': 'to',  # Togo
        'TH': 'th',  # Thailand
        'TJ': 'ti',  # Tajikistan
        'TK': 'tl',  # Tokelau
        'TL': 'tt',  # Timor-Leste
        'TM': 'tx',  # Turkmenistan
        'TN': 'ts',  # Tunisia
        'TO': 'tn',  # Tonga
        'TR': 'tu',  # Turkey
        'TT': 'td',  # Trinidad and Tobago
        'TV': 'tv',  # Tuvalu
        'TW': 'tw',  # Taiwan
        'TZ': 'tz',  # Tanzania
        
        # U
        'UA': 'up',  # Ukraine
        'UG': 'ug',  # Uganda
        'UM': 'um',  # United States Minor Outlying Islands
        'US': 'us',  # United States
        'UY': 'uy',  # Uruguay
        'UZ': 'uz',  # Uzbekistan
        
        # V
        'VA': 'vt',  # Vatican City
        'VC': 'vc',  # Saint Vincent and the Grenadines
        'VE': 've',  # Venezuela
        'VG': 'vi',  # British Virgin Islands
        'VI': 'vq',  # US Virgin Islands
        'VN': 'vm',  # Vietnam
        'VU': 'nh',  # Vanuatu
        
        # W
        'WF': 'wf',  # Wallis and Futuna
        'WS': 'ws',  # Samoa
        
        # Y
        'YE': 'ym',  # Yemen
        'YT': 'mf',  # Mayotte
        
        # Z
        'ZA': 'sf',  # South Africa
        'ZM': 'za',  # Zambia
        'ZW': 'zi',  # Zimbabwe
    }
    
    # Reverse mapping: GEC -> ISO 3166-1 alpha-2
    GEC_TO_ISO = {v: k for k, v in ISO_TO_GEC.items()}
    
    # Common country name mappings to ISO codes
    NAME_TO_ISO = {
        # Common names and variations
        'united states': 'US',
        'usa': 'US',
        'america': 'US',
        'united kingdom': 'GB',
        'uk': 'GB',
        'britain': 'GB',
        'england': 'GB',
        'germany': 'DE',
        'france': 'FR',
        'italy': 'IT',
        'spain': 'ES',
        'russia': 'RU',
        'china': 'CN',
        'japan': 'JP',
        'south korea': 'KR',
        'north korea': 'KP',
        'india': 'IN',
        'brazil': 'BR',
        'canada': 'CA',
        'australia': 'AU',
        'south africa': 'ZA',
        'nigeria': 'NG',
        'egypt': 'EG',
        'mexico': 'MX',
        'argentina': 'AR',
        'chile': 'CL',
        'colombia': 'CO',
        'venezuela': 'VE',
        'peru': 'PE',
        'ecuador': 'EC',
        'bolivia': 'BO',
        'uruguay': 'UY',
        'paraguay': 'PY',
        'guyana': 'GY',
        'suriname': 'SR',
        'netherlands': 'NL',
        'belgium': 'BE',
        'switzerland': 'CH',
        'austria': 'AT',
        'poland': 'PL',
        'czech republic': 'CZ',
        'slovakia': 'SK',
        'hungary': 'HU',
        'romania': 'RO',
        'bulgaria': 'BG',
        'greece': 'GR',
        'turkey': 'TR',
        'ukraine': 'UA',
        'belarus': 'BY',
        'lithuania': 'LT',
        'latvia': 'LV',
        'estonia': 'EE',
        'finland': 'FI',
        'sweden': 'SE',
        'norway': 'NO',
        'denmark': 'DK',
        'iceland': 'IS',
        'ireland': 'IE',
        'portugal': 'PT',
        'morocco': 'MA',
        'algeria': 'DZ',
        'tunisia': 'TN',
        'libya': 'LY',
        'sudan': 'SD',
        'ethiopia': 'ET',
        'kenya': 'KE',
        'tanzania': 'TZ',
        'uganda': 'UG',
        'rwanda': 'RW',
        'burundi': 'BI',
        'congo': 'CG',
        'democratic republic of congo': 'CD',
        'central african republic': 'CF',
        'chad': 'TD',
        'cameroon': 'CM',
        'gabon': 'GA',
        'equatorial guinea': 'GQ',
        'sao tome and principe': 'ST',
        'cape verde': 'CV',
        'senegal': 'SN',
        'gambia': 'GM',
        'guinea bissau': 'GW',
        'guinea': 'GN',
        'sierra leone': 'SL',
        'liberia': 'LR',
        'ivory coast': 'CI',
        'cote divoire': 'CI',
        'ghana': 'GH',
        'togo': 'TG',
        'benin': 'BJ',
        'burkina faso': 'BF',
        'mali': 'ML',
        'niger': 'NE',
        'mauritania': 'MR',
        'western sahara': 'EH',
        'zambia': 'ZM',
        'zimbabwe': 'ZW',
        'botswana': 'BW',
        'namibia': 'NA',
        'angola': 'AO',
        'mozambique': 'MZ',
        'malawi': 'MW',
        'madagascar': 'MG',
        'mauritius': 'MU',
        'seychelles': 'SC',
        'comoros': 'KM',
        'djibouti': 'DJ',
        'eritrea': 'ER',
        'somalia': 'SO',
        'israel': 'IL',
        'palestine': 'PS',
        'lebanon': 'LB',
        'syria': 'SY',
        'jordan': 'JO',
        'iraq': 'IQ',
        'iran': 'IR',
        'afghanistan': 'AF',
        'pakistan': 'PK',
        'bangladesh': 'BD',
        'sri lanka': 'LK',
        'maldives': 'MV',
        'nepal': 'NP',
        'bhutan': 'BT',
        'myanmar': 'MM',
        'burma': 'MM',
        'thailand': 'TH',
        'laos': 'LA',
        'vietnam': 'VN',
        'cambodia': 'KH',
        'malaysia': 'MY',
        'singapore': 'SG',
        'brunei': 'BN',
        'indonesia': 'ID',
        'philippines': 'PH',
        'taiwan': 'TW',
        'mongolia': 'MN',
        'kazakhstan': 'KZ',
        'uzbekistan': 'UZ',
        'turkmenistan': 'TM',
        'kyrgyzstan': 'KG',
        'tajikistan': 'TJ',
        'armenia': 'AM',
        'azerbaijan': 'AZ',
        'georgia': 'GE',
        'saudi arabia': 'SA',
        'yemen': 'YE',
        'oman': 'OM',
        'united arab emirates': 'AE',
        'uae': 'AE',
        'qatar': 'QA',
        'bahrain': 'BH',
        'kuwait': 'KW',
        'new zealand': 'NZ',
        'fiji': 'FJ',
        'papua new guinea': 'PG',
        'solomon islands': 'SB',
        'vanuatu': 'VU',
        'new caledonia': 'NC',
        'french polynesia': 'PF',
        'samoa': 'WS',
        'tonga': 'TO',
        'kiribati': 'KI',
        'tuvalu': 'TV',
        'nauru': 'NR',
        'palau': 'PW',
        'marshall islands': 'MH',
        'micronesia': 'FM',
    }
    
    @classmethod
    def iso_to_gec(cls, iso_code: str) -> Optional[str]:
        """
        Convert ISO 3166-1 alpha-2 code to GEC code.
        
        Args:
            iso_code: ISO 3166-1 alpha-2 code (e.g., 'US', 'DE')
            
        Returns:
            GEC code (e.g., 'us', 'gm') or None if not found
        """
        return cls.ISO_TO_GEC.get(iso_code.upper())
    
    @classmethod
    def gec_to_iso(cls, gec_code: str) -> Optional[str]:
        """
        Convert GEC code to ISO 3166-1 alpha-2 code.
        
        Args:
            gec_code: GEC code (e.g., 'us', 'gm')
            
        Returns:
            ISO 3166-1 alpha-2 code (e.g., 'US', 'DE') or None if not found
        """
        return cls.GEC_TO_ISO.get(gec_code.lower())
    
    @classmethod
    def name_to_iso(cls, country_name: str) -> Optional[str]:
        """
        Convert country name to ISO 3166-1 alpha-2 code.
        
        Args:
            country_name: Country name (e.g., 'United States', 'Germany')
            
        Returns:
            ISO 3166-1 alpha-2 code or None if not found
        """
        clean_name = country_name.lower().strip()
        return cls.NAME_TO_ISO.get(clean_name)
    
    @classmethod
    def name_to_gec(cls, country_name: str) -> Optional[str]:
        """
        Convert country name to GEC code.
        
        Args:
            country_name: Country name (e.g., 'United States', 'Germany')
            
        Returns:
            GEC code or None if not found
        """
        iso_code = cls.name_to_iso(country_name)
        if iso_code:
            return cls.iso_to_gec(iso_code)
        return None
    
    @classmethod
    def resolve_country_code(cls, identifier: str) -> Optional[str]:
        """
        Resolve any country identifier to GEC code.
        
        Args:
            identifier: Country code (ISO or GEC) or country name
            
        Returns:
            GEC code or None if not found
        """
        identifier = identifier.strip()
        
        # If it's already a 2-letter lowercase code, assume it's GEC
        if len(identifier) == 2 and identifier.islower():
            return identifier if identifier in cls.GEC_TO_ISO else None
        
        # If it's a 2-letter uppercase code, assume it's ISO
        if len(identifier) == 2 and identifier.isupper():
            return cls.iso_to_gec(identifier)
        
        # Try as country name
        return cls.name_to_gec(identifier)
    
    @classmethod
    def get_country_info(cls, identifier: str) -> Optional[Dict[str, str]]:
        """
        Get comprehensive country code information.
        
        Args:
            identifier: Country code or name
            
        Returns:
            Dictionary with ISO, GEC, and name information
        """
        gec_code = cls.resolve_country_code(identifier)
        if not gec_code:
            return None
        
        iso_code = cls.gec_to_iso(gec_code)
        
        # Find country name from reverse lookup
        country_name = None
        for name, iso in cls.NAME_TO_ISO.items():
            if iso == iso_code:
                country_name = name.title()
                break
        
        return {
            'gec_code': gec_code,
            'iso_code': iso_code,
            'name': country_name
        }
    
    @classmethod
    def list_all_countries(cls) -> List[Tuple[str, str, str]]:
        """
        List all countries with their codes.
        
        Returns:
            List of tuples (ISO code, GEC code, name)
        """
        countries = []
        for iso_code, gec_code in cls.ISO_TO_GEC.items():
            # Find a name for this country
            country_name = None
            for name, iso in cls.NAME_TO_ISO.items():
                if iso == iso_code:
                    country_name = name.title()
                    break
            
            if not country_name:
                country_name = f"Country {iso_code}"
            
            countries.append((iso_code, gec_code, country_name))
        
        return sorted(countries, key=lambda x: x[2])  # Sort by name