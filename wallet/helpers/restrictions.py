from restriction.models import PaymentRestriction, ProductsRestriction, CategoryRestriction
from datetime import datetime
from wallet.models import Transaction
from django.db.models import Sum


def get_restrictions(txn_bracelet):
    returnable_data = {
        "canBuy": False,
        "restrictions": {
            "products": [],
            "max_amount": 0
        }
    }
    restricted_products = []
    product_restrictions = ProductsRestriction.objects.filter(
        bracelet=txn_bracelet)
    if product_restrictions:
        for product_restriction in product_restrictions:
            restricted_products.append(str(product_restriction.product.id))
    restricted_categories = CategoryRestriction.objects.filter(
        bracelet=txn_bracelet)

    for category in restricted_categories:
        # Get ids of products from the category
        products = category.category.product_set.all()
        if products:
            for product in products:
                restricted_products.append(str(product.id))
    returnable_data["restrictions"]["products"] = list(
        set(restricted_products))
    returnable_data["canBuy"] = get_payment_restrictions(txn_bracelet)
    return returnable_data


def get_sum_of_transaction_amounts(transations):
    total_amount = transations.aggregate(Sum('amount'))[
        'amount__sum'] or 0

    return total_amount


def get_payment_restrictions(rfid):
    restrictions = PaymentRestriction.objects.filter(
        student__bracelet__rfid=rfid)
    for restriction in restrictions:
        # check if frequency of restriction is weekly
        if restriction.frequency == 'Weekly':
            transactions_this_week = Transaction.objects.filter(
                bracelet__rfid=rfid, date__week=datetime.today().isocalendar()[1])
            if get_sum_of_transaction_amounts(transactions_this_week) > restriction.total_per_period:
                return False
        elif restriction.frequency == 'Monthly':
            # get total count of transactions this month
            transactions_this_month = Transaction.objects.filter(
                bracelet__rfid=rfid, date__month=datetime.now().month)
            if get_sum_of_transaction_amounts(transactions_this_month) > restriction.total_per_period:
                return False
        elif restriction.frequency == 'Daily':
            # get total count of transactions today
            transactions_today = Transaction.objects.filter(
                bracelet__rfid=rfid, date__day=datetime.now().day)
            if get_sum_of_transaction_amounts(transactions_today) > restriction.total_per_period:
                return False
    return True
