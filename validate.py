def validate_args(args):
    defaults = {
        'limit': 50,
        'page': 1,
        'sort': 'id',
        'sort_order': 'asc'
    }

    try:
        data = {
            'limit': int(args.get("limit", defaults["limit"])),
            'page': int(args.get("page", defaults["page"])),
            'sort': str(args.get("sort", defaults["sort"])),
            'sort_order': str(args.get("sort_order", defaults["sort_order"])),
            '_source': {
                'include': ['id', 'title', 'imdb_rating']
            }
        }

        success = data["limit"] >= 0 and data["page"] > 0 and data["sort_order"] in ["asc", "desc"] and data["sort"] in ['id', 'title', 'imdb_rating']

        return {
            "success": success,
            "data": data
        }
    except Exception:
        return {
            "success": False,
            "data": None
        }
