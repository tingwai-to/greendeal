<p align="center">
    <img src="./static/logo.png">
</p>

<h1 align="center">Green Deal</h1>

<p align="center">
    NEO smart contract for purchasing group discounts
</p>

## Overview

Smart contract for purchasing group discounts: if enough customers buy a promotion (promo), then the discount is unlocked for all buyers. If not, then the funds are unlocked for customers to claim a refund and the seller will not be able to claim any it.

## Usage

There are two types of users: sellers and buyers. Sellers usually will be the ones setting up their promo for sale. Buyers are the ones purchasing the promo. Function parameters and examples are further explained below.

### Seller Functions

* `create` - create the promo
* `delete` - delete the promo
* `claim` - claim funds once promo is over

### Buyer Functions

* `buy` - purchase the promo
* `refund` - refund and get your money back

### Both

* `details` - get more details of promo

## Documentation

### `create`

* Example:

    > ```testinvoke <contract_hash> create ['<creator_public_key>','mydiscountcode','Opening-day-sale-for-ice-cream!','Discount-for-any-flavor',3,1546300800,5,8]```

    Here a new promo is being created for ice cream. Customers can claim this using the promo code `mydiscountcode.

* Parameters (in order):
    * **`creator_public_key`**: (public key)

        Owner of the promo's public key. This public key checked to determine whether the contract invoker has permission to `delete` or `refund` a promo after it has been created.

    * **`promo_id`**: (str)

        Can be any string you want but must be unique and cannot already be in use by another promo. As a seller, you'd probably want this to be a memorable string. Cannot contain spaces if invoking from neo-python.

    * **`title`**: (str)

        Title of your promo. Cannot contain spaces if invoking from neo-python.

    * **`description`**: (str)

        Description and details of your promo. Cannot contain spaces if invoking from neo-python.

    * **`price_per_person`**: (int)

        Price in GAS

    * **`expiration`**: (int)

        Date the promo expires, expressed in unix GMT time. Sellers can only claim funds after the date/time has passed. Buyers can refund their promo anytime before the expiration date.

    * **`min_count`**: (int)

        Minimum number of "seats" to be sold in order for the seller to claim their funds. If `min_count` not met by expiration time, buyers can get a refund.

    * **`max_count`**: (int)

        Maximum number of "seats" that can be sold
