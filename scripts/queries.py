import rdflib
import datetime
import re
from get_gestures_from_webcam import utilities


def query_answers(answer_time, end_answer_time):
    g = rdflib.Graph()
    g.parse("../rdf_data/test.xml")

    query_str = """
           PREFIX gezr: <http://fiigezr.org/fiiGezr.owl#>
           SELECT ?x ?name
           WHERE {
              ?x rdf:type/rdfs:subClassOf* gezr:Gesture .
              ?x gezr:has_gesture_time ?data .
              ?x gezr:has_gesture_name ?name .
              FILTER (?data > '""" + answer_time.strftime("%Y-%m-%dT%H:%M:%S.%f") + """'^^xsd:dateTime
              && ?data < '""" + end_answer_time.strftime("%Y-%m-%dT%H:%M:%S.%f") + """'^^xsd:dateTime)
           }"""
    qres = g.query(query_str)

    gestures = []
    for row in qres:
        gestures.append(str(row.asdict()['name']))

    if len(gestures) > 0:
        return utilities.most_frequent(gestures)
    else:
        return []


# For testing a specific time, not to be deleted
# answer_time = datetime.datetime.fromtimestamp(int(1611686427))
# print(answer_time)
# end_answer_time = answer_time + datetime.timedelta(0, 20)
# query_answers(answer_time, end_answer_time)
