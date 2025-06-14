from sqlalchemy import text
from sqlalchemy.orm import Session

def get_all_products(db: Session):
    sql = text(
        """
        SELECT * FROM products
        """
    )

    print(f"SQL: {sql}")
    result = db.execute(sql).mappings().all()
    print(f"DB操作の結果: {result}")

    return result

def get_products_by_category(category: str, db: Session):
    sql = text(
        """
        SELECT * FROM products
        WHERE category = :category
        """
    )

    print(f"SQL: {sql}")
    result = db.execute(sql, {"category": category}).mappings().all()
    print(f"DB操作の結果: {result}")

    return result

def get_cpu_by_maker(maker: str, db: Session):
    sql = text(
        """
        SELECT * FROM products
        WHERE maker = :maker
        """
    )

    print(f"SQL: {sql}")
    result = db.execute(sql, {"maker": maker}).mappings().all()
    print(f"DB操作の結果: {result}")

    return result