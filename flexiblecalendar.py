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
        "./output/year-label.tex",
        str(config.year)
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
    content = r"""
\begin{tabular}{|*{7}{C|}}
\hline
\textbf{Mo} & \textbf{Di} & \textbf{Mi} & \textbf{Do} & \textbf{Fr} & \textbf{Sa} & \textbf{So} \\ \hline
\dayCell{1}[New Year’s Day] & \dayCell{2} & \dayCell{3}[Meeting] & \dayCell{4} & \dayCell{5} & \dayCell{6} & \dayCell{7} \\ \hline
\dayCell{8} & \dayCell{9} & \dayCell{10}[Workshop] & \dayCell{11} & \dayCell{12} & \dayCell{13} & \dayCell{14} \\ \hline
\dayCell{15} & \dayCell{16} & \dayCell{17} & \dayCell{18} & \dayCell{19}[Holiday] & \dayCell{20} & \dayCell{21} \\ \hline
\dayCell{22} & \dayCell{23} & \dayCell{24} & \dayCell{25} & \dayCell{26} & \dayCell{27} & \dayCell{28} \\ \hline
\dayCell{22} & \dayCell{23} & \dayCell{24} & \dayCell{25} & \dayCell{26} & \dayCell{27} & \dayCell{28} \\ \hline
\dayCell{29} & \dayCell{30} & \dayCell{31} & & & & \\ \hline
\end{tabular}
"""

    print_content_to_file(f"./output/tables/{config_month.number:02}_old.tex", content)

    content = table_month(month, config_month.number, config, holiday_list)
    
    print_content_to_file(f"./output/tables/{config_month.number:02}.tex", content)



"""
    result = ""
    result += r"\begin{tabular}{|*{7}{C|}}" + "\n"
    result += "\\hline\n"

    result += "\\begin{minipage}[t]{0.55\\textwidth}"
    result += "\n"
    result += "\t\\small\n"
    result += "\t\\centering\n"
    result += "\t\\begin{tabular}{|*{7}{C|}}\n"
    result += "\t\\hline\n"
    result += "\t\\end{tabular}\n"
    result += "\\end{minipage}%\n"
"""

"""
    result += get_month_header_latex_block(config_month)
    result += "\n"
    result += "\\noindent\n"
    if config_month.number % 2 == 0:
        result += get_calendar_latex_block(config_month)
        result += "\\hfill\n"
        result += get_image_latex_block(config_month)
    else:
        result += get_image_latex_block(config_month)
        result += "\\hfill\n"
        result += get_calendar_latex_block(config_month)
"""


def table_week(week, month_number, cell_height_macro, holiday_list: list[Holiday]) -> str:
    row_string = ""
    for index, day in enumerate(week):
        row_string += "\t"
        if day:
            event_string = [holiday.name for holiday in holiday_list if holiday.month == month_number and holiday.day == day]
            row_string += "\\dayCell{" + str(day) + "}" + f"{{{cell_height_macro}}}"
            if event_string:
                row_string += "[" + "\\newline ".join(event_string) + "]"
        row_string += "\t"
        if index < 6:
            row_string += "&"
        else:
            row_string += "\\\\ \\hline \n"
    return row_string


# combine rows into full month LaTeX table
def table_month(month, month_number, config: Config, holiday_list: list[Holiday]) -> str:
    num_weeks = len(month[0])
    cell_height_macro = "\\cellHeightSixRows" if num_weeks == 6 else "\\cellHeightFiveRows"


    month_string = r"\begin{tabular}{|*{7}{C|}}" + "\n"
    month_string += r"\hline" + "\n"
    for index in range(7):
        month_string += "\t" + weekdays[(config.firstweekday + index) % 7] + "\t"
        if index < 6:
            month_string += "&"
        else:
            month_string += "\\\\ \\hline \n"
    for week in month[0]:
        month_string += table_week(week, month_number, cell_height_macro, holiday_list)
    month_string += r"\end{tabular}"
    return month_string


if __name__ == "__main__":
    main()
