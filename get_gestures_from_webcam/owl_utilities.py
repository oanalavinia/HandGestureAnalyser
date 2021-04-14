from owl_testing import test_owl as owl


class Owl_utilities(object):
    def __init__(self):
        self.to_process = []

    def save_data(self):
        # global record
        # if record is not None and record is True:
        print("saving data..")
        with open("../rdf_data/test.xml", 'wb') as f:
            owl.fiiGezr.save(file=f, format="rdfxml")

    def get_gesture_instance(self, gesture):
        if gesture == 'wave':
            return owl.Wave()
        elif gesture == 'thumbsUp':
            return owl.ThumbsUp()
        elif gesture == 'thumbsDown':
            return owl.ThumbsDown()
        elif gesture == 'one':
            return owl.One()
        elif gesture == 'two':
            return owl.Two()
        # elif gesture == 'peace':
        #     return owl.Peace()
        elif gesture == 'three':
            return owl.Three()
        elif gesture == 'four':
            return owl.Four()
        elif gesture == 'five':
            return owl.Five()
        elif gesture == 'fist':
            return owl.Fist()
        elif gesture == 'zoomIn':
            return owl.CloseFingers()
        elif gesture == 'zoomOut':
            return owl.ApartFingers()
        else:
            return None

    def get_contexted_rule(self, context, gesture, owl_context):
        if owl_context == 'none':
            return
        rule = None
        if context == "QuizGame" and gesture == "thumbsUp":
            rule = owl.Approve()
        elif context == "QuizGame" and gesture == "thumbsDown":
            rule = owl.Disapprove()
        elif context == "PDFDocument" and gesture == "wave":
            rule = owl.CloseFile()
        elif context == "PDFDocument" and gesture == "five":
            rule = owl.ChangePage()
        elif context == "Image" and gesture == "thumbsDown":
            rule = owl.Disapprove()
        elif context == "Image" and gesture == "five":
            rule = owl.NextImage()
        elif context == "Image" and gesture == "zoomIn":
            rule = owl.ZoomIn()
        elif context == "Image" and gesture == "zoomOut":
            rule = owl.ZoomOut()
        elif context == "MarkGame" and (
                gesture == "one" or gesture == "two" or gesture == "three" or gesture == "four" or gesture == "five"):
            rule = owl.ZoomOut()

        if rule is not None:
            owl_context.includes_rule.append(rule)
            rule.has_context.append(owl_context)
