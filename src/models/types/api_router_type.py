from enum import Enum


class ApiRouterType(Enum):
    USER = "👤 USER"
    AUTHENTICATION = "🔐 AUTHENTICATION"
    REFERRAL = "🤝 REFERRAL"
    OBJECT_STORAGE = "🏪 Object Storage"
    FILE = "📂 Files"

    # ADMINs
    ADMIN_AUTH = "⚖ ADMIN AUTH"
    ADMIN = "🕵 ADMIN"
