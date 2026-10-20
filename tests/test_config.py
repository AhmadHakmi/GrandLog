from pathlib import Path

import pytest

from app.core.config import BASE_DIR, Settings


def test_relative_sqlite_path_is_anchored_to_project_root():
    settings = Settings(database_url="sqlite:///./data/test.db")

    expected = (BASE_DIR / "data" / "test.db").resolve().as_posix()
    assert settings.database_url == f"sqlite:///{expected}"


def test_relative_sqlite_path_does_not_depend_on_working_directory(
    tmp_path, monkeypatch
):
    monkeypatch.chdir(tmp_path)

    settings = Settings(database_url="sqlite:///./grandlog.db")

    path = Path(settings.database_url.removeprefix("sqlite:///"))
    assert path.parent == BASE_DIR.resolve()


@pytest.mark.parametrize(
    "url",
    [
        "sqlite:///:memory:",
        f"sqlite:///{Path.cwd().resolve().as_posix()}/absolute.db",
        "postgresql://user:password@localhost/grandlog",
    ],
)
def test_other_database_urls_are_left_unchanged(url):
    assert Settings(database_url=url).database_url == url


def test_tests_never_use_the_real_database():
    from app.database.session import DATABASE_URL

    assert DATABASE_URL == "sqlite:///:memory:"
