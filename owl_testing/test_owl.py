from owlready2 import *

fiiGezr = get_ontology("http://fiigezr.org/fiiGezr.owl")

with fiiGezr:
    class WebCam(Thing): pass

    class Data(Thing): pass

    class User(Thing): pass

    class Gesture(Thing): pass

    class Wave(Gesture): pass
    class ThumbsUp(Gesture): pass
    class ThumbsDown(Gesture): pass
    class Fist(Gesture): pass
    class One(Gesture): pass
    class Two(Gesture): pass
    # class Peace(Gesture): pass
    class Three(Gesture): pass
    class Four(Gesture): pass
    class Five(Gesture): pass
    class Paper(Gesture): pass
    class CloseFingers(Gesture): pass
    class ApartFingers(Gesture): pass

    class Rule(Thing): pass
    class CloseCamera(Rule): pass
    class OpenBrowser(Rule): pass
    class Approve(Rule): pass
    class Disapprove(Rule): pass
    class CloseFile(Rule): pass
    class ChangePage(Rule): pass
    class NextImage(Rule): pass
    class ZoomIn(Rule): pass
    class ZoomOut(Rule): pass
    class Mark(Rule): pass

    class Context(Thing): pass
    class QuizGame(Context): pass
    class NoGame(Context): pass
    class PDFDocument(Context): pass
    class Image(Context): pass
    class MarkGame(Context): pass

    class is_caused_by(ObjectProperty):
        domain = [Rule]
        range = [Gesture]

    class causes_rule(ObjectProperty):
        domain = [Gesture]
        range = [Rule]
        inverse_property = is_caused_by


    class makes_gesture(ObjectProperty):
        domain = [User]
        range = [Gesture]


    class has_gesture_time(DataProperty):
        domain = [Gesture]
        range = [datetime.datetime]


    class has_rule_time(DataProperty):
        domain = [Rule]
        range = [datetime.datetime]


    class has_gesture_name(DataProperty):
        domain = [Gesture]
        range = [str]

    class has_gesture(DataProperty):
        domain = [Rule]
        range = [str]

    class has_context(ObjectProperty):
        domain = [Rule]
        range = [Context]

    # class includes_rule(ObjectProperty):
    #     domain = [Context]
    #     range = [Rule]
    #     inverse_property = has_context
