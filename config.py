import toml


class Month:
    name: str
    number: int
    image_path: str
    image_location: str | None = None
    image_caption: str | None = None

    def __init__(self, name: str, number: int, image_path: str, image_location: str | None = None, image_caption: str | None = None):
        self.name = name
        self.number = number
        self.image_path = image_path
        self.image_location = image_location
        self.image_caption = image_caption

    @classmethod
    def from_dict(cls, data: dict) -> 'Month':
        return cls(
            name=data.get("name", "MissingName"),
            number=data.get("number", -1),
            image_path=data.get("image_path", "MissingPath.png"),
            image_location=data.get("image_location", ""),
            image_caption=data.get("image_caption", "")
        )


class Holiday:
    month: int
    day: int
    name: str

    def __init__(self, month: int, day: int, name: str):
        self.month = month
        self.day = day
        self.name = name

    @classmethod
    def from_dict(cls, data: dict) -> 'Holiday':
        return cls(
            month=data.get("month", -1),
            day=data.get("day", -1),
            name=data.get("name", "MissingName")
        )
    
    def __str__(self) -> str:
        """User-friendly string representation (for print)."""
        return f"{self.name} ({self.day:02d}.{self.month:02d})"

    def __repr__(self) -> str:
        """Developer-friendly representation (for debugging)."""
        return f"Holiday(month={self.month}, day={self.day}, name='{self.name}')"


class Config:
    year: int
    firstweekday: int
    front_title: str
    subtitle: str | None = None
    front_image_path: str
    author: str | None = None
    months: list[Month]
    custom_holidays: list[Holiday]


def load_config(file_path: str) -> Config:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = toml.load(f)

    config = Config()
    config.year = data.get("year", 2026)
    config.firstweekday = data.get("firstweekday", 0)
    config.front_title = data.get("front_title", "pipapo")
    config.subtitle = data.get("subtitle", None)
    config.front_image_path = data.get("front_image_path", ".images/photo00.png")
    config.author = data.get("author", None)
    
    months_data = data.get("month", [])
    month_list = []
    if isinstance(months_data, dict):
        for name, info in months_data.items():
            info = dict(info)
            info["name"] = name
            month_list.append(info)
    elif isinstance(months_data, list):
        month_list = months_data
    else:
        raise ValueError(f"'month' should be a list or dict, got {type(months_data)}")
    config.months = [Month.from_dict(m) for m in month_list]

    holidays_data = data.get("custom_holiday", [])
    holiday_list = []
    if isinstance(holidays_data, dict):
        for name, info in holidays_data.items():
            info = dict(info)
            info["name"] = name
            holiday_list.append(info)
    elif isinstance(holidays_data, list):
        holiday_list = holidays_data
    else:
        raise ValueError(f"'custom_holiday' should be a list of tables, got {type(holidays_data)}")
    config.custom_holidays = [Holiday.from_dict(h) for h in holiday_list]

    return config
