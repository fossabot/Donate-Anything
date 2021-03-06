from random import randint

from django.conf import settings
from django.core.management.base import BaseCommand

from donate_anything.charity.tests.factories import (
    AppliedBusinessEditFactory,
    AppliedOrganizationEditFactory,
    BusinessApplicationFactory,
    CharityFactory,
    OrganizationApplicationFactory,
    ProposedEditFactory,
)


class Command(BaseCommand):
    help = (
        "Generates test data items. Used in conjunction with"
        "core test data for generation."
    )
    requires_migrations_checks = True

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise Exception("You cannot use this command in production.")
        print("Creating Charity app data.")

        # Create some charities
        active_org = CharityFactory.create_batch(5)
        # Add some edits
        for org in active_org[:3]:
            ProposedEditFactory.create_batch(randint(3, 10), entity=org)

        # Create applications
        org_apps = OrganizationApplicationFactory.create_batch(5)
        bus_apps = BusinessApplicationFactory.create_batch(5)

        # Create some edits
        # Last one won't have any edits since it's the newest
        AppliedOrganizationEditFactory.create_batch(30, proposed_entity=org_apps[0])
        for org in org_apps[1:-1]:
            AppliedOrganizationEditFactory.create_batch(
                randint(3, 10), proposed_entity=org
            )

        AppliedBusinessEditFactory.create_batch(30, proposed_entity=bus_apps[0])
        for bus in bus_apps[1:-1]:
            AppliedBusinessEditFactory.create_batch(randint(3, 10), proposed_entity=bus)

        print("Finished creating Charity app data.")
