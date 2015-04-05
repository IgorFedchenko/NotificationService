# coding=utf-8
import django_tables2 as tables
from notifications import models

class ActionsColumn(tables.TemplateColumn):

    class Action:
        def __init__(self, text, app_label=None, function=None, params=None, new_tab = False):
            if app_label is not None:
                href = "{% url \"" + app_label + "\" " + " ".join(params) + " %}"
            elif function is not None:
                if "record.id" in params:
                    params[params.index("record.id")] = "{{ record.id }}"
                href = "javascript:" + function + '(' + ", ".join(params) + ')'
            else:
                raise Exception("Action in table is not properly configured!")
            link_attrs = []
            if new_tab:
                link_attrs.append("target=\"_blank\"")

            self.template = "<a href=\"" + href + "\" " + " ".join(link_attrs) + ">" + text + "</a>"

    def __init__(self, actions=(), template_code="", *args, **kwargs):
        self.actions = actions
        templates = [action.template for action in actions]
        super(ActionsColumn, self).__init__(template_code="/".join(templates))


class ApplicationsTable(tables.Table):
    name = tables.Column(verbose_name="Название")
    description = tables.Column(verbose_name="Описание приложения")
    key = tables.Column(verbose_name="Ключ подписи")
    creation_date = tables.Column(verbose_name="Создано")
    actions = ActionsColumn(verbose_name="Действия",
                            actions=(
                                ActionsColumn.Action("Подробнее", app_label="app_details", params=["record.id"]),
                                ActionsColumn.Action("Скачать", app_label="download_app", params=["record.id"], new_tab=True),
                            ))

    class Meta:
        model = models.MobileApp
        attrs = {"class": "paleblue"}
        fields = ("name", "description", "key", "creation_date", "actions")
        sequence = fields

    def render_creation_date(self, value):
        return value.strftime("%H:%M %Y-%m-%d")

class ApplicationKeysTable(tables.Table):
    alias_name = tables.Column(verbose_name="Имя ключа (алиас)")
    creation_date = tables.Column(verbose_name="Создан")
    actions = ActionsColumn(verbose_name="Действия",
                            actions=(
                                ActionsColumn.Action("Удалить", function="delete_key", params=["record.id"]),
                            ))

    class Meta:
        model = models.AppKey
        attrs = {"class": "paleblue"}
        fields = ("alias_name", "creation_date", "actions", )

    def render_creation_date(self, value):
        return value.strftime("%H:%M %Y-%m-%d")

class ThemesTable(tables.Table):
    name = tables.Column(verbose_name="Название рассылки")
    creation_date = tables.Column(verbose_name="Создана")
    actions = ActionsColumn(verbose_name="Действия", actions=(
                                ActionsColumn.Action("Подробнее", app_label="theme_details", params=["record.id"]),
                                ActionsColumn.Action("Удалить", function="delete_theme", params=["record.id"])
                            ))

    class Meta:
        model = models.Theme
        attrs = {"class": "paleblue"}
        fields = ("name", "creation_date")
        sequence = fields

    def render_creation_date(self, value):
        return value.strftime("%H:%M %Y-%m-%d")

class MessagesTable(tables.Table):
    text = tables.Column(verbose_name="Текст сообщения")
    url = tables.URLColumn(verbose_name="Ссылка для перехода")
    creation_date = tables.DateTimeColumn(verbose_name="Дата отправки")

    class Meta:
        model = models.Message
        attrs = {"class": "paleblue"}
        fields = ("creation_date", "text", "url", )
        sequence = fields