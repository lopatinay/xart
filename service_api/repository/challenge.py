from sqlalchemy import func, desc

from service_api.models import ChallengeModel, VotingModel, SnapshotModel, ProductModel
from service_api.models.voting import VotingStatuses
from service_api.repository.base import BaseRepo


class ChallengeRepo(BaseRepo):
    model = ChallengeModel

    def get_results(self, challenge_id):
        results = self.db.query(
            func.count(VotingModel.author_id).label("majority"),
            VotingModel.snapshot_id,
            VotingModel.product_id,
            VotingModel.status,
        ).filter(
            VotingModel.challenge_id == challenge_id,
        ).group_by(
            VotingModel.snapshot_id,
            VotingModel.product_id,
            VotingModel.status
        ).order_by(
            desc("majority")
        ).all()

        response = []
        for majority, snapshot_id, product_id, status in results:
            response.append({
                "majority": majority,
                "snapshot_id": snapshot_id,
                "product_id": majority,
                "status": status,
            })

        return response

    def finish_challenge(self, current_user):
        self.db.query(
            ChallengeModel
        ).filter(
            ChallengeModel.votes.any(author=current_user)
        ).update({
            "is_active": False
        })
        self.db.commit()

    def create(self, current_user):

        # Check if current user has active challenge
        active_challenge = self.get_active_challenge(current_user)

        if active_challenge:
            return

        challenge = self.model()
        self.db.add(challenge)
        self.db.flush()

        # Get 100 unidentified snapshots
        snapshots = self.db.query(SnapshotModel).filter(SnapshotModel.votes == None)[:challenge.items_pre_challenge]

        # Get one random product
        random_product = self.db.query(ProductModel).order_by(func.random()).first()

        # Create votes with status IN_PROGRESS
        votes = []
        for snapshot in snapshots:
            vote = VotingModel(
                status=VotingStatuses.IN_PROGRESS,
                author_id=current_user.id,
                snapshot_id=snapshot.id,
                product_id=random_product.id,
                challenge_id=challenge.id
            )
            votes.append(vote)

        self.db.bulk_save_objects(votes)
        self.db.commit()

        return challenge

    def get_active_challenge(self, current_user):
        active_challenge = self.db.query(
            ChallengeModel
        ).filter(
            ChallengeModel.votes.any(author=current_user)
        ).filter_by(
            is_active=True
        ).first()
        return active_challenge
