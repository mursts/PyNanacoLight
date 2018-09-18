# -*- coding: utf-8 -*-
from pynanacolight.page import LoginPage, MenuPage
from pynanacolight.page_creditcharge import CreditChargeMenuPage, CreditChargeHistoryPage, CreditChargePasswordAuthPage, \
    CreditChargeInputPage, CreditChargeConfirmPage, CreditChargeCancelPage, CreditChargeCancelConfirmPage
from pynanacolight.page_gift import RegisterGiftPage, RegisterGiftCodeInputPage, RegisterGiftCodeConfirmPage

from pynanacolight.util.logger import logging

from requests import session

class PyNanacoLight:
    def __init__(self, session: session()):
        self._session = session

        self.html = None

        self.balance_card = None
        self.balance_center = None

        self.credit_charge_password = ''

        self.registered_creditcard = ''
        self.charge_count = None
        self.charge_amount = None

    def login(self, nanaco_number, card_number):
        page = LoginPage(self._session)

        page.input_nanaco_number(nanaco_number)
        page.input_card_number(card_number)

        self.html = page.click_login()

        page = MenuPage(self._session, self.html)
        self.balance_card = page.text_balance_card
        self.balance_center = page.text_balance_center

    def login_credit_charge(self, password):
        self.credit_charge_password = password

        page = MenuPage(self._session, self.html)
        self.html = page.click_login_credit_charge()

        page = CreditChargePasswordAuthPage(self._session, self.html)
        page.input_credit_charge_password(password)
        self.html = page.click_next()

        page = CreditChargeMenuPage(self._session, self.html)
        html = page.click_history()

        page = CreditChargeHistoryPage(self._session, html)
        self.registered_creditcard = page.text_registered_credit_card
        self.charge_count = page.text_charge_count
        self.charge_amount = page.text_charge_amount

    def charge(self, value: int):
        page = CreditChargeMenuPage(self._session, self.html)
        self.html = page.click_charge()

        page = CreditChargeInputPage(self._session, self.html)
        page.input_charge_amount(value)
        self.html = page.click_next()

        page = CreditChargeConfirmPage(self._session, self.html)
        self.html = page.click_confirm()

    def cancel(self, password):
        page = CreditChargeMenuPage(self._session, self.html)
        self.html = page.click_cancel()

        page = CreditChargeCancelPage(self._session, self.html)
        page.input_credit_charge_password(password)
        self.html = page.click_next()

        page = CreditChargeCancelConfirmPage(self._session, self.html)
        self.html = page.click_confirm()

    def register_giftcode(self, code):
        page = MenuPage(self._session, self.html)
        self.html = page.click_register_gift()

        page = RegisterGiftPage(self._session, self.html)
        self.html = page.click_accept()

        page = RegisterGiftCodeInputPage(self._session, self.html)
        page.input_code(code)
        self.html = page.click_submit()

        page = RegisterGiftCodeConfirmPage(self._session, self.html)
        self.html = page.click_confirm()
