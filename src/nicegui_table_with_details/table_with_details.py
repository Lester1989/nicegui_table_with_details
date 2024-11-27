from typing import Any, Callable

from nicegui import events, ui


class TableWithDetails(ui.splitter):
    """
    A component that displays a table with details of the selected row.
    The table is on the left side and the details are on the right side.
    The table is clickable and the details are editable.

    :param columns: A list of dictionaries with the columns to display in the table.
    :param pkey: The Attribute name of the primary key.
    :param get_all_data: A function that returns a list of dictionaries with the data to display in the table.
    :param get_data: A function that returns a dictionary with the data of the selected row.
    :param actions: A dictionary with the actions that can be performed on the selected row.
    :param enable_entry_creation: A boolean that enables the creation of new entries.
    :param splitter_classes: The styling classes for the splitter.
    :param table_classes: The styling classes for the table.
    :param column_classes: The styling classes for the column.
    """

    selected_row_key = None
    get_all_data: Callable[[], list[dict]] = None
    get_data: Callable[[Any], None] = None
    actions: dict[str, Callable[[dict[str, str]], None]] = None
    detail_data: dict = None
    columns: list[dict[str, str]] = None

    def __init__(
        self,
        columns: list[dict[str, str]],
        pkey: str,
        get_all_data: Callable[[], list[dict]],
        get_data: Callable[[Any], None],
        actions: dict[str, Callable[[dict[str, str]], None]],
        enable_entry_creation: bool = False,
        splitter_classes: str = "w-full m-1",
        table_classes: str = "",
        column_classes: str = "p-2",
    ) -> None:
        super().__init__()
        self.pkey = pkey
        self.get_all_data = get_all_data
        self.get_data = get_data
        self.actions = actions
        self.current_inputs = []
        self.columns = columns
        self.detail_data = {}
        self.selected_row_key = None
        self.enable_entry_creation = enable_entry_creation
        self.splitter_classes = splitter_classes
        self.table_classes = table_classes
        self.column_classes = column_classes
        self.layout()

    def layout(self):
        '''
        This method creates the layout of the component.
        '''
        with self.classes(self.splitter_classes):
            with self.before:
                self.table = ui.table(
                    columns=self.columns, rows=self.get_all_data()
                ).classes(self.table_classes)
                self.table.on("rowClick", self.load_details)
                if self.enable_entry_creation:
                    ui.button("Add new entry").on_click(self.start_creation)
            with self.after:
                self.details_column = ui.column().classes(self.column_classes)

    def load_details(self, event_data: events.GenericEventArguments):
        self.selected_row_key = event_data.args[1][self.pkey]
        self.details()

    def update_overview(self):
        self.table.rows = self.get_all_data()
        self.table.update()

    def action_and_refresh(self, action_name: str):

        self.actions[action_name](self.detail_data)
        self.update_overview()
        self.details_column.clear()

    def start_creation(self):
        self.selected_row_key = None
        self.details()

    def details(self):
        self.details_column.clear()
        with self.details_column:
            if self.selected_row_key:
                self.detail_data: dict = self.get_data(self.selected_row_key)
            else:
                self.detail_data = {}
            for column_data in self.columns:
                key = column_data["name"]
                label = column_data["label"]
                self.detail_data[key] = self.detail_data.get(key, None)
                input_element = ui.input(
                    label=label,
                    validation={"required": lambda x: x is not None} if key == self.pkey else None
                ).bind_value( self.detail_data, key )
                if self.detail_data[key] and key == self.pkey:
                    input_element.disable()
            for action in self.actions:
                ui.button(action).on_click(lambda action=action: self.action_and_refresh(action))
