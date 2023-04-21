def get_pagination_info(paging_info, before_id, limit):
    return {
        **paging_info,
        "next": (
            f"/posts?limit={limit}&before_id={paging_info['last']}"
            if (paging_info['last'] > 1)
            else None
        ),
        "prev": (
            f"/posts?limit={limit}&before_id={paging_info['before_id'] + limit}"
            if paging_info["before_id"] == (before_id or float("inf"))
            else None
        ),
    }
