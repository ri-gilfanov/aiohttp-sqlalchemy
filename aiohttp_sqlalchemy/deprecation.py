from typing import Any
import warnings

DEPRECATION_MAP = {
    'SAItemAddMixin': 'ItemAddMixin',
    'SAItemDeleteMixin': 'ItemDeleteMixin',
    'SAItemEditMixin': 'ItemEditMixin',
    'SAItemViewMixin': 'ItemViewMixin',
    'SAListAddMixin': 'ListAddMixin',
    'SAListDeleteMixin': 'ListDeleteMixin',
    'SAListEditMixin': 'ListEditMixin',
    'SAListViewMixin': 'ListViewMixin',
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
