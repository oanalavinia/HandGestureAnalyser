import rdflib
import datetime
import re
from get_gestures_from_webcam import utilities


def get_gesture(results):
    pt = re.compile("http://fiigezr.org/fiiGezr.owl#([a-z]*)\d{2}")
    gestures = []
    for result in results:
        res = pt.search(result)
        if res.group(1) is not None:
            gestures.append(res.group(1))

    return gestures


def query_answers(answer_time, end_answer_time):
    g = rdflib.Graph()
    g.parse("../rdf_data/test.xml")

    query_str = """
           PREFIX gezr: <http://fiigezr.org/fiiGezr.owl#>
           SELECT ?x
           WHERE {
              ?x rdf:type/rdfs:subClassOf* gezr:Gesture .
              ?x gezr:has_gesture_time ?data .
              FILTER (?data > '""" + answer_time.strftime("%Y-%m-%dT%H:%M:%S.%f") + """'^^xsd:dateTime
              && ?data < '""" + end_answer_time.strftime("%Y-%m-%dT%H:%M:%S.%f") + """'^^xsd:dateTime)
           }"""
    qres = g.query(query_str)

    results = []
    for row in qres:
        results.append(row.asdict()['x'])

    gestures = get_gesture(results)
    if len(gestures) > 0:
        return utilities.most_frequent(gestures)
    else:
        return []


# For testing a specific time, not to be deleted
# answer_time = datetime.datetime.fromtimestamp(int(1611686427))
# print(answer_time)
# end_answer_time = answer_time + datetime.timedelta(0, 20)
# query_answers(answer_time, end_answer_time)
