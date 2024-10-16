from locust import task, FastHttpUser
import locust.stats


locust.stats.CONSOLE_STATS_INTERVAL_SEC = 60


class MyUser(FastHttpUser):
    @task
    def load_similarity(self):
        self.client.post(
            url="/sync-chat",
            json={
                "prompts": ["string1", "string2"],
                "similarity_measure": "cosine",
            },
        )
