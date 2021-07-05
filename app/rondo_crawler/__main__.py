from app.rondo_crawler.crawler import runner


if __name__ == '__main__':
    runner(_anyio_backend="trio")
