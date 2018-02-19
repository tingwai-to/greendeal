from boa.blockchain.vm.Neo.Blockchain import GetHeight, GetHeader
from boa.blockchain.vm.Neo.Runtime import Log, GetTrigger, CheckWitness
from boa.blockchain.vm.Neo.Storage import Get, GetContext, Put, Delete
from boa.code.builtins import concat


def Main(operation, args):
#     trigger = GetTrigger()
#     if trigger == Verification():
#         is_owner = CheckWitness(OWNER)
#         if is_owner:
#             return True
#         return False

    # elif trigger == Application():
    # seller action
    if operation == 'create':
        if len(args) == 8:
            creator = args[0]  # public key
            promo_id = args[1]
            title = args[2]
            description = args[3]
            price_per_person = args[4]
            expiration = args[5]
            min_headcount = args[6]
            max_headcount = args[7]

            success = CreatePromo(creator, promo_id, title, description, price_per_person, expiration, min_headcount, max_headcount)

            if success:
                Log('Promo created')
                return True
            else:
                Log('Exiting')
                return False
        else:
            Log('incorrect number of arguments')
            return False

    # seller action
    elif operation == 'delete':
        if len(args) == 1:
            promo_id = args[0]

            authorize = IsPromoCreator(promo_id)
            if authorize:
                DeletePromo(promo_id)
                Log('Promo successfully deleted')
                return True
            else:
                Log('Permission denied')
                return False
        else:
            Log('incorrect number of arguments')
            return False

    # seller action
    elif operation == 'claim':
        if len(args) == 1:
            promo_id = args[0]

            authorize = IsPromoCreator(promo_id)
            if authorize:
                ClaimFunds(promo_id)
                Log('Promo funds successfully claimed')
                return True
            else:
                Log('Permission denied')
                return False
        else:
            Log('incorrect number of arguments')
            return False

    # buyer action
    elif operation == 'buy':
        if len(args) == 3:
            buyer = args[0]
            promo_id = args[1]
            quantity = args[2]

            success = BuyPromo(buyer, promo_id, quantity)

            if success:
                Log('Promo successfully purchased')
                return True
            else:
                Log('Exiting')
                return False
        else:
            Log('incorrect number of arguments')
            return False

    # buyer action
    elif operation == 'refund':
        if len(args) == 2:
            buyer = args[0]
            promo_id = args[1]

            success = RefundPromo(buyer, promo_id)

            if success:
                Log('Refund claimed successfully')
                return True
            else:
                Log('Exiting')
                return False
        else:
            Log('incorrect number of arguments')
            return False

    # buyer/seller action
    elif operation == 'details':
        if len(args) == 1:
            promo_id = args[0]
            Details(promo_id)
            return True
        else:
            Log('incorrect number of arguments')
            return False

    else:
        Log('operation not found')
        return False


def CreatePromo(creator, promo_id, title, description, price_per_person, expiration, min_headcount, max_headcount):
    """
    Create a promo and "register" the details onto the blockchain/storage.

    Args:
        creator (str): public key
        promo_id (str):
        title (str): can not contain spaces
        description (str): can not contain spaces
        price_per_person (int): floats not supported in VM
        expiration (int): use unix GMT time
        min_headcount (int):
        max_headcount (int):

    Returns:
        (bool): True if promo created successfully
    """
    if price_per_person < 0:
        Log('price_per_person must be positive')
        return False

    if min_headcount <= 0:
        Log('min_headcount must be greater than zero')
        return False

    if min_headcount > max_headcount:
        Log('min_headcount must be less than or equal to max_headcount')
        return False

    height = GetHeight()
    current_block = GetHeader(height)
    current_time = current_block.Timestamp

    if current_time > expiration:
        Log('expiration must be greater than current time. '
            'Note: use unix GMT time')
        return False

    promo_exists = IsPromoExist(promo_id)
    if promo_exists:
        Log('promo_id is already taken')
        return False

    creator_key = concat(promo_id, 'creator')
    title_key = concat(promo_id, 'title')
    description_key = concat(promo_id, 'description')
    price_per_person_key = concat(promo_id, 'price_per_person')
    expiration_key = concat(promo_id, 'expiration')
    min_headcount_key = concat(promo_id, 'min_headcount')
    max_headcount_key = concat(promo_id, 'max_headcount')
    purchased_headcount_key = concat(promo_id, 'purchased_headcount')

    context = GetContext()
    Put(context, promo_id, True)  # promo_exists
    Put(context, creator_key, creator)
    Put(context, title_key, title)
    Put(context, description_key, description)
    Put(context, price_per_person_key, price_per_person)
    Put(context, expiration_key, expiration)
    Put(context, min_headcount_key, min_headcount)
    Put(context, max_headcount_key, max_headcount)
    Put(context, purchased_headcount_key, 0)

    return True


