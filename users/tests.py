import pytest


@pytest.mark.django_db
def test_register(client):
    response = client.post('/graphql', {
        'query': '''
                mutation {
                  register(
                    email: "test_user5@email.com",
                    username: "test_user5",
                    password1: "supersecretpassword",
                    password2: "supersecretpassword",
                  ) {
                    success,
                    errors,
                    token,
                    refreshToken
                  }
                }
                '''
    })
    assert response.json().get('data', {}).get('register', {}).get('success') is True