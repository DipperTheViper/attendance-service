#!/usr/bin/env python3
"""
CRUD Generator for SQLAlchemy Entities - File-based grouping
Generates complete CRUD structure grouped by entity source files
"""

import inspect
import re
import uuid
from pathlib import Path
from typing import Dict, List, Any, get_origin, get_args
from sqlalchemy import Column, UUID as ORM_UUID
from sqlalchemy.orm import Mapped
from archipy.models.entities import UpdatableDeletableEntity
import argparse

# Import your entities here
from src.models.entities import *


def to_snake_case(name: str) -> str:
    """Convert CamelCase to snake_case"""
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def to_kebab_case(name: str) -> str:
    """Convert snake_case to kebab-case"""
    return name.replace("_", "-")


def to_camel_case(name: str) -> str:
    """Convert snake_case to CamelCase"""
    components = name.split("_")
    return "".join(word.capitalize() for word in components)


def get_entity_fields(entity_class) -> Dict[str, Any]:
    """Extract fields from SQLAlchemy entity"""
    fields = {}

    # Get all columns from the table
    if hasattr(entity_class, "__table__"):
        for column in entity_class.__table__.columns:
            column_name = column.name

            # Skip base entity fields
            if column_name in ["created_at", "updated_at", "deleted_at", "is_deleted"]:
                continue

            # Get type info
            python_type = column.type.python_type if hasattr(column.type, "python_type") else str
            is_nullable = column.nullable
            is_primary_key = column.primary_key

            fields[column_name] = {
                "type": python_type,
                "nullable": is_nullable,
                "primary_key": is_primary_key,
                "foreign_key": column.foreign_keys,
                "sqlalchemy_type": column.type,
            }

    # Also check for Mapped annotations
    for name, annotation in getattr(entity_class, "__annotations__", {}).items():
        if name not in fields and not name.startswith("_"):
            origin = get_origin(annotation)
            if origin is not None:
                args = get_args(annotation)
                if args:
                    field_type = args[0]
                else:
                    field_type = str
            else:
                field_type = annotation

            fields[name] = {
                "type": field_type,
                "nullable": True,
                "primary_key": False,
                "foreign_key": set(),
                "sqlalchemy_type": None,
            }

    return fields


def get_primary_key_field(entity_class) -> str:
    """Get the primary key field name"""
    fields = get_entity_fields(entity_class)
    for field_name, field_info in fields.items():
        if field_info["primary_key"]:
            return field_name
    return f"{to_snake_case(entity_class.__name__.replace('Entity', ''))}_uuid"


def get_foreign_key_fields(entity_class) -> List[str]:
    """Get foreign key field names"""
    fields = get_entity_fields(entity_class)
    fk_fields = []
    for field_name, field_info in fields.items():
        if field_info["foreign_key"]:
            fk_fields.append(field_name)
    return fk_fields


def generate_type_annotation(field_type, nullable: bool = False, field_name: str = "", sqlalchemy_type=None) -> str:
    """Generate proper type annotation string based on field type"""
    from sqlalchemy import String, Text, Integer, BigInteger, Boolean, DateTime, Date, Time, Float, Numeric
    from decimal import Decimal
    import datetime

    # Check SQLAlchemy type first for more accurate mapping
    if sqlalchemy_type is not None:
        if isinstance(sqlalchemy_type, (String, Text)):
            base_type = "StrictStr"
        elif isinstance(sqlalchemy_type, (Integer, BigInteger)):
            base_type = "int"
        elif isinstance(sqlalchemy_type, Boolean):
            base_type = "bool"
        elif isinstance(sqlalchemy_type, (DateTime,)):
            base_type = "datetime"
        elif isinstance(sqlalchemy_type, Date):
            base_type = "date"
        elif isinstance(sqlalchemy_type, Time):
            base_type = "time"
        elif isinstance(sqlalchemy_type, (Float, Numeric)):
            base_type = "float"
        elif isinstance(sqlalchemy_type, (ORM_UUID, uuid.UUID)):
            base_type = "UUID"
        else:
            base_type = "StrictStr"
    else:
        # Fallback to Python type mapping
        if field_name.endswith("_at"):
            base_type = "datetime"
        elif field_type == uuid.UUID:
            base_type = "UUID"
        elif field_type == str:
            base_type = "StrictStr"
        elif field_type == int:
            base_type = "int"
        elif field_type == bool:
            base_type = "bool"
        elif field_type == float:
            base_type = "float"
        elif field_type == Decimal:
            base_type = "Decimal"
        elif field_type == datetime.datetime:
            base_type = "datetime"
        elif field_type == datetime.date:
            base_type = "date"
        elif field_type == datetime.time:
            base_type = "time"
        else:
            base_type = "StrictStr"

    if nullable:
        return f"{base_type} | None = None"
    else:
        return base_type


