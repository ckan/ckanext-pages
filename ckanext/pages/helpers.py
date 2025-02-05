import ckan.lib.helpers as h
from ckan import model
from ckanext.pages.db import HeaderLogo, HeaderMainMenu, HeaderSecondaryMenu


def get_header_data():
    session = model.Session
    lang = h.lang()

    logo = session.query(HeaderLogo).filter_by(is_visible=True).first()
    logo_url = getattr(logo, f'logo_{lang}', None) if logo else ""

    main_menu_items = (
        session.query(HeaderMainMenu)
        .filter_by(is_visible=True).
        order_by(HeaderMainMenu.order)
        .all())

    secondary_menu_items = (
        session.query(HeaderSecondaryMenu)
        .filter_by(is_visible=True)
        .order_by(HeaderSecondaryMenu.order)
        .all()
    )

    def build_menu_tree(menu_items):
        menu_dict = {item.id: item for item in menu_items}
        root_items = []

        for item in menu_items:
            if item.parent_id:
                parent = menu_dict.get(item.parent_id)
                if parent and item not in parent.children:
                    parent.children.append(item)
            else:
                if item not in root_items:
                    root_items.append(item)

        return root_items

    main_menu_tree = build_menu_tree(main_menu_items)
    secondary_menu_tree = build_menu_tree(secondary_menu_items)

    return {
        'logo_url': logo_url,
        'main_menu_tree': main_menu_tree,
        'secondary_menu_tree': secondary_menu_tree,
        'lang': lang
    }
