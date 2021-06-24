from owlready2 import *

fiiGezr = get_ontology("http://fiigezr.org/fiiGezr.owl")

with fiiGezr:
    class WebCam(Thing): pass


    class Data(Thing): pass


    class User(Thing): pass


    class Gesture(Thing): pass


    class WaveDetected(Gesture): pass


    class ThumbsUp(Gesture): pass


    class ThumbsDown(Gesture): pass


    class FistDetected(Gesture): pass


    class OneFingerDetected(Gesture): pass


    class TwoFingersDetected(Gesture): pass


    class ThreeFingersDetected(Gesture): pass


    class FourFingersDetected(Gesture): pass


    class FiveFingersDetected(Gesture): pass


    class CloseFingersDetected(Gesture): pass


    class ApartFingersDetected(Gesture): pass


    class Rule(Thing): pass


    class Context(Thing): pass


    class isCausedByGesture(ObjectProperty):
        domain = [Rule]
        range = [Gesture]
        class_property_type = ["only"]


    class causesRule(ObjectProperty):
        domain = [Gesture]
        range = [Rule]
        inverse_property = isCausedByGesture


    class makesGesture(ObjectProperty):
        domain = [User]
        range = [Gesture]


    class hasGestureTime(DataProperty, FunctionalProperty):
        domain = [Gesture]
        range = [datetime.datetime]


    class hasRuleTime(DataProperty, FunctionalProperty):
        domain = [Rule]
        range = [datetime.datetime]


    class hasGestureName(DataProperty, FunctionalProperty):
        domain = [Gesture]
        range = [str]


    class hasGesture(DataProperty, FunctionalProperty):
        domain = [Rule]
        range = [str]


    class includesRule(ObjectProperty):
        domain = [Context]
        range = [Rule]


    class hasContext(ObjectProperty):
        domain = [Rule]
        range = [Context]
        inverse_property = includesRule
        class_property_type = ["only"]


    AllDifferent([isCausedByGesture, makesGesture, hasGestureTime, hasRuleTime, hasGestureName, hasGesture,
                  hasContext])


    # Context
    class QuizGame(Context): pass


    class NoGame(Context): pass


    class PDFDocument(Context): pass


    class Image(Context): pass


    class SelectionGame(Context): pass


    # Rules

    # QuizGame
    class QuizGameRule(Rule):
        hasContext = [QuizGame]
        isCausedByGesture = [ThumbsUp, ThumbsDown]


    class Approve(QuizGameRule):
        isCausedByGesture = [ThumbsUp]


    class Disapprove(QuizGameRule):
        isCausedByGesture = [ThumbsDown]


    # Image
    class ImageRule(Rule):
        hasContext = [Image]
        isCausedByGesture = [ApartFingersDetected, CloseFingersDetected]


    class ZoomIn(ImageRule):
        isCausedByGesture = [ApartFingersDetected]


    class ZoomOut(ImageRule):
        isCausedByGesture = [CloseFingersDetected]


    # PDFDocument
    class PDFDocumentRule(Rule):
        hasContext = [PDFDocument]
        isCausedByGesture = [ThumbsUp, ThumbsDown]


    class NextPage(PDFDocumentRule):
        isCausedByGesture = [ThumbsDown]


    class PreviousPage(PDFDocumentRule):
        isCausedByGesture = [ThumbsUp]


    # SelectionGame
    class SelectionGameRule(Rule):
        hasContext = [SelectionGame]
        isCausedByGesture = [OneFingerDetected, TwoFingersDetected, ThreeFingersDetected, FourFingersDetected,
                             FiveFingersDetected]


    class ChooseFirst(SelectionGameRule):
        isCausedByGesture = [OneFingerDetected]


    class ChooseSecond(SelectionGameRule):
        isCausedByGesture = [TwoFingersDetected]


    class ChooseThird(SelectionGameRule):
        isCausedByGesture = [ThreeFingersDetected]


    class ChooseFourth(SelectionGameRule):
        isCausedByGesture = [FourFingersDetected]


    class ChooseFifth(SelectionGameRule):
        isCausedByGesture = [FiveFingersDetected]


    AllDisjoint([User, Gesture, Context, Rule])


    # Not used
    class FreeRule(Rule): pass


    class CloseCamera(FreeRule): pass


    class OpenBrowser(FreeRule): pass


    class CloseFile(Rule): pass


    class NextImage(ImageRule): pass

User.comment = ["A person that uses the ontology."]
Gesture.comment = ["A hand gesture made by an user to a webcam. Example includes TwoFingersDetected or ThumbsUp"]

Rule.comment = [
    "An action resulted from a made gesture, in a specific context, since the same gesture could have" +
    "different consequences. For example, ThumbsUp could either mean approve or changing the page in a direction."]
QuizGameRule.comment = ["A rule applied in a QuizGame context"]
PDFDocumentRule.comment = ["A rule applied in a PDFDocument context"]
ImageRule.comment = ["A rule applied in an Image context"]
SelectionGameRule.comment = ["A rule applied in a SelectionGame context"]

Context.comment = ["The context in which a rule was created."]
QuizGame.comment = ["A trivia game where the user can say if a statement is true or false through ThumbsUp or " +
                    "ThumbsDown"]
PDFDocument.comment = ["It refers to the situation where, through ThumbsUp or ThumbsDown, the user can change the " +
                       "page of a PDF document"]
Image.comment = ["It describes the circumstances where an image can be zoomed in or zoomed out by bringing fingers " +
                 "together or apart"]
SelectionGame.comment = ["A game where the user can select a favorite movie from a list of 5 by using counting gestures, " +
                    "like TwoFingersDetected."]
