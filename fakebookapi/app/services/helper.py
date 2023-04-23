from enum import StrEnum

def get_pagination_info(resource_type, paging_info, before_id, limit):
    return {
        **paging_info,
        "next": (
            f"/{resource_type}?limit={limit}&before_id={paging_info['last']}"
            if (paging_info['last'] > 1)
            else None
        ),
        "prev": (
            f"/{resource_type}?limit={limit}&before_id={paging_info['before_id'] + limit}"
            if paging_info["before_id"] == (before_id or float("inf"))
            else None
        ),
    }


class UserStatusEnum(StrEnum):

    @classmethod
    def get_enums(cls):
        return (cls.ACTIVE, cls.PRIVATE, cls.DELETED)

    ACTIVE = "ACTIVE"
    PRIVATE = "PRIVATE"
    DELETED = "DELETED"


class PostStatusEnum(StrEnum):

    @classmethod
    def get_enums(cls):
        return (cls.PUBLISHED, cls.DRAFT, cls.DELETED)

    PUBLISHED = "PUBLISHED"
    DRAFT = "DRAFT"
    DELETED = "DELETED"
