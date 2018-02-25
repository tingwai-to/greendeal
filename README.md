<p align="center">
    <img src="./static/logo.png" width="150px">
</p>

<h1 align="center">Green Deal</h1>

<p align="center">
    NEO smart contract for purchasing group discounts
</p>

## Overview

Smart contract for purchasing group discounts: if enough customers buy a promotion (promo), then the discount becomes available for all buyers. If not enough are sold, then customers can get a refund. This means as a seller, you can be sure that you will be paid if enough customers express interest. And as a buyer, you can be sure that you will get your money back if not enough people commit to buying.

Creating this as a smart contract is useful because buyers and sellers do not need to rely on a trusted third party to handle the promotion and payment logistics. Also, since all transactions are recorded on the blockchain, buyers can easily prove payment to the sellers.

* [Script Hash](#script-hash)
* [Example](#example)
* [Usage](#usage)
* [Documentation](#documentation)
* [Deploy](#deploy)

## Script Hash

City of Zion testnet:

```
7f1fd78c94bf8509947fce77eb275c99360e9756
```

## Example

[**Video tutorial**](https://drive.google.com/open?id=14bXtYyj8lOlu1n1z_MIXoi41tUPZwqgR) for using Green Deal. Detailed explanation found in [Documentation](#documentation).

**_(Seller)_** Create a promo identified by `mypromocode`:

    testinvoke <contract_hash> create ['<creator_public_key>','mypromocode','Opening-day-sale-for-ice-cream!','Discount-for-any-flavor',3,1546300800,5,8]

**_(Buyer)_** Buy 2 tickets for `mypromocode`, each ticket costs 3 gas so 6 gas is attached:

    testinvoke <contract_hash> buy ['<buyer_public_key>','mypromocode',2] --attach-gas=6

**_(Buyer)_** Refund your tickets if you change your mind:

    testinvoke <contract_hash> refund ['<buyer_public_key>','mypromocode']

**_(Seller)_** Claim your funds if enough tickets were sold:

    testinvoke <contract_hash> claim ['mypromocode']

## Usage

There are two types of users: sellers and buyers. Sellers are the ones setting up their promo for sale. Buyers are the ones purchasing the promo. Function parameters and examples are explained below in [Documentation](#documentation).

### Seller Functions

* [`create`](#create) - create the promo
* [`delete`](#delete) - delete the promo
* [`claim`](#claim) - claim funds once promo is over

### Buyer Functions

* [`buy`](#buy) - purchase the promo
* [`refund`](#refund) - get refund on purchase

### Misc Functions

* [`details`](#details) - get all details of promo

## Documentation

### `create`

* Example:

    > `testinvoke <contract_hash> create ['<creator_public_key>','mypromocode','Opening-day-sale-for-ice-cream!','Discount-for-any-flavor',3,1546300800,5,8]`

    Here a new promo identified by `mypromocode` is being created for an ice cream sale, promo expires on Jan 1, 2019 (1546300800 unix time). A seller would typically be using this command.

* Parameters (in order):

    * **`creator_public_key`**: (public key)

        Owner of the promo's public key. This public key is checked to determine whether the wallet used to invoke has permission to `delete` or `claim` a promo after it has been created. `creator_public_key` is explicitly stated to give flexibility, eg creating a promo on behalf of the seller.

    * **`promo_id`**: (str)

        Can be any string you want but must be unique and cannot already be in use by another promo. As a seller, you'd probably want this to be a memorable string for marketing purposes. Cannot contain spaces if invoking from neo-python.

    * **`title`**: (str)

        Title of your promo. Cannot contain spaces if invoking from neo-python.

    * **`description`**: (str)

        Description and details of your promo. Cannot contain spaces if invoking from neo-python.

    * **`price_per_person`**: (int)

        Price in gas.

    * **`expiration`**: (int)

        Date the promo expires, expressed in unix GMT time. Sellers can only claim funds after the date/time has passed. Buyers can refund their promo anytime before the expiration date.

    * **`min_count`**: (int)

        Minimum number of tickets to be sold in order for the seller to claim their funds. If `min_count` is not met by expiration time, buyers can get a refund.

    * **`max_count`**: (int)

        Maximum number of tickets that can be sold.

* Success message:

    > Promo created successfully

### `delete`

* Example:

    > `testinvoke <contract_hash> delete ['mypromocode']`

    Here a promo `mypromocode` is being deleted. Promo can only be deleted if wallet's public key used to invoke matches the public key used in `create`.

* Parameters (in order):

    * **`promo_id`**: (str)

        Desired promo to delete.

* Success message:

    > Promo deleted successfully

### `claim`

* Example:

    > `testinvoke <contract_hash> claim ['mypromocode']`

    Here a seller can claim funds from promo `mypromocode` if the `min_count` and `expiration` is met. Funds can only be claimed if wallet's public key used to invoke matches the public key used in `create`.

* Parameters (in order):

    * **`promo_id`**: (str)

        Desired promo to claim funds.

* Success message:

    > Promo funds claimed successfully

### `buy`

* Example:

    > `testinvoke <contract_hash> buy ['<buyer_public_key>','mypromocode',2] --attach-gas=6`

    Here a user is purchasing 2 tickets for the promo `mypromocode`. Building on top of the `create` example used above, each "seat" costs 3 gas so the buyer attaches 6 gas.

* Parameters (in order):

    * **`buyer_public_key`**: (public key)

        This public key is tied to all the tickets purchased. `buyer_public_key` is explicitly stated to give flexibility, eg if someone wants to gift the tickets to another person. Public key is also checked for permission during `refund`.

    * **`promo_id`**: (str)

        Desired promo to purchase.

    * **`quantity`**: (int)

        Desired number of tickets to purchase. Cannot exceed the number of remaining tickets left (contract will return False if exceeded).

* Success messsage:

    > Promo purchased successfully

### `refund`

* Example:

    > `testinvoke <contract_hash> refund ['<buyer_public_key>','mypromocode']`

    Here a user requests a refund on `mypromocode` for their purchase. All tickets will be refunded. Refunds can still be issued if promos are deleted. But refunds will not be issued if the deadline has passed AND minimum number of tickets have been sold.

* Parameters (in order):

    * **`buyer_public_key`**: (public key)

        Used to check if wallet used to invoke has permission to perform a `refund`.

    * **`promo_id`**: (str)

        Desired promo to claim a refund.

* Success message:

    > Promo refunded successfully

### `details`

* Example:

    >  `testinvoke <contract_hash> details ['mypromocode']`

    Get the details of the promo `mypromocode`. Information returned: creator, title, description, price/person, expiration date, minimum count, maximum count, purchased count. Since you can preview the output by using `testinvoke`, you do not need to spend real gas to get the details.

* Example output:

    ```
    [SmartContract.Runtime.Log] [contract_hash] [b'Title']
    [SmartContract.Runtime.Log] [contract_hash] [bytearray(b'Opening-day-sale-for-ice-cream!')]
    [SmartContract.Runtime.Log] [contract_hash] [b'Description']
    [SmartContract.Runtime.Log] [contract_hash] [bytearray(b'Discount-for-any-flavor')]
    [SmartContract.Runtime.Log] [contract_hash] [b'Price/person (gas)']
    [SmartContract.Runtime.Log] [contract_hash] [bytearray(b'\x03')]
    [SmartContract.Runtime.Log] [contract_hash] [b'Expiration date']
    [SmartContract.Runtime.Log] [contract_hash] [bytearray(b'\x80\xad*\\')]
    [SmartContract.Runtime.Log] [contract_hash] [b'Minimum count']
    [SmartContract.Runtime.Log] [contract_hash] [bytearray(b'\x05')]
    [SmartContract.Runtime.Log] [contract_hash] [b'Maximum count']
    [SmartContract.Runtime.Log] [contract_hash] [bytearray(b'\x08')]
    [SmartContract.Runtime.Log] [contract_hash] [b'Purchased count']
    [SmartContract.Runtime.Log] [contract_hash] [bytearray(b'\x02')]
    ```

    Here we can see 2 tickets have already been purchased out of the 8 maximum available and a minimum of 5 is required for the promo to take effect.


## Deploy

neo-python commands to 1) compile smart contract into .avm format and 2) deploy it onto main/test/privnet.

```
build contract.py test 0710 01 True False operation []
import contract contract.avm 0710 01 True False
```
