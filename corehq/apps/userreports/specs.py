from jsonobject import JsonObject, StringProperty, ListProperty, BooleanProperty

# todo: all spec definitions will go here. moving them over piece meal when touched.
from corehq.apps.userreports.getters import DictGetter, NestedDictGetter
from corehq.apps.userreports.logic import IN_MULTISELECT, EQUAL


class IndicatorSpecBase(JsonObject):
    """
    Base class for indicator specs. All specs (for now) are assumed to have a column_id,
    a display_name, which defaults to the column_id, and either a property_name or property_path
    that defines how it references properties in documents
    """
    column_id = StringProperty(required=True)
    display_name = StringProperty()
    property_name = StringProperty()
    property_path = ListProperty()

    @classmethod
    def wrap(cls, obj):
        if 'display_name' not in obj:
            obj['display_name'] = obj['column_id']
        return super(IndicatorSpecBase, cls).wrap(obj)

    @property
    def getter(self):
        if self.property_name:
            assert not self.property_path
            return DictGetter(property_name=self.property_name)
        else:
            assert self.property_path
            return NestedDictGetter(property_path=self.property_path)


class RawIndicatorSpec(IndicatorSpecBase):
    datatype = StringProperty(required=True)
    is_nullable = BooleanProperty(default=True)
    is_primary_key = BooleanProperty(default=False)


class ChoiceListIndicatorSpec(IndicatorSpecBase):
    choices = ListProperty(required=True)
    select_style = StringProperty()

    def get_operator(self):
        return IN_MULTISELECT if self.select_style == 'multiple' else EQUAL
