# -*- coding: utf-8 -*-

from django import template
from django.template.base import token_kwargs

register = template.Library()

class WithQuerySetNode(template.Node):
    def __init__(self, nodelist, extra_context):
        self.nodelist = nodelist
        self.extra_context = extra_context
        
    def render(self, context):
        values = dict([(key, iter(val.resolve(context))) for key, val in
            self.extra_context.iteritems()])

        context.update(values)
        output = self.nodelist.render(context)
        context.pop()
        return output


@register.tag('withqs')
def with_queryset(parser, token):
    bits = token.split_contents()
    remaining_bits = bits[1:]
    extra_context = token_kwargs(remaining_bits, parser, support_legacy=True)
    if not extra_context:
        raise TemplateSyntaxError("%r expected at least one variable "
                                  "assignment" % bits[0])
    if remaining_bits:
        raise TemplateSyntaxError("%r received an invalid token: %r" %
                                  (bits[0], remaining_bits[0]))
    
    nodelist = parser.parse(('endwithqs',))
    parser.delete_first_token()
    return WithQuerySetNode(nodelist, extra_context)
