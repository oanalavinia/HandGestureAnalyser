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


# print("\nFile")
# gesture_times = ['1623857589112', '1623857593743', '1623857597248', '1623857600612', '1623857604403',
#                  '1623857607953', '1623857611634', '1623857615196', '1623857618426', '1623857621943',
#                  '1623857625759', '1623857629385', '1623857632408', '1623857635705', '1623857638896',
#                  '1623857642068', '1623857645697', '1623857649090', '1623857652038', '1623857655793',
#                  '1623857659111', '1623857662510', '1623857666124', '1623857669662', '1623857673219']
# gesture_names = ['thumbsDown', 'thumbsDown', 'thumbsDown', 'thumbsUp', 'thumbsDown',
#                  'thumbsUp', 'thumbsDown', 'thumbsDown', 'thumbsDown', 'thumbsDown',
#                  'thumbsUp', 'thumbsUp', 'thumbsDown', 'thumbsDown', 'thumbsUp',
#                  'thumbsUp', 'thumbsUp', 'thumbsUp', 'thumbsDown', 'thumbsDown',
#                  'thumbsUp', 'thumbsDown', 'thumbsUp', 'thumbsDown', 'thumbsUp']
# get_result(gesture_times, gesture_names)
#
#
# print("\nImage")
# gesture_times = ['1623857913758', '1623857917620', '1623857921022', '1623857924457', '1623857927829',
#                  '1623857931087', '1623857934364', '1623857937621', '1623857941039', '1623857944409',
#                  '1623857947701', '1623857950882', '1623857953529', '1623857956573', '1623857960193',
#                  '1623857963218', '1623857966326', '1623857969063', '1623857971563', '1623857974775',
#                  '1623857977580', '1623857980848', '1623857983568', '1623857987876', '1623857990886']
# gesture_names = ['zoomIn', 'zoomIn', 'zoomOut', 'zoomIn', 'zoomIn',
#                  'zoomOut',  'zoomOut', 'zoomOut', 'zoomIn', 'zoomIn',
#                  'zoomIn', 'zoomOut', 'zoomOut', 'zoomIn', 'zoomOut',
#                  'zoomIn', 'zoomIn', 'zoomIn', 'zoomIn', 'zoomIn',
#                  'zoomOut', 'zoomOut', 'zoomOut', 'zoomIn', 'zoomIn']
# get_result(gesture_times, gesture_names)
#
#
# print("\nQuiz")
# gesture_times = ['1623856869572', '1623856878846', '1623856890899',
#                  '1623856916219', '1623856922668', '1623856932612',
#                  '1623856952081', '1623856959199', '1623856972367',
#                  '1623856993965', '1623857000333', '1623857013408',
#                  '1623857034832', '1623857044407', '1623857056971']
# gesture_names = ['thumbsDown', 'thumbsUp', 'thumbsUp',
#                  'thumbsUp', 'thumbsUp', 'thumbsDown',
#                  'thumbsUp', 'thumbsDown', 'thumbsUp',
#                  'thumbsDown', 'thumbsUp', 'thumbsDown',
#                  'thumbsUp', 'thumbsDown', 'thumbsUp']
# get_result(gesture_times, gesture_names)
#
#
# print("\nMark")
# gesture_times = ['1623857300662',
#                  '1623857335271',
#                  '1623857351481',
#                  '1623857368261']
# gesture_names = ['five',
#                  'four',
#                  'five',
#                  'two']
# get_result(gesture_times, gesture_names)


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

print(len(gesture_times))
print(len(gesture_names))
get_result(gesture_times, gesture_names)

