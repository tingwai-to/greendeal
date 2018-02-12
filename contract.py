# from boa.blockchain.vm.Neo.Account import *
from boa.blockchain.vm.Neo.Action import RegisterAction
# from boa.blockchain.vm.Neo.App import *
# from boa.blockchain.vm.Neo.Asset import *
# from boa.blockchain.vm.Neo.Block import *
# from boa.blockchain.vm.Neo.Blockchain import *
# from boa.blockchain.vm.Neo.Contract import *
# from boa.blockchain.vm.Neo.Header import *
# from boa.blockchain.vm.Neo.Input import *
# from boa.blockchain.vm.Neo.Output import *
from boa.blockchain.vm.Neo.Runtime import Log, GetTrigger, CheckWitness
from boa.blockchain.vm.Neo.Storage import Get, GetContext, Put, Delete
# from boa.blockchain.vm.Neo.Transaction import GetHash
from boa.blockchain.vm.Neo.TransactionAttribute import *
# from boa.blockchain.vm.Neo.TransactionType import *
from boa.blockchain.vm.Neo.TriggerType import Application, Verification
# from boa.blockchain.vm.Neo.Validator import *
from boa.blockchain.vm.System.ExecutionEngine import GetScriptContainer

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
            title = args[0]
            description = args[1]
            price_per_person = args[2]
            expiration = args[3]
            min_headcount = args[4]
            max_headcount = args[5]

            CreatePromotion(title, description, price_per_person, expiration, min_headcount, max_headcount)
            Log('Promotion created')

        else:
            return False

    # vendor action
    elif operation == 'delete':
        if l == 1:
            promotion_id = args[0]

            RefundAll()
            DeletePromotion()
            Log('Promotion deleted, all funds returned')

        else:
            return False

    # vendor action
    elif operation == 'claim':
        VendorClaim()

    # consumer action
    elif operation == 'buy':
        if l == 2:
            promotion_id = args[0]
            quantity = args[1]

            BuyPromotion(promotion_id, quantity)
            Log('Promotion successfully purchased')
        else:
            return False

    # consumer/vendor action
    elif operation == 'inspect':
        Inspect(promotion_id)

    else:
        Log('Invalid operation')
        return False

    return False


def CreatePromotion(title, description, price_per_person, expiration, min_headcount, max_headcount):
    if price_per_person < 0:
        Log('price_per_person must be positive')
        return False

    if min_headcount <= 0:
        Log('min_headcount must be greater than zero')
        return False

    if min_headcount > max_headcount:
        Log('min_headcount must be less than or equal to max_headcount')
        return False

    context = GetContext()
    Put(context, 'title', title)
    Put(context, 'description', description)
    Put(context, 'price_per_person', price_per_person)
    Put(context, 'expiration', expiration)
    Put(context, 'min_headcount', min_headcount)
    Put(context, 'max_headcount', max_headcount)
    Put(context, 'remaining', max_headcount)

    return True


def DeletePromotion():
    context = GetContext()
    Delete(context, 'title')
    Delete(context, 'description')
    Delete(context, 'price_per_person')
    Delete(context, 'expiration')
    Delete(context, 'min_headcount')
    Delete(context, 'max_headcount')
    Delete(context, 'remaining')

    return True


def BuyPromotion(promotion_id, quantity):
    context = GetContext()
    remaining = Get(context, 'remaining')

    if remaining == 0:
        Log('Promotion has sold out!')
        return False

    if quantity < 1:
        Log('Please enter quantity of at least one')
        return False

    if remaining - quantity < 0:
        Log('Not enough seats remaining, available amount: ')
        Log(remaining)
        return False

    # TODO: check timestamp and if expired

    remaining -= quantity
    Put(context, 'remaining', remaining)

#     TODO: implement subtracting funds from account

    return True


def RefundAll():
    # allow customers to withdraw funds
    pass


def Inspect(promotion_id):
    context = GetContext()
    title = Get(context, 'title')
    description = Get(context, 'description')
    price_per_person = Get(context, 'price_per_person')
    expiration = Get(context, 'expiration')
    min_headcount = Get(context, 'min_headcount')
    max_headcount = Get(context, 'max_headcount')
    remaining = Get(context, 'remaining')

    Log('Title, Description, Price/person, Expiration Date, Min Headcount, '
        'Max Headcount, Remaining')
    Log(title)
    Log(description)
    Log(price_per_person)
    Log(expiration)
    Log(min_headcount)
    Log(max_headcount)
    Log(remaining)

    return True


def VendorClaim(promotion_id):
    context = GetContext()
    # TODO: write logic for vendor to claim funds if headcount met and after deadline