def BuyPromo(buyer, promo_id, quantity):
    """
    Purchase <quantity> tickets for promo. Buyer public key + quantity bought
    is also stored in case of refund.

    Args:
        buyer (str): buyer's public key
        promo_id (str):
        quantity (int):

    Returns:
        (bool): True if promo purchased successfully
    """
    promo_exists = IsPromoExist(promo_id)
    if not promo_exists:
        Log('Promo not found')
        return False

    context = GetContext()
    purchased_headcount_key = concat(promo_id, 'purchased_headcount')
    purchased_headcount = Get(context, purchased_headcount_key)
    max_headcount_key = concat(promo_id, 'max_headcount')
    max_headcount = Get(context, max_headcount_key)

    remaining = max_headcount - purchased_headcount

    if remaining == 0:
        Log('Promo has sold out!')
        return False

    if quantity < 1:
        Log('Please enter quantity of at least one')
        return False

    if remaining - quantity < 0:
        Log('Not enough tickets remaining, available amount: ')
        Log(remaining)
        return False

    expired = IsPromoExpired(promo_id)
    if expired:
        Log('Promo has expired!')
        return False

    buyer_key = concat(promo_id, buyer)
    purchased_quantity = Get(context, buyer_key)
    if purchased_quantity:
        Log('Promo already claimed using given public key')
        return False

    purchased_headcount += quantity
    Put(context, purchased_headcount_key, purchased_headcount)

    buyer_key = concat(promo_id, buyer)
    Put(context, buyer_key, quantity)

    # TODO: subtract funds from account

    return True


def DeletePromo(promo_id):
    expired = IsPromoExpired(promo_id)
    if expired:
        Log('Promo has already finished, can no longer delete it!')
        return False

    context = GetContext()
    Delete(context, promo_id)  # delete promo_exists

    return True


def ClaimFunds(promo_id):
    promo_exists = IsPromoExist(promo_id)
    if not promo_exists:
        Log('Promo not found')
        return False

    expired = IsPromoExpired(promo_id)
    if not expired:
        Log('Promo not over yet! Cannot claim funds yet')
        return False

    context = GetContext()
    min_headcount_key = concat(promo_id, 'min_headcount')
    min_headcount = Get(context, min_headcount_key)
    purchased_headcount_key = concat(promo_id, 'purchased_headcount')
    purchased_headcount = Get(context, purchased_headcount_key)

    if purchased_headcount < min_headcount:
        Log('Not enough tickets were sold by deadline, buyers can claim refund')
        return False

    price_per_person_key = concat(promo_id, 'price_per_person')
    price_per_person = Get(context, price_per_person_key)

    funds_amount = purchased_headcount * price_per_person
    # TODO: transfer funds to promo creator

    return True


