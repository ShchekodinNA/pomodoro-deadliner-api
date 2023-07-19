from typing import Type, Optional, List, Sequence
from sqlalchemy import select, delete, exc, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql._typing import ColumnExpressionArgument, _TypedColumnClauseArgument
from pydantic import BaseModel
from src.database import Base


class IAsyncRepo:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def _execute(self, stmt) -> Result:
        result: Result = await self._session.execute(stmt)
        return result

    async def _exexute_with_scalar_return(self, stmt) -> Sequence:
        result = await self._execute(stmt)
        result_list = result.scalars().all()
        return result_list

    async def _delete(self, model: Type[Base], object_id: int) -> int:
        stmt = delete(model).where(model.id == object_id).returning(model.id)
        exec_result = await self._delete_by_stmt(stmt)
        (deleted_id,) = exec_result.one()
        return deleted_id

    async def _delete_by_stmt(
        self, stmt
    ) -> List[int]:  # TODO add correct types after test
        exec_result = await self._execute(stmt)
        return exec_result

    async def _add(self, *args: Base) -> None:
        try:
            self._session.add_all(args)
            await self._session.flush()
        except exc.IntegrityError as err:
            raise KeyError("item(s) not unique") from err

    async def _add_schema_out(
        self, object_: Base, read_schema: Type[BaseModel]
    ) -> BaseModel:
        await self._add(object_)
        return read_schema(**object_.__dict__)

    async def _get(
        self, model: Type[Base], id_: int, options: Optional[list] = None
    ) -> Base:
        stmt = select(model).where(model.id == id_)
        if options is not None:
            stmt = stmt.options(*options)
        db_obj = await self._get_one_record(stmt, model)
        return db_obj

    async def _get_one_record(self, stmt, model: Type[Base]) -> Base:
        exec_result = await self._execute(stmt)
        db_obj = exec_result.scalar()
        if db_obj is None:
            raise KeyError(f"{model.__name__} with passed_params isnot found.")
        return db_obj

    def get_read_shchema(
        self, db_object: Base, read_schema: Type[BaseModel]
    ) -> BaseModel:
        return read_schema(**db_object.__dict__)

    async def _update(
        self,
        db_object: Base,
        update_schema: BaseModel,
        exclude_from_dict: tuple = {
            "id",
        },
    ) -> Base:
        obj_data = db_object.__dict__
        schema_data = update_schema.dict(exclude=exclude_from_dict)
        table_fields = list(db_object.__table__.columns.keys())
        is_changed = False
        for field in obj_data:
            if field in schema_data and schema_data.get(field) is not None:
                if field in table_fields:
                    setattr(db_object, field, schema_data[field])
                    is_changed = True
                else:
                    table_name = (db_object.__table__.name).title().replace("_", "")
                    raise KeyError(
                        f"Update scheme for {table_name} have incorrect params"
                    )
        if is_changed:
            await self._add(db_object)
            await self._session.refresh(db_object)
        return db_object

    async def _update_by(self, model: Type[Base], update_schema: BaseModel) -> Base:
        db_object = await self._get(model, update_schema.id)
        db_object = await self._update(db_object, update_schema)
        return db_object
