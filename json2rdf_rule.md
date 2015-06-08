
### The definition of json data to rdf triple 
INPUT: doc
OUTPUT: triples

PREFIXES = {
    "food":"http://data.lirmm.fr/ontologies/#",
    "gr":"http://purl.org/goodrelations/v1#",
    "s":"http://http://schema.org/address",
    "foo":"http://exmaple.com"
    }

RULES = [
    {"[address]_address":
        "type":"s:PostalAddress",
        "s:streetAddress": address,
        "s:postalCode": "210012",
        "addressLocality": "南京, 江苏"
        }
    },
    {"_openhour": 
        {"type":"gr:OpeningHoursSpecification,
        "gr:opens":{"type_literal":("08:00:00","xsd:time")},
        "gr:closes":{"type_literal":("20:00:00","xsd:time")},
        "gr:hasOpeningHoursDayOfWeek":["gr:Monday", "gr:Tuesday", "gr:Wednesday", "gr:Thursday", "gr:Friday"]
        }
    },
    {"_location":
        {"type:"gr:Location",
        "s:address":address,
        "s:latitude":lat,
        "s:longtitude":lon,
        "gr:hasOpeningHoursSpecification":_openhour
        }
    },
    {name:
        {"type":"gr:BusinessEntity",
        "s:address":_location,
        "gr:name": {"plain_literal":[name, "zh-cn"]},
        "gr:hasPos
]


example:
    ?ls a s:PostalAdrress;
        s:streetAddress ?add;
        s:postalCode ?ptcd;
        s:addressLocality ?loc.

    ?s = `name` + '_location'
    ?add = `address`
    ?ptcd = '210012'
    ?addressLocality = "南京, 江苏"

    ?bs a gr:BusinessEntity;
        gr:name ?

