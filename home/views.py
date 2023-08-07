from django.http import HttpResponse
from django.shortcuts import render
import stripe
from django.conf import settings
from django.shortcuts import redirect

stripe.api_key = settings.STRIPE_SECRET_KEY


def home(request):
    template_name = 'home.html'
    return render(request, template_name)
    # return HttpResponse('Hello world')


def stripePay(request):
    template_name = 'home.html'
    if request.method == "POST":
        amount = int(request.POST["amount"])
        # Create customer
        try:
            customer = stripe.Customer.create(
                email=request.POST.get("email"),
                name=request.POST.get("full_name"),
                description=request.POST.get("desc"),
                source=request.POST['stripeToken'],
            )
            # print("description=======> ", customer.description)

        except stripe.error.CardError as e:
            return HttpResponse("<h1>There was an error charging your card:</h1>"+str(e))

        except stripe.error.RateLimitError as e:
            # handle this e, which could be stripe related, or more generic
            return HttpResponse("<h1>Rate error!</h1>")

        except stripe.error.InvalidRequestError as e:
            return HttpResponse("<h1>Invalid requestor!</h1>")

        except stripe.error.AuthenticationError as e:
            return HttpResponse("<h1>Invalid API auth!</h1>")

        except stripe.error.StripeError as e:
            return HttpResponse("<h1>Stripe error!</h1>")

        except Exception as e:
            pass

        # Stripe charge
        charge = stripe.PaymentIntent.create(
            customer=customer,
            amount=int(amount)*100,
            currency='usd',
            description=customer.description,
        )
        transRetrive = stripe.PaymentIntent.retrieve(
            charge["id"],
            api_key=settings.STRIPE_SECRET_KEY,
        )
        charge.save()  # Uses the same API Key.
        return redirect("pay_success/")
    context = {
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY
    }
    return render(request, template_name, context)


def paysuccess(request):
    return render(request, "success.html")
