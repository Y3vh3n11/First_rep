from datetime import datetime
from django.shortcuts import get_object_or_404, redirect, render
from .forms import AuthorForm, QuoteForm
from utils.migration import get_mongodb
from django.contrib.auth.decorators import login_required


db = get_mongodb()


def main(request):
    quotes = db.quotes.find()
    return render(request, "quotes/index.html", context={"quotes": quotes})


def author_info(request, slug_author):
    author = db.authors.find_one({"fullname": slug_author})
    return render(request, "quotes/author_info.html", context={"author": author})


@login_required
def author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            db.authors.insert_one(
                {
                    "fullname": form.cleaned_data["fullname"],
                    "born_date": form.cleaned_data["born_date"],
                    "born_location": form.cleaned_data["born_location"],
                    "description": form.cleaned_data["description"],
                }
            )

            return redirect(to="quotes:main")
        else:
            return render(request, "quotes/author.html", {"form": form})
    else:
        return render(request, "quotes/author.html", {"form": AuthorForm()})


@login_required
def quote(request):
    authors = db.authors.find()

    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            db.quotes.insert_one(
                {
                    "tags": request.POST.getlist("tag"),
                    "author": db.authors.find_one(
                        {"fullname": request.POST.get("author")}
                    ),
                    "quote": form.cleaned_data["quote"],
                }
            )

            return redirect(to="quotes:main")
        else:
            return render(
                request, "quotes/quote.html", {"authors": authors, "form": form}
            )
    return render(
        request, "quotes/quote.html", {"authors": authors, "form": QuoteForm()}
    )
