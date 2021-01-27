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
    class Peace(Gesture): pass
    class Three(Gesture): pass
    class Four(Gesture): pass
    class Five(Gesture): pass
    class Paper(Gesture): pass

    class gesture_time(AnnotationProperty): pass

    class Rule(Thing): pass
    class CloseCamera(Rule): pass
    class OpenBrowser(Rule): pass

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

    class Point(Thing): pass

    class has_for_x(DataProperty, FunctionalProperty):
        range = [int]

    class has_for_y(DataProperty, FunctionalProperty):
        range = [int]
    
    class Wrist(Point): pass

    class Finger(Thing): pass       # index, middle, ring and pinky
    class Thumb(Thing): pass        # thumb

    class IndexFinger(Finger): pass
    class MiddleFinger(Finger): pass
    class RingFinger(Finger): pass
    class PinkyFinger(Finger): pass

    # common finger points
    class MCP(Point): pass
    class has_for_mcp(ObjectProperty):
        domain = [Finger, Thumb]
        range = [MCP]

    class Tip(Point): pass
    class has_for_tip(ObjectProperty):
        domain = [Finger, Thumb]
        range = [Tip]

    # finger specific points
    class PIP(Point): pass
    class has_for_pip(ObjectProperty):
        domain = [Finger]
        range = [PIP]

    class DIP(Point): pass
    class has_for_dip(ObjectProperty):
        domain = [Finger]
        range = [DIP]

    # thumb specific points
    class CMC(Point): pass
    class has_for_cmc(ObjectProperty):
        domain = [Thumb]
        range = [CMC]

    class IP(Point): pass
    class has_for_ip(ObjectProperty):
        domain = [Thumb]
        range = [IP]

    class Hand(Thing): pass
    class has_for_wrist(ObjectProperty):
        domain = [Hand]
        range = [Wrist]
    class has_for_thumb(ObjectProperty):
        domain = [Hand]
        range = [Thumb]
    class has_for_index_finger(ObjectProperty):
        domain = [Hand]
        range = [IndexFinger]
    class has_for_middle_finger(ObjectProperty):
        domain = [Hand]
        range = [MiddleFinger]
    class has_for_ring_finger(ObjectProperty):
        domain = [Hand]
        range = [RingFinger]
    class has_for_pinky_finger(ObjectProperty):
        domain = [Hand]
        range = [PinkyFinger]

    def create_hand(points_list):
        #0
        wrist = Wrist()
        wrist.has_for_x = points_list[0][0]
        wrist.has_for_y = points_list[0][1]

        #1
        thumb_cmc = CMC()
        thumb_cmc.has_for_x = points_list[1][0]
        thumb_cmc.has_for_y = points_list[1][1]
        #2
        thumb_mcp = MCP()
        thumb_mcp.has_for_x = points_list[2][0]
        thumb_mcp.has_for_y = points_list[2][1]
        #3
        thumb_ip = IP()
        thumb_ip.has_for_x = points_list[3][0]
        thumb_ip.has_for_y = points_list[3][1]
        #4
        thumb_tip = Tip()
        thumb_tip.has_for_x = points_list[4][0]
        thumb_tip.has_for_y = points_list[4][1]

        #5
        index_mcp = MCP()
        index_mcp.has_for_x = points_list[5][0]
        index_mcp.has_for_y = points_list[5][1]
        #6
        index_pip = PIP()
        index_pip.has_for_x = points_list[6][0]
        index_pip.has_for_y = points_list[6][1]
        #7
        index_dip = DIP()
        index_dip.has_for_x = points_list[7][0]
        index_dip.has_for_y = points_list[7][1]
        #8
        index_tip = Tip()
        index_tip.has_for_x = points_list[8][0]
        index_tip.has_for_y = points_list[8][1]

        #9
        middle_mcp = MCP()
        middle_mcp.has_for_x = points_list[9][0]
        middle_mcp.has_for_y = points_list[9][1]
        #10
        middle_pip = PIP()
        middle_pip.has_for_x = points_list[10][0]
        middle_pip.has_for_y = points_list[10][1]
        #11
        middle_dip = DIP()
        middle_dip.has_for_x = points_list[11][0]
        middle_dip.has_for_y = points_list[11][1]
        #12
        middle_tip = Tip()
        middle_tip.has_for_x = points_list[12][0]
        middle_tip.has_for_y = points_list[12][1]

        #13
        ring_mcp = MCP()
        ring_mcp.has_for_x = points_list[13][0]
        ring_mcp.has_for_y = points_list[13][1]
        #14
        ring_pip = PIP()
        ring_pip.has_for_x = points_list[14][0]
        ring_pip.has_for_y = points_list[14][1]
        #15
        ring_dip = DIP()
        ring_dip.has_for_x = points_list[15][0]
        ring_dip.has_for_y = points_list[15][1]
        #16
        ring_tip = Tip()
        ring_tip.has_for_x = points_list[16][0]
        ring_tip.has_for_y = points_list[16][1]

        #17
        pinky_mcp = MCP()
        pinky_mcp.has_for_x = points_list[17][0]
        pinky_mcp.has_for_y = points_list[17][1]
        #18
        pinky_pip = PIP()
        pinky_pip.has_for_x = points_list[18][0]
        pinky_pip.has_for_y = points_list[18][1]
        #19
        pinky_dip = DIP()
        pinky_dip.has_for_x = points_list[19][0]
        pinky_dip.has_for_y = points_list[19][1]
        #20
        pinky_tip = Tip()
        pinky_tip.has_for_x = points_list[20][0]
        pinky_tip.has_for_y = points_list[20][1]

        thumb = Thumb()
        thumb.has_for_cmc = [thumb_cmc]
        thumb.has_for_mcp = [thumb_mcp]
        thumb.has_for_ip = [thumb_ip]
        thumb.has_for_tip = [thumb_tip]

        index_finger = IndexFinger()
        index_finger.has_for_mcp = [index_mcp]
        index_finger.has_for_pip = [index_pip]
        index_finger.has_for_dip = [index_dip]
        index_finger.has_for_tip = [index_tip]

        middle_finger = MiddleFinger()
        middle_finger.has_for_mcp = [middle_mcp]
        middle_finger.has_for_pip = [middle_pip]
        middle_finger.has_for_dip = [middle_dip]
        middle_finger.has_for_tip = [middle_tip]

        ring_finger = RingFinger()
        ring_finger.has_for_mcp = [ring_mcp]
        ring_finger.has_for_pip = [ring_pip]
        ring_finger.has_for_dip = [ring_dip]
        ring_finger.has_for_tip = [ring_tip]

        pinky_finger = PinkyFinger()
        pinky_finger.has_for_mcp = [pinky_mcp]
        pinky_finger.has_for_pip = [pinky_pip]
        pinky_finger.has_for_dip = [pinky_dip]
        pinky_finger.has_for_tip = [pinky_tip]

        hand = Hand()
        hand.has_for_wrist = [wrist]
        hand.has_for_thumb = [thumb]
        hand.has_for_index_finger = [index_finger]
        hand.has_for_middle_finger = [middle_finger]
        hand.has_for_ring_finger = [ring_finger]
        hand.has_for_pinky_finger = [pinky_finger]

        return hand