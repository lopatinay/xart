from service_api.repository.challenge import ChallengeRepo


class ChallengeUseCases:
    def __init__(self, challenge_repo: ChallengeRepo):
        self.challenge_repo = challenge_repo

    def create(self, current_user):
        challenge = self.challenge_repo.create(current_user)
        return challenge

    def get_active_challenge(self, current_user):
        challenge = self.challenge_repo.get_active_challenge(current_user)
        return challenge

    def get_results(self, challenge_id):
        results = self.challenge_repo.get_results(challenge_id)
        return results
