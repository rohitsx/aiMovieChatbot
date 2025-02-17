from locust import HttpUser, task, between

class LoadTest(HttpUser):
    wait_time = between(1.1, 2)

    @task
    def test_endpoint(self):
        self.client.post("/chat/l4", json={"script": "jagoa graohc gago"})
