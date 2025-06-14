def test_login_page(client):
    response = client.get('/login', follow_redirects=False)
    assert response.status_code == 200 or response.status_code == 302
