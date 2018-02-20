from boa.code.builtins import concat

class Promo():
    """
    Object for getting storage keys for promo
    """

    # Initialize keys
    promo_id = None
    creator_key = None
    title_key = None
    description_key = None
    price_per_person_key = None
    expiration_key = None
    min_count_key = None
    max_count_key = None
    purchased_count_key = None


def get_promo_storage_keys(promo_id) -> Promo:
    promo = Promo()

    creator_key = concat(promo_id, 'creator')
    title_key = concat(promo_id, 'title')
    description_key = concat(promo_id, 'description')
    price_per_person_key = concat(promo_id, 'price_per_person')
    expiration_key = concat(promo_id, 'expiration')
    min_count_key = concat(promo_id, 'min_count')
    max_count_key = concat(promo_id, 'max_count')
    purchased_count_key = concat(promo_id, 'purchased_count')

    promo.creator_key = creator_key
    promo.title_key = title_key
    promo.description_key = description_key
    promo.price_per_person_key = price_per_person_key
    promo.expiration_key = expiration_key
    promo.min_count_key = min_count_key
    promo.max_count_key = max_count_key
    promo.purchased_count_key = purchased_count_key

    return promo
