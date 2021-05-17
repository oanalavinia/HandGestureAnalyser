from owl import ontology_manipulations as owl
from datetime import datetime


class Owl_utilities(object):
    def __init__(self):
        self.to_process = []

    def save_data(self):
        print("saving data..")
        with open("../rdf_data/test.xml", 'wb') as f:
            owl.fiiGezr.save(file=f, format="rdfxml")

    def get_gesture_instance(self, gesture):
        if gesture == 'wave':
            return owl.WaveDetected()
        elif gesture == 'thumbsUp':
            return owl.ThumbsUp()
        elif gesture == 'thumbsDown':
            return owl.ThumbsDown()
        elif gesture == 'one':
            return owl.OneFingerDetected()
        elif gesture == 'two':
            return owl.TwoFingersDetected()
        # elif gesture == 'peace':
        #     return owl.Peace()
        elif gesture == 'three':
            return owl.ThreeFingersDetected()
        elif gesture == 'four':
            return owl.FourFingersDetected()
        elif gesture == 'five':
            return owl.FiveFingersDetected()
        elif gesture == 'fist':
            return owl.FistDetected()
        elif gesture == 'zoomOut':
            return owl.CloseFingersDetected()
        elif gesture == 'zoomIn':
            return owl.ApartFingersDetected()
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
            rule = owl.NextPage()
        elif context == "PDFDocument" and gesture == "four":
            rule = owl.PreviousPage()
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
            rule = self.get_mark_rule(gesture)

        if rule is not None:
            # The inverse has_context is automatically inferred from rule.
            owl_context.includes_rule.append(rule)
            # rule.has_context.append(owl_context)
            rule.has_rule_time = datetime.now()
            self.save_data()

    def get_mark_rule(self, gesture):
        if gesture == "one":
            return owl.ChooseFirst()
        elif gesture == "two":
            return owl.ChooseSecond()
        elif gesture == "three":
            return owl.ChooseThird()
        elif gesture == "four":
            return owl.ChooseFourth()
        elif gesture == "five":
            return owl.ChooseFifth()
