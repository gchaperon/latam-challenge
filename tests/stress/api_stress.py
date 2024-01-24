from locust import HttpUser, task


class StressUser(HttpUser):
    @task
    def predict_argentinas(self) -> None:
        self.client.post(
            "/predict",
            json={
                "flights": [
                    {"OPERA": "Aerolineas Argentinas", "TIPOVUELO": "N", "MES": 3}
                ]
            },
        )

    @task
    def predict_latam(self) -> None:
        self.client.post(
            "/predict",
            json={"flights": [{"OPERA": "Grupo LATAM", "TIPOVUELO": "N", "MES": 3}]},
        )
