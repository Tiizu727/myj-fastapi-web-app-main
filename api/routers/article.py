from fastapi import APIRouter, Depends, HTTPException, UploadFile, Body
from sqlalchemy.orm import Session

import api.cruds.article as article_crud
from api.db import get_db

router = APIRouter()


@router.post("/article")
def create_article(
    article_content=Body(),
    db: Session = Depends(get_db),
):
    print("受けたデータ\n", article_content)
    result = article_crud.create_article(db, article_content)

    print("返すデータ\n", result)
    return result

@router.get("/article/{article_id}")
def get_article(
    article_id: int,
    db: Session = Depends(get_db),
):
    result = article_crud.get_article(db, article_id=article_id)

    # 記事が存在しない場合
    if result is None:
        raise HTTPException(status_code=404, detail="Article not found")

    return result


@router.get("/articles")
def get_all_articles(
    db: Session = Depends(get_db),
):
    return article_crud.get_all_articles(db)


@router.put("/article/{article_id}")
def update_article(
    article_id: int,
    article_update=Body(),
    db: Session = Depends(get_db),
):
    print("受けたデータ\n", article_update)
    result = article_crud.update_article(db, article_id, article_update)

    print("返すデータ\n", result)
    return result

@router.delete("/article/{article_id}")
def delete_article(
    article_id: int,
    db: Session = Depends(get_db),
):
    result = article_crud.delete_article(db, article_id)

    print("返すデータ\n", result)
    return result

