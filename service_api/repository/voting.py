from service_api.models import VotingModel
from service_api.models.voting import VotingStatuses
from service_api.repository.base import BaseRepo


class VotingRepo(BaseRepo):
    model = VotingModel

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
        # add_columns(slugify(Artist.Name).label("name_slug"))
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
