
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User

from .forms import CustomUserCreationForm
from .models import TimePunch


def sign_up(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Save the user object but don't commit to the database yet
            user = form.save(commit=False)
            # Mark the user as inactive until they confirm their email
            user.is_active = False
            user.save()

            # --- Start Email Sending Logic ---
            # Get the current site
            current_site = request.get_host()
            subject = 'Activate Your TimeSheet Account'
            # Render the email message from an HTML template
            message = render_to_string('registration/activation_email.html', {
                'user': user,
                'domain': current_site,
                # Encode the user's ID to be safely used in a URL
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                # Generate a one-time use token
                'token': default_token_generator.make_token(user),
            })

            # Send the email
            send_mail(subject, message, 'from@yourtimesheet.com', [user.email])

            # Show a confirmation page to the user
            return render(request, 'registration/activation_sent.html')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})


@login_required
def dashboard(request):
    employee = request.user

    # Get all punches for the user, ordered by time
    punches = TimePunch.objects.filter(employee=employee).order_by('timestamp')

    # --- Calculate Work Sessions ---
    work_sessions = []
    last_in_punch = None
    for punch in punches:
        if punch.punch_type == 'IN':
            last_in_punch = punch
        elif punch.punch_type == 'OUT' and last_in_punch:
            # We found a matching pair (IN -> OUT)
            duration = punch.timestamp - last_in_punch.timestamp

            # Format the duration into hours and minutes
            total_seconds = duration.total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)

            work_sessions.append({
                'date': last_in_punch.timestamp.date(),
                'hours_worked': f'{hours}h {minutes}m',
                'out_punch_id': punch.id,
                'confirmed': punch.confirmed,
            })
            # Reset last_in_punch so it can't be paired again
            last_in_punch = None

    # Determine current status based on the very last punch
    latest_punch = punches.last()
    current_status = "Clocked Out"
    if latest_punch and latest_punch.punch_type == "IN":
        current_status = "Clocked In"

    context = {
        'current_status': current_status,
        # We send the processed sessions, reversed so the newest appear first
        'work_sessions': reversed(work_sessions),
    }
    return render(request, 'timesheet/dashboard.html', context)


@login_required
def clock_in(request):
    """
    Handles the clock-in action. Creates a new 'IN' TimePunch.
    """
    TimePunch.objects.create(employee=request.user, punch_type="IN")
    return redirect('dashboard')


@login_required
def clock_out(request):
    """
    Handles the clock-out action. Creates a new 'OUT' TimePunch.
    """
    TimePunch.objects.create(employee=request.user, punch_type="OUT")
    return redirect('dashboard')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('dashboard')
    else:
        return render(request, 'registration/activation_invalid.html')

@login_required
def toggle_confirmation(request, punch_id): # Renamed function
    if request.method == 'POST':
        punch = TimePunch.objects.get(pk=punch_id, employee=request.user)

        # This is the new toggle logic:
        # It flips the boolean value (True becomes False, False becomes True)
        punch.confirmed = not punch.confirmed

        punch.save()
    return redirect('dashboard')