def get_entity_source_file(entity_class) -> str:
    """Get the source file name (without .py) for an entity"""
    module = inspect.getmodule(entity_class)
    if module and hasattr(module, "__file__"):
        file_path = Path(module.__file__)
        return file_path.stem  # Returns filename without extension
    return "unknown"


def group_entities_by_file(entity_classes: List) -> Dict[str, List]:
    """Group entity classes by their source file"""
    grouped = {}
    for entity_class in entity_classes:
        file_name = get_entity_source_file(entity_class)
        if file_name not in grouped:
            grouped[file_name] = []
        grouped[file_name].append(entity_class)
    return grouped


def generate_domain_dtos_for_file(file_name: str, entities: List) -> str:
    """Generate domain interface DTOs for all entities in a file"""
    all_dtos = []

    # Generate DTOs for each entity
    for entity_class in entities:
        entity_name = entity_class.__name__.replace("Entity", "")
        snake_name = to_snake_case(entity_name)
        fields = get_entity_fields(entity_class)
        pk_field = get_primary_key_field(entity_class)

        # Filter fields for different operations
        create_fields = {
            k: v
            for k, v in fields.items()
            if not v["primary_key"] and k not in ["created_at", "updated_at", "deleted_at", "is_deleted"]
        }

        update_fields = {k: v for k, v in create_fields.items()}

        # Create field definitions
        create_field_defs = []
        for field_name, field_info in create_fields.items():
            type_annotation = generate_type_annotation(
                field_info["type"],
                field_info["nullable"],
                field_name,
                field_info["sqlalchemy_type"],
            )
            create_field_defs.append(f"    {field_name}: {type_annotation}")

        update_field_defs = []
        for field_name, field_info in update_fields.items():
            type_annotation = generate_type_annotation(
                field_info["type"],
                True,
                field_name,
                field_info["sqlalchemy_type"],
            )
            update_field_defs.append(f"    {field_name}: {type_annotation}")

        output_field_defs = []
        for field_name, field_info in fields.items():
            type_annotation = generate_type_annotation(
                field_info["type"],
                field_info["nullable"],
                field_name,
                field_info["sqlalchemy_type"],
            )
            output_field_defs.append(f"    {field_name}: {type_annotation}")

        # Generate DTOs for this entity
        entity_dtos = f"""
class Create{entity_name}RestInputDTOV1(BaseDTO):
{chr(10).join(create_field_defs) if create_field_defs else "    pass"}


class Create{entity_name}InputDTOV1(Create{entity_name}RestInputDTOV1):
    user_uuid: UUID | None = None

    @classmethod
    def create(
        cls,
        user_uuid: UUID | None = None,
        input_dto: Create{entity_name}RestInputDTOV1 = None,
    ):
        if input_dto:
            return cls(user_uuid=user_uuid, **input_dto.model_dump(mode="json"))
        return cls(user_uuid=user_uuid)


class Create{entity_name}OutputDTOV1(BaseDTO):
    {pk_field}: UUID


class Get{entity_name}InputDTOV1(BaseDTO):
    {pk_field}: UUID


class Get{entity_name}OutputDTOV1(BaseDTO):
{chr(10).join(output_field_defs)}


class Update{entity_name}RestInputDTOV1(BaseDTO):
{chr(10).join(update_field_defs) if update_field_defs else "    pass"}


class Update{entity_name}InputDTOV1(Update{entity_name}RestInputDTOV1):
    {pk_field}: UUID


class Delete{entity_name}InputDTOV1(BaseDTO):
    {pk_field}: UUID


class Search{entity_name}InputDTOV1(BaseDTO):
    # TODO: Add search fields as needed
    pagination: PaginationDTO
    sort_info: SortDTO[str]  # Replace with appropriate sort enum

    @classmethod
    def create(
        cls,
        page: int = 1,
        page_size: int = 10,
        sort_column: str = "created_at",
        sort_order: SortOrderType = SortOrderType.DESCENDING,
    ):
        pagination = PaginationDTO(page=page, page_size=page_size)
        sort_info = SortDTO[str](column=sort_column, order=sort_order)
        return cls(pagination=pagination, sort_info=sort_info)


class {entity_name}ItemDTOV1(BaseDTO):
{chr(10).join(output_field_defs)}


class Search{entity_name}OutputDTOV1(BaseDTO):
    {snake_name}s: list[{entity_name}ItemDTOV1]
    total: int
"""
        all_dtos.append(entity_dtos)

    # Combine all DTOs with imports at the top
    return f"""from archipy.models.dtos.base_dtos import BaseDTO
from archipy.models.dtos.pagination_dto import PaginationDTO
from archipy.models.dtos.sort_dto import SortDTO
from archipy.models.types.sort_order_type import SortOrderType
from datetime import datetime, date, time
from decimal import Decimal
from pydantic import StrictStr
from uuid import UUID

from src.models.types.enums import *

{chr(10).join(all_dtos)}
"""


