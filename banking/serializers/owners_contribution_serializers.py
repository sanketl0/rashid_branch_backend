from rest_framework import serializers
from banking.models.owners_contribution_model import OwnersContribution


class OwnersContributionSerializer(serializers.ModelSerializer):
    class Meta:
        model=OwnersContribution
        fields='__all__'