import atexit
import logging
import os
import subprocess
import time

import redis

logger = logging.getLogger(__name__)

class RedisManager:
    def __init__(self) -> None:
        self.REDIS_HOST: str = "localhost"
        self.REDIS_PORT: str = "6379"
        self.REDIS_DB: str = "0"

        self.redis_client: redis.Redis | None = None
        self.redis_process: subprocess.Popen | None = None

        self.get_env_vars()
        self.setup_redis()

    def get_env_vars(self) -> None:
        self.redis_host = os.getenv("REDIS_HOST")
        self.redis_port = os.getenv("REDIS_PORT")

    def setup_redis(self, try_to_start: bool = False) -> None:
        logger.info("Checking Redis ...")

        if self.check_redis_connection():
            logger.info("Redis connection successful!")
            return

        if try_to_start:
            # Try to start Redis if it is not running
            # TODO: Compare subprocess.Popen with multiprocessing.Process
            logger.info("Trying to start Redis ...")
            self.initialize_redis()
            if self.check_redis_connection():
                logger.info("Redis connection successful!")
                return

        raise Exception("Could not start Redis")


    def check_redis_connection(self) -> bool:
        if self.redis_client is not None:
            return True

        redis_client = redis.Redis(
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            db=self.REDIS_DB
        )

        try:
            redis_client.ping()
            self.redis_client = redis_client
            return True
        except redis.exceptions.ConnectionError:
            return False
        except Exception:
            return False

    def initialize_redis(self) -> None:
        try:
            # start redis server in background
            self.redis_process = subprocess.Popen(
                ["redis-server", "--dir", "./"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            # Register callback when program exits
            atexit.register(self._terminate_redis)

            time.sleep(2)
            if not self.check_redis_connection():
                raise Exception("Could not start Redis")
            logger.info(f"Redis process started with PID {self.redis_process.pid}")
        except Exception as e:
            logger.error(e)
            raise e

    def _terminate_redis(self) -> None:
        """
        Callback to terminate the redis server when the program exits
        """
        if self.redis_process is not None:
            try:
                self.redis_process.terminate()
                self.redis_process.wait(timeout=5)
                self.redis_process = None
            except Exception as e:
                logger.error(e)
                raise e
