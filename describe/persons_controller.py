import random
from describe.models import PersonModel, RandomizationModel
from describe.exceptions import CannotFindReceiver
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class PersonsController:

    MAX_ITERATIONS = 100

    def get_person(self, user):
        person = None

        try:
            person = PersonModel.objects.get(user_id=user.pk)
        except ObjectDoesNotExist:
            person = self.create(user)

        return person


    def create(self, user):

        person = PersonModel()
        person.user_id = user
        person.save()

        return person

    def get_rand_user_not_me(self, me):

        current_it = 0
        selected_user = me

        all_users = list(User.objects.all())
        all_users_count = len(all_users)

        while current_it < PersonsController.MAX_ITERATIONS and me.pk == selected_user.pk:
            rand = random.randint(1, all_users_count * 10000) % all_users_count
            selected_user = all_users[rand]
            current_it += 1

        if selected_user.pk == me.pk:
            raise RuntimeError('Cannot randomize person')

        return selected_user

    def draw(self, user):

        current_it = 0
        receiver = None

        while current_it < PersonsController.MAX_ITERATIONS and receiver == None:
            current_it += 1

            try:
                receiver = self.get_rand_user_not_me(user)
            except RuntimeError:
                raise CannotFindReceiver()

            if self._users_in_the_same_group(user, receiver):
                receiver = None
                continue

            if self._receiver_already_drawn(receiver):
                receiver = None
                continue

        if receiver == None:
            raise CannotFindReceiver()

        self._save_randomization_between(user, receiver)

    def _users_in_the_same_group(self, user, receiver):
        user_groups = user.groups.values_list('name', flat=True)
        receiver_group = receiver.groups.values_list('name', flat=True)

        if not user_groups or not receiver_group:
            return False

        return receiver_group[0] == user_groups[0]

    def _receiver_already_drawn(self, receiver):
        already_drawn = False

        for model in RandomizationModel.objects.all():
            if(model.giving_id == receiver.pk):
                already_drawn = True
                break

        return already_drawn

    def _save_randomization_between(self, user, receiver):
        randModel = RandomizationModel()
        randModel.user_id = user.pk
        randModel.giving_id = receiver.pk
        randModel.save()