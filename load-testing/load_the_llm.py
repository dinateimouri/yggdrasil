from locust import task, FastHttpUser
import locust.stats


locust.stats.CONSOLE_STATS_INTERVAL_SEC = 60


class EndUser(FastHttpUser):
    @task
    def load_the_llm(self):
        self.client.post(
            url="/sync-chat",
            json={
                "prompts": ["string", "string"],
                "similarity_measure": "cosine",
            },
        )