def generate_repository_dtos_for_file(file_name: str, entities: List) -> str:
    """Generate repository interface DTOs for all entities in a file"""
    all_dtos = []

    for entity_class in entities:
        entity_name = entity_class.__name__.replace("Entity", "")
        snake_name = to_snake_case(entity_name)
        fields = get_entity_fields(entity_class)
        pk_field = get_primary_key_field(entity_class)

        # Create field definitions
        create_fields = {
            k: v
            for k, v in fields.items()
            if not v["primary_key"] and k not in ["created_at", "updated_at", "deleted_at", "is_deleted"]
        }

        create_field_defs = []
        for field_name, field_info in create_fields.items():
            type_annotation = generate_type_annotation(
                field_info["type"],
                field_info["nullable"],
                field_name,
                field_info["sqlalchemy_type"],
            )
            create_field_defs.append(f"    {field_name}: {type_annotation}")

        entity_dtos = f"""
class Create{entity_name}CommandDTO(BaseDTO):
{chr(10).join(create_field_defs) if create_field_defs else "    pass"}


class Create{entity_name}ResponseDTO(BaseDTO):
    {pk_field}: UUID


class Get{entity_name}QueryDTO(BaseDTO):
    {pk_field}: UUID


class Get{entity_name}ResponseDTO(BaseDTO):
{chr(10).join(f"    {k}: {generate_type_annotation(v['type'], v['nullable'], k, v['sqlalchemy_type'])}" for k, v in fields.items())}


class Update{entity_name}CommandDTO(BaseDTO):
    {pk_field}: UUID
{chr(10).join(f"    {k}: {generate_type_annotation(v['type'], True, k, v['sqlalchemy_type'])}" for k, v in create_fields.items())}


class Delete{entity_name}CommandDTO(BaseDTO):
    {pk_field}: UUID


class Search{entity_name}QueryDTO(BaseDTO):
    # TODO: Add search fields as needed
    pagination: PaginationDTO
    sort_info: SortDTO[str]


class Search{entity_name}ResponseDTO(BaseDTO):
    {snake_name}s: list[Get{entity_name}ResponseDTO]
    total: int
"""
        all_dtos.append(entity_dtos)

    return f"""from archipy.models.dtos.base_dtos import BaseDTO
from archipy.models.dtos.pagination_dto import PaginationDTO
from archipy.models.dtos.sort_dto import SortDTO
from datetime import datetime, date, time
from decimal import Decimal
from pydantic import StrictStr
from uuid import UUID

from src.models.types.enums import *

{chr(10).join(all_dtos)}
"""


