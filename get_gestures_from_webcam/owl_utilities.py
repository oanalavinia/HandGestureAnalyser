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
        elif gesture == 'peace':
            return owl.Peace()
        elif gesture == 'three':
            return owl.Three()
        elif gesture == 'four':
            return owl.Four()
        elif gesture == 'five':
            return owl.Five()
        elif gesture == 'fist':
            return owl.Fist()
        else:
            return None
