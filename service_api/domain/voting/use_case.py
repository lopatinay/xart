from service_api.models import UserRoles
from service_api.repository.challenge import ChallengeRepo
from service_api.repository.voting import VotingRepo


class VotingPermissionDeniedError(Exception):
    pass


class VotingUseCases:
    def __init__(self, voting_repo: VotingRepo, challenge_repo: ChallengeRepo = None):
        self.voting_repo = voting_repo
        self.challenge_repo = challenge_repo

    def vote(self, current_user, payload):
        self.voting_repo.vote(current_user, payload)
        next_voting = self.voting_repo.get(current_user)

        if next_voting is None:
            self.challenge_repo.finish_challenge(current_user)
            return

        return self.voting_repo.get(current_user)

    def all(self, current_user):
        return self.voting_repo.all(current_user)

    def get(self, current_user):
        next_voting = self.voting_repo.get(current_user)
        if next_voting is None:
            self.challenge_repo.finish_challenge(current_user)
            return
        return next_voting

    def to_group_review(self, current_user, voting_id):
        if current_user.role != UserRoles.ADMIN:
            raise VotingPermissionDeniedError("You cannot change voting status")

        return self.voting_repo.to_group_review(voting_id)
