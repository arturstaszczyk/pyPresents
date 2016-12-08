from describe.models import RandomizationModel, PersonModel


class DisplayController:

    def __init__(self):
        pass

    def can_user_describe_present(self):
        relations = RandomizationModel.objects.all()
        people = PersonModel.objects.all()

        all_give = True
        givers = [x.user_id for x in relations]
        for person in people:
            if person.pk in givers:
                givers.remove(person.pk)
            else:
                all_give = False

        return len(people) == len(relations) and len(people) > 0 and all_give and len(givers) == 0