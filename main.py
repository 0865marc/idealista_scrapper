from idealista.app.main import IdealistaScraper


def main() -> None:
    IdealistaScraper(host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
