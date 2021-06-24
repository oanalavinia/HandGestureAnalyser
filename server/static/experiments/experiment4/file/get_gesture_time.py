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


print("\nFile exp4")
gesture_times = ['1623859787611', '1623859792211', '1623859796169', '1623859800052', '1623859804668',
                 '1623859808958', '1623859814061', '1623859817651', '1623859821574', '1623859825572',
                 '1623859833393', '1623859838358', '1623859842786', '1623859846899', '1623859850496',
                 '1623859855082', '1623859858850', '1623859863181', '1623859867736', '1623859872782',
                 '1623859876745', '1623859889360', '1623859894730', '1623859900447', '1623859904929']
gesture_names = ['thumbsDown', 'thumbsDown', 'thumbsDown', 'thumbsDown', 'thumbsDown',
                 'thumbsUp', 'thumbsDown', 'thumbsDown', 'thumbsDown', 'thumbsDown',
                 'thumbsUp', 'thumbsDown', 'thumbsDown', 'thumbsDown', 'thumbsDown',
                 'thumbsDown', 'thumbsDown', 'thumbsUp', 'thumbsDown', 'thumbsDown',
                 'thumbsDown', 'thumbsDown', 'thumbsUp', 'thumbsUp', 'thumbsUp']

get_result(gesture_times, gesture_names)

