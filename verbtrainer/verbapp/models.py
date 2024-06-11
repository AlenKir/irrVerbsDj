import random

from django.db import models
from django.forms import model_to_dict


class IrregularVerb(models.Model):
    base = models.CharField(max_length=100, verbose_name="Infinitiv")
    translation = models.CharField(max_length=100)
    past_simple = models.CharField(max_length=100, verbose_name="Präteritum")
    past_participle = models.CharField(max_length=100, verbose_name="Partizip II")
    memory_score = models.IntegerField(default=0)

    class Meta:
        unique_together = ('base', 'past_simple', 'past_participle')

    def __str__(self):
        return (f"{self.base} {self.translation} "
                f"{self.past_simple} {self.past_participle}")

    def get_verb_as_dict(self):
        return model_to_dict(self)

    @staticmethod
    def get_random_verb_as_task(hide_forms=1):
        ordered_verbs = IrregularVerb.objects.all().order_by('memory_score')
        max_score = max(verb.memory_score for verb in ordered_verbs)
        max_score = max_score if max_score != 0 else 1e-6
        weights = [(max_score - verb.memory_score) / max_score for verb in ordered_verbs]
        chosen_verb = random.choices(ordered_verbs, weights=weights)[0]
        return chosen_verb.get_task(hide_forms)

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
        memory_score = 0

        assert int(getattr(self, "id")) == int(answer["id"]), "IDs do not match"
        del answer["id"]

        for field in answer:
            solution = getattr(self, field)
            if solution != answer[field]:
                error_fields.append(field)
                results[field] += f" (correct: {solution})"

        if len(error_fields) == 0:
            memory_score += 1
        else:
            memory_score -= 1
        self.update_memory_score(memory_score)

        return results, error_fields

    def update_memory_score(self, change):
        self.memory_score += change
        self.save()
