from rest_framework.routers import Route, DynamicRoute, DefaultRouter

class CustomRouter(DefaultRouter):
    """
    A router which 
    """
    routes = [
        Route(
            url=r'^{prefix}s$',
            mapping={'get':'list'},
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix':'List'}
        ),
        Route(
            url=r'^add-{prefix}$',
            mapping={'post':'create'},
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix':'List'}
        ),
    ]