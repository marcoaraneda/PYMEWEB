from apps.stores.models import Store

def get_store_by_slug(store_slug: str) -> Store:
    return Store.objects.get(slug=store_slug, is_active=True)
