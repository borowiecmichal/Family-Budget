import pytest
from graphql_relay import to_global_id


def get_token(client, user):
    login_attributes = f'username: "{user.username}", password: "supersecretpassword"'
    response = client.post('/graphql', {
        'query': '''
            mutation {
              tokenAuth(''' + login_attributes + ''') {
                success,
                errors,
                unarchiving,
                token,
                refreshToken,
                unarchiving,
                user {
                  id,
                  username,
                }
              }
            }
            '''
    })
    return response.json().get('data', {}).get('tokenAuth', {}).get('token')


@pytest.mark.django_db
def test_auth(client, test_user1):
    token = get_token(client, test_user1)
    assert token is not None


@pytest.mark.django_db
def test_create_budget(client, test_user1):
    headers = {
        'HTTP_AUTHORIZATION': "JWT " + get_token(client, test_user1),
    }
    response = client.post('/graphql', {
        'query': '''
        mutation{
            createOrUpdateBudget(input: {name:"budget_test", participants:[]}){
                budget{
                    id
                }
                errors{
                    field
                    messages
                }
            }
        }
        '''
    }, **headers)
    assert response.json().get('data', {}).get('createOrUpdateBudget', {}).get('budget', {}).get('id') is not None


@pytest.mark.django_db
def test_create_budget(client, test_user1):
    headers = {
        'HTTP_AUTHORIZATION': "JWT " + get_token(client, test_user1),
    }
    response = client.post('/graphql', {
        'query': '''
        mutation{
            createOrUpdateBudget(input: {name:"budget_test", participants:[]}){
                budget{
                    id
                    participantAssociations {
                        edges {
                            node{
                                isOwner
                                participant{
                                    username
                                }
                            }
                        }
                    }
                }
                errors{
                    field
                    messages
                }
            }
        }
        '''
    }, **headers)
    owner_node = \
        response.json().get('data', {}).get('createOrUpdateBudget', {}).get('budget', {}).get(
            'participantAssociations')[
            'edges'][0]['node']
    assert response.json().get('data', {}).get('createOrUpdateBudget', {}).get('budget', {}).get('id') is not None
    assert owner_node['isOwner'] is True
    assert owner_node['participant']['username'] == test_user1.username


@pytest.mark.django_db
def test_update_budget(client, test_budget1, test_user1, test_user2):
    headers = {
        'HTTP_AUTHORIZATION': "JWT " + get_token(client, test_user1),
    }
    budget_gid = to_global_id('budgets.schema.BudgetNode', test_budget1.id)
    response = client.post('/graphql', {
        'query': '''
        mutation{
            createOrUpdateBudget(input: {id: "''' + budget_gid + '''", name:"changed_name", participants: []}){
                budget{
                    id
                    name
                    participantAssociations {
                         edges {
                             node{
                                 isOwner
                                 participant{
                                     username
                                 }
                             }
                         }
                     }
                }
                errors{
                    field
                    messages
                }
            }
        }
        '''
    }, **headers)
    participant_nodes = \
        response.json().get('data', {}).get('createOrUpdateBudget', {}).get('budget', {}).get(
            'participantAssociations')[
            'edges']
    assert response.json().get('data', {}).get('createOrUpdateBudget', {}).get('budget', {}).get(
        'name') == 'changed_name'
    assert len(participant_nodes) == 1


@pytest.mark.django_db
def test_delete_budget(client, test_budget1, test_user1, test_user2):
    headers = {
        'HTTP_AUTHORIZATION': "JWT " + get_token(client, test_user1),
    }
    budget_gid = to_global_id('budgets.schema.BudgetNode', test_budget1.id)
    response = client.post('/graphql', {
        'query': '''
        mutation {
            deleteBudget(input: { id: "''' + budget_gid + '''" }) {
                id
                message
            }
        }
        '''
    }, **headers)
    assert response.json().get('data', {}).get('deleteBudget', {}).get('message') == 'deleted'


