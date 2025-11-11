import calendar
import sys
from tqdm import tqdm

from config import Config, Holiday, Month, load_config
from constants import weekdays
from public_holidays import get_public_holidays


def main():
    if len(sys.argv) != 2:
        print("Usage: python flexiblecalendar.py [config.toml]")
        sys.exit(1)

    config: Config = load_config(sys.argv[1])

    y = calendar.Calendar(firstweekday=config.firstweekday)
    selected_year = y.yeardayscalendar(config.year, width=1)

    config.months.sort(key=lambda x: x.number)

    print_year_label(config)
    print_title(config)
    print_subtitle(config)
    print_author(config)
    tqdm_max = min(len(selected_year), len(config.months))

    holiday_list = get_holiday_list(config)
    print(holiday_list)

    for (month, config_month) in tqdm(zip(selected_year, config.months), total=tqdm_max, desc="Generating calendar"):
        print_month_embedding_code(config_month)
        print_month_dates_code(month, config_month, config, holiday_list)

    exit(0)


def print_content_to_file(filename: str, content: str):
    tex_file = open(filename, "w")
    tex_file.write(content)
    tex_file.close()


def print_year_label(config: Config):
    print_content_to_file(
        "./output/config/year-label.tex",
        str(config.year)
    )


def print_title(config: Config):
    print_content_to_file(
        "./output/config/title.tex",
        str(config.front_title)
    )


def print_subtitle(config: Config):
    subtitle_content = str(config.subtitle) if config.subtitle else ""
    print_content_to_file(
        "./output/config/subtitle.tex",
        subtitle_content
    )


def print_author(config: Config):
    author_content = str(config.author) if config.author else ""
    print_content_to_file(
        "./output/config/author.tex",
        author_content
    )


def get_holiday_list(config: Config) -> list[Holiday]:
        """Return a sorted list of holidays for the given year, combining public and custom holidays.
        returns:
            list[Holiday]: A sorted list of Holiday objects.
        """
        public_holidays = get_public_holidays(config.year)
        custom_holidays = config.custom_holidays
        holiday_list = public_holidays + custom_holidays
        holiday_list.sort(key=lambda x: (x.month, x.day, x.name))
        return holiday_list


def print_month_embedding_code(config_month):
    content = "\\newpage\n\n"
    if config_month.number % 2 == 0:
        content += r"\begin{minipage}[s][\textheight][t]{0.6908\linewidth}" + "\n"
        content += r"\vfill" + "\n"
        content += r"\raggedleft" + "\n"
        content += f"\\input{{../output/tables/{config_month.number:02}.tex}}\n"
        content += r"\end{minipage}"
        content += r"\begin{minipage}[s][\textheight][c]{0.2908\linewidth}" + "\n"
        content += r"\raggedleft" + "\n"
        content += f"\\textbf{{\\fontsize{{35}}{{42}}\\selectfont {config_month.name}-{config_month.number:02}}}\\par\n"
        content += r"\vfill" + "\n"
        content += f"\\includegraphics[width=\\textwidth,keepaspectratio]{{{config_month.image_path}}}\n"
        content += "\t\\newline\n"
        content += r"\begin{center}" + "\n"
        if config_month.image_location:
            content += f"\t\\emoji{{pushpin}} \\small {config_month.image_location}\n"
        else:
            content += f"\t\\small \\textit{{{config_month.image_caption}}}\n"
        content += r"\end{center}" + "\n"
        content += r"\end{minipage}" + "\n"

    else:
        content += r"\begin{minipage}[s][\textheight][c]{0.2908\linewidth}" + "\n"
        content += r"\raggedright" + "\n"
        content += f"\\textbf{{\\fontsize{{35}}{{42}}\\selectfont {config_month.number:02}-{config_month.name}}}\\par\n"
        content += r"\vfill" + "\n"
        content += f"\\includegraphics[width=\\textwidth,keepaspectratio]{{{config_month.image_path}}}\n"
        content += "\t\\newline\n"
        content += r"\begin{center}" + "\n"
        if config_month.image_location:
            content += f"\t\\emoji{{pushpin}} \\small {config_month.image_location}\n"
        else:
            content += f"\t\\small \\textit{{{config_month.image_caption}}}\n"
        content += r"\end{center}" + "\n"
        content += r"\end{minipage}"
        content += r"\begin{minipage}[s][\textheight][t]{0.6908\linewidth}" + "\n"
        content += r"\vfill" + "\n"
        content += r"\raggedleft" + "\n"
        content += f"\\input{{../output/tables/{config_month.number:02}.tex}}\n"
        content += r"\end{minipage}" + "\n"

    print_content_to_file(
        f"./output/months/{config_month.number:02}.tex",
        content
    )


def print_month_dates_code(month, config_month: Month, config: Config, holiday_list: list[Holiday]):
    content = table_month(month, config_month.number, config, holiday_list)
    print_content_to_file(f"./output/tables/{config_month.number:02}.tex", content)


def table_week(week, month_number, cell_height_macro, holiday_list: list[Holiday], prev_month_days: int) -> str:
    row_string = ""
    next_month_start = 0
    for index, day in enumerate(week):
        row_string += "\t"
        if day:
            event_string = [h.name for h in holiday_list if h.month == month_number and h.day == day]
            row_string += f"\\dayCell{{{day}}}{{{cell_height_macro}}}"
            if event_string:
                row_string += "[" + "\\newline ".join(event_string) + "]"
        elif week[0] == 0:
            off_day = prev_month_days - week.count(0) + index + 1
            event_string = [h.name for h in holiday_list if h.month == month_number - 1 and h.day == off_day]
            row_string += f"\\offDay{{{off_day}}}{{{cell_height_macro}}}"
            if event_string:
                row_string += "[" + "\\newline ".join(event_string) + "]"
        else:
            next_month_start += 1
            event_string = [h.name for h in holiday_list if h.month == month_number + 1 and h.day == next_month_start]
            row_string += f"\\offDay{{{next_month_start}}}{{{cell_height_macro}}}"
            if event_string:
                row_string += "[" + "\\newline ".join(event_string) + "]"

        row_string += "\t"
        if index < 6:
            row_string += "&"
        else:
            row_string += "\\\\ \\hline \n"
    return row_string


def table_month(month, month_number, config: Config, holiday_list: list[Holiday]) -> str:
    num_weeks = len(month[0])
    cell_height_macro = "\\cellHeightSixRows" if num_weeks == 6 else "\\cellHeightFiveRows"

    prev_month = month_number - 1 if month_number > 1 else 12
    prev_month_days = calendar.monthrange(config.year, prev_month)[1]

    month_string = r"\begin{tabular}{|*{7}{C|}}" + "\n"
    month_string += r"\hline" + "\n"
    for index in range(7):
        month_string += "\t" + weekdays[(config.firstweekday + index) % 7] + "\t"
        if index < 6:
            month_string += "&"
        else:
            month_string += "\\\\ \\hline \n"
    for week in month[0]:
        month_string += table_week(week, month_number, cell_height_macro, holiday_list, prev_month_days)
    month_string += r"\end{tabular}"
    return month_string


if __name__ == "__main__":
    main()
