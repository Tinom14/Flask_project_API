from app import app, USERS, POSTS, models
from flask import request, Response
import json
from http import HTTPStatus


@app.post('/posts/create')
def post_create():
    data = request.get_json()
    post_id = len(POSTS)
    author_id = data['author_id']
    text = data['text']
    if not models.User.is_valid_id(author_id):
        return Response(response='Автор не зарегистрирован',
                        status=HTTPStatus.BAD_REQUEST)
    USERS[author_id].posts.append(post_id)
    post = models.Post(post_id, author_id, text)
    POSTS.append(post)
    return Response(
        json.dumps(post.to_dict()),
        status=HTTPStatus.CREATED,
        mimetype='application/json'
    )


@app.get('/posts/<int:post_id>')
def post_get(post_id):
    if not models.Post.is_valid_id(post_id):
        return Response(response='Поста с таким номером не существует', status=HTTPStatus.NOT_FOUND)
    post = POSTS[post_id]
    return Response(
        json.dumps(post.to_dict()),
        HTTPStatus.OK,
        mimetype="application/json"
    )


@app.post('/posts/<int:post_id>/reaction')
def post_reaction(post_id):
    if not models.Post.is_valid_id(post_id):
        return Response(response='Поста с таким номером не существует', status=HTTPStatus.NOT_FOUND)
    data = request.get_json()
    user_id = data['user_id']
    if not models.User.is_valid_id(user_id):
        return Response(response='Пользователя с таким номером не существует',
                        status=HTTPStatus.BAD_REQUEST)
    reaction = data['reaction']
    POSTS[post_id].reactions.append(reaction)
    USERS[user_id].total_reactions += 1
    return Response(status=HTTPStatus.OK)


@app.delete('/posts/<int:post_id>')
def delete_post(post_id):
    if not models.Post.is_valid_id(post_id):
        return Response(response='Пост с таким номером не существует', status=HTTPStatus.NOT_FOUND)
    post = POSTS[post_id]
    post.status = "deleted"
    del_post = post.to_dict()
    del_post["status"] = post.status
    return Response(
        json.dumps(del_post),
        HTTPStatus.OK,
        mimetype="application/json"
    )

