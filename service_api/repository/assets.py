import os


from service_api.configs import RuntimeConfig
from service_api.models import ProductModel


class AssetsRepo:

    @staticmethod
    def all_products():
        return os.listdir(str(RuntimeConfig.products_dir))

    @staticmethod
    def all_snapshots():

        snapshots_dirs = os.listdir(str(RuntimeConfig.snapshots_dir))
        snapshots_files = []
        for snapshot_dir in snapshots_dirs:
            for snapshot in os.listdir(str(RuntimeConfig.snapshots_dir.joinpath(snapshot_dir))):
                snapshots_files.append("%s/%s" % (snapshot_dir, snapshot))
        return snapshots_files


def populate_data():
    from sqlalchemy.dialects.postgresql import insert

    from service_api.services import db_session
    from service_api.models import SnapshotModel

    session = db_session()
    assets_repo = AssetsRepo()

    products = assets_repo.all_products()
    snapshots = assets_repo.all_snapshots()

    stmt = insert(ProductModel).values([{"file_name": file_name} for file_name in products])
    stmt = stmt.on_conflict_do_nothing(constraint="product_file_name_key")
    session.execute(stmt)

    stmt = insert(SnapshotModel).values([{"file_name": file_name} for file_name in snapshots])
    stmt = stmt.on_conflict_do_nothing(constraint="snapshot_file_name_key")
    session.execute(stmt)

    session.commit()