def RefundPromo(buyer, promo_id):
    """
    Refund all of buyer's purchased tickets for specified promo

    Args:
        buyer (str): buyer's public key
        promo_id (str):

    Returns:
        (bool): True if successfully refunded
    """
    promo_exists = IsPromoExist(promo_id)
    if not promo_exists:
        Log('Promo not found')
        return False

    context = GetContext()
    expired = IsPromoExpired(promo_id)

    min_headcount_key = concat(promo_id, 'min_headcount')
    min_headcount = Get(context, min_headcount_key)
    purchased_headcount_key = concat(promo_id, 'purchased_headcount')
    purchased_headcount = Get(context, purchased_headcount_key)

    if expired and purchased_headcount > min_headcount:
        Log('Promo refund deadline has passed')
        return False

    buyer_key = concat(promo_id, buyer)
    refund_quantity = Get(context, buyer_key)
    if not refund_quantity:
        Log('No purchases were made using given public key')
        return False

    Delete(context, buyer_key)

    price_per_person_key = concat(promo_id, 'price_per_person')
    price_per_person = Get(context, price_per_person_key)

    refund_amount = refund_quantity * price_per_person
    # TODO: refund to wallet

    # update purchased_headcount
    purchased_headcount -= refund_quantity
    Put(context, purchased_headcount_key, purchased_headcount)

    return True


def Details(promo_id):
    """
    Prints details of specified promo into CLI:
    Creator, Title, Description, Price/person, Expiration Date, Min Headcount,
    Max Headcount, Purchased Headcount

    Args:
        promo_id (str):

    Returns:
        (bool): True if promo found and details successfully printed
    """
    promo_exists = IsPromoExist(promo_id)
    if not promo_exists:
        Log('Promo not found')
        return False

    context = GetContext()
    creator_key = concat(promo_id, 'creator')
    title_key = concat(promo_id, 'title')
    description_key = concat(promo_id, 'description')
    price_per_person_key = concat(promo_id, 'price_per_person')
    expiration_key = concat(promo_id, 'expiration')
    min_headcount_key = concat(promo_id, 'min_headcount')
    max_headcount_key = concat(promo_id, 'max_headcount')
    purchased_headcount_key = concat(promo_id, 'purchased_headcount')

    creator = Get(context, creator_key)
    title = Get(context, title_key)
    description = Get(context, description_key)
    price_per_person = Get(context, price_per_person_key)
    expiration = Get(context, expiration_key)
    min_headcount = Get(context, min_headcount_key)
    max_headcount = Get(context, max_headcount_key)
    purchased_headcount = Get(context, purchased_headcount_key)

    Log('Creator, Title, Description, Price/person, Expiration Date, '
        'Minimum Headcount, Maximum Headcount, Purchased Headcount')
    Log(creator)
    Log(title)
    Log(description)
    Log(price_per_person)
    Log(expiration)
    Log(min_headcount)
    Log(max_headcount)
    Log(purchased_headcount)

    return True


def IsPromoCreator(promo_id):
    """
    Check if smart contract invoker is creator of promo

    Args:
        promo_id (str):

    Returns:
        (bool): True if contract invoker is creator of promo
    """
    promo_exists = IsPromoExist(promo_id)
    if not promo_exists:
        Log('Promo not found')
        return False

    context = GetContext()
    creator_key = concat(promo_id, 'creator')
    creator = Get(context, creator_key)

    return CheckWitness(creator)


def IsPromoExpired(promo_id):
    """
    Check if promo has expired or not

    Args:
        promo_id (str):

    Returns:
        (bool): True if promotion has expired
    """
    context = GetContext()
    expiration_key = concat(promo_id, 'expiration')
    expiration = Get(context, expiration_key)

    height = GetHeight()
    current_block = GetHeader(height)
    current_time = current_block.Timestamp

    expired = current_time > expiration
    return expired


def IsPromoExist(promo_id):
    """
    Check if promo is in Storage

    Args:
        promo_id (str):

    Returns:
        (bool): True if promo_id already exists in storage
    """
    context = GetContext()
    promo_exists = Get(context, promo_id)
    return promo_exists
