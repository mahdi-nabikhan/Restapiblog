from locust import HttpUser, task, between


class AccountUser(HttpUser):
    """
    Locust user implementation for load testing authentication
    and account-related endpoints.

    This user simulates an authenticated client performing
    common account operations against the Django REST Framework API.

    Covered endpoints:
        - JWT token creation
        - JWT token refresh
        - JWT token verification
        - Current user retrieval
        - User profile retrieval
        - Detailed profile retrieval

    Load profile:
        Read-heavy workload with occasional token validation
        and refresh requests.

    Authentication:
        Uses JWT authentication and stores access/refresh tokens
        during user initialization.

    Purpose:
        Measure authentication throughput, response latency,
        authorization overhead, and endpoint stability under load.
    """
    wait_time = between(1, 3)

    access_token = None
    refresh_token = None

    def on_start(self):
        response = self.client.post(
            "/api/v1/accounts/jwt/create/",
            json={
                "email": "test@test.com",
                "password": "12345678"
            }
        )

        if response.status_code == 200:
            data = response.json()
            self.access_token = data["access"]
            self.refresh_token = data["refresh"]

        self.headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

    @task(5)
    def me(self):
        self.client.get(
            "/api/v1/accounts/me/",
            headers=self.headers
        )

    @task(3)
    def profile(self):
        self.client.get(
            "/api/v1/accounts/profile/",
            headers=self.headers
        )

    @task(3)
    def profile_detail(self):
        self.client.get(
            "/api/v1/accounts/profile/detail/",
            headers=self.headers
        )

    @task(2)
    def verify_jwt(self):
        self.client.post(
            "/api/v1/accounts/jwt/verify/",
            json={
                "token": self.access_token
            }
        )

    @task(1)
    def refresh_jwt(self):
        self.client.post(
            "/api/v1/accounts/jwt/refresh/",
            json={
                "refresh": self.refresh_token
            }
        )
        



class BlogUser(HttpUser):
    """
    Locust user implementation for load testing blog-related APIs.

    This user simulates a typical authenticated visitor browsing
    content, reading posts, interacting with comments, and
    performing occasional content management operations.

    Covered endpoints:
        - Post list
        - Post detail
        - Cached post list
        - User post list
        - Comment list
        - Comment creation
        - Post image retrieval
        - Post create/update/delete operations

    Load profile:
        Primarily read-oriented traffic with a small percentage
        of write operations to mimic real-world production usage.

    Authentication:
        Authenticates through JWT and reuses the access token
        for protected resources.

    Purpose:
        Evaluate API responsiveness, database performance,
        cache efficiency, and overall system scalability
        under concurrent user traffic.
    """
    wait_time = between(1, 3)

    access_token = None

    def on_start(self):
        response = self.client.post(
            "/api/v1/accounts/jwt/create/",
            json={
                "email": "test@test.com",
                "password": "12345678"
            }
        )

        if response.status_code == 200:
            data = response.json()

            self.access_token = data["access"]

            self.headers = {
                "Authorization": f"Bearer {self.access_token}"
            }
        else:
            self.headers = {}

  

    @task(10)
    def post_list(self):
        self.client.get("/api/v1/blog/post/")

    @task(7)
    def post_detail(self):
        post_id = random.randint(1, 50)

        self.client.get(
            f"/api/v1/blog/post/{post_id}/"
        )

    @task(5)
    def cached_post_list(self):
        self.client.get(
            "/api/v1/blog/post/list/cache/"
        )

    @task(2)
    def user_posts(self):
        self.client.get(
            "/api/v1/blog/user/post/",
            headers=self.headers
        )

    # ==================
    # Comments
    # ==================

    @task(3)
    def comment_list(self):
        post_id = random.randint(1, 50)

        self.client.get(
            f"/api/v1/blog/comments/{post_id}/"
        )

    @task(1)
    def create_comment(self):
        post_id = random.randint(1, 50)

        self.client.post(
            f"/api/v1/blog/comments/{post_id}/",
            json={
                "body": "Created by Locust"
            },
            headers=self.headers
        )

    # ==================
    # Images
    # ==================

    @task(2)
    def image_list(self):
        post_id = random.randint(1, 50)

        self.client.get(
            f"/api/v1/blog/img/post/{post_id}/"
        )

    # ==================
    # ViewSet CRUD
    # ==================

    @task(1)
    def create_post(self):
        self.client.post(
            "/api/v1/blog/posts/",
            json={
                "title": f"Locust Post {random.randint(1,99999)}",
                "content": "Performance Testing"
            },
            headers=self.headers
        )

    @task(1)
    def update_post(self):
        post_id = random.randint(1, 50)

        self.client.patch(
            f"/api/v1/blog/posts/{post_id}/",
            json={
                "title": "Updated By Locust"
            },
            headers=self.headers
        )

    @task(1)
    def delete_post(self):
        post_id = random.randint(1000, 2000)

        self.client.delete(
            f"/api/v1/blog/posts/{post_id}/",
            headers=self.headers
        )