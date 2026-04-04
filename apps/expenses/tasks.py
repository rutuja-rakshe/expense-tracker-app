import logging
from celery import shared_task
from django.contrib.auth import get_user_model
from django.db.models import Sum, Q
from apps.expenses.models import Expense, TransactionType

logger = logging.getLogger('apps.expenses')
User = get_user_model()


@shared_task(bind=True, max_retries=3)
def send_monthly_summary(self, user_id, year, month):
    try:
        user = User.objects.get(id=user_id)
        qs = Expense.objects.filter(user=user, date__year=year, date__month=month)
        totals = qs.aggregate(
            income=Sum('amount', filter=Q(type=TransactionType.INCOME)),
            expenses=Sum('amount', filter=Q(type=TransactionType.EXPENSE)),
        )
        logger.info(
            f'Monthly summary: user={user.email} {year}-{month:02d} '
            f'income={totals["income"]} expenses={totals["expenses"]}'
        )
        # TODO: wire up Django send_mail here
    except User.DoesNotExist:
        logger.error(f'User {user_id} not found')
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)


@shared_task
def send_budget_alert(user_id, category, used_pct):
    try:
        user = User.objects.get(id=user_id)
        logger.warning(f'Budget alert: user={user.email} category={category} used={used_pct:.1f}%')
        # TODO: send email/push notification
    except User.DoesNotExist:
        logger.error(f'User {user_id} not found for budget alert')