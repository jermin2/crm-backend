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
            name='{basename}-create',
            detail=False,
            initkwargs={'suffix':'Detail'}
        ),
        Route(
            url=r'^update-{prefix}/{lookup}$',
            mapping={'put':'update'},
            name='{basename}-update',
            detail=True,
            initkwargs={'suffix':'Detail'}
        )
    ]