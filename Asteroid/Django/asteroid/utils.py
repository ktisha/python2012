def render_to_response(request, template_name, context_dict = {}):
    from django.template import RequestContext
    from django.shortcuts import render_to_response as _render_to_response

    context = RequestContext(request, context_dict)
    return _render_to_response(template_name, context_instance=context)

def expose(template_name):
    def renderer(func):
        def wrapper(request, *args, **kw):
            output = func(request, *args, **kw)
            if not isinstance(output, dict):
                return output

            return render_to_response(request, template_name, output)

        return wrapper

    return renderer