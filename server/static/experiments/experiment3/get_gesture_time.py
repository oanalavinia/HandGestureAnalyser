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
gesture_times = ['1623600034006', '1623600037111', '1623600041389', '1623600045723', '1623600049092',
                 '1623600054347', '1623600057985', '1623600061965', '1623600065372', '1623600069315',
                 '1623600073444', '1623600077620', '1623600082069', '1623600087419', '1623600091419',
                 '1623600095744', '1623600099859', '1623600104185', '1623600108062', '1623600112125',
                 '1623600116512', '1623600120832', '1623600125006', '1623600129114', '1623600134059']
gesture_names = ['thumbsDown', 'thumbsDown', 'thumbsDown', 'thumbsDown', 'thumbsUp',
                 'thumbsUp', 'thumbsDown', 'thumbsDown', 'thumbsDown', 'thumbsDown',
                 'thumbsDown', 'thumbsUp', 'thumbsUp', 'thumbsUp', 'thumbsDown',
                 'thumbsDown', 'thumbsUp', 'thumbsUp', 'thumbsDown', 'thumbsDown',
                 'thumbsDown', 'thumbsDown', 'thumbsDown', 'thumbsUp', 'thumbsUp']
get_result(gesture_times, gesture_names)


print("\nImage")
gesture_times = ['1623600406028', '1623600410476', '1623600414145', '1623600417468', '1623600420763',
                 '1623600424221', '1623600440986',
                 '1623600444255', '1623600447238', '1623600451050', '1623600453881', '1623600457281', '1623600461298',
                 '1623600464757', '1623600468628', '1623600472288', '1623600476264', '1623600480133',
                 '1623600483679', '1623600486908', '1623600490363', '1623600494110']
gesture_names = ['zoomOut', 'zoomOut', 'zoomOut', 'zoomOut', 'zoomOut',
                 'zoomOut',  'zoomIn',
                 'zoomIn', 'zoomIn', 'zoomIn', 'zoomOut', 'zoomOut',
                 'zoomIn', 'zoomOut', 'zoomIn', 'zoomIn', 'zoomOut',
                 'zoomIn', 'zoomOut', 'zoomOut', 'zoomOut', 'zoomIn']
get_result(gesture_times, gesture_names)


print("\nQuiz")
gesture_times = ['1623599414636', '1623599424229', '1623599433745',
                 '1623599453569', '1623599463768',
                 '1623599489488', '1623599499680', '1623599509461',
                 '1623599528895', '1623599540566', '1623599548377',
                 '1623599567100', '1623599575661', '1623599583813']
gesture_names = ['thumbsDown', 'thumbsUp', 'thumbsUp',
                 'thumbsUp', 'thumbsUp',
                 'thumbsDown', 'thumbsDown', 'thumbsDown',
                 'thumbsUp', 'thumbsUp', 'thumbsUp',
                 'thumbsDown', 'thumbsUp', 'thumbsUp']
get_result(gesture_times, gesture_names)


print("\nMark")
gesture_times = ['1623599221990',
                 '1623599242416',
                 '1623599258171',
                 '1623599275852',
                 '1623599292421']
gesture_names = ['three',
                 'five',
                 'four',
                 'five',
                 'two']
get_result(gesture_times, gesture_names)
