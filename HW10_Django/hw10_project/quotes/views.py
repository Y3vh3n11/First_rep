from django.shortcuts import render
from .utils import get_mongo
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


from .forms import AuthorForm, QuoteForm
from .models import Author, Tag, Quote

def main(request):
    db = get_mongo()
    quotes = db.quotes.find()
    return render(request, 'quotes/index.html', context={'quotes': quotes})

@login_required
def quote(request):
    authors = Author.objects.all()
    tags = Tag.objects.all()

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save(commit=False)
            new_quote.author = Author.objects.get(fullname__in=request.POST.getlist('author'))
            new_quote.save()

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)
            
            return redirect(to='quotes:main')
        else:
            return render(request, 'quotes/quote.html', {"authors": authors, "tags": tags, "form": form})
    return render(request, 'quotes/quote.html', {"authors": authors, "tags": tags, "form": QuoteForm()})

@login_required
def author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes:main')
        else:
            return render(request, 'quotes/author.html', {'form': form})
    else:
        return render(request, 'quotes/author.html', {'form': AuthorForm()})