def generate_postgres_adapter_for_file(file_name: str, entities: List) -> str:
    """Generate PostgreSQL adapter for all entities in a file"""
    all_methods = []
    all_imports = set()

    for entity_class in entities:
        entity_name = entity_class.__name__.replace("Entity", "")
        snake_name = to_snake_case(entity_name)
        pk_field = get_primary_key_field(entity_class)

        # Add entity to imports
        all_imports.add(entity_class.__name__)

        methods = f"""
    async def create_{snake_name}(self, input_dto: Create{entity_name}CommandDTO) -> Create{entity_name}ResponseDTO:
        _entity = {entity_class.__name__}(**input_dto.model_dump())
        result = await self._adapter.create(entity=_entity)
        return Create{entity_name}ResponseDTO.model_validate(obj=result)

    async def get_{snake_name}(self, input_dto: Get{entity_name}QueryDTO) -> Get{entity_name}ResponseDTO:
        select_query = select({entity_class.__name__}).where({entity_class.__name__}.is_deleted.is_(False))
        _query = self._apply_filter(
            query=select_query,
            field={entity_class.__name__}.{pk_field},
            value=input_dto.{pk_field},
            operation=FilterOperationType.EQUAL,
        )
        result = await self._adapter.execute(statement=_query)
        entity = result.scalar()

        if not entity:
            raise NotFoundError(resource_type={entity_class.__name__}.__name__)

        return Get{entity_name}ResponseDTO.model_validate(obj=entity)

    async def search_{snake_name}s(self, input_dto: Search{entity_name}QueryDTO) -> Search{entity_name}ResponseDTO:
        query: Select = select({entity_class.__name__}).where({entity_class.__name__}.is_deleted.is_(False))

        if input_dto.user_uuid:
            query = self._apply_filter(
                query=query,
                field={entity_class.__name__}.user_uuid,
                value=input_dto.user_uuid,
                operation=FilterOperationType.EQUAL,
            )

        entities, total = await self._adapter.execute_search_query(
            query=query,
            entity={entity_class.__name__},
            sort_info=input_dto.sort_info,
            pagination=input_dto.pagination,
        )

        return Search{entity_name}ResponseDTO({snake_name}s=entities, total=total)

    async def update_{snake_name}(self, input_dto: Update{entity_name}CommandDTO) -> None:
        update_data = input_dto.model_dump(exclude={{"{pk_field}"}}, exclude_none=True)
        if not update_data:
            return

        update_query: Update = (
            update({entity_class.__name__})
            .where(
                {entity_class.__name__}.{pk_field} == input_dto.{pk_field},
                {entity_class.__name__}.is_deleted.is_(False),
            )
            .values(**update_data)
        )

        result = await self._adapter.execute(statement=update_query)
        if result.rowcount == 0:
            raise NotFoundError(resource_type={entity_class.__name__}.__name__)

    async def delete_{snake_name}(self, input_dto: Delete{entity_name}CommandDTO) -> None:
        delete_query = (
            update({entity_class.__name__})
            .where(
                {entity_class.__name__}.{pk_field} == input_dto.{pk_field},
                {entity_class.__name__}.is_deleted.is_(False),
            )
            .values(is_deleted=True)
        )

        result = await self._adapter.execute(statement=delete_query)
        if result.rowcount == 0:
            raise NotFoundError(resource_type={entity_class.__name__}.__name__)
"""
        all_methods.append(methods)

    # Generate DTO imports
    dto_imports = []
    for entity_class in entities:
        entity_name = entity_class.__name__.replace("Entity", "")
        dto_imports.extend(
            [
                f"Create{entity_name}CommandDTO",
                f"Create{entity_name}ResponseDTO",
                f"Get{entity_name}QueryDTO",
                f"Get{entity_name}ResponseDTO",
                f"Update{entity_name}CommandDTO",
                f"Delete{entity_name}CommandDTO",
                f"Search{entity_name}QueryDTO",
                f"Search{entity_name}ResponseDTO",
            ],
        )

    return f"""from archipy.adapters.base.sqlalchemy.adapters import SQLAlchemyFilterMixin
from archipy.adapters.postgres.sqlalchemy.adapters import AsyncPostgresSQLAlchemyAdapter
from archipy.models.errors import NotFoundError
from archipy.models.types.base_types import FilterOperationType
from sqlalchemy import delete, select, update, func, or_
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.expression import Select, Update

from src.models.dtos.{file_name}.repository.{file_name}_repository_interface_dtos import (
    {', '.join(dto_imports)}
)
from src.models.entities import {', '.join(sorted(all_imports))}


class {to_camel_case(file_name)}PostgresAdapter(SQLAlchemyFilterMixin):
    def __init__(self, adapter: AsyncPostgresSQLAlchemyAdapter) -> None:
        self._adapter: AsyncPostgresSQLAlchemyAdapter = adapter
{chr(10).join(all_methods)}
"""


