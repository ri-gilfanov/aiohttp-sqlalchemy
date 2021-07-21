import warnings
from typing import Any

DEPRECATION_MAP = {
    'OffsetPagination': 'OffsetPaginationMixin',
    'SAItemAddMixin': 'ItemAddMixin',
    'SAItemDeleteMixin': 'ItemDeleteMixin',
    'SAItemEditMixin': 'ItemEditMixin',
    'SAItemViewMixin': 'ItemViewMixin',
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
