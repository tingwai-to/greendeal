<p align="center">
    <img src="./static/logo.png">
</p>

<h1 align="center">Green Deal</h1>

<p align="center">
    NEO smart contract for purchasing group discounts
</p>

## Overview

Smart contract for purchasing group discounts: if enough customers buy a promotion (promo), then the discount is available for all buyers. If not, then the funds are unlocked for customers to claim a refund and the seller will not be able to claim any it.

Creating this as a smart contract is useful because buyers and sellers do not need to rely on a trusted third party to setup the promotion and payment logistics. Also, since all transactions are recorded on the blockchain, buyers can easily prove payment to the sellers.

## Contract Address

```
# TODO
```

## Usage

There are two types of users: sellers and buyers. Sellers are be the ones setting up their promo for sale. Buyers are the ones purchasing the promo. Function parameters and examples are explained below.

### Seller Functions

* `create` - create the promo
* `delete` - delete the promo
* `claim` - claim funds once promo is over

### Buyer Functions

* `buy` - purchase the promo
* `refund` - refund and get your money back

### Misc Functions

* `details` - get all details of promo

## Documentation

### `create`

* Example:

    > `testinvoke <contract_hash> create ['<creator_public_key>','mydiscountcode','Opening-day-sale-for-ice-cream!','Discount-for-any-flavor',3,1546300800,5,8]`

    Here a new promo is being created for ice cream. A seller would typically be using this command.

* Parameters (in order):

    * **`creator_public_key`**: (public key)

        Owner of the promo's public key. This public key is checked to determine whether the wallet used to invoke has permission to `delete` or `claim` a promo after it has been created.

    * **`promo_id`**: (str)

        Can be any string you want but must be unique and cannot already be in use by another promo. As a seller, you'd probably want this to be a memorable string. Cannot contain spaces if invoking from neo-python.

    * **`title`**: (str)

        Title of your promo. Cannot contain spaces if invoking from neo-python.

    * **`description`**: (str)

        Description and details of your promo. Cannot contain spaces if invoking from neo-python.

    * **`price_per_person`**: (int)

        Price in gas.

    * **`expiration`**: (int)

        Date the promo expires, expressed in unix GMT time. Sellers can only claim funds after the date/time has passed. Buyers can refund their promo anytime before the expiration date.

    * **`min_count`**: (int)

        Minimum number of "seats" to be sold in order for the seller to claim their funds. If `min_count` not met by expiration time, buyers can get a refund.

    * **`max_count`**: (int)

        Maximum number of "seats" that can be sold.

### `delete`

* Example:

    > `testinvoke <contract_hash> delete ['mydiscountcode']`

    Here a promo by the `promo_id` of `mydiscountcode` is being deleted. Promo can only be deleted if wallet's public key used to invoke matches the public key used in `create`

* Parameters (in order):

    * **`promo_id`**: (str)

        Desired promo to delete.

### `claim`

* Example:

    > `testinvoke <contract_hash> claim ['mydiscountcode']`

    Here a seller can claim funds from promo `mydiscountcode` if the `min_count` and `expiration` is met. Promo can only be claimed if wallet's public key used to invoke matches the public key used in `create`.

### `buy`

* Example:

    > `testinvoke <contract_hash> buy ['<buyer_public_key>','mydiscountcode',2] --attach-gas=6`

    Here a user is purchasing 2 "seats" for the promo `mydiscountcode`. Building on top of the `create` example used above, each "seat" costs 3 gas so the buyer attaches 6 gas.

* Parameters (in order):

    * **`buyer_public_key`**: (public key)

        This public key is tied to the `quantity` of tickets purchased. `buyer_public_key` is explicitly stated to give flexibility, eg if someone wants to gift the "seats" to another person. Public key is also checked for permission during `refund`.

    * **`promo_id`**: (str)

        Desired promo to purchase.

    * **`quantity`** (int)

        Desired number of "seats" to purchase. Cannot exceed the number of remaining "seats" left (contract will throw error if exceeded).

### `refund`

* Example:

    > `testinvoke <contract_hash> refund ['<buyer_public_key>','mydiscountcode']`

    Here a user requests a refund for their purchase. All "seats" will be refunded. Refund will only pass if the expiration date has not passed.

    * **`buyer_public_key`** (public key)

        Checks is wallet used to invoke has permission to perform a `refund`.

    * **`promo_id`** (str)

        Desired promo to claim a refund.

### `details`

* Example:

    >  `testinvoke <contract_hash> details ['mydiscountcode']`

    Get the details of the promo `mydiscountcode`. Information returned: creator, title, description, price/person, expiration date, minimum count, maximum count, purchased count.

* Example output:
    ```
    [SmartContract.Runtime.Log] [contract_hash] [bytearray(b'Creator, Title, Description, Price/person, Expiration Date, Minimum count, Maximum count, Purchased count')]
    [SmartContract.Runtime.Log] [contract_hash] [bytearray(b'\x03\x1alo\xbb\xdf\x02\xca5\x17E\xfa\x86\xb9\xbaZ\x94R\xd7\x85\xacO\x7f\xc2\xb7T\x8c\xa2\xa4lO\xcfJ')]
    [SmartContract.Runtime.Log] [contract_hash] [bytearray(b'Opening-day-sale-for-ice-cream!')]
    [SmartContract.Runtime.Log] [contract_hash] [bytearray(b'Discount-for-any-flavor')]
    [SmartContract.Runtime.Log] [contract_hash] [bytearray(b'\x03')]
    [SmartContract.Runtime.Log] [contract_hash] [bytearray(b'\x80\xad*\\')]
    [SmartContract.Runtime.Log] [contract_hash] [bytearray(b'\x05')]
    [SmartContract.Runtime.Log] [contract_hash] [bytearray(b'\t')]
    [SmartContract.Runtime.Log] [contract_hash] [bytearray(b'\x02')]
    ```
