import random
import string
from table_with_details import TableWithDetails
from nicegui import ui

columns = [
    {"name": "name", "label": "Name", "field": "name"},
    {"name": "age", "label": "Age", "field": "age"},
]
data_rows = [
    {"name": "Alice", "age": 18},
    {"name": "Bob", "age": 21},
    {"name": "Carol"},
    {"name": "Derek", "age": 41},
]

@ui.page("/")
def main():
    with ui.column().classes("w-full p-4"):
        TableWithDetails(
            columns=columns,
            pkey="name",
            get_all_data=lambda: data_rows,
            get_data=lambda key: next((row for row in data_rows if row["name"] == key), {}),
            actions={
                'Save':lambda new_dict: (
                    data_rows.append(new_dict)
                    if all(new_dict["name"] != row["name"] for row in data_rows)
                    else next(
                        (row for row in data_rows if row["name"] == new_dict["name"]), {}
                    ).update(new_dict)
                ),
                'Delete':lambda new_dict: data_rows.remove(
                    next((row for row in data_rows if row["name"] == new_dict["name"]), {})
                ),
            },
            enable_entry_creation=True,
        )


ui.run(
    title="bla",
    dark=True,
    storage_secret="".join(random.choices(string.ascii_letters + string.digits, k=32)),
)
