from django.shortcuts import render, redirect

from django.contrib.auth import login, logout

from .forms import SignUpForm

# Create your views here.
def frontpage(request):
    return render(request, 'core/frontpage.html')



# logout view
def LogoutView(request):
    logout(request)
    return redirect('frontpage')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect('frontpage')
    else:
        form = SignUpForm()
    
    return render(request, 'core/signup.html', {'form': form})