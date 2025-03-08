from django.shortcuts import render, redirect
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import BreathingTechniqueForm
from django.db.models import Q

@login_required
def new_breath(request):
    if request.method == "POST":
        form = BreathingTechniqueForm(request.POST)
        if form.is_valid():
            technique = form.save(commit=False)
            technique.user = request.user  # Associate with logged-in user
            technique.save()
            return redirect("breathing_list")  # Redirect to list of techniques
    else:
        form = BreathingTechniqueForm()

    return render(request, "home/newbreath.html", {"form": form})

def newbreath_view(request):
    if request.method == 'POST':
        form = BreathingTechniqueForm(request.POST)
        
        if form.is_valid():  # ✅ Validate the form before saving
            technique = form.save(commit=False)  # Don't save yet
            technique.user = request.user
            technique.save()  # Now save it properly
            
            # ✅ Fetch cleaned data from the form instead of raw POST data
            in_time = form.cleaned_data.get('in_time', 0)
            in_hold_time = form.cleaned_data.get('in_hold_time', 0)
            out_time = form.cleaned_data.get('out_time', 0)
            out_hold_time = form.cleaned_data.get('out_hold_time', 0)

            # ✅ Ensure time values are integers before creating `BreathingPhase`
            try:
                in_time = int(in_time) if in_time else 0
                in_hold_time = int(in_hold_time) if in_hold_time else 0
                out_time = int(out_time) if out_time else 0
                out_hold_time = int(out_hold_time) if out_hold_time else 0
            except ValueError:
                return render(request, "home/newbreath.html", {"form": form, "error": "Invalid time values"})

            # ✅ Create the corresponding phases
            BreathingPhase.objects.create(technique=technique, name='Inhale', duration=in_time)
            BreathingPhase.objects.create(technique=technique, name='Hold', duration=in_hold_time)
            BreathingPhase.objects.create(technique=technique, name='Exhale', duration=out_time)
            BreathingPhase.objects.create(technique=technique, name='Hold', duration=out_hold_time)

            return redirect('home')  # Redirect to home after saving

    else:
        form = BreathingTechniqueForm()  # ✅ Show an empty form when loading the page

    return render(request, 'home/newbreath.html', {"form": form})


def home(request):
    use_reggae = request.session.get('use_reggae', False)
    # Prefetch phases to reduce database queries
    if request.user.is_authenticated:
        # If logged in, show both user-specific and global techniques
        techniques = BreathingTechnique.objects.filter(
            Q(user=request.user) | Q(is_global=True)
        ).prefetch_related('phases')
    else:
        # If anonymous, show only global techniques
        techniques = BreathingTechnique.objects.filter(
            is_global=True
        ).prefetch_related('phases')
    for technique in techniques:
        if technique.out_hold_time and technique.in_hold_time:
            print(f"in and out hol times{technique}")
            print(technique.in_time, technique.in_hold_time, technique.out_time, technique.out_hold_time)
            total_duration = int(technique.in_time) + int(technique.in_hold_time) + int(technique.out_time) + int(technique.out_hold_time)
            print(total_duration)
            BPM = 60/total_duration
            print(f"{BPM} Breaths Per Minute")
        elif technique.in_hold_time:
            print(f"only in_hold_time{technique}")
            print(technique.in_time, technique.in_hold_time, technique.out_time)
            total_duration = int(technique.in_time) + int(technique.in_hold_time) + int(technique.out_time)
            print(total_duration)
            BPM = 60/total_duration
            print(f"{BPM} Breaths Per Minute")
        elif technique.out_hold_time:
            print(f"only in_hold_time{technique}")
            print(technique.in_time, technique.in_hold_time, technique.out_time)
            total_duration = int(technique.in_time) + int(technique.in_hold_time) + int(technique.out_time)
            print(total_duration)
            BPM = 60/total_duration
            print(f"{BPM} Breaths Per Minute")
        else:
            print(f"no in or out hold time{technique}")
            print(technique.in_time, technique.out_time)
            total_duration = int(technique.in_time + technique.out_time)
            print(total_duration)
            BPM = 60/total_duration
            print(f"{BPM} Breaths Per Minute")
            
        
    use_reggae = request.session.get('use_reggae', False)
    css_file = 'reggae-styles.css' if use_reggae else 'styles.css'
    return render(request, 'home/home.html', {'css_file': css_file, 'techniques': techniques})
    

# def activate_reggae(request):
#     return render(request, 'home/home.html', {
#         'css_file': 'reggae-styles.css'
#     })

def toggle_reggae(request):
    # Read the current session value (defaults to False if not set)
    current_value = request.session.get('use_reggae', False)
    # Flip it
    request.session['use_reggae'] = not current_value

    # Redirect back to home (or wherever you want)
    
    return redirect('home') 

@login_required
def profile_view(request):
    return render(request, 'home/profile.html')

@login_required
def breathing_list(request):
    user_techniques = BreathingTechnique.objects.filter(user=request.user)
    global_techniques = BreathingTechnique.objects.filter(is_global=True)

    return render(request, "home/breathing_list.html", {
        "user_techniques": user_techniques,
        "global_techniques": global_techniques,
    })

@login_required
def record_breathing_session(request):
    if request.method == 'POST':
        technique_id = request.POST.get('technique_id')  # from a hidden input or form field
        duration = request.POST.get('duration')          # total seconds, from JS

        if technique_id and duration:
            try:
                # Fetch the chosen technique (optional if you want to associate one)
                technique = BreathingTechnique.objects.get(id=technique_id)
            except BreathingTechnique.DoesNotExist:
                technique = None

            # Create the stats record
            BreathingStats.objects.create(
                user=request.user,
                technique=technique,
                session_duration=duration,
            )

        # Redirect or render a success page
        return redirect('home')  # or wherever you want
    
    else:
        # If GET request, you could show available techniques, or a "start breathing" page
        techniques = BreathingTechnique.objects.all()
        return render(request, 'home/start_breathing.html', {
            'techniques': techniques
        })

@login_required
def breathing_stats(request):
    """Show the user's breathing session stats."""
    stats_qs = BreathingStats.objects.filter(user=request.user).select_related('technique')

    # Calculate total time across all sessions
    total_time = stats_qs.aggregate(Sum('session_duration'))['session_duration__sum'] or 0

    # Pass the individual session records and the total time to the template
    context = {
        'stats': stats_qs,
        'total_time': total_time,
    }
    return render(request, 'home/breathing_stats.html', context)