def generate_repository_for_file(file_name: str, entities: List) -> str:
    """Generate repository for all entities in a file"""
    all_methods = []
    dto_imports = []

    for entity_class in entities:
        entity_name = entity_class.__name__.replace("Entity", "")
        snake_name = to_snake_case(entity_name)

        dto_imports.extend(
            [
                f"Create{entity_name}CommandDTO",
                f"Create{entity_name}ResponseDTO",
                f"Get{entity_name}QueryDTO",
                f"Get{entity_name}ResponseDTO",
                f"Update{entity_name}CommandDTO",
                f"Delete{entity_name}CommandDTO",
                f"Search{entity_name}QueryDTO",
                f"Search{entity_name}ResponseDTO",
            ],
        )

        methods = f"""
    async def create_{snake_name}(self, input_dto: Create{entity_name}CommandDTO) -> Create{entity_name}ResponseDTO:
        return await self._postgres_adapter.create_{snake_name}(input_dto=input_dto)

    async def get_{snake_name}(self, input_dto: Get{entity_name}QueryDTO) -> Get{entity_name}ResponseDTO:
        return await self._postgres_adapter.get_{snake_name}(input_dto=input_dto)

    async def search_{snake_name}s(self, input_dto: Search{entity_name}QueryDTO) -> Search{entity_name}ResponseDTO:
        return await self._postgres_adapter.search_{snake_name}s(input_dto=input_dto)

    async def update_{snake_name}(self, input_dto: Update{entity_name}CommandDTO) -> None:
        await self._postgres_adapter.update_{snake_name}(input_dto=input_dto)

    async def delete_{snake_name}(self, input_dto: Delete{entity_name}CommandDTO) -> None:
        await self._postgres_adapter.delete_{snake_name}(input_dto=input_dto)
"""
        all_methods.append(methods)

    return f"""from src.models.dtos.{file_name}.repository.{file_name}_repository_interface_dtos import (
    {', '.join(dto_imports)}
)
from src.repositories.{file_name}.adapters.{file_name}_postgres_adapter import {to_camel_case(file_name)}PostgresAdapter


class {to_camel_case(file_name)}Repository:
    def __init__(self, postgres_adapter: {to_camel_case(file_name)}PostgresAdapter):
        self._postgres_adapter: {to_camel_case(file_name)}PostgresAdapter = postgres_adapter
{chr(10).join(all_methods)}
"""


def generate_logic_for_file(file_name: str, entities: List) -> str:
    """Generate logic layer for all entities in a file"""
    all_methods = []
    domain_dto_imports = []
    repo_dto_imports = []

    for entity_class in entities:
        entity_name = entity_class.__name__.replace("Entity", "")
        snake_name = to_snake_case(entity_name)
        pk_field = get_primary_key_field(entity_class)

        domain_dto_imports.extend(
            [
                f"Create{entity_name}InputDTOV1",
                f"Create{entity_name}OutputDTOV1",
                f"Get{entity_name}InputDTOV1",
                f"Get{entity_name}OutputDTOV1",
                f"Update{entity_name}InputDTOV1",
                f"Delete{entity_name}InputDTOV1",
                f"Search{entity_name}InputDTOV1",
                f"Search{entity_name}OutputDTOV1",
            ],
        )

        repo_dto_imports.extend(
            [
                f"Create{entity_name}CommandDTO",
                f"Create{entity_name}ResponseDTO",
                f"Get{entity_name}QueryDTO",
                f"Get{entity_name}ResponseDTO",
                f"Update{entity_name}CommandDTO",
                f"Delete{entity_name}CommandDTO",
                f"Search{entity_name}QueryDTO",
                f"Search{entity_name}ResponseDTO",
            ],
        )

        methods = f"""
    @async_postgres_sqlalchemy_atomic_decorator
    async def create_{snake_name}(self, input_dto: Create{entity_name}InputDTOV1) -> Create{entity_name}OutputDTOV1:
        command = Create{entity_name}CommandDTO.model_validate(input_dto)
        response: Create{entity_name}ResponseDTO = await self._repository.create_{snake_name}(input_dto=command)
        return Create{entity_name}OutputDTOV1.model_validate(obj=response)

    @async_postgres_sqlalchemy_atomic_decorator
    async def get_{snake_name}(self, input_dto: Get{entity_name}InputDTOV1) -> Get{entity_name}OutputDTOV1:
        query = Get{entity_name}QueryDTO.model_validate(obj=input_dto)
        response: Get{entity_name}ResponseDTO = await self._repository.get_{snake_name}(input_dto=query)
        return Get{entity_name}OutputDTOV1.model_validate(obj=response)

    @async_postgres_sqlalchemy_atomic_decorator
    async def search_{snake_name}s(self, input_dto: Search{entity_name}InputDTOV1) -> Search{entity_name}OutputDTOV1:
        repository_dto = Search{entity_name}QueryDTO.model_validate(input_dto)
        response: Search{entity_name}ResponseDTO = await self._repository.search_{snake_name}s(input_dto=repository_dto)
        return Search{entity_name}OutputDTOV1.model_validate(response)

    @async_postgres_sqlalchemy_atomic_decorator
    async def update_{snake_name}(self, input_dto: Update{entity_name}InputDTOV1) -> None:
        command = Update{entity_name}CommandDTO.model_validate(obj=input_dto)
        await self._repository.update_{snake_name}(input_dto=command)

    @async_postgres_sqlalchemy_atomic_decorator
    async def delete_{snake_name}(self, input_dto: Delete{entity_name}InputDTOV1) -> None:
        command = Delete{entity_name}CommandDTO.model_validate(obj=input_dto)
        await self._repository.delete_{snake_name}(input_dto=command)
"""
        all_methods.append(methods)

    return f"""from archipy.helpers.decorators.sqlalchemy_atomic import async_postgres_sqlalchemy_atomic_decorator
from uuid import UUID

from src.models.dtos.{file_name}.domain.v1.{file_name}_domain_interface_dtos import (
    {', '.join(domain_dto_imports)}
)
from src.models.dtos.{file_name}.repository.{file_name}_repository_interface_dtos import (
    {', '.join(repo_dto_imports)}
)
from src.repositories.{file_name}.{file_name}_repository import {to_camel_case(file_name)}Repository


class {to_camel_case(file_name)}Logic:
    def __init__(
        self,
        repository: {to_camel_case(file_name)}Repository,
    ) -> None:
        self._repository: {to_camel_case(file_name)}Repository = repository
{chr(10).join(all_methods)}
"""


