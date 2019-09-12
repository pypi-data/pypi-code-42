# coding: utf-8

"""
    Nomad Pilot

    This is the API descriptor for the Nomad Pilot API, responsible for shipping and logistics processing.  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Contact: paul@samarkand.global
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six


class Package(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'dimension': 'Dimension',
        'items': 'list[PackageItem]',
        'ship_from': 'Address',
        'ship_to': 'Address',
        'bill': 'Address',
        'order_ref': 'str',
        'seller_order_ref': 'str',
        'order_time': 'str',
        'gross_weight': 'float',
        'net_weight': 'float',
        'total_price': 'float',
        'currency': 'str',
        'mass_unit': 'str',
        'length_unit': 'str',
        'created_at': 'str',
        'updated_at': 'str',
        'pay_method': 'str',
        'pay_merchant_name': 'str',
        'pay_amount': 'float',
        'pay_id': 'str',
        'paid_at': 'str',
        'products_total_tax': 'float',
        'shipping_cost': 'float',
        'non_cash_deduction_amount': 'float',
        'customer_note': 'str'
    }

    attribute_map = {
        'dimension': 'dimension',
        'items': 'items',
        'ship_from': 'shipFrom',
        'ship_to': 'shipTo',
        'bill': 'bill',
        'order_ref': 'orderRef',
        'seller_order_ref': 'sellerOrderRef',
        'order_time': 'order_time',
        'gross_weight': 'gross_weight',
        'net_weight': 'net_weight',
        'total_price': 'total_price',
        'currency': 'currency',
        'mass_unit': 'massUnit',
        'length_unit': 'lengthUnit',
        'created_at': 'createdAt',
        'updated_at': 'updatedAt',
        'pay_method': 'payMethod',
        'pay_merchant_name': 'payMerchantName',
        'pay_amount': 'payAmount',
        'pay_id': 'payId',
        'paid_at': 'paidAt',
        'products_total_tax': 'productsTotalTax',
        'shipping_cost': 'shippingCost',
        'non_cash_deduction_amount': 'nonCashDeductionAmount',
        'customer_note': 'customerNote'
    }

    def __init__(self, dimension=None, items=None, ship_from=None, ship_to=None, bill=None, order_ref=None, seller_order_ref=None, order_time=None, gross_weight=None, net_weight=None, total_price=None, currency='RMB', mass_unit='Kilogram', length_unit='Centimetre', created_at=None, updated_at=None, pay_method=None, pay_merchant_name=None, pay_amount=None, pay_id=None, paid_at=None, products_total_tax=None, shipping_cost=None, non_cash_deduction_amount=None, customer_note=None):  # noqa: E501
        """Package - a model defined in OpenAPI"""  # noqa: E501

        self._dimension = None
        self._items = None
        self._ship_from = None
        self._ship_to = None
        self._bill = None
        self._order_ref = None
        self._seller_order_ref = None
        self._order_time = None
        self._gross_weight = None
        self._net_weight = None
        self._total_price = None
        self._currency = None
        self._mass_unit = None
        self._length_unit = None
        self._created_at = None
        self._updated_at = None
        self._pay_method = None
        self._pay_merchant_name = None
        self._pay_amount = None
        self._pay_id = None
        self._paid_at = None
        self._products_total_tax = None
        self._shipping_cost = None
        self._non_cash_deduction_amount = None
        self._customer_note = None
        self.discriminator = None

        if dimension is not None:
            self.dimension = dimension
        if items is not None:
            self.items = items
        if ship_from is not None:
            self.ship_from = ship_from
        if ship_to is not None:
            self.ship_to = ship_to
        if bill is not None:
            self.bill = bill
        if order_ref is not None:
            self.order_ref = order_ref
        if seller_order_ref is not None:
            self.seller_order_ref = seller_order_ref
        if order_time is not None:
            self.order_time = order_time
        if gross_weight is not None:
            self.gross_weight = gross_weight
        if net_weight is not None:
            self.net_weight = net_weight
        if total_price is not None:
            self.total_price = total_price
        self.currency = currency
        self.mass_unit = mass_unit
        self.length_unit = length_unit
        if created_at is not None:
            self.created_at = created_at
        if updated_at is not None:
            self.updated_at = updated_at
        if pay_method is not None:
            self.pay_method = pay_method
        if pay_merchant_name is not None:
            self.pay_merchant_name = pay_merchant_name
        if pay_amount is not None:
            self.pay_amount = pay_amount
        if pay_id is not None:
            self.pay_id = pay_id
        if paid_at is not None:
            self.paid_at = paid_at
        if products_total_tax is not None:
            self.products_total_tax = products_total_tax
        if shipping_cost is not None:
            self.shipping_cost = shipping_cost
        if non_cash_deduction_amount is not None:
            self.non_cash_deduction_amount = non_cash_deduction_amount
        if customer_note is not None:
            self.customer_note = customer_note

    @property
    def dimension(self):
        """Gets the dimension of this Package.  # noqa: E501


        :return: The dimension of this Package.  # noqa: E501
        :rtype: Dimension
        """
        return self._dimension

    @dimension.setter
    def dimension(self, dimension):
        """Sets the dimension of this Package.


        :param dimension: The dimension of this Package.  # noqa: E501
        :type: Dimension
        """

        self._dimension = dimension

    @property
    def items(self):
        """Gets the items of this Package.  # noqa: E501

        Contents of package  # noqa: E501

        :return: The items of this Package.  # noqa: E501
        :rtype: list[PackageItem]
        """
        return self._items

    @items.setter
    def items(self, items):
        """Sets the items of this Package.

        Contents of package  # noqa: E501

        :param items: The items of this Package.  # noqa: E501
        :type: list[PackageItem]
        """

        self._items = items

    @property
    def ship_from(self):
        """Gets the ship_from of this Package.  # noqa: E501


        :return: The ship_from of this Package.  # noqa: E501
        :rtype: Address
        """
        return self._ship_from

    @ship_from.setter
    def ship_from(self, ship_from):
        """Sets the ship_from of this Package.


        :param ship_from: The ship_from of this Package.  # noqa: E501
        :type: Address
        """

        self._ship_from = ship_from

    @property
    def ship_to(self):
        """Gets the ship_to of this Package.  # noqa: E501


        :return: The ship_to of this Package.  # noqa: E501
        :rtype: Address
        """
        return self._ship_to

    @ship_to.setter
    def ship_to(self, ship_to):
        """Sets the ship_to of this Package.


        :param ship_to: The ship_to of this Package.  # noqa: E501
        :type: Address
        """

        self._ship_to = ship_to

    @property
    def bill(self):
        """Gets the bill of this Package.  # noqa: E501


        :return: The bill of this Package.  # noqa: E501
        :rtype: Address
        """
        return self._bill

    @bill.setter
    def bill(self, bill):
        """Sets the bill of this Package.


        :param bill: The bill of this Package.  # noqa: E501
        :type: Address
        """

        self._bill = bill

    @property
    def order_ref(self):
        """Gets the order_ref of this Package.  # noqa: E501

        Order reference number. Default is from Odoo.  # noqa: E501

        :return: The order_ref of this Package.  # noqa: E501
        :rtype: str
        """
        return self._order_ref

    @order_ref.setter
    def order_ref(self, order_ref):
        """Sets the order_ref of this Package.

        Order reference number. Default is from Odoo.  # noqa: E501

        :param order_ref: The order_ref of this Package.  # noqa: E501
        :type: str
        """

        self._order_ref = order_ref

    @property
    def seller_order_ref(self):
        """Gets the seller_order_ref of this Package.  # noqa: E501

        Order reference number. Also could be from retailers, e.g. Youzan.  # noqa: E501

        :return: The seller_order_ref of this Package.  # noqa: E501
        :rtype: str
        """
        return self._seller_order_ref

    @seller_order_ref.setter
    def seller_order_ref(self, seller_order_ref):
        """Sets the seller_order_ref of this Package.

        Order reference number. Also could be from retailers, e.g. Youzan.  # noqa: E501

        :param seller_order_ref: The seller_order_ref of this Package.  # noqa: E501
        :type: str
        """

        self._seller_order_ref = seller_order_ref

    @property
    def order_time(self):
        """Gets the order_time of this Package.  # noqa: E501

        ISO 8601 format, '2019-01-19T18:30:52.442118+00:00' or '2019-01-19T18:30:52+00:00'  # noqa: E501

        :return: The order_time of this Package.  # noqa: E501
        :rtype: str
        """
        return self._order_time

    @order_time.setter
    def order_time(self, order_time):
        """Sets the order_time of this Package.

        ISO 8601 format, '2019-01-19T18:30:52.442118+00:00' or '2019-01-19T18:30:52+00:00'  # noqa: E501

        :param order_time: The order_time of this Package.  # noqa: E501
        :type: str
        """

        self._order_time = order_time

    @property
    def gross_weight(self):
        """Gets the gross_weight of this Package.  # noqa: E501

        Use Kilogram as the basic unit of mass.  # noqa: E501

        :return: The gross_weight of this Package.  # noqa: E501
        :rtype: float
        """
        return self._gross_weight

    @gross_weight.setter
    def gross_weight(self, gross_weight):
        """Sets the gross_weight of this Package.

        Use Kilogram as the basic unit of mass.  # noqa: E501

        :param gross_weight: The gross_weight of this Package.  # noqa: E501
        :type: float
        """

        self._gross_weight = gross_weight

    @property
    def net_weight(self):
        """Gets the net_weight of this Package.  # noqa: E501

        Use Kilogram as the basic unit of mass.  # noqa: E501

        :return: The net_weight of this Package.  # noqa: E501
        :rtype: float
        """
        return self._net_weight

    @net_weight.setter
    def net_weight(self, net_weight):
        """Sets the net_weight of this Package.

        Use Kilogram as the basic unit of mass.  # noqa: E501

        :param net_weight: The net_weight of this Package.  # noqa: E501
        :type: float
        """

        self._net_weight = net_weight

    @property
    def total_price(self):
        """Gets the total_price of this Package.  # noqa: E501

        The total price of this package.  # noqa: E501

        :return: The total_price of this Package.  # noqa: E501
        :rtype: float
        """
        return self._total_price

    @total_price.setter
    def total_price(self, total_price):
        """Sets the total_price of this Package.

        The total price of this package.  # noqa: E501

        :param total_price: The total_price of this Package.  # noqa: E501
        :type: float
        """

        self._total_price = total_price

    @property
    def currency(self):
        """Gets the currency of this Package.  # noqa: E501

        Price makes sense under an explicit currency.  # noqa: E501

        :return: The currency of this Package.  # noqa: E501
        :rtype: str
        """
        return self._currency

    @currency.setter
    def currency(self, currency):
        """Sets the currency of this Package.

        Price makes sense under an explicit currency.  # noqa: E501

        :param currency: The currency of this Package.  # noqa: E501
        :type: str
        """
        if currency is None:
            raise ValueError("Invalid value for `currency`, must not be `None`")  # noqa: E501

        self._currency = currency

    @property
    def mass_unit(self):
        """Gets the mass_unit of this Package.  # noqa: E501

        weight Unit of measurement  # noqa: E501

        :return: The mass_unit of this Package.  # noqa: E501
        :rtype: str
        """
        return self._mass_unit

    @mass_unit.setter
    def mass_unit(self, mass_unit):
        """Sets the mass_unit of this Package.

        weight Unit of measurement  # noqa: E501

        :param mass_unit: The mass_unit of this Package.  # noqa: E501
        :type: str
        """
        if mass_unit is None:
            raise ValueError("Invalid value for `mass_unit`, must not be `None`")  # noqa: E501

        self._mass_unit = mass_unit

    @property
    def length_unit(self):
        """Gets the length_unit of this Package.  # noqa: E501

        length Unit of measurement  # noqa: E501

        :return: The length_unit of this Package.  # noqa: E501
        :rtype: str
        """
        return self._length_unit

    @length_unit.setter
    def length_unit(self, length_unit):
        """Sets the length_unit of this Package.

        length Unit of measurement  # noqa: E501

        :param length_unit: The length_unit of this Package.  # noqa: E501
        :type: str
        """
        if length_unit is None:
            raise ValueError("Invalid value for `length_unit`, must not be `None`")  # noqa: E501

        self._length_unit = length_unit

    @property
    def created_at(self):
        """Gets the created_at of this Package.  # noqa: E501

        The time when current order was created. ISO_8601 format  # noqa: E501

        :return: The created_at of this Package.  # noqa: E501
        :rtype: str
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this Package.

        The time when current order was created. ISO_8601 format  # noqa: E501

        :param created_at: The created_at of this Package.  # noqa: E501
        :type: str
        """

        self._created_at = created_at

    @property
    def updated_at(self):
        """Gets the updated_at of this Package.  # noqa: E501

        The time when current order was updated. ISO_8601 format  # noqa: E501

        :return: The updated_at of this Package.  # noqa: E501
        :rtype: str
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this Package.

        The time when current order was updated. ISO_8601 format  # noqa: E501

        :param updated_at: The updated_at of this Package.  # noqa: E501
        :type: str
        """

        self._updated_at = updated_at

    @property
    def pay_method(self):
        """Gets the pay_method of this Package.  # noqa: E501


        :return: The pay_method of this Package.  # noqa: E501
        :rtype: str
        """
        return self._pay_method

    @pay_method.setter
    def pay_method(self, pay_method):
        """Sets the pay_method of this Package.


        :param pay_method: The pay_method of this Package.  # noqa: E501
        :type: str
        """

        self._pay_method = pay_method

    @property
    def pay_merchant_name(self):
        """Gets the pay_merchant_name of this Package.  # noqa: E501


        :return: The pay_merchant_name of this Package.  # noqa: E501
        :rtype: str
        """
        return self._pay_merchant_name

    @pay_merchant_name.setter
    def pay_merchant_name(self, pay_merchant_name):
        """Sets the pay_merchant_name of this Package.


        :param pay_merchant_name: The pay_merchant_name of this Package.  # noqa: E501
        :type: str
        """

        self._pay_merchant_name = pay_merchant_name

    @property
    def pay_amount(self):
        """Gets the pay_amount of this Package.  # noqa: E501

        The amount of final paid.  # noqa: E501

        :return: The pay_amount of this Package.  # noqa: E501
        :rtype: float
        """
        return self._pay_amount

    @pay_amount.setter
    def pay_amount(self, pay_amount):
        """Sets the pay_amount of this Package.

        The amount of final paid.  # noqa: E501

        :param pay_amount: The pay_amount of this Package.  # noqa: E501
        :type: float
        """

        self._pay_amount = pay_amount

    @property
    def pay_id(self):
        """Gets the pay_id of this Package.  # noqa: E501

        The serial number of current pay.  # noqa: E501

        :return: The pay_id of this Package.  # noqa: E501
        :rtype: str
        """
        return self._pay_id

    @pay_id.setter
    def pay_id(self, pay_id):
        """Sets the pay_id of this Package.

        The serial number of current pay.  # noqa: E501

        :param pay_id: The pay_id of this Package.  # noqa: E501
        :type: str
        """

        self._pay_id = pay_id

    @property
    def paid_at(self):
        """Gets the paid_at of this Package.  # noqa: E501

        The time when the pay was made. ISO_8601 format  # noqa: E501

        :return: The paid_at of this Package.  # noqa: E501
        :rtype: str
        """
        return self._paid_at

    @paid_at.setter
    def paid_at(self, paid_at):
        """Sets the paid_at of this Package.

        The time when the pay was made. ISO_8601 format  # noqa: E501

        :param paid_at: The paid_at of this Package.  # noqa: E501
        :type: str
        """

        self._paid_at = paid_at

    @property
    def products_total_tax(self):
        """Gets the products_total_tax of this Package.  # noqa: E501

        The sum tax of all products in current order, including Non-cash deduction amount.  # noqa: E501

        :return: The products_total_tax of this Package.  # noqa: E501
        :rtype: float
        """
        return self._products_total_tax

    @products_total_tax.setter
    def products_total_tax(self, products_total_tax):
        """Sets the products_total_tax of this Package.

        The sum tax of all products in current order, including Non-cash deduction amount.  # noqa: E501

        :param products_total_tax: The products_total_tax of this Package.  # noqa: E501
        :type: float
        """

        self._products_total_tax = products_total_tax

    @property
    def shipping_cost(self):
        """Gets the shipping_cost of this Package.  # noqa: E501

        The shipping cost of current order, excluding the shipping cost on each contained products. If delivery free, just set 0.  # noqa: E501

        :return: The shipping_cost of this Package.  # noqa: E501
        :rtype: float
        """
        return self._shipping_cost

    @shipping_cost.setter
    def shipping_cost(self, shipping_cost):
        """Sets the shipping_cost of this Package.

        The shipping cost of current order, excluding the shipping cost on each contained products. If delivery free, just set 0.  # noqa: E501

        :param shipping_cost: The shipping_cost of this Package.  # noqa: E501
        :type: float
        """

        self._shipping_cost = shipping_cost

    @property
    def non_cash_deduction_amount(self):
        """Gets the non_cash_deduction_amount of this Package.  # noqa: E501

        Amount that deducted by non-cash, e.g. member points, virtual currency, voucher code, etc.  # noqa: E501

        :return: The non_cash_deduction_amount of this Package.  # noqa: E501
        :rtype: float
        """
        return self._non_cash_deduction_amount

    @non_cash_deduction_amount.setter
    def non_cash_deduction_amount(self, non_cash_deduction_amount):
        """Sets the non_cash_deduction_amount of this Package.

        Amount that deducted by non-cash, e.g. member points, virtual currency, voucher code, etc.  # noqa: E501

        :param non_cash_deduction_amount: The non_cash_deduction_amount of this Package.  # noqa: E501
        :type: float
        """

        self._non_cash_deduction_amount = non_cash_deduction_amount

    @property
    def customer_note(self):
        """Gets the customer_note of this Package.  # noqa: E501

        The special note from the buyer.  # noqa: E501

        :return: The customer_note of this Package.  # noqa: E501
        :rtype: str
        """
        return self._customer_note

    @customer_note.setter
    def customer_note(self, customer_note):
        """Sets the customer_note of this Package.

        The special note from the buyer.  # noqa: E501

        :param customer_note: The customer_note of this Package.  # noqa: E501
        :type: str
        """

        self._customer_note = customer_note

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Package):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
