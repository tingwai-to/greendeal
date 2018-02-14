# from boa.blockchain.vm.Neo.Account import *
from boa.blockchain.vm.Neo.Action import RegisterAction
# from boa.blockchain.vm.Neo.App import *
# from boa.blockchain.vm.Neo.Asset import *
# from boa.blockchain.vm.Neo.Block import *
from boa.blockchain.vm.Neo.Blockchain import GetHeight, GetHeader
# from boa.blockchain.vm.Neo.Contract import *
# from boa.blockchain.vm.Neo.Header import *
# from boa.blockchain.vm.Neo.Input import *
# from boa.blockchain.vm.Neo.Output import *
from boa.blockchain.vm.Neo.Runtime import Log, GetTrigger, CheckWitness
from boa.blockchain.vm.Neo.Storage import Get, GetContext, Put, Delete
# from boa.blockchain.vm.Neo.Transaction import GetHash
# from boa.blockchain.vm.Neo.TransactionAttribute import *
# from boa.blockchain.vm.Neo.TransactionType import *
from boa.blockchain.vm.Neo.TriggerType import Application, Verification
# from boa.blockchain.vm.Neo.Validator import *
from boa.blockchain.vm.System.ExecutionEngine import GetScriptContainer
from boa.code.builtins import sha1, concat

OWNER = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

def Main(operation, args):
#     trigger = GetTrigger()
#     if trigger == Verification():
#         is_owner = CheckWitness(OWNER)
#         if is_owner:
#             return True
#         return False

    # elif trigger == Application():
    l = len(args)

    # vendor action
    if operation == 'create':
        if l == 6:
            promo_id = args[0]
            title = args[1]
            description = args[2]
            price_per_person = args[3]
            expiration = args[4]
            min_headcount = args[5]
            max_headcount = args[6]

            CreatePromo(promo_id, title, description, price_per_person, expiration, min_headcount, max_headcount)
            Log('Promo created')

        else:
            return False

    # vendor action
    elif operation == 'delete':
        if l == 1:
            promo_id = args[0]

            authorize = IsPromoCreator()
            if authorize:
                RefundAll()
                DeletePromo(promo_id)
                Log('Promo deleted, all funds returned')
            else:
                Log('Permission denied, not creator of promo')

        else:
            return False

    # vendor action
    elif operation == 'claim':
        if l == 1:
            promo_id = args[0]
            ClaimFunds(promo_id)

        else:
            return False

    # consumer action
    elif operation == 'buy':
        if l == 2:
            promo_id = args[0]
            quantity = args[1]

            BuyPromo(promo_id, quantity)
            Log('Promo successfully purchased')

        else:
            return False

    # consumer/vendor action
    elif operation == 'details':
        if l == 1:
            promo_id = args[0]
            Details(promo_id)

        else:
            return False

    else:
        Log('Invalid operation')
        return False

    return False


def CreatePromo(promo_id, title, description, price_per_person, expiration, min_headcount, max_headcount):
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
    time = current_block.Timestamp

    if time > expiration:
        Log('expiration must be greater than current time. '
            'Note: use unix GMT time')
        return False

    keys = GetLookupKeys(promo_id)

    context = GetContext()
    Put(context, keys[0], title)
    Put(context, keys[1], description)
    Put(context, keys[2], price_per_person)
    Put(context, keys[3], expiration)
    Put(context, keys[4], min_headcount)
    Put(context, keys[5], max_headcount)
    Put(context, keys[6], max_headcount)  # remaining_headcount

    return True


def DeletePromo(promo_id):
    keys = GetLookupKeys(promo_id)

    context = GetContext()
    Delete(context, keys[0])
    Delete(context, keys[1])
    Delete(context, keys[2])
    Delete(context, keys[3])
    Delete(context, keys[4])
    Delete(context, keys[5])
    Delete(context, keys[6])

    return True


def BuyPromo(promo_id, quantity):
    # Deposit funds and purchase <quantity> seats in promo

    promo_hash = sha1(promo_id)

    context = GetContext()
    remaining_key = concat(promo_hash, 'remaining')
    remaining = Get(context, remaining_key)

    if remaining == 0:
        Log('Promo has sold out!')
        return False

    if quantity < 1:
        Log('Please enter quantity of at least one')
        return False

    if remaining - quantity < 0:
        Log('Not enough seats remaining, available amount: ')
        Log(remaining)
        return False

    expired = IsPromoExpired(promo_id)
    if expired:
        Log('Promo has expired!')
        return False

    remaining -= quantity

    Put(context, remaining_key, remaining)

#     TODO: implement subtracting funds from account

    return True


def RefundAll():
    # allow customers to withdraw funds
    pass


def Details(promo_id):
    # Prints details of promo:
    # Title, Description, Price/person, Expiration Date, Min Headcount,
    # Max Headcount, Remaining
    keys = GetLookupKeys(promo_id)

    context = GetContext()

    Log('Title, Description, Price/person, Expiration Date, Min Headcount, '
        'Max Headcount, Remaining')
    for key in keys:
        value = Get(context, key)
        Log(value)

    return True


def ClaimFunds(promo_id):
    # Let creator of promo claim funds

    expired = IsPromoExpired(promo_id)
    if not expired:
        Log('Promo not over yet! Cannot claim funds yet')
        return False

    authorize = IsPromoCreator()
    if not authorize:
        Log('Not promo creator, cannot claim funds.')

    context = GetContext()

    promo_hash = sha1(promo_id)
    min_headcount_key = concat(promo_hash, 'min_headcount')
    min_headcount = Get(context, min_headcount_key)
    max_headcount_key = concat(promo_hash, 'max_headcount')
    max_headcount = Get(context, max_headcount_key)
    remaining_key = concat(promo_hash, 'remaining')
    remaining = Get(context, remaining_key)

    # check if enough people bought promo
    if max_headcount - remaining < min_headcount:
        Log('Not enough promos sold, purchasers can claim their deposit.')
        return False

    # TODO: claim funds
    pass

def GetLookupKeys(promo_id):
    # Gets promo's keys to get/set values in storage

    promo_hash = sha1(promo_id)

    title_key = concat(promo_hash, 'title')
    description_key = concat(promo_hash, 'description')
    price_per_person_key = concat(promo_hash, 'price_per_person')
    expiration_key = concat(promo_hash, 'expiration')
    min_headcount_key = concat(promo_hash, 'min_headcount')
    max_headcount_key = concat(promo_hash, 'max_headcount')
    remaining_key = concat(promo_hash, 'remaining')

    keys = [title_key, description_key, price_per_person_key, expiration_key,
            min_headcount_key, max_headcount_key, remaining_key]

    return keys

def IsPromoCreator():
    # TODO
    pass

def IsPromoExpired(promo_id):
    # Checks if promotion has expired or not

    promo_hash = sha1(promo_id)

    context = GetContext()
    expiration_key = concat(promo_hash, 'expiration')
    expiration = Get(context, expiration_key)

    height = GetHeight()
    current_block = GetHeader(height)
    time = current_block.Timestamp

    expired = time > expiration
    return expired
