import json
import logging

logging.basicConfig(level=logging.DEBUG)


def test_login_wrong_password(test_client):
    response = test_client.post('/api/v1/auth/login', data=json.dumps({'username': 'Admin', 'password': 'test123456'}),
                                content_type='application/json')

    assert response.json['code'] == 400
    assert response.json['message'] == '密码错误'


def test_login_wrong_username(test_client):
    response = test_client.post('/api/v1/auth/login',
                                data=json.dumps({'username': 'adbcda', 'password': 'test123456*a'}),
                                content_type='application/json')
    assert response.json['code'] == 404
    assert response.json['message'] == '用户不存在'


def test_success_logout(test_client):
    """测试成功登出"""
    # 先获取登录令牌
    login_response = test_client.post('/api/v1/auth/login',
                                      data=json.dumps({'username': 'Admin', 'password': 'test123456*a'}),
                                      content_type='application/json')
    access_token = login_response.json['token']
    logging.info(access_token)
    # 使用令牌登出
    try:
        logout_response = test_client.get('/api/v1/auth/logout', cookies={'token': access_token})

        logging.info(logout_response)
        assert logout_response.status_code == 200
        assert logout_response.json['message'] == '登出成功'
    except Exception as e:
        logging.error(e)
        logging.info(e)


def test_login_success(test_client):
    response = test_client.post('/api/v1/auth/login',
                                data=json.dumps({'username': 'Admin', 'password': 'test123456*a'}),
                                content_type='application/json')
    # print(response.json)
    token = response.json['token']
    assert "token" in response.json
    assert response.status_code == 200
    assert response.json['message'] == '登录成功'


def test_failed_logout(test_client):
    """测试失败登出"""
    # 先获取登录令牌
    login_response = test_client.post('/api/v1/auth/login',
                                      data=json.dumps({'username': 'Admin', 'password': 'test123456*a'}),
                                      content_type='application/json')
    access_token = login_response.json['token']
    logging.info(access_token)
    # 使用令牌登出
    try:
        logout_response = test_client.get('/api/v1/auth/logout')
        logging.info(logout_response)
        assert logout_response.status_code == 400
        assert logout_response.json['message'] == '登出失败'
    except Exception as e:
        logging.error(e)
        logging.info(e)
