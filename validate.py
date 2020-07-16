def validate_args(args):
    try:
        limit = int(args.get("limit", 50))
        page = int(args.get("page", 1))
        sort = str(args.get("sort", "id"))
        sort_order = str(args.get("sort_order", "asc"))
        return {
            "success": limit >= 0 and page > 0 and sort_order in ["asc", "desc"] and sort in ["id"]
        }
    except Exception:
        return {
            "success": False
        }
