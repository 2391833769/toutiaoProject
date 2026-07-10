from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from cache.news_cache import set_cache_categories
from cache.news_cache import get_cached_categories
from models.news import Category, News


# 查询新闻分类
async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    data = await get_cached_categories()
    if data:
        return data
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    categories = result.scalars().all()
    # 存入缓存
    if categories:
        await set_cache_categories(jsonable_encoder(categories))
    return categories 


# 获取指定类型【对应页码】新闻列表
async def get_news_list(db: AsyncSession, category_id: int, offset: int = 1, limit: int = 10):
    stmt = select(News).where(News.category_id == category_id).offset(offset).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


# 获取指定类型【全部】新闻列表
async def get_all_news_list(db: AsyncSession, category_id: int):
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one()


# 获取【指定id】新闻
async def get_news_by_id(db: AsyncSession, news_id: int):
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


# 更新【指定id】新闻浏览量
async def update_news_views(db: AsyncSession, news_id: int):
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    news = result.scalar_one_or_none()
    if news:
        news.views += 1
        await db.commit()
        return news

    return None


# 获取相关新闻
async def get_related_news(db: AsyncSession, news_id: int, category_id: int, limit: int = 5):
    stmt = (select(
            News.id,
            News.title,
            News.image,
            News.content,
            News.author,
            News.category_id,
            News.views,
            News.publish_time).
            where(News.id != news_id, News.category_id != category_id).
            order_by(News.views.desc(), News.publish_time.desc()).
            limit(limit))
    result = await db.execute(stmt)
    return result.mappings().all()