def generate_service_for_file(file_name: str, entities: List) -> str:
    """Generate FastAPI service for all entities in a file"""
    all_endpoints = []
    dto_imports = []
    router_type_name = file_name.upper()

    for entity_class in entities:
        entity_name = entity_class.__name__.replace("Entity", "")
        snake_name = to_snake_case(entity_name)
        kebab_name = to_kebab_case(snake_name)
        pk_field = get_primary_key_field(entity_class)

        dto_imports.extend(
            [
                f"Create{entity_name}RestInputDTOV1",
                f"Create{entity_name}InputDTOV1",
                f"Create{entity_name}OutputDTOV1",
                f"Get{entity_name}InputDTOV1",
                f"Get{entity_name}OutputDTOV1",
                f"Update{entity_name}RestInputDTOV1",
                f"Update{entity_name}InputDTOV1",
                f"Delete{entity_name}InputDTOV1",
                f"Search{entity_name}InputDTOV1",
                f"Search{entity_name}OutputDTOV1",
            ],
        )

        endpoints = f"""

@routerV1.post(
    path="/{{user_uuid}}/{kebab_name}s",
    response_model=Create{entity_name}OutputDTOV1,
)
@inject
async def create_{snake_name}(
    user_uuid: UUID,
    input_dto: Create{entity_name}RestInputDTOV1,
    logic: {to_camel_case(file_name)}Logic = Depends(Provide[ServiceContainer.{file_name}_logic]),
) -> Create{entity_name}OutputDTOV1:
    input_dto = Create{entity_name}InputDTOV1.create(user_uuid=user_uuid, input_dto=input_dto)
    return await logic.create_{snake_name}(input_dto=input_dto)


@routerV1.get(
    path="/{{user_uuid}}/{kebab_name}s/{{{pk_field}}}",
    response_model=Get{entity_name}OutputDTOV1,
    responses=Utils.get_fastapi_exception_responses([NotFoundError]),
)
@inject
async def get_{snake_name}(
    user_uuid: UUID,
    {pk_field}: UUID,
    logic: {to_camel_case(file_name)}Logic = Depends(Provide[ServiceContainer.{file_name}_logic]),
) -> Get{entity_name}OutputDTOV1:
    input_dto = Get{entity_name}InputDTOV1({pk_field}={pk_field})
    return await logic.get_{snake_name}(input_dto=input_dto)


@routerV1.get(
    path="/{{user_uuid}}/{kebab_name}s",
    response_model=Search{entity_name}OutputDTOV1,
)
@inject
async def search_{snake_name}s(
    user_uuid: UUID,
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=10, ge=1, le=100, description="Number of items per page"),
    logic: {to_camel_case(file_name)}Logic = Depends(Provide[ServiceContainer.{file_name}_logic]),
) -> Search{entity_name}OutputDTOV1:
    input_dto = Search{entity_name}InputDTOV1.create(
        page=page,
        page_size=page_size,
    )
    return await logic.search_{snake_name}s(input_dto=input_dto)


@routerV1.put(
    path="/{{user_uuid}}/{kebab_name}s/{{{pk_field}}}",
)
@inject
async def update_{snake_name}(
    user_uuid: UUID,
    {pk_field}: UUID,
    input_dto: Update{entity_name}RestInputDTOV1,
    logic: {to_camel_case(file_name)}Logic = Depends(Provide[ServiceContainer.{file_name}_logic]),
) -> None:
    update_dto = Update{entity_name}InputDTOV1(**input_dto.model_dump(), {pk_field}={pk_field})
    await logic.update_{snake_name}(input_dto=update_dto)


@routerV1.delete(
    path="/{{user_uuid}}/{kebab_name}s/{{{pk_field}}}",
)
@inject
async def delete_{snake_name}(
    user_uuid: UUID,
    {pk_field}: UUID,
    logic: {to_camel_case(file_name)}Logic = Depends(Provide[ServiceContainer.{file_name}_logic]),
) -> None:
    input_dto = Delete{entity_name}InputDTOV1({pk_field}={pk_field})
    await logic.delete_{snake_name}(input_dto=input_dto)
"""
        all_endpoints.append(endpoints)

    return f"""from archipy.models.errors import NotFoundError
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query
from uuid import UUID

from src.configs.containers import ServiceContainer
from src.logics.{file_name}.{file_name}_logic import {to_camel_case(file_name)}Logic
from src.models.dtos.{file_name}.domain.v1.{file_name}_domain_interface_dtos import (
    {', '.join(sorted(set(dto_imports)))}
)
from src.models.types.api_router_type import ApiRouterType
from src.utils.utils import Utils

routerV1: APIRouter = APIRouter(tags=[ApiRouterType.{router_type_name}])

{chr(10).join(all_endpoints)}
"""


