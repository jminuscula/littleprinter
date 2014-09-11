import re
import random
import wikipedia
import string

from django.core.management.base import BaseCommand, CommandError
from medical_eponyms.models import MedicalEponym


class Command(BaseCommand):
    SEED = 2014
    LIST_ARTICLE = "list of eponymously named diseases"
    help = "Regenerates the eponym database"

    def _eponyms_in_section(self, section):
        eponyms = []
        for ep in re.findall(r'(.*?) – ', section):
            eponyms.append(re.sub(' \(.*?\)', '', ep))
        return eponyms

    def _eponym_articles(self, eponyms):
        for ep in eponyms:
            try:
                page = wikipedia.page(ep)
                yield ep, page.title, page.summary
            except (wikipedia.WikipediaException):
                pass

    def handle(self, *args, **options):

        self.stdout.write("Deleting registered eponyms…", ending=" ")
        deleted = MedicalEponym.objects.all().delete()
        self.stdout.write("{0} deleted".format(deleted))

        eponyms = []
        self.stdout.write("Fetching eponyms…", ending=" ")
        list_art = wikipedia.page(self.LIST_ARTICLE)
        for letter in string.ascii_uppercase:
            section = list_art.section(letter)
            eponyms += self._eponyms_in_section(section)

        self.stdout.write("{0} found".format(len(eponyms)))
        orders = list(range(len(eponyms)))
        random.seed(self.SEED)
        random.shuffle(orders)
        for name, title, summary in self._eponym_articles(eponyms):
            MedicalEponym.objects.create(name=name,
                                         title=title,
                                         # trim at first paragraph
                                         summary=summary.split("\n")[0],
                                         order=orders.pop())
            self.stdout.write(".", ending="")
            self.stdout.flush()
        self.stdout.write("\nDone")
