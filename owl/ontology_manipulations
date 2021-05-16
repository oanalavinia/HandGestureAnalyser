from owlready2 import *

fiiGezr = get_ontology("http://fiigezr.org/fiiGezr.owl")

with fiiGezr:
    class WebCam(Thing): pass

    class Data(Thing): pass

    class User(Thing): pass

    class Gesture(Thing): pass

    class WaveDetected(Gesture): pass
    class ThumbsUpDetected(Gesture): pass
    class ThumbsDownDetected(Gesture): pass
    class FistDetected(Gesture): pass
    class OneFingerDetected(Gesture): pass
    class TwoFingersDetected(Gesture): pass
    # class Peace(Gesture): pass
    class ThreeFingersDetected(Gesture): pass
    class FourFingersDetected(Gesture): pass
    class FiveFingersDetected(Gesture): pass
    # class PaperDetected(Gesture): pass
    class CloseFingersDetected(Gesture): pass
    class ApartFingersDetected(Gesture): pass

    class Rule(Thing): pass
        # equivalent_to = [Thing & is_caused_by.only(1, Gesture)]

    class Context(Thing): pass

    class is_caused_by(ObjectProperty):
        domain = [Rule]
        range = [Gesture]
        owlready_class_property_type = ["only"]

    class causes_rule(ObjectProperty):
        domain = [Gesture]
        range = [Rule]
        inverse_property = is_caused_by


    class makes_gesture(ObjectProperty):
        domain = [User]
        range = [Gesture]


    class has_gesture_time(DataProperty, FunctionalProperty):
        domain = [Gesture]
        range = [datetime.datetime]


    class has_rule_time(DataProperty, FunctionalProperty):
        domain = [Rule]
        range = [datetime.datetime]


    class has_gesture_name(DataProperty, FunctionalProperty):
        domain = [Gesture]
        range = [str]

    class has_gesture(DataProperty, FunctionalProperty):
        domain = [Rule]
        range = [str]

    class includes_rule(ObjectProperty):
        domain = [Context]
        range = [Rule]

    class has_context(ObjectProperty):
        domain = [Rule]
        range = [Context]
        inverse_property = includes_rule
        owlready_class_property_type = ["only"]

    # Context
    class QuizGame(Context): pass

    class NoGame(Context): pass

    class PDFDocument(Context): pass

    class Image(Context): pass

    class MarkGame(Context): pass

    # Rules

    # QuizGame
    class QuizGameRule:
        has_context = [QuizGame]
        is_caused_by =[ThumbsUpDetected, ThumbsDownDetected]

    class Approve(QuizGameRule):
        is_caused_by = [ThumbsUpDetected]

    class Disapprove(QuizGameRule):
        is_caused_by = [ThumbsDownDetected]

    # Image
    class ImageRule(Rule):
        has_context = [Image]
        is_caused_by = [ApartFingersDetected, CloseFingersDetected]

    class ZoomIn(ImageRule):
        is_caused_by = [ApartFingersDetected]

    class ZoomOut(ImageRule):
        is_caused_by = [CloseFingersDetected]

    # PDFDocument
    class PDFDocumentRule(Rule):
        has_context = [PDFDocument]
        is_caused_by = [ThumbsUpDetected, ThumbsDownDetected]

    class NextPage(PDFDocumentRule):
        is_caused_by = [ThumbsUpDetected]

    class PreviousPage(PDFDocumentRule):
        is_caused_by = [ThumbsUpDetected]

    # MarkGame
    class MarkGameRule(Rule):
        has_context = [MarkGame]
        is_caused_by = [OneFingerDetected, TwoFingersDetected, ThreeFingersDetected, FourFingersDetected, FiveFingersDetected]

    class Mark(MarkGameRule): pass

    class ChooseFirst(Mark):
        is_caused_by = [OneFingerDetected]

    class ChooseSecond(Mark):
        is_caused_by = [TwoFingersDetected]

    class ChooseThird(Mark):
        is_caused_by = [ThreeFingersDetected]

    class ChooseFourth(Mark):
        is_caused_by = [FourFingersDetected]

    class ChooseFifth(Mark):
        is_caused_by = [FiveFingersDetected]

    AllDisjoint([User, Gesture, Context, Rule])

    # Not used
    class FreeRule(Rule): pass

    class CloseCamera(FreeRule): pass

    class OpenBrowser(FreeRule): pass

    class CloseFile(Rule): pass

    class NextImage(ImageRule): pass




