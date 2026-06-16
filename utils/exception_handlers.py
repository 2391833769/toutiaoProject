from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from utils.exception import http_exception_handler, integrity_error_handler, sqlalchemy_error_handler, \
    general_exception_handler


def register_exception_handlers(app):
    """
    注册全局异常处理
    """
    app.add_exception_handler(HTTPException, http_exception_handler)     # 业务
    app.add_exception_handler(InterruptedError, integrity_error_handler) # 数据完整性约束
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler) # 数据库
    app.add_exception_handler(Exception, general_exception_handler)      # 兜底