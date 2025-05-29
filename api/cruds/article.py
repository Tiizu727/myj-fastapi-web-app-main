from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import datetime

def create_article(
        db: Session,
        content: dict,
):
    sql = text(
        """
        INSERT INTO articles_mb (title, body, regist_date, user_id)
        VALUES (:title, :body, :regist_date, :user_id)
        """
    )
    params = {
        "title": content.get("title"),
        "body": content.get("body"),
        "regist_date": datetime.now(),
        "user_id": content.get("user_id"),
    }

    print(f"SQL: {sql}\nParams: {params}")
    result = db.execute(sql, params)
    db.commit()
    new_article_id = result.lastrowid

    if new_article_id is None:
        raise ValueError("記事の作成に失敗しました。")

    new_article = get_article(db, article_id=new_article_id)
    print(f"DB操作の結果: {new_article}")

    return new_article 

def get_article(
        db: Session,
        article_id: int,
):
    sql = text(
        """
        SELECT * FROM articles_mb
        WHERE id = :id
        """
    )
    params = {"id": article_id}

    print(f"SQL: {sql}\nParams: {params}")
    result = db.execute(sql, params).first()
    
    if result is not None:
        result = result._asdict()
    
    print(f"DB操作の結果: {result}")

    return result


def get_all_articles(
        db: Session,
):
    sql = text(
        """
        SELECT * FROM articles_mb
        """
    )

    print(f"SQL: {sql}")
    result = db.execute(sql).mappings().all()
    print(f"DB操作の結果: {result}")

    return result


def update_article(
        db: Session,
        article_id: int,
        article_update: dict,
):
    sql = text(
        """
        UPDATE articles_mb
        SET title = :title, body = :body, regist_date = :regist_date
        WHERE id = :id
        """
    )
    params = {
        "id": article_id,
        "title": article_update.get("title"),
        "body": article_update.get("body"),
        "regist_date": datetime.now(),
    }

    print(f"SQL: {sql}\nParams: {params}")
    result = db.execute(sql, params)
    db.commit()
    updated_article = get_article(db, article_id=article_id)
    print(f"DB操作の結果: {updated_article}")

    return updated_article


def delete_article(
        db: Session,
        article_id: int,
):
    sql = text(
        """
        DELETE FROM articles_mb
        WHERE id = :id
        """
    )
    params = {"id": article_id}

    print(f"SQL: {sql}\nParams: {params}")
    res = db.execute(sql, params)
    db.commit()
    deleted_article = get_article(db, article_id=article_id)
    print(f"DB操作の結果: {deleted_article}")

    return deleted_article