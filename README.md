# Irregular Verbs Trainer

Welcome to the Irregular Verbs Trainer repository. This is a simple web application designed to help users learn and practice irregular verbs effectively.

## Features

- **Practice Irregular Verbs:** Choose to practice one, two, or all three forms of irregular verbs.
- **Add and Edit Verbs:** Easily add new verbs or edit existing ones.
- **Spaced Repetition:** Has a simple spaced repetition feature to reinforce learning.
- **Track Progress:** Monitor progress by checking how familiar you are with each verb.

### Irregular Verbs Dataset

It's possible to add irregular verbs from a CSV file included in the project (data/verbs.cvs), however it was scraped together from several sources and changed for personal convenience, may contain typos or mistakes.

```bash
python manage.py loadverbs /path/to/your/irregular_verbs.csv