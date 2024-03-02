from restriction.models import PaymentRestriction, ProductRestriction, CategoryRestriction
from datetime import datetime
from wallet.models import Transaction


def get_restrictions(txn_bracelet):
    returnable_data = {
        "canBuy": False,
        "restrictions": {
            "products": [],
            "max_amount": 0
        }
    }
    restricted_products = []
    product_restrictions = ProductRestriction.objects.filter(
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


def get_payment_restrictions(txn_bracelet):
    restrictions = PaymentRestriction.objects.filter(
        bracelet=txn_bracelet)
    for restriction in restrictions:
        # check if frequency of restriction is weekly
        if restriction.frequency == 'Weekly':
            # get total count of transactions this week of year
            transactions_this_week = Transaction.objects.filter(
                bracelet=txn_bracelet, date__week=datetime.today().isocalendar()[1])
            if transactions_this_week.count() > restriction.count_per_period:
                return False
        elif restriction.frequency == 'Monthly':
            # get total count of transactions this month
            transactions_this_month = Transaction.objects.filter(
                bracelet=txn_bracelet, date__month=datetime.now().month)
            if transactions_this_month.count() > restriction.count_per_period:
                return False
        elif restriction.frequency == 'Daily':
            # get total count of transactions today
            transactions_today = Transaction.objects.filter(
                bracelet=txn_bracelet, date__day=datetime.now().day)
            if transactions_today.count() > restriction.count_per_period:
                return False
    return True
