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
gesture_times = ['1623594596468', '1623594600629', '1623594606675', '1623594608707', '1623594612921',
                 '1623594616774', '1623594620433', '1623594623399', '1623594627020', '1623594630933',
                 '1623594634517', '1623594638835', '1623594642658', '1623594646251', '1623594650469',
                 '1623594656981', '1623594662930', '1623594667118', '1623594671574', '1623594674353',
                 '1623594755562', '1623594759920', '1623594764102', '1623594768630', '1623594772678']
gesture_names = ['thumbsUp', 'thumbsDown', 'thumbsUp', 'thumbsUp', 'thumbsUp',
                 'thumbsDown', 'thumbsUp', 'thumbsDown', 'thumbsDown', 'thumbsDown',
                 'thumbsDown', 'thumbsUp', 'thumbsUp', 'thumbsUp', 'thumbsUp',
                 'thumbsDown', 'thumbsUp', 'thumbsUp', 'thumbsDown', 'thumbsDown',
                 'thumbsUp', 'thumbsDown', 'thumbsUp', 'thumbsDown', 'thumbsUp']
get_result(gesture_times, gesture_names)

#
print("\nImage")
gesture_times = ['1623595107553', '1623595130382', '1623595138447', '1623595154835',
                 '1623595159624', '1623595166368', '1623595183778', '1623595189298',
                 '1623595192491', '1623595203565', '1623595208501', '1623595220104',
                 '1623595226211', '1623595231524', '1623595239120', '1623595243566',
                 '1623595256514', '1623595260772', '1623595265834', '1623595270005', '1623595274614']
gesture_names = ['zoomIn', 'zoomIn', 'zoomOut', 'zoomIn',
                 'zoomOut', 'zoomOut', 'zoomIn', 'zoomOut',
                 'zoomIn', 'zoomOut', 'zoomOut', 'zoomIn',
                 'zoomOut', 'zoomIn', 'zoomIn', 'zoomOut',
                 'zoomOut', 'zoomIn', 'zoomOut', 'zoomOut', 'zoomIn']
get_result(gesture_times, gesture_names)
#

print("\nQuiz")
gesture_times = ['1623595900363', '1623595907811', '1623595919136',
                 '1623595945653', '1623595953227',
                 '1623595986727', '1623595995521', '1623596004357',
                 '1623596039581',
                 '1623596084257']
gesture_names = ['thumbsDown', 'thumbsUp', 'thumbsUp',
                 'thumbsUp', 'thumbsDown',
                 'thumbsUp', 'thumbsUp', 'thumbsUp',
                 'thumbsUp',
                 'thumbsUp']
get_result(gesture_times, gesture_names)


print("\nMark")
gesture_times = ['1623595618353',
                 '1623595674616',
                 '1623595695569',
                 '1623595715444']
gesture_names = ['two',
                 'five',
                 'one',
                 'four']
get_result(gesture_times, gesture_names)

# print("\nMark")
# results = [0.737755, 2.718692, 2.54402, 1.228743, 1.273534]
# print("Min ")
# print(min(results))
# print("Max ")
# print(max(results))
# print("Mean ")
# print(mean(results))
# print("Median ")
# print(median(results))
# print(mean([0.737755, 2.718692, 2.54402, 1.228743, 1.273534]))