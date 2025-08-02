from save_result.result_to_sql import save_to_sql
from save_result.result_to_csv import save_to_csv

import click


@click.command()
@click.argument("count", type=int)
@click.option("--sql", is_flag=True, help="Сохранить в базу данных")
@click.option("--csv", is_flag=True, help="Сохранить в csv, можно указать путь (--path)")
@click.option("--path", default="./csv/tenders.csv", type=str, help="Путь куда сохранить. Можно не указывать, по дефолту ./csv/tenders.csv")
def main(count, sql, csv, path):
    if sql and csv:
        click.echo("Выберите один вариант для сохранения информации")
        return
    elif not sql and not csv:
        click.echo("Укажите формат сохранения: --sql или --csv")
        return
    elif sql:
        save_to_sql(count)
    elif csv:
        save_to_csv(count, path)


if __name__ == "__main__":
    main()
