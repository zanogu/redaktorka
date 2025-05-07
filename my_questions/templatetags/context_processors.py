from my_questions.constants import *

def is_debug(request):
    return {'is_debug': TEST_MODE}

def question_part_names(request):
    return {'question_part_names': QUESTION_PART_NAMES}

def control_element_names(request):
    return {'control_element_names': CONTROL_ELEMENT_NAMES}
def terms(request):
    return {'terms': TERMS}