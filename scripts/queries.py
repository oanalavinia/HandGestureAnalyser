import rdflib
import datetime
from get_gestures_from_webcam import utilities
from get_gestures_from_webcam import get_gestures_from_webcam as gst_module
from owl_testing import test_owl as owl
import webbrowser


class Queries(object):
    def __init__(self, gestures_handler):
        self.gestures_handler = gestures_handler
        self.owl_utilities = self.gestures_handler.get_owl_utilities()

    def query_answers(self, answer_time, end_answer_time):
        g = rdflib.Graph()
        self.owl_utilities.save_data()
        f = open("../rdf_data/test.xml", "r")
        g.parse(f, format="application/rdf+xml")
        f.close()

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

    def query_movies(self, movie_time, end_movie_time):
        g = rdflib.Graph()
        self.owl_utilities.save_data()
        f = open("../rdf_data/test.xml", "r")
        g.parse(f, format="application/rdf+xml")
        f.close()

        query_str = """
               PREFIX gezr: <http://fiigezr.org/fiiGezr.owl#>
               SELECT ?x ?name
               WHERE {
                  ?x rdf:type/rdfs:subClassOf* gezr:Gesture .
                  ?x gezr:has_gesture_time ?data .
                  ?x gezr:has_gesture_name ?name .
                  FILTER (?data > '""" + movie_time.strftime("%Y-%m-%dT%H:%M:%S.%f") + """'^^xsd:dateTime
                  && ?data < '""" + end_movie_time.strftime("%Y-%m-%dT%H:%M:%S.%f") + """'^^xsd:dateTime)
               }"""
        qres = g.query(query_str)

        gestures = []
        for row in qres:
            gestures.append(str(row.asdict()['name']))

        if len(gestures) > 0:
            return utilities.most_frequent(gestures)
        else:
            return []

    def queryGesturesInSession(self, start_time):
        g = rdflib.Graph()
        f = open("../rdf_data/test.xml", "r")
        g.parse(f, format="application/rdf+xml")

        query_str = """
                   PREFIX gezr: <http://fiigezr.org/fiiGezr.owl#>
                   SELECT ?x ?name
                   WHERE {
                      ?x rdf:type/rdfs:subClassOf* gezr:Gesture .
                      ?x gezr:has_gesture_time ?data .
                      ?x gezr:has_gesture_name ?name .
                      FILTER (?data > '""" + start_time.strftime("%Y-%m-%dT%H:%M:%S.%f") + """'^^xsd:dateTime
                      && ?data < '""" + datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f") + """'^^xsd:dateTime)
                   }"""
        qres = g.query(query_str)

        gestures = []
        for row in qres:
            gestures.append(str(row.asdict()['name']))
        counts = dict()
        for gesture in gestures:
            counts[gesture] = counts.get(gesture, 0) + 1
        return counts

    def query_last_10s_gestures(self, current_time):
        start_time = current_time - datetime.timedelta(0, 10)
        # print("query last 10s gestures start time: {}".format(start_time))
        g = rdflib.Graph()
        gst_module.save_data()
        f = open("../rdf_data/test.xml", "r")
        g.parse(f, format="application/rdf+xml")
        f.close()
        query_str = """
                   PREFIX gezr: <http://fiigezr.org/fiiGezr.owl#>
                   SELECT ?x ?name (count(distinct ?x) as ?count)
                   WHERE {
                      ?x rdf:type/rdfs:subClassOf* gezr:Gesture .
                      ?x gezr:has_gesture_time ?data .
                      ?x gezr:has_gesture_name ?name .
                      FILTER (?data > '""" + start_time.strftime("%Y-%m-%dT%H:%M:%S.%f") + """'^^xsd:dateTime
                      && ?data < '""" + current_time.strftime("%Y-%m-%dT%H:%M:%S.%f") + """'^^xsd:dateTime)
                   }
                   GROUP BY ?name
                   ORDER BY DESC(?count)
                   """
        qres = g.query(query_str)

        gestures = []
        times = []
        instances = []
        for row in qres:
            # print("name '{}' count {} x {}".format(row.asdict()['name'], row.asdict()['count'], row.asdict()['x']))
            times.append(int(row.asdict()['count']))
            gestures.append(str(row.asdict()['name']))
            instances.append(row[0])

        print("found gestures: {} with times {}".format(gestures, times))

        if len(times) > 0 and len(gestures) > 0:
            if times[0] > 100 and gestures[0] == 'wave':
                self.create_close_camera_rule(g, gestures[0])
            elif times[0] > 100 and gestures[0] == 'five':
                self.create_open_browser_rule(g, gestures[0])

    def create_close_camera_rule(self, g, gesture):
        camera_rule = owl.CloseCamera()
        camera_rule.has_gesture.append(gesture)
        print("create close_camera rule {}".format(camera_rule))
        query_str = """
                        PREFIX gezr: <http://fiigezr.org/fiiGezr.owl#>
                        CONSTRUCT {
                          ?x gezr:causes_rule ?r
                        }
                        WHERE {
                          ?x rdf:type/rdfs:subClassOf* gezr:Gesture .
                          ?r rdf:type/rdfs:subClassOf* gezr:Rule .
                          ?x gezr:has_gesture_name ?name .
                          ?r gezr:has_gesture ?name .
                        }
                    """
        qres = g.query(query_str)
        for row in qres:
            # Create camera rule.
            camera_rule.has_rule_time.append(datetime.datetime.now())
            # print("wave '{}' prop {} rule {}".format(row[0], row[1], row[2]))
            # Get existing wave and bind it to the rule.
            # wave = owl.Wave(str(row[0])[31:])
            name = str(row[0])
            wave = owl.Wave('#' + name.split('#')[1])
            print(wave)
            wave.causes_rule.append(camera_rule)
            camera_rule.is_caused_by.append(wave)
            break

    def create_open_browser_rule(self, g, gesture):
        # Create browser rule.
        browser_rule = owl.OpenBrowser()
        browser_rule.has_gesture.append(gesture)
        print("create open_browser rule {}".format(browser_rule))
        # Query.
        query_str = """
                        PREFIX gezr: <http://fiigezr.org/fiiGezr.owl#>
                        CONSTRUCT {
                          ?x gezr:causes_rule ?r
                        }
                        WHERE {
                          ?x rdf:type/rdfs:subClassOf* gezr:Gesture .
                          ?r rdf:type/rdfs:subClassOf* gezr:Rule .
                          ?x gezr:has_gesture_name ?name .
                          ?r gezr:has_gesture ?name .
                        }
                    """
        qres = g.query(query_str)
        for row in qres:
            browser_rule.has_rule_time.append(datetime.datetime.now())
            # Get existing five and bind it to the rule.
            # five = owl.Five(str(row[0])[31:])
            name = str(row[0])
            five = owl.Five('#' + name.split('#')[1])
            print("open browser sesame {}".format(five))
            five.causes_rule.append(browser_rule)
            browser_rule.is_caused_by.append(five)

            webbrowser.open("https://google.com")
            break

    def check_close_camera(self, current_time):
        start_time = current_time - datetime.timedelta(0, 5)
        # print("check close camera rule start time: {}".format(start_time))
        g = rdflib.Graph()
        # gst_module.save_data()
        f = open("../rdf_data/test.xml", "r")
        g.parse(f, format="application/rdf+xml")
        f.close()
        query_str = """
                       PREFIX gezr: <http://fiigezr.org/fiiGezr.owl#>
                       SELECT (count(distinct ?r) as ?count)
                       WHERE {
                          ?r rdf:type/rdfs:subClassOf* gezr:Rule .
                          ?r gezr:has_rule_time ?data .
                          FILTER (?data > '""" + start_time.strftime("%Y-%m-%dT%H:%M:%S.%f") + """'^^xsd:dateTime
                          && ?data < '""" + current_time.strftime("%Y-%m-%dT%H:%M:%S.%f") + """'^^xsd:dateTime)
                       }
                       """
        qres = g.query(query_str)

        result = None
        for row in qres:
            result = int(row[0])
            break

        if result and result > 0:
            return True
        return False

# For testing a specific answer, not to be deleted.
# answer_time = datetime.datetime.fromtimestamp(int(1611686427))
# print(answer_time)
# end_answer_time = answer_time + datetime.timedelta(0, 20)
# query_answers(answer_time, end_answer_time)

# Testing last 10s gestures.
# answer_time = datetime.datetime.fromtimestamp(int(1611740765))
# print(answer_time)
# query_last_10s_gestures(answer_time)

# Testing last 10s gestures.
# answer_time = datetime.datetime.fromtimestamp(int(1611740765))
# date_time_str = '2020-01-27 08:15:27.243860'
# answer_time = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')
# print(answer_time)
# check_close_camera(answer_time)
