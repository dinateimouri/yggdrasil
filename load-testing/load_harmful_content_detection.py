from locust import task, FastHttpUser
import locust.stats


locust.stats.CONSOLE_STATS_INTERVAL_SEC = 60
class MyUser(FastHttpUser):
    @task
    def load_harmful_content_detection(self):
        self.client.post(url="/sync-chat", json={"prompts": ["you are liar", "you are liar"], "similarity_measure": "cosine"})

