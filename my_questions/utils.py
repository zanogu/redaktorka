from my_questions.models import *
from typing import Dict, List
from my_questions.forms import *

class ArgumentException(BaseException):
    pass

class Renderer():

    @staticmethod
    def question_to_dict(
            question: Question,
            used_versions: List[Version],
            if_empty_take_last: bool = True
    ) -> Dict:
        if not if_empty_take_last and len(used_versions) == 0:
            raise ArgumentException("No used versions")

        all_versions = question.version_set.all()
        question_dict = {}

        if len(all_versions) == 0:
            return question_dict
        if len(used_versions) == 0:
            q1 = question.version_set.all()[0]
            question_dict = model_to_dict(q1)
            question_dict["editor_comments_forms"] = (
                EditVersionComment({'editor_comments': q1.editor_comments, 'pk': q1.id}))
        else:
            q1 = used_versions[0]
            question_dict = model_to_dict(q1)
            question_dict["editor_comments_forms"] = (
                EditVersionComment({'editor_comments': q1.editor_comments, 'pk': q1.id}))



        for i, v in question_dict.items():
            question_dict[i] = [v]

        if len(used_versions) > 1:
            for uv in used_versions[1:]:
                if uv.question == question:
                    for key, value in model_to_dict(uv).items():
                        if (value is not None and value != ""
                                and value not in question_dict[key]):
                            question_dict[key].append(value)
                    question_dict["editor_comments_forms"].append(
                        EditVersionComment({'editor_comments': q1.editor_comments,
                                            'pk': uv.id}))

        for uuv in all_versions:
            for key, value in model_to_dict(uuv).items():
                if ((value is not None and value != "")
                        and (len(question_dict[key]) == 0)):
                    question_dict[key].append(value)


        return question_dict

    @staticmethod
    def test_to_list(test: Test) -> List:
        test_list = []

        versions = test.version.all()
        tqs = TestQuestion.objects.filter(test=test)
        print(tqs)

        for tq in tqs:
            q = tq.question
            q_dict = Renderer.question_to_dict(
                    q,
                    [v for v in versions if v in q.version_set.all()]
                )
            q_dict["rating"] = RateQuestion(instance=tq)
            q_dict["is_answered"] = IsAnsweredQuestion(instance=tq)
            test_list.append(q_dict)
        return test_list



