from src.connectors.athena.auth import AthenaAuth


if __name__ == "__main__":

    auth = AthenaAuth()

    token = auth.get_token()

    print("TOKEN RECEIVED:")
    print(token[:40] + "...")