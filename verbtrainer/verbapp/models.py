import random

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Subquery, OuterRef, Value
from django.db.models.functions import Coalesce
from django.forms import model_to_dict


class IrregularVerb(models.Model):
    base = models.CharField(max_length=100, verbose_name="Infinitiv")
    translation = models.CharField(max_length=100)
    past_simple = models.CharField(max_length=100, verbose_name="Präteritum")
    past_participle = models.CharField(max_length=100, verbose_name="Partizip II")

    class Meta:
        unique_together = ('base', 'past_simple', 'past_participle')

    def __str__(self):
        return (f"{self.base} {self.translation} "
                f"{self.past_simple} {self.past_participle}")

    def get_verb_as_dict(self):
        return model_to_dict(self)

    def get_task(self, hide_forms=1):
        forms = ['base', 'past_simple', 'past_participle']
        random.shuffle(forms)
        hide_forms = forms[:hide_forms]

        task = self.get_verb_as_dict()
        for form in hide_forms:
            task[form] = ""

        return task, hide_forms, task['translation']

    def check_forms(self, answer):
        results = answer.copy()
        error_fields = []

        assert int(getattr(self, "id")) == int(answer["id"]), "IDs do not match"
        del answer["id"]

        for field in answer:
            solution = getattr(self, field)
            if solution != answer[field]:
                error_fields.append(field)
                results[field] += f" (correct: {solution})"
        return results, error_fields


class UserVerbStats(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    verb = models.ForeignKey(IrregularVerb, on_delete=models.CASCADE)
    memory_score = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'verb')

    def update_memory_score(self, errors):
        if errors == 0:
            self.memory_score += 1
        else:
            self.memory_score -= errors
        self.save()

    @staticmethod
    def get_random_verb_as_task(user, level=1):
        score_subquery = UserVerbStats.objects.filter(
            verb=OuterRef('pk'), user=user
        ).values('memory_score')[:1]
        verbs = IrregularVerb.objects.annotate(
            memory_score=Coalesce(Subquery(score_subquery), Value(0))
        )

        max_score = max(verb.memory_score for verb in verbs)
        min_score = min(verb.memory_score for verb in verbs)
        if max_score == 0 and min_score == 0:
            max_score = 1e-6
        if max_score == min_score:
            weights = [1.0 for _ in verbs]
        else:
            weights = [
                (max_score - verb.memory_score) / (max_score - min_score)
                for verb in verbs
            ]

        verb = random.choices(verbs, weights=weights)[0]
        return verb.get_task(level)