def generate_api_router_type_addition(file_name: str) -> str:
    """Generate API router type addition"""
    display_name = file_name.replace("_", " ").title()
    return f'    {file_name.upper()} = "📋 {display_name.upper()}"'


def generate_container_additions(file_name: str) -> str:
    """Generate dependency injection container additions"""
    camel_name = to_camel_case(file_name)

    return f"""
    # region {file_name}
    _{file_name}_postgres_adapter = providers.ThreadSafeSingleton(
        {camel_name}PostgresAdapter,
        adapter=_postgres_adapter,
    )
    _{file_name}_repository = providers.ThreadSafeSingleton(
        {camel_name}Repository,
        postgres_adapter=_{file_name}_postgres_adapter,
    )
    {file_name}_logic = providers.ThreadSafeSingleton(
        {camel_name}Logic,
        repository=_{file_name}_repository,
    )
    # endregion
"""


def generate_dispatcher_additions(file_name: str) -> str:
    """Generate dispatcher additions"""
    return f"""from src.services.{file_name}.v1 import {file_name}_service

    app.include_router(
        router={file_name}_service.routerV1,
        prefix="/api/v1/users",
        dependencies=dependencies,
        responses=common_private_response,
    )"""


def create_directories(base_path: Path, file_name: str):
    """Create necessary directory structure"""
    directories = [
        f"src/models/dtos/{file_name}",
        f"src/models/dtos/{file_name}/domain",
        f"src/models/dtos/{file_name}/domain/v1",
        f"src/models/dtos/{file_name}/repository",
        f"src/repositories/{file_name}",
        f"src/repositories/{file_name}/adapters",
        f"src/logics/{file_name}",
        f"src/services/{file_name}",
        f"src/services/{file_name}/v1",
    ]

    for directory in directories:
        dir_path = base_path / directory
        dir_path.mkdir(parents=True, exist_ok=True)

        # Create __init__.py files
        init_file = dir_path / "__init__.py"
        if not init_file.exists():
            init_file.write_text("")


def write_file(file_path: Path, content: str, dry_run: bool = False):
    """Write content to file or print to stdout if dry_run is True"""
    if dry_run:
        print(f"\n{'=' * 80}")
        print(f"FILE: {file_path}")
        print(f"{'=' * 80}")
        print(content)
        print(f"{'=' * 80}")
    else:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
        print(f"Generated: {file_path}")


