# lint_plugins
A collection of useful Linter plugins.

Today, there are two flake8 plugins in this project. The goal is to add various additional plugins over time.

The two plugins are:
* Missing timezone: alert on SQLAlchemy models defining a datetime column that is not timezone aware.
* Mistyped nullable column: alert on SQLAlchemy models defining a row whose type Optionality doesn't agree with the columns nullability.

See more details below.

## Background

This project was born from a concrete need I had in my projects, and after repeatedly fixing bugs with similar root causes. Since I lately I work mostly with SQLAlchemy 2.0, with type annotations and the declarative base, this is what the plugins support.

## Why flake8?

* Ruff doesn't allow plugins
* Flake8 is fast and stable, and allows plugins
* The plugins are allowed are of the right type: more detections, as opposed to say, mypy.

## Missing Timezone

Alert on SQLAlchemy models defining a datetime column that is not timezone aware.

* It is best practice to store timestamps as timezone aware in the DB.
* It is better to be consistent and have all stored timestamps stored the same way.
* Having only some timestamps be non-timezone aware causes real bugs

Good:
```
timestamp: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, default=None)
```

Bad:
```
timestamp: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=False), nullable=True, default=None)
timestamp: Mapped[Optional[datetime]] = mapped_column(DateTime(), nullable=True, default=None)
```

## Mistyped nullable column

Alert on SQLAlchemy models defining a row whose type Optionality doesn't agree with the columns nullability.

* While sometimes it makes sense having an SQLAlchemy field's type annotation different from the column type, usually it's a cause for bugs.
* The more dangerous type is where the column is nullable, but the field is not Optional, as your type checker will assume everywhere that the field can't be None.
* The less dangerous type is where the type annotation is Optional and the column isn't nullable. Less risk of bugs, but more wasteful code. (There is a small risk of bugs where the type checker will allow you to write None's to the field)
* SQLAlchemy does support inferring nullability from the type annotation, but still conflicts may exist, and I believe in this case "explicit is better than implicit".
* Note: Both `Optional[str]` and `str | None` are considered Optional by this linter plugin.

Good:
```
timestamp: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, default=None)
```

Bad:
```
timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=True, default=None)
timestamp: Mapped[Optional[str]] = mapped_column(String, nullable=False)
```

### Contributing

Contributions are welcome!
It would be great if this could become a repository of many useful linter plugins. Reach out to me you want to contribute. 


