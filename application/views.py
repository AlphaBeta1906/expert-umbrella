from django.shortcuts import render
from django.http import HttpRequest
from markdown import markdown

# Create your views here.


def about(request: HttpRequest):
    content = open("application/docs/about.md").read()
    content = markdown(content)

    return render(
        request,
        "generic.html",
        {"title": "About this site", "content": content},
    )


def license(request: HttpRequest):
    content = open("application/docs/license.md").read()
    content = markdown(content)

    return render(
        request, "generic.html", {"title": "Licensing", "content": content}
    )
