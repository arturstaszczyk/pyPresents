from describe.models import RandomizationModel, PersonModel


class DisplayController:

    def __init__(self):
        pass

    def can_user_describe_present(self):
        relations = RandomizationModel.objects.all()
        people = PersonModel.objects.all()

        return len(people) == len(relations) and len(people) > 0