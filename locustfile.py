from locust import HttpUser, task


class StressUser(HttpUser):
    @task
    def stress(self):
        self.client.get("/stress")
