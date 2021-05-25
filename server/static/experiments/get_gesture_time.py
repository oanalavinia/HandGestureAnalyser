import rdflib
import datetime
from statistics import mean, median


def get_gesture_time(start_time_str, gesture_name):
    date_format = '%Y-%m-%dT%H:%M:%S.%f'
    start_time = datetime.datetime.fromtimestamp(int(start_time_str) / 1000)
    # print(datetime.datetime.strptime('2021-05-23T18:29:28.765696', 'YYYY-mm-ddTHH:MM:SS.mmmmmm'))
    # print(datetime.datetime.strptime('2021-05-23T18:29:28.765696', '%Y-%m-%dT%H:%M:%S.%f'))
    # gesture_time = datetime.datetime.strptime('2021-05-23T20:09:24.947000', date_format)

    # gesture_name = 'thumbsUp'
    # gesture_name = 'thumbsDown'
    # gesture_name = "two"
    # print(start_time)
    # print(gesture_time)
    # # print((gesture_time-start_time).microseconds)
    # print((gesture_time-start_time).total_seconds())


    g = rdflib.Graph()
    f = open("../experiments/experiment_1/data.xml", "r")
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
gesture_times = ['1621870302802', '1621870307166', '1621870310882', '1621870314950', '1621870318358',
                 '1621871798512', '1621871802627', '1621871809404', '1621871815954', '1621871820875',
                 '1621871874201', '1621871878181', '1621871882188', '1621871885315', '1621871888604',
                 '1621871921979', '1621871926362', '1621871929205', '1621871931718', '1621871935103',
                 '1621872004544', '1621872007423', '1621872010483', '1621872013151', '1621872018847']
gesture_names = ['thumbsDown', 'thumbsDown', 'thumbsUp', 'thumbsDown', 'thumbsUp',
                 'thumbsDown', 'thumbsDown', 'thumbsUp', 'thumbsUp', 'thumbsUp',
                 'thumbsUp', 'thumbsUp', 'thumbsDown', 'thumbsUp', 'thumbsDown',
                 'thumbsDown', 'thumbsUp', 'thumbsDown', 'thumbsUp', 'thumbsDown',
                 'thumbsUp', 'thumbsDown', 'thumbsDown', 'thumbsUp', 'thumbsDown']
get_result(gesture_times, gesture_names)


print("\nImage")
gesture_times = ['1621877307740', '1621877314554', '1621877325998', '1621877330428', '1621877334220',
                 '1621877462294', '1621877465943', '1621877469067', '1621877472434', '1621877475357',
                 '1621877497673', '1621877499814', '1621877505197', '1621877507155', '1621877509691',
                 '1621877608778', '1621877610613', '1621877613105', '1621877615872', '1621877618158',
                 '1621877635643', '1621877637875', '1621877640421', '1621877642903', '1621877645123']
gesture_names = ['zoomIn', 'zoomOut', 'zoomOut', 'zoomIn', 'zoomOut',
                 'zoomOut', 'zoomOut', 'zoomIn', 'zoomIn', 'zoomOut',
                 'zoomIn', 'zoomOut', 'zoomIn', 'zoomOut', 'zoomIn',
                 'zoomIn', 'zoomIn', 'zoomIn', 'zoomOut', 'zoomIn',
                 'zoomOut', 'zoomOut', 'zoomIn', 'zoomOut', 'zoomOut']
get_result(gesture_times, gesture_names)


print("\nQuiz")
gesture_times = ['1621878874614', '1621878893905',
                 '1621878956071', '1621878965222', '1621878975188',
                 '1621879007628', '1621879015679', '1621879026386',
                 '1621879070748', '1621879079854', '1621879091609',
                 '1621879152177']
gesture_names = ['thumbsUp', 'thumbsUp',
                 'thumbsUp', 'thumbsUp', 'thumbsDown',
                 'thumbsDown', 'thumbsDown', 'thumbsDown',
                 'thumbsDown', 'thumbsUp', 'thumbsDown',
                 'thumbsUp']
get_result(gesture_times, gesture_names)


print("\nMark")
results = [0.737755, 2.718692, 2.54402, 1.228743, 1.273534]
print("Min ")
print(min(results))
print("Max ")
print(max(results))
print("Mean ")
print(mean(results))
print("Median ")
print(median(results))
# print(mean([0.737755, 2.718692, 2.54402, 1.228743, 1.273534]))