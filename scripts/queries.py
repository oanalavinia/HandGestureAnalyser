import rdflib


def query_answers(answer_time, end_answer_time):
    return
    # g = rdflib.Graph()
    # g.parse("rdf/test.xml")
    #
    # qres = g.query(
    #     """
    #        PREFIX gezr: <http://fiigezr.org/fiiGezr.owl#>
    #        SELECT *
    #        WHERE {
    #           ?x rdf:type gezr:Wave .
    #           ?x gezr:has_gesture_time ?data .
    #           FILTER (?data > "2021-01-27T00:52:49.609473"^^xsd:dateTime)
    #        }""")
    #
    # for row in qres:
    #     print(row)


# qres = g.query(
#         """
#            PREFIX gezr: <http://fiigezr.org/fiiGezr.owl#>
#            SELECT *
#            WHERE {
#               ?x rdf:type gezr:Wave .
#               ?x gezr:has_gesture_time ?data .
#               FILTER (?data > "2021-01-27T00:52:49.609473"^^xsd:dateTime)
#            }""")