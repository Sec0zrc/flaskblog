import logging
import json
import pytest

# @pytest.mark.timeout(5)
logging.basicConfig(level=logging.INFO)
access_token = None


def test_posts_get_success(test_client):
    response = test_client.get('/api/v1/posts?page=1&per_page=10')
    assert response.status_code == 200
    assert response.json['code'] == 200
    assert response.json['message'] == '获取文章列表成功'
    assert response.json['data'] != []

    # 测试非法参数, 返回默认值,如果传入参数不是 int, 则返回默认值
    response2 = test_client.get('/api/v1/posts?page=a&per_page=10')
    assert response2.status_code == 200
    assert response2.json['code'] == 200
    assert response2.json['message'] == '获取文章列表成功'


def test_posts_get_fail(test_client):
    response1 = test_client.get('/api/v1/posts?page=-1&per_page=10')
    assert response1.status_code == 200
    logging.info(response1.json)
    assert response1.json['code'] == 400
    assert response1.json['message'] == '获取文章列表失败'


def test_posts_get_fail2(test_client):
    response2 = test_client.get('/api/v1/posts?page=1&per_page=-11')
    assert response2.status_code == 200
    assert response2.json['code'] == 400
    assert response2.json['message'] == '获取文章列表失败'


def test_posts_get_id_success(test_client):
    response = test_client.get('/api/v1/posts/1')
    assert response.status_code == 200
    assert response.json['code'] == 200
    assert response.json['message'] == '获取文章成功'
    assert response.json['data'] != []


def test_posts_get_id_fail(test_client):
    response = test_client.get('/api/v1/posts/100')
    assert response.status_code == 200
    assert response.json['code'] == 404
    assert response.json['message'] == '文章不存在'


def test_login_success(test_client):
    # 先登录，获取登录的 token

    login = test_client.post('/api/v1/auth/login',
                             data=json.dumps({'username': 'Admin', 'password': 'test123456*a'}),
                             content_type='application/json')
    global access_token
    access_token = login.json['token']


def test_posts_post_success(test_client):
    data = {
        "title": "Test Post",
        "content": "This is a test post.",
        "category": "python",
        "tag": "pwn",
        "status": 1
    }
    data = json.dumps(data)
    logging.info(f"data:{data}")
    global access_token
    response = test_client.post('/api/v1/posts',
                                data=data,
                                headers={'Authorization': 'Bearer ' + access_token},
                                content_type='application/json')
    # assert response.status_code == 200
    # assert response.json['code'] == 200
    # assert response.json['message'] == '添加文章成功'
