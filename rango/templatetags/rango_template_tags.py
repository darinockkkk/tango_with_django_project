from django import template
from rango.models import Category

# create instance of template.Library(), required to register new template tags
register = template.Library()

# decorator
# whenever this function is used in template, run it and insert results inside rango/categories.html
@register.inclusion_tag('rango/categories.html')
#  this new template is used to render list of categories you provide in dict thats returned in function.
# this rendered list can then be injected into response of view that initially called template tag!
def get_category_list(current_category=None):
    return {'categories': Category.objects.all(),
            'current_category': current_category}

# dict example:
# {
#    'categories': [
#        Category(name='Python', slug='python'),
#        Category(name='Django', slug='django'),
#        Category(name='Flask', slug='flask'),
#    ]
#}