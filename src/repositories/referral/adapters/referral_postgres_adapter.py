from archipy.adapters.base.sqlalchemy.adapters import SQLAlchemyFilterMixin
from archipy.adapters.postgres.sqlalchemy.adapters import AsyncPostgresSQLAlchemyAdapter
from archipy.models.errors import NotFoundError
from archipy.models.types.base_types import FilterOperationType
from sqlalchemy import select, update
from sqlalchemy.sql.expression import Select, Update

from src.models.dtos.referral.repository.referral_repository_interface_dtos import (
    CreateReferralCommandDTO,
    CreateReferralResponseDTO,
    GetReferralQueryDTO,
    GetReferralResponseDTO,
    UpdateReferralCommandDTO,
    DeleteReferralCommandDTO,
    SearchReferralQueryDTO,
    SearchReferralResponseDTO,
)
from src.models.entities import ReferralEntity


class ReferralPostgresAdapter(SQLAlchemyFilterMixin):
    def __init__(self, adapter: AsyncPostgresSQLAlchemyAdapter) -> None:
        self._adapter: AsyncPostgresSQLAlchemyAdapter = adapter

    async def create_referral(self, input_dto: CreateReferralCommandDTO) -> CreateReferralResponseDTO:
        _entity = ReferralEntity(**input_dto.model_dump())
        result = await self._adapter.create(entity=_entity)
        return CreateReferralResponseDTO.model_validate(obj=result)

    async def get_referral(self, input_dto: GetReferralQueryDTO) -> GetReferralResponseDTO:
        select_query = select(ReferralEntity)
        _query = self._apply_filter(
            query=select_query,
            field=ReferralEntity.referral_uuid,
            value=input_dto.referral_uuid,
            operation=FilterOperationType.EQUAL,
        )
        result = await self._adapter.execute(statement=_query)
        entity = result.scalar()

        if not entity:
            raise NotFoundError(resource_type=ReferralEntity.__name__)

        return GetReferralResponseDTO.model_validate(obj=entity)

    async def search_referrals(self, input_dto: SearchReferralQueryDTO) -> SearchReferralResponseDTO:
        query: Select = select(ReferralEntity)
        if input_dto.user_uuid:
            query = self._apply_filter(
                query=query,
                field=ReferralEntity.user_uuid,
                value=input_dto.user_uuid,
                operation=FilterOperationType.EQUAL,
            )
        # Add search filters here as needed

        entities, total = await self._adapter.execute_search_query(
            query=query,
            entity=ReferralEntity,
            sort_info=input_dto.sort_info,
            pagination=input_dto.pagination,
        )

        return SearchReferralResponseDTO(referrals=entities, total=total)

    async def update_referral(self, input_dto: UpdateReferralCommandDTO) -> None:
        update_data = input_dto.model_dump(exclude={"referral_uuid"}, exclude_none=True)
        if not update_data:
            return

        update_query: Update = (
            update(ReferralEntity).where(ReferralEntity.referral_uuid == input_dto.referral_uuid).values(**update_data)
        )

        result = await self._adapter.execute(statement=update_query)
        if result.rowcount == 0:
            raise NotFoundError(resource_type=ReferralEntity.__name__)

    async def delete_referral(self, input_dto: DeleteReferralCommandDTO) -> None:
        delete_query = (
            update(ReferralEntity)
            .where(
                ReferralEntity.referral_uuid == input_dto.referral_uuid,
                ReferralEntity.is_deleted._is(False),
            )
            .values(is_deleted=True)
        )

        result = await self._adapter.execute(statement=delete_query)
        if result.rowcount == 0:
            raise NotFoundError(resource_type=ReferralEntity.__name__)
