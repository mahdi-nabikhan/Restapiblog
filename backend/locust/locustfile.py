from locust import HttpUser, task, between


class AccountUser(HttpUser):
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