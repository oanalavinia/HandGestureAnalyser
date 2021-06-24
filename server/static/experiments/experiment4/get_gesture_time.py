import rdflib
import datetime
from statistics import mean, median


def get_gesture_time(start_time_str, gesture_name):
    date_format = '%Y-%m-%dT%H:%M:%S.%f'
    start_time = datetime.datetime.fromtimestamp(int(start_time_str) / 1000)

    g = rdflib.Graph()
    f = open("test.xml", "r")
    g.parse(f, format="application/rdf+xml")
    f.close()

    query_str = """
           PREFIX gezr: <http://fiigezr.org/fiiGezr.owl#>
           SELECT ?x ?name ?time
           WHERE {
              ?x rdf:type/rdfs:subClassOf* gezr:Gesture .
              ?x gezr:hasGestureTime ?time .
              ?x gezr:hasGestureName ?name .
              FILTER (?time > '""" + start_time.strftime("%Y-%m-%dT%H:%M:%S.%f") + """'^^xsd:dateTime
              && regex(?name, '""" + gesture_name + """', "i"))
           }
           ORDER BY ASC(?time)
           LIMIT 1
           """
    qres = g.query(query_str)

    gestures = []
    for row in qres:
        gestures.append(str(row.asdict()['time']))

    # print(gestures)
    gesture_time = datetime.datetime.strptime(gestures[0], date_format)

    return (gesture_time-start_time).total_seconds()


def get_result(gesture_times, gesture_names):
    i = 0
    results = []
    for i in range(len(gesture_times)):
        # print(i)
        results.append(get_gesture_time(gesture_times[i], gesture_names[i]))

    print(results)
    print("Min ")
    print(min(results))
    print("Max ")
    print(max(results))
    print("Mean ")
    print(mean(results))
    print("Median ")
    print(median(results))


print("\nFile")
gesture_times = ['1623840933588', '1623840938188', '1623840940000', '1623840957185',
                 '1623840967858', '1623840975773', '1623840978133', '1623840982887',
                 '1623840986178', '1623840996175', '1623841001623', '1623841005838', '1623841010704',
                 '1623841017517', '1623841023019', '1623841030334', '1623841034513', '1623841038277',
                 '1623841041736', '1623841046013', '1623841050649', '1623841054637', '1623841058634', '1623841063751', '1623841068506']
gesture_names = ['thumbsDown', 'thumbsDown', 'thumbsDown', 'thumbsDown', 'thumbsDown',
                 'thumbsUp', 'thumbsUp', 'thumbsDown', 'thumbsDown', 'thumbsDown',
                 'thumbsDown', 'thumbsDown', 'thumbsDown', 'thumbsDown', 'thumbsUp',
                 'thumbsDown', 'thumbsDown', 'thumbsDown', 'thumbsDown', 'thumbsDown',
                 'thumbsUp', 'thumbsUp', 'thumbsDown', 'thumbsDown', 'thumbsUp']
get_result(gesture_times, gesture_names)


print("\nImage")
gesture_times = ['1623841250661', '1623841254281', '1623841257430', '1623841261655', '1623841264892',
                 '1623841269528', '1623841274021', '1623841279413', '1623841283429', '1623841286620',
                 '1623841290103', '1623841293629', '1623841297145', '1623841301629',
                 '1623841320616', '1623841327227', '1623841331725',
                 '1623841337560', '1623841350073', '1623841354951']
gesture_names = ['zoomOut', 'zoomOut', 'zoomOut', 'zoomOut', 'zoomOut',
                 'zoomOut',  'zoomOut', 'zoomIn', 'zoomIn', 'zoomIn',
                 'zoomIn', 'zoomIn', 'zoomIn', 'zoomIn',
                 'zoomIn', 'zoomOut', 'zoomIn',
                 'zoomOut', 'zoomIn', 'zoomIn']
get_result(gesture_times, gesture_names)


print("\nQuiz")
gesture_times = ['1623840452982', '1623840462893', '1623840473617',
                 '1623840503592', '1623840511678', '1623840517283',
                 '1623840558336', '1623840565346', '1623840581102',
                 '1623840604802', '1623840616885', '1623840626317',
                 '1623840644731', '1623840659962', '1623840666834']
gesture_names = ['thumbsDown', 'thumbsUp', 'thumbsUp',
                 'thumbsUp', 'thumbsUp', 'thumbsUp',
                 'thumbsDown', 'thumbsDown', 'thumbsUp',
                 'thumbsUp', 'thumbsDown', 'thumbsUp',
                 'thumbsDown', 'thumbsUp', 'thumbsDown']
get_result(gesture_times, gesture_names)


print("\nMark")
gesture_times = ['1623840196048',
                 '1623840226741',
                 '1623840247125']
gesture_names = ['two',
                 'two',
                 'four']
get_result(gesture_times, gesture_names)
