from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm, ItemForm
from .models import Item, Message

@login_required
def update_status(request, item_id):
    item = get_object_or_404(
        Item,
        id=item_id,
        user=request.user
    )

    # Restrict status changes: only open items can be resolved
    if item.status != 'Open':
        return redirect('dashboard')

    action = request.GET.get('status') or request.POST.get('status')
    
    if action == 'Closed':
        item.status = 'Closed'
    else:
        if item.report_type == 'Lost':
            item.status = 'Recovered'
        elif item.report_type == 'Found':
            item.status = 'Given Away'

    item.save()
    return redirect('dashboard')

@login_required
def all_reports(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    location = request.GET.get('location', '').strip()
    status = request.GET.get('status', '').strip()
    report_type = request.GET.get('report_type', '').strip()

    items = Item.objects.all()

    if query:
        # Expand search to query categories, locations, and reporter details
        items = items.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query) |
            Q(location__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__username__icontains=query)
        )

    if category:
        items = items.filter(category=category)

    if location:
        items = items.filter(location=location)

    if status:
        items = items.filter(status=status)

    if report_type:
        items = items.filter(report_type=report_type)

    items = items.order_by('-created_at')

    # Get dropdown options from choices
    categories = [c[0] for c in Item.CATEGORY_CHOICES]
    locations = [l[0] for l in Item.LOCATION_CHOICES]
    statuses = [s[0] for s in Item.STATUS_CHOICES]
    report_types = [r[0] for r in Item.REPORT_TYPES]

    return render(
        request,
        'all_reports.html',
        {
            'items': items,
            'query': query,
            'categories': categories,
            'locations': locations,
            'statuses': statuses,
            'report_types': report_types,
            'selected_category': category,
            'selected_location': location,
            'selected_status': status,
            'selected_report_type': report_type,
        }
    )

@login_required
def report_item(request):
    if request.method == 'POST':
        form = ItemForm(
            request.POST,
            request.FILES
        )
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            return redirect('dashboard')
    else:
        form = ItemForm()

    return render(
        request,
        'report_item.html',
        {'form': form}
    )

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    # Calculate stats for public home page counters
    stats = {
        'total': Item.objects.count(),
        'lost': Item.objects.filter(report_type='Lost').count(),
        'found': Item.objects.filter(report_type='Found').count(),
        'recovered': Item.objects.filter(status='Recovered').count(),
        'given_away': Item.objects.filter(status='Given Away').count(),
    }
    return render(request, 'home.html', {'stats': stats})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(
        request,
        'register.html',
        {'form': form}
    )

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    error_message = None
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            error_message = "Invalid Register Number or Password."
    else:
        form = LoginForm()

    return render(
        request,
        'login.html',
        {
            'form': form,
            'error_message': error_message
        }
    )

@login_required
def dashboard(request):
    # Compute Dashboard statistics
    stats = {
        'total': Item.objects.count(),
        'lost': Item.objects.filter(report_type='Lost').count(),
        'found': Item.objects.filter(report_type='Found').count(),
        'recovered': Item.objects.filter(status='Recovered').count(),
        'given_away': Item.objects.filter(status='Given Away').count(),
    }

    # Fetch user's own reports
    items = Item.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'dashboard.html',
        {
            'items': items,
            'stats': stats
        }
    )

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    
    # Fetch suggestions of the opposite report type with the same category
    opposite_type = 'Found' if item.report_type == 'Lost' else 'Lost'
    suggestions = Item.objects.filter(
        report_type=opposite_type,
        status='Open',
        category=item.category
    ).exclude(id=item.id)
    
    # Sort: matching location comes first
    suggestions = list(suggestions)
    suggestions.sort(key=lambda x: (x.location == item.location, x.title == item.title), reverse=True)
    suggestions = suggestions[:3]
    
    return render(
        request,
        'item_detail.html',
        {
            'item': item,
            'suggestions': suggestions
        }
    )

@login_required
def confirm_recovery(request, item_id):
    item = get_object_or_404(
        Item,
        id=item_id,
        user=request.user
    )
    
    if item.status != 'Open':
        return redirect('dashboard')
        
    opposite_type = 'Found' if item.report_type == 'Lost' else 'Lost'
    
    # Fetch suggestions of matching opposite items
    matches = Item.objects.filter(
        report_type=opposite_type,
        status='Open',
        category=item.category
    ).exclude(id=item.id)
    
    matches = list(matches)
    matches.sort(key=lambda x: (x.location == item.location, x.title == item.title), reverse=True)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        matched_item_id = request.POST.get('matched_item')
        
        if action == 'close':
            item.status = 'Closed'
            item.save()
        else:
            if item.report_type == 'Lost':
                item.status = 'Recovered'
            else:
                item.status = 'Given Away'
            item.save()
            
            if matched_item_id:
                matched_item = get_object_or_404(
                    Item,
                    id=matched_item_id,
                    report_type=opposite_type,
                    status='Open'
                )
                if matched_item.report_type == 'Lost':
                    matched_item.status = 'Recovered'
                else:
                    matched_item.status = 'Given Away'
                matched_item.save()
                
        return redirect('dashboard')
        
    return render(
        request,
        'confirm_recovery.html',
        {
            'item': item,
            'matches': matches
        }
    )

@login_required
def send_message(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    
    # Students cannot message themselves
    if item.user == request.user:
        return redirect('item_detail', item_id=item.id)
        
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(
                sender=request.user,
                receiver=item.user,
                item=item,
                content=content
            )
            return redirect(f"/item/{item.id}/?sent=success")
            
    return redirect('item_detail', item_id=item.id)

@login_required
def inbox_view(request, item_id=None, other_user_id=None):
    # Fetch all messages for current user
    all_msgs = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).order_by('-created_at')

    # Group messages by (item, other_user)
    conversations = {}
    for msg in all_msgs:
        other_user = msg.receiver if msg.sender == request.user else msg.sender
        key = (msg.item.id if msg.item else None, other_user.id)
        if key not in conversations:
            unread_in_thread = Message.objects.filter(
                item=msg.item,
                sender=other_user,
                receiver=request.user,
                is_read=False
            ).count()
            conversations[key] = {
                'item': msg.item,
                'other_user': other_user,
                'last_message': msg,
                'unread_count': unread_in_thread
            }

    conversations_list = list(conversations.values())

    active_thread = None
    history = []
    if item_id and other_user_id:
        active_item = get_object_or_404(Item, id=item_id)
        active_other_user = get_object_or_404(User, id=other_user_id)
        
        # Fetch message history
        history = Message.objects.filter(
            Q(sender=request.user, receiver=active_other_user) |
            Q(sender=active_other_user, receiver=request.user),
            item=active_item
        ).order_by('created_at')
        
        # Mark thread messages as read
        Message.objects.filter(
            item=active_item,
            sender=active_other_user,
            receiver=request.user,
            is_read=False
        ).update(is_read=True)
        
        active_thread = {
            'item': active_item,
            'other_user': active_other_user
        }

        if request.method == 'POST':
            content = request.POST.get('content', '').strip()
            if content:
                Message.objects.create(
                    sender=request.user,
                    receiver=active_other_user,
                    item=active_item,
                    content=content
                )
                return redirect('inbox_thread', item_id=item_id, other_user_id=other_user_id)

    elif conversations_list:
        first_conv = conversations_list[0]
        # Avoid redirect loops by checking parameters
        return redirect('inbox_thread', item_id=first_conv['item'].id, other_user_id=first_conv['other_user'].id)

    return render(
        request,
        'inbox.html',
        {
            'conversations': conversations_list,
            'active_thread': active_thread,
            'history': history
        }
    )