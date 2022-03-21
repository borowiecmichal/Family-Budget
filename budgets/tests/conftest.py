from datetime import datetime

import pytest

from budgets.models import Budget, BudgetParticipant, Income, Expanse
from users.models import BaseUser


@pytest.fixture
def test_user1():
    test_user1 = BaseUser.objects.create_user(
        username='test_user1',
        password='supersecretpassword',
        first_name='John',
        last_name='Smith',
        email="test_user1@email.com",
    )
    return test_user1


@pytest.fixture
def test_user2():
    test_user2 = BaseUser.objects.create_user(
        username='test_user2',
        password='supersecretpassword',
        first_name='John',
        last_name='Smith',
        email="test_user2@email.com",
    )
    return test_user2


@pytest.fixture
def test_budget1(test_user1, test_user2):
    test_budget1 = Budget.objects.create(
        name='test_budget2'
    )
    owner_participation = BudgetParticipant.objects.create(
        participant=test_user1,
        budget=test_budget1,
        is_owner=True
    )
    user_participation = BudgetParticipant.objects.create(
        participant=test_user2,
        budget=test_budget1,
        is_owner=False
    )
    test_budget1.participant_associations.set([owner_participation, user_participation])
    return test_budget1


@pytest.fixture
def test_income(test_budget1):
    income = Income.objects.create(
        amount=214.58,
        description='test income',
        transaction_date=datetime.today().date(),
        budget=test_budget1,
    )
    return income


@pytest.fixture
def test_expanse(test_budget1):
    expanse = Expanse.objects.create(
        amount=214.58,
        description='test expanse',
        transaction_date=datetime.today().date(),
        budget=test_budget1,
        category=test_budget1.expanse_categories.first()
    )
    return expanse
