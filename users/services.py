import stripe
from rest_framework.exceptions import APIException

from config.settings import STRIPE_API_KEY
from lms.models import Course

stripe.api_key = STRIPE_API_KEY


def create_stripe_product_and_price(instance):
    """
    Создаёт продукт и цену в Stripe для курса или урока.
    Args:
        instance: Объект Course или Lesson
    """
    # Определяем тип объекта
    is_course = isinstance(instance, Course)

    # Название продукта
    product_name = f"Курс: {instance.title}" if is_course else f"Урок: {instance.title}"

    # Создаём продукт в Stripe
    product = stripe.Product.create(name=product_name)

    # Конвертируем цену в копейки (для RUB)
    unit_amount = int(instance.price * 100)  # Например, 1000 руб → 100000 коп

    # Создаём цену
    price = stripe.Price.create(
        currency="rub",
        unit_amount=unit_amount,
        product=product.id,
    )

    # Сохраняем ID в модель
    instance.stripe_product_id = product.id
    instance.stripe_price_id = price.id
    instance.save()

    return product.id, price.id


def create_checkout_session(stripe_price_id):
    """Создаёт сессию оплаты в Stripe"""

    try:
        session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price": stripe_price_id,
                    "quantity": 1,
                }
            ],
            mode="payment",
            payment_method_types=["card"],
            success_url="https://example.com/success",
            cancel_url="https://example.com/cancel",
        )
        return {"session_id": session.id, "checkout_url": session.url}
    except Exception as e:
        raise Exception(f"Stripe error: {str(e)}")


def get_checkout_session_status(session_id: str) -> dict:
    """
    Получает статус сессии Stripe Checkout по ID.
    Возвращает словарь с полями:
    - status: 'open', 'complete', 'expired', 'cancelled'
    - amount: сумма в копейках
    - currency: валюта (например, 'rub')
    - customer_email: email покупателя (если указан)
    - payment_status: 'paid', 'unpaid', 'no_payment_required'
    """
    try:
        session = stripe.checkout.Session.retrieve(session_id)

        return {
            "status": session.status,
            "amount": session.amount_total,
            "currency": session.currency,
            "customer_email": session.customer_details.get("email") if session.customer_details else None,
            "payment_status": session.payment_status,
            "url": session.url,
        }
    except stripe.error.StripeError as e:
        raise APIException(f"Ошибка Stripe: {e.user_message}")
    except Exception as e:
        raise APIException(f"Неизвестная ошибка: {str(e)}")