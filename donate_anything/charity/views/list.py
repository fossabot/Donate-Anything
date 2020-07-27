from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, Paginator
from django.http import Http404, HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext_lazy as _

from donate_anything.charity.forms import (
    BusinessForm,
    OrganizationForm,
    SuggestedEditForm,
)
from donate_anything.charity.models import (
    AppliedBusinessEdit,
    AppliedOrganizationEdit,
    BusinessApplication,
    Charity,
    OrganizationApplication,
)


def organization(request, pk):
    charity = get_object_or_404(Charity, id=pk)
    context = {
        "name": charity.name,
        "description": charity.description,
        "how_to_donate": charity.how_to_donate,
    }
    return render(request, "organization/organization.html", context)


@login_required
def applied_organization(request, pk):
    obj = get_object_or_404(OrganizationApplication, id=pk)
    context = {"obj": obj}
    if request.user == obj.applier:
        context["form"] = OrganizationForm(
            instance=obj, initial={"social_media": obj.extra["social_media"]}
        )
    else:
        context["suggest_form"] = SuggestedEditForm()
    return render(request, "organization/apply/view_org.html", context)


@login_required
def applied_business(request, pk):
    obj = get_object_or_404(BusinessApplication, id=pk)
    context = {"obj": obj}
    if request.user == obj.applier:
        context["form"] = BusinessForm(instance=obj)
    else:
        context["suggest_form"] = SuggestedEditForm()
    return render(request, "organization/apply/view_bus.html", context)


def _paginate_and_return_json(qs, request) -> JsonResponse:
    """Paginates qs and and checks
    for certain query parameters for
    list organization edits
    """
    unseen = request.GET.get("unseen", False)
    if unseen == "1":
        qs = qs.filter(viewed=False)
    # Already ordered by time since AutoField
    try:
        paginator = Paginator(qs, 25, allow_empty_first_page=False)
        page_obj = paginator.get_page(request.GET.get("page", 1))
    except EmptyPage:
        raise Http404()
    if len(page_obj.object_list) == 0:
        raise Http404()
    if unseen == "1":
        data = {
            "data": [
                [x.id, x.user.get_username(), x.edit, x.created, x.updated]
                for x in page_obj.object_list
            ]
        }
    else:
        data = {
            "data": [
                [x.id, x.user.get_username(), x.edit, x.created, x.updated, x.viewed]
                for x in page_obj.object_list
            ]
        }
    return JsonResponse(data=data)


@login_required
def applied_organization_edits(request, pk):
    """Returns suggested edits for OrganizationApplications
    using Paginator. Returns username, edit, datetime
    """
    qs = (
        AppliedOrganizationEdit.objects.select_related("user")
        .filter(proposed_entity_id=pk)
        .order_by("id")
    )
    return _paginate_and_return_json(qs, request)


@login_required
def applied_business_edits(request, pk):
    """Returns suggested edits for BusinessApplications
    using Paginator. Returns username, user pk, edit, created+updated
    """
    qs = (
        AppliedBusinessEdit.objects.select_related("user")
        .filter(proposed_entity_id=pk)
        .order_by("id")
    )
    return _paginate_and_return_json(qs, request)


def _mark_view(user_id: int, obj):
    if obj.proposed_entity.applier_id != user_id:
        return HttpResponseForbidden(
            _("You must be the applicant to mark a suggestion as viewed.")
        )
    obj.viewed = not obj.viewed
    obj.save(update_fields=["viewed"])
    return HttpResponse()


@login_required
def viewed_org_edit(request, edit_pk: int):
    """Mark an organization edit as viewed.
    Reversible
    """
    obj = get_object_or_404(AppliedOrganizationEdit, id=edit_pk)
    return _mark_view(request.user.id, obj)


@login_required
def viewed_bus_edit(request, edit_pk: int):
    """Mark a business edit as viewed.
    Reversible
    """
    obj = get_object_or_404(AppliedBusinessEdit, id=edit_pk)
    return _mark_view(request.user.id, obj)