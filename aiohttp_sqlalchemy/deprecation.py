import warnings
from typing import Any

DEPRECATION_MAP = {
    'ItemAddMixin': 'UnitAddMixin',
    'ItemDeleteMixin': 'UnitDeleteMixin',
    'ItemEditMixin': 'UnitEditMixin',
    'ItemViewMixin': 'UnitViewMixin',
    'OffsetPagination': 'OffsetPaginationMixin',
    'SAItemAddMixin': 'UnitAddMixin',
    'SAItemDeleteMixin': 'UnitDeleteMixin',
    'SAItemEditMixin': 'UnitEditMixin',
    'SAItemViewMixin': 'UnitViewMixin',
    'SAListAddMixin': 'ListAddMixin',
    'SAListDeleteMixin': 'ListDeleteMixin',
    'SAListEditMixin': 'ListEditMixin',
    'SAListViewMixin': 'ListViewMixin',
    'SAModelDeleteMixin': 'DeleteStatementMixin',
    'SAModelEditMixin': 'UpdateStatementMixin',
    'SAModelViewMixin': 'SelectStatementMixin',
    'SAPrimaryKeyMixin': 'PrimaryKeyMixin',
}


def _handle_deprecation(name: str) -> Any:
    if name in DEPRECATION_MAP.keys():
        warnings.warn(
            f'`{name}` is deprecated. '
            f'Use `{DEPRECATION_MAP[name]}`.',
            DeprecationWarning,
            stacklevel=3,
        )
        return DEPRECATION_MAP.get(name)
    return None
