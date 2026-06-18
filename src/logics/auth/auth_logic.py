import secrets
from uuid import UUID

from archipy.helpers.decorators.sqlalchemy_atomic import async_postgres_sqlalchemy_atomic_decorator
from archipy.models.errors import NotFoundError, InvalidArgumentError
from async_lru import alru_cache

from src.configs.runtime_config import RuntimeConfig
from src.logics.referral.referral_logic import ReferralLogic
from src.logics.user.user_logic import UserLogic
from src.models.dtos.auth.domain_interface.v1.auth_domain_interface_dtos import (
    CreateTOTPInputDTOV1,
    CreateTOTPOutputDTOV1,
    RefreshTokenInputDTOV1,
    RefreshTokenOutputDTOV1,
    VerifyTOTPInputDTOV1,
    VerifyTOTPOutputDTOV1,
    LoginOutputDTOV1,
    LoginInputDTOV1,
)
from src.models.dtos.auth.repository_interface.auth_repository_interface_dtos import (
    CreateTOTPCommandDTO,
    CreateTOTPResponseDTO,
    VerifyTOTPCommandDTO,
)
from src.models.dtos.user.domain.v1.user_domain_interface_dtos import (
    GetUserInputDTOV1,
    SearchAuthUserInputDTOV1,
    SearchAuthUsersOutputDTOV1,
    GetAdminUserInputDTOV1,
    GetAdminUserOutputDTOV1,
)
from src.models.exceptions.auth import AuthPermissionDeniedError
from src.repositories.auth.auth_repository import AuthRepository
from src.utils.utils import Utils


class AuthLogic:
    def __init__(
        self,
        repository: AuthRepository,
        user_logic: UserLogic = None,
        referral_logic: ReferralLogic = None,
    ) -> None:
        self._repository = repository
        self._user_logic: UserLogic = user_logic
        self._referral_logic: ReferralLogic = referral_logic

    @async_postgres_sqlalchemy_atomic_decorator
    async def create_totp(self, input_dto: CreateTOTPInputDTOV1) -> CreateTOTPOutputDTOV1:
        referer_uuid = None
        # if (_code := input_dto.referral_code) is not None:
        #     referer_uuid = await self._referral_logic.check_referral_code(input_dto.referral_code)
        user_output_dto = await self._get_cashed_auth_user(
            input_dto=SearchAuthUserInputDTOV1(phone_number=input_dto.phone_number, referer_uuid=referer_uuid),
        )

        totp, expire_in = Utils.generate_totp(secret=user_output_dto.user_uuid)

        totp_is_expire: bool = False

        create_totp_command = CreateTOTPCommandDTO(
            totp_code=totp,
            nonce_code=secrets.token_hex(5),
            phone_number=input_dto.phone_number,
            is_expire=totp_is_expire,
            expire_time=expire_in,
        )
        # todo: change this after domain change
        message = f"""کد تایید شما : {totp}"""
        print(message)
        sms_input_dto = ...

        totp_dto: CreateTOTPResponseDTO = await self._repository.create_totp(command=create_totp_command)

        # send the otp

        return CreateTOTPOutputDTOV1(
            phone_number=input_dto.phone_number,
            nonce_code=totp_dto.nonce_code,
            expires_in=expire_in,
        )

    @async_postgres_sqlalchemy_atomic_decorator
    async def verify_totp(self, input_dto: VerifyTOTPInputDTOV1) -> VerifyTOTPOutputDTOV1:
        # await self._verify_totp(input_dto=input_dto)

        user_output_dto = await self._get_cashed_auth_user(
            input_dto=SearchAuthUserInputDTOV1(phone_number=input_dto.phone_number),
        )
        if not user_output_dto.user_uuid:
            raise NotFoundError(resource_type="UserEntity")

        await self._check_user_exist(user_uuid=user_output_dto.user_uuid)

        access_token: str = Utils.create_access_token(
            user_uuid=user_output_dto.user_uuid,
        )
        refresh_token: str = Utils.create_refresh_token(user_uuid=user_output_dto.user_uuid)
        return VerifyTOTPOutputDTOV1(access_token=access_token, refresh_token=refresh_token)

    async def _verify_totp(self, input_dto: VerifyTOTPInputDTOV1) -> None:
        try:
            command = VerifyTOTPCommandDTO.model_validate(obj=input_dto)
            await self._repository.verify_totp(command=command)
        except NotFoundError as exception:
            raise InvalidArgumentError(argument_name="totp") from exception
        except Exception as exception:
            raise exception

    @alru_cache(ttl=RuntimeConfig.global_config().AUTH_GET_USER_CACHE_EXPIRATION_SECONDS)
    async def _get_cashed_auth_user(
        self,
        input_dto: SearchAuthUserInputDTOV1,
    ) -> SearchAuthUsersOutputDTOV1:
        return await self._user_logic.search_auth_users(input_dto=input_dto)

    @alru_cache(ttl=RuntimeConfig.global_config().AUTH_GET_USER_CACHE_EXPIRATION_SECONDS)
    async def _check_user_exist(self, user_uuid: UUID) -> None:
        try:
            isinstance(user_uuid, UUID)  # Basic type check
            await self._user_logic.get_user(input_dto=GetUserInputDTOV1(user_uuid=user_uuid))
        except NotFoundError as exception:
            raise NotFoundError(resource_type="UserEntity") from exception
        except InvalidArgumentError as exception:
            raise InvalidArgumentError(argument_name="user_uuid") from exception
        except Exception as exception:
            raise exception

    @async_postgres_sqlalchemy_atomic_decorator
    async def refresh_token(self, input_dto: RefreshTokenInputDTOV1) -> RefreshTokenOutputDTOV1:
        payload: dict[str, any] = Utils.decode_token(token=input_dto.refresh_token, verify_type="refresh")
        user_uuid: UUID = Utils.extract_user_uuid(payload=payload)
        access_token: str = Utils.create_access_token(
            user_uuid=user_uuid,
        )
        return RefreshTokenOutputDTOV1(access_token=access_token)

    @async_postgres_sqlalchemy_atomic_decorator
    async def login(self, input_dto: LoginInputDTOV1) -> LoginOutputDTOV1:
        user_input_dto: GetAdminUserInputDTOV1 = GetAdminUserInputDTOV1(username=input_dto.username)
        user_output_dto: GetAdminUserOutputDTOV1 = await self._user_logic.get_admin_user(input_dto=user_input_dto)

        if not Utils.verify_password(
            password=input_dto.password,
            stored_password=user_output_dto.hashed_password,
        ):
            raise AuthPermissionDeniedError()

        access_token: str = Utils.create_access_token(user_uuid=user_output_dto.user_uuid)
        refresh_token: str = Utils.create_refresh_token(user_uuid=user_output_dto.user_uuid)
        return LoginOutputDTOV1(access_token=access_token, refresh_token=refresh_token)
