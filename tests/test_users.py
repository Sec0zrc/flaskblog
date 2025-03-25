import json
import logging

logging.basicConfig(level=logging.INFO)

# Admin user token
access_token = None


def test_users_get_success(test_client):
    # 先登录，获取token
    login_response = test_client.post('/api/v1/auth/login',
                                      data=json.dumps({'username': 'Admin', 'password': 'test123456*a'}),
                                      content_type='application/json')
    global access_token
    access_token = login_response.json['token']
    logging.info(access_token)

    # 请求获取用户列表
    try:
        response = test_client.get('/api/v1/users', cookies={'token': access_token}, content_type='application/json')
        assert response.status_code == 200
        assert response.json['code'] == 200
        assert response.json['msg'] == 'success'
    except Exception as e:
        logging.error(e)


def test_users_get_fail(test_client):
    # 请求获取用户列表
    try:
        response = test_client.get('/api/v1/users', content_type='application/json')
        assert response.status_code == 403
        assert response.json['code'] == 403
        assert response.json['msg'] == 'Permission denial.'
    except Exception as e:
        logging.error(e)


def test_users_post_success(test_client):
    try:
        response = test_client.post('/api/v1/users',
                                    data=json.dumps({'username': 'test_user', 'password': 'test123456*a'}),
                                    content_type='application/json')
        assert response.status_code == 200
        assert response.json['code'] == 201
        assert response.json['msg'] == 'success'
    except Exception as e:
        logging.error(e)


def test_users_post_fail(test_client):
    try:
        response = test_client.post('/api/v1/users',
                                    data=json.dumps({'username': 'test_user'}),
                                    content_type='application/json')
        assert response.status_code == 400
    except Exception as e:
        logging.error(e)


def test_users_put_success(test_client):
    try:
        response = test_client.put('/api/v1/users/1',
                                   data=json.dumps({'username': 'test_user', 'password': 'aaaaaa*a'}),
                                   cookies={'token': access_token},
                                   content_type='application/json')
        assert response.status_code == 200
        assert response.json['code'] == 200
        assert response.json['msg'] == '用户密码修改成功'
    except Exception as e:
        logging.error(e)


def test_users_put_auth_fail(test_client):
    try:
        response = test_client.put('/api/v1/users/1',
                                   data=json.dumps({'username': 'test_user', 'password': 'aaaaaa*a'}),
                                   )
        assert response.status_code == 200
        assert response.json['code'] == 403
        assert response.json['msg'] == 'Permission denial!'
    except Exception as e:
        logging.error(e)


def test_users_put_username_fail(test_client):
    try:
        response = test_client.put('/api/v1/users/1',
                                   data=json.dumps({'username': '123123', 'password': 'aaaaaa*a'}),
                                   cookies={'token': access_token}
                                   )
        assert response.status_code == 200
        assert response.json['code'] == 404
        assert response.json['message'] == '用户不存在'

    except Exception as e:
        logging.error(e)


def test_users_delete_success(test_client):
    try:
        response = test_client.delete('/api/v1/users/6',
                                      cookies={'token': access_token},
                                      content_type='application/json')
        assert response.status_code == 200
        assert response.json['code'] == 200
        assert response.json['message'] == '用户删除成功'
    except Exception as e:
        logging.error(e)


def test_users_delete_user_not_found_fail(test_client):
    try:
        response = test_client.delete('/api/v1/users/6',
                                      content_type='application/json')
        assert response.status_code == 200
        assert response.json['code'] == 404
        assert response.json['message'] == '用户不存在'
    except Exception as e:
        logging.error(e)


def test_users_delete_auth_fail(test_client):
    try:
        response = test_client.delete('/api/v1/users/2',
                                      content_type='application/json')
        assert response.status_code == 200
        assert response.json['code'] == 403
        assert response.json['message'] == 'Permission denial!'
    except Exception as e:
        logging.error(e)
