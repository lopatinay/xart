from service_api.models import VotingModel, UserModel, UserRoles, ChallengeModel
from service_api.models.voting import VotingStatuses
from service_api.repository.base import BaseRepo


class ExtraVotingAlreadyExist(Exception):
    pass


class VotingRepo(BaseRepo):
    model = VotingModel

    def to_group_review(self, voting_id):
        vote = self.db.get(self.model, voting_id)

        extra_voting_exits = self.db.query(self.model).filter_by(
            product_id=vote.product_id,
            snapshot_id=vote.snapshot_id
        ).count()

        if extra_voting_exits > 1:
            raise ExtraVotingAlreadyExist("Extra voting already exist")

        self.db.query(
            ChallengeModel
        ).filter_by(
            id=vote.challenge_id
        ).update({
            "is_active": True
        })

        users = self.db.query(
            UserModel
        ).filter(
            UserModel.role == UserRoles.QA,
            UserModel.votes != vote
        ).all()

        extra_voting = [
            VotingModel(
                author_id=user.id,
                snapshot_id=vote.snapshot_id,
                product_id=vote.product_id,
                challenge_id=vote.challenge_id,
                status=VotingStatuses.IN_PROGRESS
            )
            for user in users
        ]
        self.db.add_all(extra_voting)

        self.db.commit()
        return extra_voting

    def vote(self, current_user, payload):
        decision = payload["decision"]

        self.db.query(self.model).filter_by(
            author=current_user,
            status=VotingStatuses.IN_PROGRESS,
            snapshot_id=payload["snapshot_id"],
            product_id=payload["product_id"],
        ).update({
            "status": VotingStatuses.MATCH if decision else VotingStatuses.UNMATCH
        })
        self.db.commit()

    def all(self, current_user):
        vote = self.db.query(self.model).filter_by(
            author=current_user,
            status=VotingStatuses.IN_PROGRESS
        ).all()
        return vote

    def get(self, current_user):
        vote = self.db.query(self.model).filter_by(
            author=current_user,
            status=VotingStatuses.IN_PROGRESS
        )

        vote_count = vote.count()

        if not vote_count:
            return

        vote = vote.first()
        vote.count = vote_count
        return vote
