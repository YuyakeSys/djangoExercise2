# Pagination component
class Pagination(object):

    def __init__(self, request, queryset, page_size=3, page_param='page'):
        page = request.GET.get(page_param, "1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.page_size = page_size


