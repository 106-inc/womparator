# womparator
State of the art ML-based solution for documents comparison

## How to run
In repository's root, do (Docker is required):
```bash
docker-compose up
```

After that, open page on address `http://localhost:${WOMP_FRONT_PORT}` to access web interface.

To access backend server, go to `http://localhost:${WOMP_BACK_PORT}`
> If you can't use the default ports values from .env file, you can create  your own one and pass it to compose command as follows:
> ```bash
> docker-compose --env-file /path/to/env up
> ```
