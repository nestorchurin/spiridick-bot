from datetime import datetime

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import LabeledPrice, Message, PreCheckoutQuery

import config
import storage

router = Router()

CURRENCY = "XTR"


@router.message(Command("buy"), F.chat.type == "private")
async def cmd_buy(message: Message):
    await message.answer_invoice(
        title="Скидання кулдауну /dick",
        description=(
            f"Скидає кулдаун ({config.COOLDOWN_TEXT}): одразу можеш знову "
            f"прописати /dick у будь-якій групі."
        ),
        payload="reset_cooldown",
        currency=CURRENCY,
        prices=[LabeledPrice(label="Скидання кулдауну", amount=config.ATTEMPT_COST)],
    )


@router.message(Command("buy"))
async def cmd_buy_group(message: Message):
    await message.answer("Скинути кулдаун можна лише в приватному чаті зі мною: @spiridick_bot")


@router.pre_checkout_query()
async def on_pre_checkout(query: PreCheckoutQuery):
    if query.invoice_payload != "reset_cooldown":
        await query.answer(ok=False, error_message="Невідома позиція оплати")
        return
    await query.answer(ok=True)


@router.message(F.successful_payment)
async def on_successful_payment(message: Message):
    payment = message.successful_payment
    await storage.get_store().reset_cooldown(message.from_user.id)
    await storage.get_store().add_payment(
        message.from_user.id,
        payment.telegram_payment_charge_id,
        payment.total_amount,
        int(datetime.now().timestamp()),
    )
    await message.answer(
        "Оплачено! ⭐ Твій кулдаун скинуто.\n"
        "Можеш одразу прописати /dick у будь-якій групі."
    )