@pytest.mark.django_db
def test_fail_delete_budget(client, test_budget1, test_user2):
    headers = {
        'HTTP_AUTHORIZATION': "JWT " + get_token(client, test_user2),
    }
    budget_gid = to_global_id('budgets.schema.BudgetNode', test_budget1.id)
    response = client.post('/graphql', {
        'query': '''
        mutation {
            deleteBudget(input: { id: "''' + budget_gid + '''" }) {
                id
                message
            }
        }
        '''
    }, **headers)
    assert response.json().get('errors') is not None


@pytest.mark.django_db
def test_create_expanse_category(client, test_budget1, test_user1, test_user2):
    headers = {
        'HTTP_AUTHORIZATION': "JWT " + get_token(client, test_user1),
    }
    budget_gid = to_global_id('budgets.schema.BudgetNode', test_budget1.id)
    response = client.post('/graphql', {
        'query': '''
        mutation{
            createOrUpdateExpanseCategory(input: {name:"new category", budget: "''' + budget_gid + '''"}){
                expanseCategory{
                    name
                }
                errors{
                    field
                    messages
                }
            }
        }
        '''
    }, **headers)
    assert response.json().get('data', {}).get('createOrUpdateExpanseCategory', {}).get('expanseCategory', {}).get(
        'name') == 'new category'
    assert response.json().get('data', {}).get('createOrUpdateExpanseCategory', {}).get('errors') == []
    assert test_budget1.expanse_categories.all().count() == 6


@pytest.mark.django_db
def test_create_expanse(client, test_budget1, test_user1):
    headers = {
        'HTTP_AUTHORIZATION': "JWT " + get_token(client, test_user1),
    }
    category_gid = to_global_id('budgets.schema.ExpanseCategoryNode', test_budget1.expanse_categories.first().id)
    budget_gid = to_global_id('budgets.schema.BudgetNode', test_budget1.id)
    response = client.post('/graphql', {
        'query': '''
        mutation{
            createOrUpdateExpanse(input: {budget: "''' + budget_gid + '''", description:"exanse 1", transactionDate:"2022-03-19", amount: 20.05, category: "''' + category_gid + '''" }){
                expanse{
                    id
                }
                errors{
                    field
                    messages
                }
            }
        }
        '''
    }, **headers)
    assert response.json().get('data', {}).get('createOrUpdateExpanse', {}).get('expanse', {}).get('id') is not None
    assert response.json().get('data', {}).get('createOrUpdateExpanse', {}).get('errors') == []
    assert test_budget1.expanses.all().count() == 1


@pytest.mark.django_db
def test_create_expanse(client, test_budget1, test_user1):
    headers = {
        'HTTP_AUTHORIZATION': "JWT " + get_token(client, test_user1),
    }
    budget_gid = to_global_id('budgets.schema.BudgetNode', test_budget1.id)
    response = client.post('/graphql', {
        'query': '''
        mutation{
            createOrUpdateIncome(input: {budget: "''' + budget_gid + '''", description:"income 1", transactionDate:"2022-03-19", amount: 20.05 }){
                income{
                    id
                }
                errors{
                    field
                    messages
                }
            }
        }
        '''
    }, **headers)
    assert response.json().get('data', {}).get('createOrUpdateIncome', {}).get('income', {}).get('id') is not None
    assert response.json().get('data', {}).get('createOrUpdateIncome', {}).get('errors') == []
    assert test_budget1.incomes.all().count() == 1


@pytest.mark.django_db
def test_budgets_properties(client, test_budget1, test_income, test_user1):
    assert float(test_budget1.incomes_sum) == float(214.58)
    assert test_budget1.incomes.all().count() == 1

@pytest.mark.django_db
def test_expanse_category_properties(client, test_budget1, test_expanse, test_user1):
    assert float(test_budget1.incomes_sum) == float(0)
    assert float(test_budget1.expanses_sum) == float(214.58)
    assert float(test_budget1.expanse_categories.first().expanses_sum) == float(214.58)
    assert float(test_budget1.expanse_categories.last().expanses_sum) == float(0)