def generate_crud_for_file(file_name: str, entities: List, base_path: Path = Path("."), dry_run: bool = False):
    """Generate complete CRUD structure for all entities in a file"""
    print(f"Generating CRUD for file: {file_name}")
    print(f"  Entities: {', '.join([e.__name__ for e in entities])}")

    if not dry_run:
        # Create directories only if not dry run
        create_directories(base_path, file_name)

    # Generate domain DTOs
    domain_dtos = generate_domain_dtos_for_file(file_name, entities)
    write_file(
        base_path / f"src/models/dtos/{file_name}/domain/v1/{file_name}_domain_interface_dtos.py",
        domain_dtos,
        dry_run,
    )

    # Generate repository DTOs
    repository_dtos = generate_repository_dtos_for_file(file_name, entities)
    write_file(
        base_path / f"src/models/dtos/{file_name}/repository/{file_name}_repository_interface_dtos.py",
        repository_dtos,
        dry_run,
    )

    # Generate PostgreSQL adapter
    postgres_adapter = generate_postgres_adapter_for_file(file_name, entities)
    write_file(
        base_path / f"src/repositories/{file_name}/adapters/{file_name}_postgres_adapter.py",
        postgres_adapter,
        dry_run,
    )

    # Generate repository
    repository = generate_repository_for_file(file_name, entities)
    write_file(base_path / f"src/repositories/{file_name}/{file_name}_repository.py", repository, dry_run)

    # Generate logic
    logic = generate_logic_for_file(file_name, entities)
    write_file(base_path / f"src/logics/{file_name}/{file_name}_logic.py", logic, dry_run)

    # Generate service
    service = generate_service_for_file(file_name, entities)
    write_file(base_path / f"src/services/{file_name}/v1/{file_name}_service.py", service, dry_run)

    # Print additions needed
    container_additions = generate_container_additions(file_name)
    dispatcher_additions = generate_dispatcher_additions(file_name)
    api_router_type_addition = generate_api_router_type_addition(file_name)

    if dry_run:
        print(f"\n{'=' * 80}")
        print(f"CONTAINER ADDITIONS FOR {file_name}")
        print(f"{'=' * 80}")
        print(container_additions)

        print(f"\n{'=' * 80}")
        print(f"DISPATCHER ADDITIONS FOR {file_name}")
        print(f"{'=' * 80}")
        print(dispatcher_additions)

        print(f"\n{'=' * 80}")
        print(f"API ROUTER TYPE ADDITION FOR {file_name}")
        print(f"{'=' * 80}")
        print(api_router_type_addition)
    else:
        print(f"\n=== CONFIGURATION UPDATES FOR {file_name} ===")
        print(f"\n1. Add this to your containers.py file:")
        print(container_additions)

        print(f"\n2. Add this to your dispatcher.py file in set_dispatch_routes function:")
        print(dispatcher_additions)

        print(f"\n3. Add this to your ApiRouterType enum in api_router_type.py:")
        print(api_router_type_addition)

    print(f"\nCRUD generation completed for {file_name}!")
    print("=" * 60)


def main():
    """Main function to generate CRUD grouped by entity files"""
    parser = argparse.ArgumentParser(description="CRUD Generator for SQLAlchemy Entities - File-based grouping")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print generated code to stdout instead of writing to files",
    )
    parser.add_argument("--file", type=str, help="Generate CRUD for specific file by name (e.g., 'user')")

    args = parser.parse_args()

    # Get all entity classes
    entity_classes = []

    # Import all entities from the entities module
    import src.models.entities as entities_module

    for name in dir(entities_module):
        obj = getattr(entities_module, name)
        if (
            inspect.isclass(obj)
            and issubclass(obj, UpdatableDeletableEntity)
            and obj != UpdatableDeletableEntity
            and name.endswith("Entity")
        ):
            entity_classes.append(obj)

    if not entity_classes:
        print("No entity classes found!")
        return

    # Group entities by file
    grouped_entities = group_entities_by_file(entity_classes)

    if args.file:
        # Generate for specific file
        if args.file in grouped_entities:
            generate_crud_for_file(args.file, grouped_entities[args.file], dry_run=args.dry_run)
        else:
            print(f"File '{args.file}' not found!")
            print("Available files:")
            for file_name in sorted(grouped_entities.keys()):
                print(f"  - {file_name} ({len(grouped_entities[file_name])} entities)")
        return

    print(f"Found {len(entity_classes)} entity classes in {len(grouped_entities)} files:")
    for i, (file_name, entities) in enumerate(sorted(grouped_entities.items())):
        entity_names = ", ".join([e.__name__ for e in entities])
        print(f"{i + 1}. {file_name}.py ({len(entities)} entities): {entity_names}")

    print("\nChoose an option:")
    print("0. Generate CRUD for all files")
    print("1-N. Generate CRUD for specific file")

    try:
        choice = int(input("Enter your choice: "))

        if choice == 0:
            # Generate for all files
            for file_name, entities in sorted(grouped_entities.items()):
                generate_crud_for_file(file_name, entities, dry_run=args.dry_run)
                print("-" * 50)
        elif 1 <= choice <= len(grouped_entities):
            # Generate for specific file
            file_name = sorted(grouped_entities.keys())[choice - 1]
            entities = grouped_entities[file_name]
            generate_crud_for_file(file_name, entities, dry_run=args.dry_run)
        else:
            print("Invalid choice!")

    except ValueError:
        print("Please enter a valid number!")
    except KeyboardInterrupt:
        print("\nOperation cancelled!")
    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
