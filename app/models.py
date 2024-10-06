from app import USERS, POSTS, EMAILS
import re


class User:
    def __init__(self, user_id, first_name, last_name, email):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.total_reactions = 0
        self.posts = []
        self.status = 'created'

    def to_dict(self):
        return {
            "id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "total_reactions": self.total_reactions,
            "posts": self.posts
        }

    @staticmethod
    def is_valid_email(email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) and email not in EMAILS

    @staticmethod
    def is_valid_id(user_id):
        return 0 <= user_id < len(USERS) and USERS[user_id].status != "deleted"

    def __lt__(self, other):
        return self.total_reactions < other.total_reactions

    @staticmethod
    def get_leaderboard(rev=False):
        leaderboard = [user.to_dict() for user in sorted(USERS, reverse=rev) if User.is_valid_id(user.user_id)]
        for user in leaderboard:
            del user['posts']
        return leaderboard

    def repr(self):
        if self.status == "created":
            return f'{self.user_id} {self.first_name} {self.last_name}'
        else:
            return "User deleted"


class Post:
    def __init__(self, post_id, author_id, text):
        self.post_id = post_id
        self.author_id = author_id
        self.text = text
        self.reactions = []
        self.status = "created"

    @staticmethod
    def is_valid_id(post_id):
        return 0 <= post_id < len(POSTS) and POSTS[post_id].status != "deleted"

    def to_dict(self):
        return {
            "id": self.post_id,
            "author_id": self.author_id,
            "text": self.text,
            "reactions": self.reactions,
        }

    def repr(self):
        if self.status == 'created':
            return f'{self.post_id} {self.author_id} {self.text}'
        else:
            return "Post deleted"