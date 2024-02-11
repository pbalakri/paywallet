from datetime import datetime
from restriction.models import PaymentRestriction
from wallet.models import Transaction


def check_for_payment_restrictions(txn_wallet):
    # Get all payment restrictions for this wallet

    restrictions = PaymentRestriction.objects.filter(
        wallet=txn_wallet)
    for restriction in restrictions:
        # check if frequency of restriction is weekly
        if restriction.frequency == 'Weekly':
            # get total count of transactions this week of year
            transactions_this_week = Transaction.objects.filter(
                wallet=txn_wallet, date__week=datetime.today().isocalendar()[1])
            if transactions_this_week.count() > restriction.count_per_period:
                raise Exception(
                    'You have exceeded your weekly transaction limit')
        elif restriction.frequency == 'Monthly':
            # get total count of transactions this month
            transactions_this_month = Transaction.objects.filter(
                wallet=txn_wallet, date__month=datetime.now().month)
            if transactions_this_month.count() > restriction.count_per_period:
                raise Exception(
                    'You have exceeded your monthly transaction limit')
        elif restriction.frequency == 'Daily':
            # get total count of transactions today
            transactions_today = Transaction.objects.filter(
                wallet=txn_wallet, date__day=datetime.now().day)
            if transactions_today.count() > restriction.count_per_period:
                raise Exception(
                    'You have exceeded your daily transaction limit')

    return True
