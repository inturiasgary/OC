from django.conf import settings
from django import template
from sermons.models import Sermon, Attachment, Pastor, Subject

register = template.Library()


@register.tag
def get_sermons(parser, token):
    """
        {% get_sermons 5 as sermons_items %}
    """
    bits = token.split_contents()
    if len(bits) == 3:
        limit = None
    elif len(bits) == 4:
        try:
            limit = abs(int(bits[1]))
        except ValueError:
            raise template.TemplateSyntaxError("If provided, second argument to `get_news` must be a positive whole number.")
    if bits[-2].lower() != 'as':
        raise template.TemplateSyntaxError("Missing 'as' from 'get_sermons' template tag.  Format is {% get_sermons 5 as sermons_items %}.")
    return SermonsItemNode(bits[-1], limit)


class SermonsItemNode(template.Node):
    """
    Returns a QuerySet of published SermonsItems based on the lookup parameters.
    """

    def __init__(self, varname, limit=None, author=None, category_slug=None, filters=None):
        self.varname = varname
        self.limit = limit
        self.filters = filters
        self.author = author
        self.category = category_slug

    def render(self, context):
        # Base QuerySet, which will be filtered further if necessary.
        sermons = Sermon.objects.all()

        # Do we filter by author?  If so, first attempt to resolve `author` as
        # a template.Variable.  If that doesn't work, use `author` as a literal
        # NewsAuthor.slug lookup.
        if self.author is not None:
            try:
                author_slug = template.Variable(self.author).resolve(context)
            except template.VariableDoesNotExist:
                author_slug = self.author
            sermons = sermons.filter(author__slug=author_slug)

        if self.category is not None:
            try:
                category_slug = template.Variable(self.category).resolve(context)
            except template.VariableDoesNotExist:
                category_slug = self.category
            sermons = sermons.filter(category__slug=category_slug)

        # Apply any additional lookup filters
        if self.filters:
            sermons = sermons.filter(**self.filters)

        # Apply a limit.
        if self.limit:
            sermons = sermons[:self.limit]

        context[self.varname] = sermons
        return u''


def parse_token(token):
    """
    Parses a token into 'slug', 'limit', and 'varname' values.
    Token must follow format {% tag_name <slug> [<limit>] as <varname> %}
    """
    bits = token.split_contents()
    if len(bits) == 5:
        # A limit was passed it -- try to parse / validate it.
        try:
            limit = abs(int(bits[2]))
        except:
            limit = None
    elif len(bits) == 4:
        # No limit was specified.
        limit = None
    else:
        # Syntax is wrong.
        raise template.TemplateSyntaxError("Wrong number of arguments: format is {%% %s <slug> [<limit>] as <varname> %%}" % bits[0])
    if bits[-2].lower() != 'as':
        raise template.TemplateSyntaxError("Missing 'as': format is {%% %s <slug> [<limit>] as <varname> %%}" % bits[0])
    return (bits[1], limit, bits[-1])


@register.tag
def get_posts_by_author(parser,token):
    """
    {% get_posts_by_author <slug> [<limit>] as <varname> %}
        {% get_posts_by_author foo 5 as news_items %}   # 5 articles
        {% get_posts_by_author foo as news_items %} # all articles
    """
    author_slug, limit, varname = parse_token(token)
    return SermonsItemNode(varname, limit, author=author_slug)


@register.tag
def get_posts_by_category(parser,token):
    """
    {% get_posts_by_category <slug> [<limit>] as <varname> %}
        {% get_posts_by_category foo 5 as news_items %} # 5 articles
        {% get_posts_by_category foo as news_items %}   # all articles
    """
    category_slug, limit, varname = parse_token(token)
    return SermonsItemNode(varname, limit, category_slug=category_slug)

@register.tag
def get_news_by_category(parser,token):
    """
    This is because I got sick of having to debug issues due to the fact that I typed one or the other.
    """
    return get_posts_by_category(parser,token)


@register.tag
def get_posts_by_tag(parser,token):
    """
    {% get_posts_by_tag <tag> [<limit>] as <varname> %}
    """
    tag, limit, varname = parse_token(token)
    return SermonsItemNode(varname, limit, filters={'tags__contains':tag})

@register.tag
def months_with_sermons(parser, token):
    """
        {% months_with_sermons 4 as months %}
    """
    bits = token.split_contents()
    if len(bits) == 3:
        limit = None
    elif len(bits) == 4:
        try:
            limit = abs(int(bits[1]))
        except ValueError:
            raise template.TemplateSyntaxError("If provided, second argument to months_with_sermons` must be a positive whole number.")
    if bits[-2].lower() != 'as':
        raise template.TemplateSyntaxError("Missing 'as' from 'months_with_sermons' template tag.  Format is {% months_with_news 5 as months %}.")
    return MonthNode(bits[-1], limit=limit)


class MonthNode(template.Node):

    def __init__(self,varname,limit=None):
        self.varname = varname
        self.limit = limit  # for MonthNode inheritance

    def render(self, context):
        try:
            months = Sermons.objects.dates('date', 'month', order="DESC")
        except:
            months = None
        if self.limit is not None:
            months = list(months)
            months = months[:self.limit]
        context[self.varname] = months
        return ''

