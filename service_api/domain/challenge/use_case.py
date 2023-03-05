from fastapi import HTTPException, status

from service_api.repository.challenge import ChallengeRepo


class ChallengeUseCases:
    def __init__(self, challenge_repo: ChallengeRepo):
        self.challenge_repo = challenge_repo

    def create(self, current_user):
        challenge = self.challenge_repo.create(current_user)

        if challenge is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You already have an active challenge",
            )

        return challenge

    def get_active_challenge(self, current_user):
        challenge = self.challenge_repo.get_active_challenge(current_user)
        return challenge
