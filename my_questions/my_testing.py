from my_questions.models import *
from my_questions.utils import *

q = Question.objects.get(pk=18)
v = Version.objects.get(pk=28)
v2 = Version.objects.get(pk=29)
v4 = Version.objects.get(pk=26)

q_rend = Renderer.question_to_dict(q,[v, v4, v2], if_empty_take_last=True)
# print(q_rend)

t = Test.objects.get(pk=7)
print(Renderer.test_to_list(t))

