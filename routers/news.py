from email.policy import HTTP

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_config import get_db
from crud import news

router = APIRouter(prefix="/api/news", tags=["news"])

#新闻分类
@router.get("/categories")
async def get_categories(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    categories = await news.get_categories(db, skip=skip, limit=limit)
    return {
        "code": 200,
        "message": "获取新闻分类成功",
        "data": categories
    }

#新闻列表
@router.get("/list")
async def get_new_list(
        category_id: int = Query(..., alias="categoryId"),
        page: int = 1,
        page_size: int = Query(10, alias="pageSize", le=100),
        db: AsyncSession = Depends(get_db)
):
    offset = (page - 1) *  page_size
    news_list = await news.get_news_list(db, category_id, offset, page_size)
    total = await news.get_all_news_list(db, category_id)
    has_more = total > offset + page_size
    return {
        "code": 200,
        "message": "获取新闻列表成功",
        "data": {
            "list": news_list,
            "total": total,
            "hasMore": has_more
        }
    }


#新闻详情
@router.get("/detail")
async def get_news_detail(new_id: int = Query(..., alias="id"), db: AsyncSession = Depends(get_db)):
    news_detail = await news.get_news_by_id(db, new_id)
    views_res = await news.update_news_views(db, new_id)
    related_news = await news.get_related_news(db, new_id, category_id=news_detail.category_id)

    if not news_detail:
        raise HTTPException(status_code=404, detail="新闻不存在")

    if not views_res:
        raise HTTPException(status_code=404, detail="新闻不存在")


    return {
        "code": 200,
        "message": "success",
        "data": {
            "id": news_detail.id,
            "title": news_detail.title,
            "content": news_detail.content,
            "image": news_detail.image,
            "author": news_detail.author,
            "category_id": news_detail.category_id,
            "views": news_detail.views,
            "publish_time": news_detail.publish_time.strftime("%Y-%m-%d %H:%M:%S"),
            "relatedNews": related_news
        }
    }

