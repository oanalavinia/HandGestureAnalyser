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
    # i = 0
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
gesture_times = ['1624196376775', '1624196379399', '1624196382391', '1624196385026', '1624196387779',
                 '1624196393000', '1624196395783', '1624196398716', '1624196401728', '1624196404661',
                 '1624196407518', '1624196412749', '1624196415492', '1624196418406', '1624196421777',
                 '1624196424519', '1624196427560', '1624196430894', '1624196436019', '1624196439101',
                 '1624196442257', '1624196445768', '1624196448884', '1624196451968', '1624196454940']
gesture_names = ['thumbsDown', 'thumbsDown', 'thumbsDown', 'thumbsUp', 'thumbsUp',
                 'thumbsDown', 'thumbsDown', 'thumbsDown', 'thumbsDown', 'thumbsDown',
                 'thumbsUp', 'thumbsUp', 'thumbsUp', 'thumbsUp', 'thumbsDown',
                 'thumbsUp', 'thumbsUp', 'thumbsDown', 'thumbsDown', 'thumbsUp',
                 'thumbsUp', 'thumbsUp', 'thumbsDown', 'thumbsDown', 'thumbsUp']
get_result(gesture_times, gesture_names)


print("\nImage")
gesture_times = ['1624196176217', '1624196178901', '1624196182134', '1624196184828', '1624196187741',
                 '1624196190892', '1624196193725', '1624196196592', '1624196199531', '1624196202627',
                 '1624196205526', '1624196208821', '1624196212332', '1624196215329', '1624196218420',
                 '1624196221163', '1624196224122', '1624196227253', '1624196230740', '1624196236158',
                 '1624196241768', '1624196244720', '1624196247714', '1624196250808', '1624196253437']
gesture_names = ['zoomIn', 'zoomIn', 'zoomOut', 'zoomOut', 'zoomOut',
                 'zoomOut',  'zoomOut', 'zoomIn', 'zoomIn', 'zoomIn',
                 'zoomOut', 'zoomIn', 'zoomOut', 'zoomOut', 'zoomOut',
                 'zoomOut', 'zoomIn', 'zoomIn', 'zoomOut', 'zoomOut',
                 'zoomIn', 'zoomIn', 'zoomIn', 'zoomOut', 'zoomOut']
get_result(gesture_times, gesture_names)


print("\nQuiz")
gesture_times = ['1624195746110', '1624195756282', '1624195765644',
                 '1624195785165', '1624195804277',
                 '1624195825972', '1624195836684', '1624195844545',
                 '1624195869114', '1624195875173', '1624195884455',
                 '1624195912661', '1624195923065']
gesture_names = ['thumbsUp', 'thumbsUp', 'thumbsDown',
                 'thumbsDown', 'thumbsUp',
                 'thumbsUp', 'thumbsDown', 'thumbsDown',
                 'thumbsDown', 'thumbsDown', 'thumbsUp',
                 'thumbsUp', 'thumbsDown']
print(len(gesture_times))
print(len(gesture_names))
get_result(gesture_times, gesture_names)


print("\nMark")
gesture_times = ['1624195040798',
                 '1624195058568',
                 '1624195075571',
                 '1624195097708',
                 '1624195122057']
gesture_names = ['five',
                 'two',
                 'three',
                 'one',
                 'two']
get_result(gesture_times, gesture_names)


