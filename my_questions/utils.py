from .models import *
from typing import Dict, List

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
            question_dict = model_to_dict(question.version_set.all()[0])
        else:
            question_dict = model_to_dict(used_versions[0])

        for i, v in question_dict.items():
            question_dict[i] = [v]

        if len(used_versions) > 1:
            for uv in used_versions[1:]:
                if uv.question == question:
                    for key, value in model_to_dict(uv).items():
                        if (value is not None and value != ""
                                and value not in question_dict[key]):
                            question_dict[key].append(value)

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
            test_list.append(
                Renderer.question_to_dict(
                    q,
                    [v for v in versions if v in q.version_set.all()]
                )
            )
        return test_list



