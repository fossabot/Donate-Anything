from django.contrib import messages
from django.db.models import Count, F
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView, ListView

from donate_anything.forum.forms import ForumForm
from donate_anything.forum.models import Message, Thread


class ForumView(ListView):
    """Show list of threads with last message
    """

    model = Thread
    paginate_by = 20
    template_name = "forum/landing.html"

    def get_queryset(self):
        """Gets queryset with values: thread id, thread OP username,
        thread created, thread views, last message, last message user,
        last message created, number of replies

        Basically, somewhat copying the django-machina template.
        """
        # Exclude the original post from post count
        return (
            Thread.objects.prefetch_related("message_set")
            .annotate(num_posts=Count("message") - 1)
            .exclude(accepted=True)
            .order_by("-created")
        )


forum_view = ForumView.as_view()


class ThreadView(ListView):
    model = Message
    paginate_by = 30
    template_name = "forum/thread.html"

    def get_queryset(self):
        Thread.objects.filter(id=self.kwargs["thread"]).update(views=F("views") + 1)
        return Message.objects.order_by("id").filter(thread_id=self.kwargs["thread"])

    def get_context_data(self, **kwargs):
        context = super(ThreadView, self).get_context_data(**kwargs)
        context["thread_forum_form"] = ForumForm()
        return context


thread_view = ThreadView.as_view()


class ThreadFormView(FormView):
    form_class = ForumForm

    def get_success_url(self):
        return reverse("forum:thread", kwargs={"thread": self.kwargs["thread"]})

    def post(self, request, *args, **kwargs):
        form = self.get_form_class()(
            request.POST, user=request.user, thread=self.kwargs["thread"]
        )
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        form.save()
        messages.add_message(
            self.request, messages.INFO, _("Successfully posted."),
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(
            self.request, messages.ERROR, form.errors,
        )
        return HttpResponseRedirect(self.get_success_url())


thread_form_view = ThreadFormView.as_view()
