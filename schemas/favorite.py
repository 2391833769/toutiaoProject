from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

from schemas.base import NewsItemBase


class FavoriteCheckResponse(BaseModel):
    is_favorite: bool = Field(..., alias="isFavorite")
    model_config = ConfigDict(populate_by_name=True)


class FavoriteAddRequest(BaseModel):
    news_id: int = Field(..., alias="newsId")


class FavoriteNewsItemResponse(NewsItemBase):
    favorite_id: int = Field(alias="favoriteId")
    favorite_time: datetime = Field(alias="favoriteTime")


#收藏列表接口响应模型类
class FavoriteListResponse(BaseModel):
    list: list[NewsItemBase]
    total: int
    has_more: bool = Field(alias="hasMore")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )