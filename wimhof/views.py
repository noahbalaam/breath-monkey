from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from .models import WimHofSession, BreathingRound, WimHofStats
from .forms import WimHofSessionForm
import json

def wimhof_home(request):
    """Main WimHof breathing page."""
    # Get default/global sessions and user's custom sessions if logged in
    if request.user.is_authenticated:
        sessions = WimHofSession.objects.filter(
            Q(is_global=True) | Q(user=request.user)
        ).prefetch_related('rounds')
    else:
        sessions = WimHofSession.objects.filter(is_global=True).prefetch_related('rounds')
    
    # Get session ID from query param or use the first session
    session_id = request.GET.get('session')
    selected_session = None
    
    if session_id:
        try:
            selected_session = sessions.get(id=session_id)
        except WimHofSession.DoesNotExist:
            pass
    
    if not selected_session and sessions.exists():
        selected_session = sessions.first()
    
    context = {
        'sessions': sessions,
        'selected_session': selected_session,
    }
    
    return render(request, 'wimhof/wimhof_home.html', context)

@login_required
def create_session(request):
    """Create a new WimHof breathing session."""
    if request.method == 'POST':
        form = WimHofSessionForm(request.POST)
        
        if form.is_valid():
            # Create the session
            session = form.save(commit=False)
            session.user = request.user
            session.save()
            
            # Create the rounds based on form data
            round_count = form.cleaned_data['round_count']
            starting_breaths = form.cleaned_data['starting_breaths']
            breath_increment = form.cleaned_data['breath_increment']
            ramp_up = form.cleaned_data['ramp_up']
            
            for i in range(1, round_count + 1):
                if ramp_up:
                    # Calculate breaths for this round (starting + increment * (round_num - 1))
                    breath_count = starting_breaths + (breath_increment * (i - 1))
                else:
                    breath_count = starting_breaths
                
                BreathingRound.objects.create(
                    session=session,
                    round_number=i,
                    breath_count=breath_count
                )
            
            return redirect('wimhof_home')
    else:
        form = WimHofSessionForm()
    
    return render(request, 'wimhof/create_session.html', {'form': form})

@login_required
def session_detail(request, session_id):
    """View and edit a specific WimHof session."""
    session = get_object_or_404(WimHofSession, id=session_id)
    # Check if user owns this session or if it's global
    if not session.is_global and session.user != request.user:
        return HttpResponse("Not authorized", status=403)
    
    rounds = session.rounds.all().order_by('round_number')
    
    context = {
        'session': session,
        'rounds': rounds,
    }
    
    return render(request, 'wimhof/session_detail.html', context)

@login_required
@require_POST
def save_stats(request):
    """Save statistics from a completed WimHof session."""
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id')
        round_data = data.get('round_data', {})
        
        session = None
        if session_id:
            try:
                session = WimHofSession.objects.get(id=session_id)
            except WimHofSession.DoesNotExist:
                pass
        
        stats = WimHofStats.objects.create(
            user=request.user,
            session=session,
            round_data=round_data
        )
        
        return JsonResponse({'status': 'success', 'stats_id': stats.id})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@login_required
def view_stats(request):
    """View WimHof breathing statistics."""
    stats = WimHofStats.objects.filter(user=request.user).order_by('-timestamp')
    
    context = {
        'stats': stats,
    }
    
    return render(request, 'wimhof/view_stats.html', context)

